"""Tests for fix_quotes.py"""

import tempfile
from pathlib import Path

import pytest

from fix_quotes import (
    LEFT_DQ,
    RIGHT_DQ,
    STRAIGHT_DQ,
    fix_quotes_in_text,
    has_cjk,
    is_cjk,
    process_body,
    process_file,
)


# ---------------------------------------------------------------------------
# is_cjk / has_cjk
# ---------------------------------------------------------------------------


class TestIsCjk:
    def test_chinese_character(self):
        assert is_cjk("中")

    def test_ascii_letter(self):
        assert not is_cjk("a")

    def test_digit(self):
        assert not is_cjk("1")

    def test_cjk_punctuation(self):
        assert is_cjk("。")  # U+3002, in CJK Symbols range

    def test_fullwidth_comma(self):
        assert is_cjk("，")  # U+FF0C, in Fullwidth Forms range


class TestHasCjk:
    def test_pure_ascii(self):
        assert not has_cjk("hello world 123")

    def test_with_chinese(self):
        assert has_cjk("hello 你好")

    def test_empty(self):
        assert not has_cjk("")

    def test_only_punctuation_ascii(self):
        assert not has_cjk("hello, world!")

    def test_fullwidth_punctuation(self):
        assert has_cjk("hello，world")


# ---------------------------------------------------------------------------
# fix_quotes_in_text — core logic
# ---------------------------------------------------------------------------


class TestFixQuotesInText:
    # --- ASCII content → straight quotes ---

    def test_straight_quotes_stay_straight_for_ascii(self):
        assert fix_quotes_in_text('"hello world"') == '"hello world"'

    def test_curly_quotes_become_straight_for_ascii(self):
        assert fix_quotes_in_text("\u201chello world\u201d") == '"hello world"'

    def test_mixed_quotes_become_straight_for_ascii(self):
        assert fix_quotes_in_text("\u201chello world\"") == '"hello world"'

    def test_numbers_get_straight_quotes(self):
        assert fix_quotes_in_text('"12345"') == '"12345"'

    def test_ascii_with_punctuation(self):
        assert fix_quotes_in_text('"hello, world!"') == '"hello, world!"'

    def test_single_ascii_word(self):
        assert fix_quotes_in_text('"R"') == '"R"'

    # --- CJK content → curly Chinese quotes ---

    def test_chinese_content_gets_curly_quotes(self):
        assert fix_quotes_in_text('"你好世界"') == "\u201c你好世界\u201d"

    def test_straight_quotes_become_curly_for_chinese(self):
        assert fix_quotes_in_text('"你好"') == "\u201c你好\u201d"

    def test_mixed_content_with_cjk_gets_curly(self):
        assert fix_quotes_in_text('"hello你好"') == "\u201chello你好\u201d"

    def test_content_with_cjk_punctuation_gets_curly(self):
        assert fix_quotes_in_text('"hello，world"') == "\u201chello，world\u201d"

    # --- Multiple quote pairs in the same text ---

    def test_two_pairs_different_styles(self):
        text = '他说"hello"，然后"你好"'
        expected = '他说"hello"，然后\u201c你好\u201d'
        assert fix_quotes_in_text(text) == expected

    def test_two_pairs_both_ascii(self):
        text = '"foo" and "bar"'
        expected = '"foo" and "bar"'
        assert fix_quotes_in_text(text) == expected

    def test_two_pairs_both_chinese(self):
        text = "\u201c第一\u201d和\u201c第二\u201d"
        expected = "\u201c第一\u201d和\u201c第二\u201d"
        assert fix_quotes_in_text(text) == expected

    # --- Edge cases ---

    def test_empty_quotes_get_straight(self):
        assert fix_quotes_in_text('""') == '""'

    def test_unpaired_single_quote_unchanged(self):
        text = '只有一个"没关系'
        assert fix_quotes_in_text(text) == text

    def test_three_quotes_pairs_first_two(self):
        # Three quotes: pair 1st-2nd, 3rd is unpaired and left as-is
        text = '"hello" and "'
        result = fix_quotes_in_text(text)
        assert result == '"hello" and "'

    def test_no_quotes(self):
        text = "no quotes here"
        assert fix_quotes_in_text(text) == text

    def test_preserves_surrounding_text(self):
        text = '前面 "R语言" 后面'
        expected = "前面 \u201cR语言\u201d 后面"
        assert fix_quotes_in_text(text) == expected


