---
name: translate-post
description: Use when translating a blog post between Chinese and English, when user says "翻译", "translate", or asks to create a Chinese/English version of an article
---

# Translate Blog Post

Translate a blog post between Chinese and English, creating the corresponding language file with proper front matter and natural prose.

## File Convention

| Language | Filename       | Example URL         |
|----------|---------------|---------------------|
| Chinese  | `index.md`    | `/zh/post/...`      |
| English  | `index.en.md` | `/en/post/...`      |

Both files live in the same post directory (e.g., `content/post/2025-05-05-grow-together/`).

## Workflow

1. **Identify source**: Read the existing file to determine the source language
   - Only `index.md` exists → source is Chinese, create `index.en.md`
   - Only `index.en.md` exists → source is English, create `index.md`
   - Both exist → inform user, ask which to update
2. **Translate front matter** (see rules below)
3. **Translate body** (see quality guidelines below)
4. **Write the target file**
5. **Build and verify**: Run `hugo` to confirm no errors

## Front Matter Rules

**Keep unchanged:**
- `slug` — must be identical so Hugo links the translation pair
- `date`
- `originalLang` — always reflects the *original writing language*, not the current file's language
- `categories`
- `tags` (may add relevant tags in the target language if appropriate)

**Translate:**
- `title` — translate naturally, not literally

**Author name mapping:**
- Chinese: `author: 谭显英`
- English: `author: Xianying Tan`

### Example: Chinese original → English translation

Source `index.md`:
```yaml
---
title: 一起长大
author: 谭显英
date: '2025-05-05'
slug: grow-together
originalLang: zh
tags:
  - life
---
```

Target `index.en.md`:
```yaml
---
title: Growing Together
author: Xianying Tan
date: '2025-05-05'
slug: grow-together
originalLang: zh
tags:
  - life
---
```

Note: `originalLang: zh` stays `zh` in both files — this tells the template system which language was the original, so the AI translation notice appears only on the translated version.

## Translation Quality Guidelines

**Voice and tone:**
- Preserve the author's personal voice — this is a personal blog, not corporate copy
- Match the register: casual essays stay casual, technical posts stay precise
- The author's Chinese writing is literary and reflective; English translations should feel equally natural and eloquent, not stilted

**Prose quality:**
- Translate meaning and intent, NOT word-by-word
- Restructure sentences to sound natural in the target language
- Chinese tends toward parallel structures and four-character idioms — convert these into idiomatic English equivalents rather than literal translations
- English tends toward shorter sentences — when translating to Chinese, combine where natural

**Technical content:**
- Keep code blocks, command examples, and technical terms unchanged
- Translate surrounding explanations naturally
- Keep library/tool names in their original form (e.g., "blogdown", "Hugo", "RStudio")

**What NOT to add:**
- Do NOT add translator notes or commentary in the article body
- Do NOT add "本文由 AI 辅助翻译" in the body — this is handled automatically by the template
- Do NOT change the meaning or add/remove content

## Translation Notice (Automatic)

The template (`layouts/_default/single.html`) automatically shows:
- On Chinese translation of English original: "本文由 AI 辅助翻译，原文为英文"
- On English translation of Chinese original: "Translated with AI assistance, originally written in Chinese"

No manual action needed — this is driven by `originalLang` vs the page's language.
