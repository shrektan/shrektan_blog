# Bilingual Blog Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add Chinese/English bilingual support to shrektan.com using Hugo's native multilingual system.

**Architecture:** Hugo's built-in i18n with file-suffix approach (`index.md` for Chinese, `index.en.md` for English). Language prefix URLs (`/zh/`, `/en/`). Browser language detection at root. Separate RSS feeds and menus per language.

**Tech Stack:** Hugo 0.78.2 (existing), TOML config, Go templates, Netlify redirects, vanilla JavaScript

**Design doc:** `docs/plans/2026-02-27-bilingual-blog-design.md`

---

### Task 1: Update Hugo config for multilingual support

**Files:**
- Modify: `config.toml`

**Step 1: Replace config with multilingual version**

Replace the entire `config.toml` with:

```toml
baseurl = "https://shrektan.com"
title = "Xianying's Blog"
theme = "hugo-xmin"
googleAnalytics = "UA-68366586-1"
disqusShortname = ""
ignoreFiles = ["_cache$", "\\.knit\\.md$", "\\.utf8\\.md$"]
footnotereturnlinkcontents = "↩"
enableEmoji = true
hasCJKLanguage = true

defaultContentLanguage = "zh"
defaultContentLanguageInSubdir = true

[permalinks]
    post = "/post/:year/:month/:day/:slug/"
    note = "/note/:year/:month/:day/:slug/"

[languages]
  [languages.zh]
    languageName = "中文"
    languageCode = "zh-cn"
    weight = 1
    [languages.zh.params]
      description = "谭显英的个人博客"
      footer = "&copy; [谭显英](https://shrektan.com) 2017 -- 2025 | [Github](https://github.com/shrektan)"
    [[languages.zh.menu.main]]
      name = "主页"
      url = "/"
      weight = 1
    [[languages.zh.menu.main]]
      name = "关于"
      url = "/about/"
      weight = 2
    [[languages.zh.menu.main]]
      name = "类别"
      url = "/categories/"
      weight = 3
    [[languages.zh.menu.main]]
      name = "标签"
      url = "/tags/"
      weight = 4
    [[languages.zh.menu.main]]
      name = "订阅"
      url = "/index.xml"
      weight = 5

  [languages.en]
    languageName = "English"
    languageCode = "en"
    weight = 2
    [languages.en.params]
      description = "Xianying Tan's personal blog"
      footer = "&copy; [Xianying Tan](https://shrektan.com) 2017 -- 2025 | [Github](https://github.com/shrektan)"
    [[languages.en.menu.main]]
      name = "Home"
      url = "/"
      weight = 1
    [[languages.en.menu.main]]
      name = "About"
      url = "/about/"
      weight = 2
    [[languages.en.menu.main]]
      name = "Categories"
      url = "/categories/"
      weight = 3
    [[languages.en.menu.main]]
      name = "Tags"
      url = "/tags/"
      weight = 4
    [[languages.en.menu.main]]
      name = "Subscribe"
      url = "/index.xml"
      weight = 5

[params]
    highlightjsVersion = "11.3.1"
    highlightjsCDN = "//cdn.bootcss.com"
    highlightjsLang = ["r", "yaml"]
    highlightjsTheme = "default"
    GithubEdit = "https://github.com/shrektan/shrektan_blog/edit/master/content/"

[params.giscus]
    repo = "shrektan/shrektan_blog"
    repoID = "MDEwOlJlcG9zaXRvcnkxMTkyNDkyNTU="
    category = "Comments"
    categoryID = "DIC_kwDOBxuZZ84C2pup"
    mapping = "pathname"
    strict = "0"
    reactionsEnabled = "1"
    emitMetadata = "0"
    inputPosition = "top"
    theme = "preferred_color_scheme"
    loading = "lazy"

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
```

