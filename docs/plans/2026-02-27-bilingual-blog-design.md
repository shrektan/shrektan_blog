# Bilingual Blog Design

## Overview

Add Chinese/English bilingual support to shrektan.com using Hugo's native multilingual system. Each post will have both language versions, with AI-assisted translation and author review.

## Technical Approach: Hugo Native i18n + Separate Files

### Content Structure

```
content/post/2025-05-05-grow-together/
├── index.md        ← Chinese (default language, no suffix)
├── index.en.md     ← English version
└── images/
    └── image2.png  ← Shared assets
```

### Hugo Configuration

- Default language: `zh` (Chinese)
- `defaultContentLanguageInSubdir = true` → Chinese also gets `/zh/` prefix
- Two language entries: `[languages.zh]` and `[languages.en]`
- Separate menus per language

### URL Structure

| Page | Chinese | English |
|------|---------|---------|
| Home | `/zh/` | `/en/` |
| Post | `/zh/post/2025/05/05/slug/` | `/en/post/2025/05/05/slug/` |
| About | `/zh/about/` | `/en/about/` |
| RSS | `/zh/index.xml` | `/en/index.xml` |

### Root Path

`shrektan.com/` → JavaScript browser language detection → redirect to `/zh/` or `/en/`.

### Old URL Compatibility

Netlify `_redirects` file: `/post/* → /zh/post/:splat 301`

## UI Design

### Language Switcher

Navigation bar right side: `[EN]` on Chinese pages, `[中文]` on English pages. Links to the corresponding page in the other language (or that language's homepage if translation doesn't exist).

### Translation Notice

In front matter: `originalLang: zh` or `originalLang: en`.

- If current language != originalLang → show notice:
  - Chinese page, English original: "本文原文为英文 · Read the original"
  - English page, Chinese original: "Originally written in Chinese · 阅读中文原文"
- If current language == originalLang → no notice (this is the original)

### Menus

Separate menus per language (no more "主页/Home" combined labels).

### RSS

Separate feeds per language, automatically handled by Hugo.

### Comments (Giscus)

Independent per language version (different pathnames → different discussions). Language setting follows page language.

## Translation Workflow

1. Author writes one version (e.g., `index.md` in Chinese)
2. Run `scripts/translate.sh content/post/2025-05-05-slug/`
3. Script generates `index.en.md` via AI API with proper front matter
4. Author reviews and edits the translation
5. Commit both files

## Migration Strategy

- Old posts: keep `index.md` as-is, no English version initially
- Translate old posts gradually, by importance
- New posts: always create both versions
