# shrektan.com Blog

## Stack
- Hugo v0.78.2 (extended) — very old, do NOT assume modern Hugo features
- Theme: hugo-xmin (custom partials in layouts/ override theme)
- Hosting: **Cloudflare Pages** (NOT Netlify)
- Bilingual: zh (default) + en, `defaultContentLanguageInSubdir = true`
- Live alternate hostname: `blog.shrektan.com` serves the same content. Canonical tags point to `shrektan.com` so SEO is anchored there, but Google still tracks both URL spaces.

## Cloudflare Pages gotchas
- Static files take priority over `_redirects` — cannot redirect away from existing HTML files
- No `!` force flag, no `Language=` conditions — these are Netlify-only syntax
- `_redirects` only fires when no static file matches the path
- Catch-all redirects must come AFTER specific rules. The `/categories/* → /zh/categories/:splat` and `/tags/* → /zh/tags/:splat` catch-alls assume every term exists in ZH — terms that were removed (old `cn`/`en` categories) or that only live in EN (e.g. `git` tag) need explicit overrides above the catch-all, otherwise they 301 into a 404. See `static/_redirects`.

## Taxonomy / SEO notes
- Hugo 0.78.2 with the current config does NOT generate ghost `/zh/` pages for EN-only posts on a clean build. The Cloudflare deploy is always clean, so no `_headers` workaround is needed. (Earlier CLAUDE.md notes about ghost pages were based on dirty local builds.)
- When adding a tag/category that only lives in one language, add a matching `_redirects` override so the cross-language URL doesn't 404.
- EN posts currently use fragmented category names (`Tech`/`技术`, `Life`/`生活`, `Musings`/`随想`/`Thoughts`/`Random Thoughts`) — known content debt, creates thin duplicate taxonomy pages.

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

## Session Learnings
- [2026-04-14] Session learnings stored in `memories/` — read these at session start for project context.