Key changes:
- Removed top-level `languageCode` (now per-language)
- Removed top-level `[[menu.main]]` (now per-language)
- Added `defaultContentLanguage = "zh"` and `defaultContentLanguageInSubdir = true`
- Added `[languages]` section with zh/en
- Giscus `lang` removed from config (will be set dynamically in template)
- `preserveTaxonomyNames` removed (deprecated in Hugo 0.55+)

**Step 2: Verify Hugo builds without errors**

Run: `hugo --buildFuture 2>&1 | head -20`
Expected: Build succeeds, pages output for `/zh/` paths

**Step 3: Commit**

```bash
git add config.toml
git commit -m "feat: add multilingual Hugo config for zh/en"
```

---

### Task 2: Add language switcher to navigation

**Files:**
- Create: `layouts/partials/header.html` (override theme header)
- Modify: `static/css/style.css`

**Step 1: Create project-level header.html**

Create `layouts/partials/header.html`:

```html
<!DOCTYPE html>
<html lang="{{ .Site.Language.Lang }}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ .Title }} | {{ .Site.Title }}</title>
    <link rel="stylesheet" href="{{ "/css/style.css" | relURL }}" />
    <link rel="stylesheet" href="{{ "/css/fonts.css" | relURL }}" />
    {{ partial "head_custom.html" . }}
    {{ if .IsTranslated }}
    {{ range .Translations }}
    <link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}" />
    {{ end }}
    <link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}" />
    {{ end }}
  </head>

  <body>
    <nav>
    <ul class="menu">
      {{ range .Site.Menus.main }}
      <li><a href="{{ .URL | relURL }}">{{ .Name }}</a></li>
      {{ end }}
      <li class="lang-switch">
        {{ if .IsTranslated }}
          {{ range .Translations }}
          <a href="{{ .Permalink }}">{{ .Language.LanguageName }}</a>
          {{ end }}
        {{ else }}
          {{ range $.Site.Languages }}
            {{ if ne .Lang $.Site.Language.Lang }}
            <a href="{{ (printf "/%s/" .Lang) | absURL }}">{{ .LanguageName }}</a>
            {{ end }}
          {{ end }}
        {{ end }}
      </li>
    </ul>
    <hr/>
    </nav>
```

**Step 2: Add language switcher CSS**

Append to `static/css/style.css`:

```css
/* language switcher */
.lang-switch {
  float: right;
}
.lang-switch a {
  font-weight: bold;
}
```

**Step 3: Verify language switcher renders**

Run: `hugo --buildFuture && grep -l "lang-switch" public/zh/index.html`
Expected: File found, contains language switcher markup

**Step 4: Commit**

```bash
git add layouts/partials/header.html static/css/style.css
git commit -m "feat: add language switcher to navigation bar"
```

---

### Task 3: Add translation notice to article pages

**Files:**
- Create: `layouts/_default/single.html` (override theme single page)

**Step 1: Create single.html with translation notice**

Create `layouts/_default/single.html`:

```html
{{ partial "header.html" . }}
<div class="article-meta">
<h1><span class="title">{{ .Title }}</span></h1>
{{ with .Params.subtitle }}<h1><span class="subtitle">{{ . }}</span></h1>{{ end }}
{{ with .Params.author }}<h2 class="author">{{ . }}</h2>{{ end }}
{{ if .Params.date }}<h2 class="date">{{ .Date.Format "2006/01/02" }}</h2>{{ end }}
{{ if and .Params.originalLang (ne .Params.originalLang .Language.Lang) }}
<p class="translation-notice">
  {{ if eq .Language.Lang "zh" }}
    本文原文为英文{{ if .IsTranslated }} · {{ range .Translations }}<a href="{{ .Permalink }}">Read the original</a>{{ end }}{{ end }}
  {{ else }}
    Originally written in Chinese{{ if .IsTranslated }} · {{ range .Translations }}<a href="{{ .Permalink }}">阅读中文原文</a>{{ end }}{{ end }}
  {{ end }}
</p>
{{ end }}
</div>

<main>
{{ .Content }}
</main>

{{ partial "footer.html" . }}
```