# ---------------------------------------------------------------------------
# process_body — code block / frontmatter preservation
# ---------------------------------------------------------------------------


class TestProcessBody:
    def test_preserves_fenced_code_block(self):
        body = '这是"你好"的测试\n\n```python\nprint("hello")\n```\n\n结束'
        result = process_body(body)
        assert 'print("hello")' in result  # code block untouched
        assert "\u201c你好\u201d" in result  # text fixed

    def test_preserves_inline_code(self):
        body = '使用`"quoted"`来表示"字符串"'
        result = process_body(body)
        assert '`"quoted"`' in result  # inline code untouched
        assert "\u201c字符串\u201d" in result  # text fixed

    def test_body_with_no_code(self):
        body = '他说"hello"然后说"你好"'
        result = process_body(body)
        assert '"hello"' in result
        assert "\u201c你好\u201d" in result

    def test_body_all_code(self):
        body = '```\n"hello"\n```'
        result = process_body(body)
        assert result == body  # entirely code, nothing changed

    def test_multiple_code_blocks(self):
        body = '"hello" text\n```\ncode "here"\n```\nmiddle "中文"\n```\nmore "code"\n```\nend "world"'
        result = process_body(body)
        assert result.startswith('"hello"')  # ASCII → straight
        assert 'code "here"' in result  # code block preserved
        assert "\u201c中文\u201d" in result  # CJK → curly
        assert 'more "code"' in result  # code block preserved
        assert result.endswith('"world"')  # ASCII → straight


# ---------------------------------------------------------------------------
# process_file — full integration
# ---------------------------------------------------------------------------


class TestProcessFile:
    def _write_temp_md(self, content: str, suffix: str = ".md") -> str:
        """Write content to a temp file and return its path."""
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        f.write(content)
        f.close()
        return f.name

    def test_chinese_file_mixed_quotes(self):
        content = '---\ntitle: "测试"\n---\n他说"hello"然后"你好"\n'
        path = self._write_temp_md(content)
        process_file(path)
        result = Path(path).read_text(encoding="utf-8")
        # Frontmatter untouched
        assert 'title: "测试"' in result
        # Body fixed per content
        assert '"hello"' in result
        assert "\u201c你好\u201d" in result

    def test_english_file_curly_quotes_fixed(self):
        content = "---\ntitle: Test\n---\nHe said \u201chello\u201d\n"
        path = self._write_temp_md(content, suffix=".en.md")
        process_file(path)
        result = Path(path).read_text(encoding="utf-8")
        assert '"hello"' in result

    def test_dry_run_does_not_write(self):
        content = '---\ntitle: Test\n---\n"你好"\n'
        path = self._write_temp_md(content)
        process_file(path, dry_run=True)
        result = Path(path).read_text(encoding="utf-8")
        assert result == content  # unchanged on disk

    def test_no_change_when_already_correct(self):
        content = '---\ntitle: Test\n---\n"hello" and \u201c你好\u201d\n'
        path = self._write_temp_md(content)
        changed = process_file(path)
        assert not changed

    def test_frontmatter_quotes_preserved(self):
        content = "---\ntitle: \u201c测试\u201d\ndate: '2025-01-01'\n---\nbody\n"
        path = self._write_temp_md(content)
        process_file(path)
        result = Path(path).read_text(encoding="utf-8")
        # Frontmatter must stay exactly as-is
        assert "title: \u201c测试\u201d" in result
