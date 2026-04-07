# shrektan.com Blog

## Stack
- Hugo v0.78.2 (extended) — very old, do NOT assume modern Hugo features
- Theme: hugo-xmin (custom partials in layouts/ override theme)
- Hosting: **Cloudflare Pages** (NOT Netlify)
- Bilingual: zh (default) + en, `defaultContentLanguageInSubdir = true`

## Cloudflare Pages gotchas
- Static files take priority over `_redirects` — cannot redirect away from existing HTML files
- Use `_headers` file for HTTP header overrides on static pages (X-Robots-Tag, Link canonical)
- No `!` force flag, no `Language=` conditions — these are Netlify-only syntax
- `_redirects` only fires when no static file matches the path

## Hugo 0.78.2 known issue
- EN-only posts (only `index.en.md`, no `index.md`) generate ghost pages under `/zh/` path
- Ghost pages use the THEME's templates (missing canonical, description, hreflang)
- Managed via `static/_headers` (X-Robots-Tag: noindex + Link canonical)
- When adding new EN-only posts, add corresponding entry to `_headers` and `_redirects`

## Build
- `hugo --gc` to build (output in public/)
- No build script or CI config — deployed directly via Cloudflare Pages git integration

## Content conventions
- Posts live in `content/post/YYYY-MM-DD-slug/` with `index.md` (zh) and/or `index.en.md` (en)
- Required frontmatter: `title`, `date`, `slug`, `categories`, `tags`, `description` (for SEO)
- `originalLang: zh|en` — tracks which language was written first (used by translation workflow)
- About page: `content/about.md` (zh) + `content/about.en.md` (en)

## Key layout overrides (over hugo-xmin theme)
- `layouts/partials/head_custom.html` — all SEO meta tags (canonical, OG, JSON-LD, description)
- `layouts/partials/header.html` — nav bar with language switcher + hreflang tags
- `layouts/partials/giscus.html` — comments integration
- `layouts/_default/single.html` / `list.html` — page templates