**Step 2: Add CSS for translation notice**

Append to `static/css/style.css`:

```css
/* translation notice */
.translation-notice {
  color: #999;
  font-size: 0.85em;
  font-style: italic;
  margin-top: -10px;
}
.translation-notice a {
  color: #666;
}
```

**Step 3: Commit**

```bash
git add layouts/_default/single.html static/css/style.css
git commit -m "feat: add translation notice for non-original language posts"
```

---

### Task 4: Update Giscus to use dynamic language

**Files:**
- Modify: `layouts/partials/giscus.html`

**Step 1: Update giscus.html to use site language**

Replace the `data-lang` line in `layouts/partials/giscus.html`:

Change:
```
    data-lang="{{ .lang | default "en" }}"
```
To:
```
    data-lang="{{ $.Site.Language.Lang }}"
```

This makes Giscus automatically use `zh` for Chinese pages and `en` for English pages.

**Step 2: Commit**

```bash
git add layouts/partials/giscus.html
git commit -m "feat: make Giscus language follow page language"
```

---

### Task 5: Create root redirect page

**Files:**
- Create: `layouts/index.html` (root page template)
- Create: `layouts/index.redir` (Netlify redirect alternative)

**Step 1: Create root index.html for browser language detection**

Create `layouts/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Redirecting...</title>
  <script>
    (function() {
      var lang = navigator.language || navigator.userLanguage || '';
      var target = lang.toLowerCase().startsWith('zh') ? '/zh/' : '/en/';
      window.location.replace(target);
    })();
  </script>
  <noscript>
    <meta http-equiv="refresh" content="0; url=/zh/" />
  </noscript>
</head>
<body>
  <p>Redirecting... <a href="/zh/">中文</a> | <a href="/en/">English</a></p>
</body>
</html>
```

Note: This template is placed at `layouts/index.html` which overrides the default homepage. Hugo's multilingual system generates `/zh/index.html` and `/en/index.html` from `layouts/_default/list.html`, while the root `/index.html` uses this template.

**Step 2: Add Netlify redirects for old URLs**

Create `static/_redirects`:

```
/post/*          /zh/post/:splat     301
/note/*          /zh/note/:splat     301
/about/          /zh/about/          301
/categories/*    /zh/categories/:splat 301
/tags/*          /zh/tags/:splat     301
/index.xml       /zh/index.xml       301
```

**Step 3: Commit**

```bash
git add layouts/index.html static/_redirects
git commit -m "feat: add root language redirect and old URL compatibility"
```

---

### Task 6: Migrate existing post front matter

**Files:**
- Modify: All 54 `content/post/*/index.md` files

**Step 1: Write migration script**

Create `scripts/migrate-frontmatter.sh`:

```bash
#!/bin/bash
# Migrate front matter: remove cn/en from categories, add originalLang
set -euo pipefail

for f in content/post/*/index.md; do
  echo "Processing: $f"

  # Detect language from categories
  if grep -q "^  - cn$" "$f"; then
    LANG="zh"
  elif grep -q "^  - en$" "$f"; then
    LANG="en"
  else
    echo "  SKIP: no cn/en category found"
    continue
  fi

  # Remove the cn/en category line
  if [ "$LANG" = "zh" ]; then
    sed -i '' '/^  - cn$/d' "$f"
  else
    sed -i '' '/^  - en$/d' "$f"
  fi

  # Add originalLang after slug line
  if ! grep -q "^originalLang:" "$f"; then
    sed -i '' "/^slug:/a\\
originalLang: $LANG" "$f"
  fi

  echo "  Done: originalLang=$LANG"
done
```

**Step 2: Run migration script**

Run: `bash scripts/migrate-frontmatter.sh`
Expected: All 54 posts processed, each gets `originalLang` field and loses `cn`/`en` category

**Step 3: Spot-check a few files**

Run: `head -12 content/post/2025-05-05-grow-together/index.md`
Expected: `originalLang: zh` present, no `- cn` in categories

