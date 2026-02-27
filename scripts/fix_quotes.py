#!/usr/bin/env python3
"""Fix quotation marks in Markdown files.

Rules:
- Chinese articles (or text near CJK characters): use \u201c\u201d (curly double quotes)
- English articles: use " (U+0022, straight double quotes)

Language detection:
- *.en.md files → English
- Otherwise, detect from CJK character count in body

Preserves:
- YAML frontmatter (quotes there are YAML syntax)
- Fenced code blocks (```...```)
- Inline code (`...`)

Usage:
    uv run scripts/fix_quotes.py file.md               # fix a single file
    uv run scripts/fix_quotes.py content/post/          # fix all .md files recursively
    uv run scripts/fix_quotes.py file.md --dry-run      # preview changes without writing
"""

import re
import sys
from pathlib import Path

LEFT_DQ = "\u201c"  # "
RIGHT_DQ = "\u201d"  # "
STRAIGHT_DQ = '"'  # "

# All characters we treat as "a double quote"
ALL_DQ = {STRAIGHT_DQ, LEFT_DQ, RIGHT_DQ}

# Regex to match segments we must NOT modify:
#   1. Fenced code blocks: ```...```
#   2. Inline code: `...` (single line only)
CODE_RE = re.compile(r"(```[^\n]*\n.*?```|`[^`\n]+`)", re.DOTALL)


def is_cjk(ch: str) -> bool:
    """Check if a character is CJK."""
    cp = ord(ch)
    return (
        (0x4E00 <= cp <= 0x9FFF)  # CJK Unified Ideographs
        or (0x3400 <= cp <= 0x4DBF)  # Extension A
        or (0x20000 <= cp <= 0x2A6DF)  # Extension B
        or (0xF900 <= cp <= 0xFAFF)  # Compatibility Ideographs
        or (0x3000 <= cp <= 0x303F)  # CJK Symbols & Punctuation
        or (0xFF01 <= cp <= 0xFF60)  # Fullwidth Forms
    )


def detect_lang(filepath: str, body: str) -> str:
    """Detect article language from filename or body content."""
    if ".en." in Path(filepath).name:
        return "en"
    cjk_count = sum(1 for c in body if is_cjk(c))
    return "zh" if cjk_count > 20 else "en"


def fix_dq_chinese(text: str, opening: bool) -> tuple[str, bool]:
    """Convert all double quotes to Chinese curly style \u201c\u201d.

    Tracks opening/closing state across calls so quotes spanning
    across code blocks are handled correctly.
    Returns (fixed_text, new_opening_state).
    """
    result = []
    for ch in text:
        if ch in ALL_DQ:
            result.append(LEFT_DQ if opening else RIGHT_DQ)
            opening = not opening
        else:
            result.append(ch)
    return "".join(result), opening


def fix_dq_english(text: str) -> str:
    """Convert all curly double quotes to straight "."""
    return text.replace(LEFT_DQ, STRAIGHT_DQ).replace(RIGHT_DQ, STRAIGHT_DQ)


def process_body(body: str, lang: str) -> str:
    """Fix quotes in markdown body, preserving code blocks."""
    parts = []
    last = 0
    opening = True  # track open/close state across text segments

    for m in CODE_RE.finditer(body):
        # Process text before this code segment
        text = body[last : m.start()]
        if lang == "zh":
            text, opening = fix_dq_chinese(text, opening)
        else:
            text = fix_dq_english(text)
        parts.append(text)
        parts.append(m.group())  # keep code as-is
        last = m.end()

    # Process remaining text after last code segment
    text = body[last:]
    if lang == "zh":
        text, opening = fix_dq_chinese(text, opening)
    else:
        text = fix_dq_english(text)
    parts.append(text)

    return "".join(parts)


def process_file(filepath: str, dry_run: bool = False) -> bool:
    """Process a markdown file. Returns True if changes were made."""
    content = Path(filepath).read_text(encoding="utf-8")

    # Separate YAML frontmatter (don't touch it)
    fm = ""
    body = content
    fm_match = re.match(r"(---\n.*?\n---\n)", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        body = content[fm_match.end() :]

    lang = detect_lang(filepath, body)
    fixed_body = process_body(body, lang)
    fixed = fm + fixed_body

    changed = fixed != content
    if changed:
        print(f"  Fixed ({lang}): {filepath}")
        # Show changed lines
        orig_lines = content.splitlines()
        fixed_lines = fixed.splitlines()
        for i, (a, b) in enumerate(zip(orig_lines, fixed_lines), 1):
            if a != b:
                print(f"    L{i}:")
                print(f"      - {a}")
                print(f"      + {b}")
        if not dry_run:
            Path(filepath).write_text(fixed, encoding="utf-8")
    else:
        print(f"  OK ({lang}): {filepath}")

    return changed


def main() -> None:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    paths = [a for a in args if not a.startswith("--")]

    if not paths:
        print(__doc__)
        sys.exit(1)

    files: list[str] = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            files.append(str(path))
        elif path.is_dir():
            files.extend(str(f) for f in sorted(path.rglob("*.md")))

    if not files:
        print("No .md files found.")
        sys.exit(1)

    changed = 0
    for f in files:
        if process_file(f, dry_run):
            changed += 1

    mode = "would change" if dry_run else "changed"
    print(f"\n  {changed}/{len(files)} files {mode}.")


if __name__ == "__main__":
    main()