Run: `head -12 content/post/2018-01-28-my-very-first-blog/index.md`
Expected: `originalLang: en` present, no `- en` in categories

**Step 4: Verify Hugo builds**

Run: `hugo --buildFuture 2>&1 | tail -5`
Expected: Build succeeds

**Step 5: Commit**

```bash
git add content/post/ scripts/migrate-frontmatter.sh
git commit -m "refactor: migrate post front matter to use originalLang instead of cn/en categories"
```

---

### Task 7: Create English version of About page

**Files:**
- Create: `content/about.en.md`

**Step 1: Create English About page**

Create `content/about.en.md` using the existing `content/about.md` content (which is already in English):

```markdown
---
title: About Me
author: Xianying Tan
---

- I've learned [actuarial science](https://en.wikipedia.org/wiki/Actuarial_science) for almost 7 years and I am working in financial industry as a quant.
- My father bought me a computer when I was 10 years old (around 2000) and I felt love in it immediately. However, I had to learn everything by myself because there's simply no people knew much about computers at that time in my hometown. I have developed a good intuition about how computers work but I didn't realize my passion on programming until my first internship as an assitant acturay in a life insurance company.
- R is my favouite language but occationally I need C++ as the core calculating engine to boost the performance. Excel and VBA is also on my skill set because they're quite handy and used widely in the office. I had some experience on VB.NET but no a big fan of it. I also know a little bit about shell, javascript, css, html, etc.
```

**Step 2: Create Chinese About page**

Replace content of `content/about.md` with a Chinese version (author to write or translate):

```markdown
---
title: 关于我
author: 谭显英
---

TODO: 作者撰写中文版关于页面
```

**Step 3: Commit**

```bash
git add content/about.md content/about.en.md
git commit -m "feat: split About page into zh/en versions"
```

---

### Task 8: Create English homepage content

**Files:**
- Create: `content/_index.en.md`

**Step 1: Create English homepage**

Create `content/_index.en.md`:

```markdown
---
title: Home
---

[<img src="/img/monkey-circle.png" style="max-width:15%;min-width:40px;float:right;" alt="Shrektan's Github Repo" />](https://github.com/shrektan)

One of my favorite quotes from "Leading" by Alex Ferguson:

> There's a reason that God gave us two ears, two eyes and one mouth. It's so you can listen and watch twice as much as you talk. Best of all, listening costs you nothing.
```

**Step 2: Commit**

```bash
git add content/_index.en.md
git commit -m "feat: add English homepage content"
```

---

### Task 9: Create one sample translation for demo

**Files:**
- Create: `content/post/2025-05-05-grow-together/index.en.md`

**Step 1: Create English translation of the "一起长大" post**

Create `content/post/2025-05-05-grow-together/index.en.md` with front matter:

```yaml
---
title: Growing Together
author: Xianying Tan
date: '2025-05-05'
slug: grow-together
originalLang: zh
categories:
  - life
tags:
  - life
  - parenting
---
```

Body: AI-assisted translation of the Chinese original. Author will review.

**Step 2: Verify both versions render**

Run: `hugo --buildFuture && ls public/zh/post/2025/05/05/grow-together/ public/en/post/2025/05/05/grow-together/`
Expected: Both directories contain `index.html`

**Step 3: Check language switcher works**

Run: `grep "lang-switch" public/zh/post/2025/05/05/grow-together/index.html`
Expected: Contains link to `/en/post/2025/05/05/grow-together/`

**Step 4: Check translation notice renders**

Run: `grep "Originally written in Chinese" public/en/post/2025/05/05/grow-together/index.html`
Expected: Found

**Step 5: Commit**

```bash
git add content/post/2025-05-05-grow-together/index.en.md
git commit -m "feat: add sample English translation of 'Growing Together'"
```

---

### Task 10: Update Netlify config for Hugo version

**Files:**
- Modify: `netlify.toml`

**Step 1: Verify Hugo version supports multilingual**

Hugo 0.78.2 fully supports multilingual with `defaultContentLanguageInSubdir`. No version change needed, but ensure the build command works.

The existing `netlify.toml` should work as-is since `hugo --buildFuture` will automatically pick up the multilingual config. No changes needed unless build fails.

**Step 2: Test full build**

Run: `hugo --buildFuture 2>&1`
Expected: Build succeeds with output showing both `/zh/` and `/en/` paths

**Step 3: Verify key output files exist**

Run:
```bash
ls public/index.html          # Root redirect page
ls public/zh/index.html       # Chinese homepage
ls public/en/index.html       # English homepage
ls public/zh/index.xml        # Chinese RSS
ls public/en/index.xml        # English RSS
```
Expected: All files exist

**Step 4: Commit any remaining changes**

```bash
git add -A
git commit -m "chore: verify full build with multilingual setup"
```

---

### Task 11: Create translation helper script

**Files:**
- Create: `scripts/translate.sh`

**Step 1: Create the script**

Create `scripts/translate.sh`:

```bash
#!/bin/bash
# Usage: ./scripts/translate.sh content/post/2025-05-05-slug/
# Generates the missing language version of a post.
set -euo pipefail

POST_DIR="${1:?Usage: $0 <post-directory>}"

if [ ! -d "$POST_DIR" ]; then
  echo "Error: Directory $POST_DIR does not exist"
  exit 1
fi

ZH_FILE="$POST_DIR/index.md"
EN_FILE="$POST_DIR/index.en.md"

if [ -f "$ZH_FILE" ] && [ ! -f "$EN_FILE" ]; then
  echo "Chinese source found. Will generate English version."
  echo "Source: $ZH_FILE"
  echo "Target: $EN_FILE"
  echo ""
  echo "TODO: Integrate with AI translation API"
  echo "For now, copy and manually translate:"
  cp "$ZH_FILE" "$EN_FILE"
  echo "Created: $EN_FILE (copy of Chinese — please translate)"

elif [ -f "$EN_FILE" ] && [ ! -f "$ZH_FILE" ]; then
  echo "English source found. Will generate Chinese version."
  echo "Source: $EN_FILE"
  echo "Target: $ZH_FILE"
  echo ""
  cp "$EN_FILE" "$ZH_FILE"
  echo "Created: $ZH_FILE (copy of English — please translate)"

elif [ -f "$ZH_FILE" ] && [ -f "$EN_FILE" ]; then
  echo "Both versions already exist:"
  echo "  $ZH_FILE"
  echo "  $EN_FILE"
  exit 0

else
  echo "Error: No index.md or index.en.md found in $POST_DIR"
  exit 1
fi
```

**Step 2: Make executable**

Run: `chmod +x scripts/translate.sh`

**Step 3: Test the script**

Run: `./scripts/translate.sh content/post/2018-01-28-my-very-first-blog/`
Expected: Reports that only one version exists and creates a copy

**Step 4: Clean up test output** (delete the test copy)

Run: Remove any generated test files that shouldn't be committed yet.

**Step 5: Commit**

```bash
git add scripts/translate.sh
git commit -m "feat: add translation helper script scaffold"
```

---

## Summary of file changes

**Modified:**
- `config.toml` — multilingual config
- `static/css/style.css` — language switcher + translation notice CSS
- `layouts/partials/giscus.html` — dynamic language
- `content/about.md` — Chinese version
- All 54 `content/post/*/index.md` — front matter migration

**Created:**
- `layouts/partials/header.html` — with language switcher + hreflang tags
- `layouts/_default/single.html` — with translation notice
- `layouts/index.html` — root redirect page
- `static/_redirects` — Netlify old URL redirects
- `content/_index.en.md` — English homepage
- `content/about.en.md` — English About page
- `content/post/2025-05-05-grow-together/index.en.md` — sample translation
- `scripts/migrate-frontmatter.sh` — front matter migration script
- `scripts/translate.sh` — translation helper script
