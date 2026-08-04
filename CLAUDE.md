# shrektan.com Blog

## Stack
- Hugo (extended) — local toolchain is v0.159.1 as of 2026-08-05 (Homebrew). The old "v0.78.2, assume nothing modern" note is stale; local builds are clean on current Hugo, with one deprecation warning for `.Site.Languages` (removed in a future release — will need fixing eventually).
- **No Hugo version is pinned in this repo** — no `HUGO_VERSION` file, no `netlify.toml`, no `minVersion` in `config.toml`. The version Cloudflare Pages builds with lives in the Pages dashboard env vars and cannot be read from here. If a deploy ever breaks on a feature that works locally, that gap is the first place to look.
- Theme: hugo-xmin (custom partials in layouts/ override theme)
- Hosting: **Cloudflare Pages** (NOT Netlify)
- Bilingual: zh (default) + en, `defaultContentLanguageInSubdir = true`
- Alternate hostname: `blog.shrektan.com` is 301-redirected to `shrektan.com` at the Cloudflare edge (Redirect Rule on the `shrektan.com` zone, matches on `Hostname eq blog.shrektan.com`). DNS record stays; Pages custom-domain mapping may or may not be removed — Redirect Rule fires first either way. Do NOT re-enable it as a live mirror: it creates "Alternate page (proper canonical)" entries in GSC that cannot be dismissed and trigger repeated false "validation failed" noise.

## Cloudflare Pages gotchas
- Static files take priority over `_redirects` — cannot redirect away from existing HTML files
- No `!` force flag, no `Language=` conditions — these are Netlify-only syntax
- `_redirects` only fires when no static file matches the path
- Catch-all redirects must come AFTER specific rules. The `/categories/* → /zh/categories/:splat` and `/tags/* → /zh/tags/:splat` catch-alls assume every term exists in ZH — terms that were removed (old `cn`/`en` categories) or that only live in EN (e.g. `git` tag) need explicit overrides above the catch-all, otherwise they 301 into a 404. See `static/_redirects`.

## GSC status vs error — don't "validate fix" the status-class items
- Google Search Console 的「网页未编入索引」报告里**既有真错误、也有正常状态**，混在一起。分辨规则：
  - **真错误**：标题里有「404」「重定向异常」「无法抓取」「服务器错误」「已屏蔽」——这些要动代码。
  - **正常状态**（不要碰）：「备用网页（有适当的规范标记）」「已抓取 - 尚未编入索引」「已发现 - 尚未编入索引」——这些是 Google 在报告"为什么没收录"，但原因是 by design，不是故障。
- **绝对不要按「验证修复」**：如果状态是正常类，按了必然失败（因为没东西修），然后反复触发"验证失败"邮件，制造假警报。
- 历次在这个项目上的"修复"：`7981408`（真 404，正确修）、`2134e70`（真 404，正确修）、`2026-04-20` session（误判「备用网页」为错误，决定 301 消灭 blog.shrektan.com 来彻底从报告里消掉）。

## Taxonomy / SEO notes
- The current config does NOT generate ghost `/zh/` pages for EN-only posts on a clean build (re-verified 2026-08-05 on Hugo 0.159.1). The Cloudflare deploy is always clean, so no `_headers` workaround is needed. (Earlier CLAUDE.md notes about ghost pages were based on dirty local builds.)
- When adding a tag/category that only lives in one language, add a matching `_redirects` override so the cross-language URL doesn't 404.
- EN posts currently use fragmented category names (`Tech`/`技术`, `Life`/`生活`, `Musings`/`随想`/`Thoughts`/`Random Thoughts`) — known content debt, creates thin duplicate taxonomy pages.

## Build
- `hugo --gc` to build (output in public/)
- No build script or CI config — deployed directly via Cloudflare Pages git integration

## Content conventions
- Posts live in `content/post/YYYY-MM-DD-slug/` with `index.md` (zh) and/or `index.en.md` (en)
- Required frontmatter: `title`, `date`, `slug`, `categories`, `tags`, `description` (for SEO)
- **`date` must carry a time + offset when publishing same-day** (e.g. `'2026-08-05T01:00:00+08:00'`). `config.toml` sets no `timeZone`, so a bare `date: 'YYYY-MM-DD'` is parsed as UTC midnight. Writing after local midnight in +08:00 means that instant is still up to 8 hours in the future by UTC, and Hugo silently drops the page — no error, no warning, it just isn't in `public/`. Bit us on `2026-08-05-the-other-half-of-intuition`. **Always confirm the new post actually appears under `public/{zh,en}/post/...` after building**; the page-count table alone won't tell you.
- `originalLang: zh|en` — tracks which language was written first (used by translation workflow)
- About page: `content/about.md` (zh) + `content/about.en.md` (en)
- **Inline images**: `img-01.jpg`, `img-02.jpg` ... in post directory, referenced via `![alt](img-NN.jpg)` in markdown. Count scales with word count (see `blog-coauthoring` Skill Step 3.5). `img-01.*` doubles as OG image automatically (see `head_custom.html`).
- **Legacy `cover.jpg`**: Convention deprecated for new posts. Old posts keep their `cover.jpg` as OG fallback — `head_custom.html` checks `img-01.*` first, then `cover.*`. Don't delete old covers.

## Key layout overrides (over hugo-xmin theme)
- `layouts/partials/head_custom.html` — all SEO meta tags (canonical, OG, JSON-LD, description)
- `layouts/partials/header.html` — nav bar with language switcher + hreflang tags
- `layouts/partials/giscus.html` — comments integration
- `layouts/_default/single.html` / `list.html` — page templates

## Session Learnings
- [2026-04-14] Session learnings stored in `memories/` — read these at session start for project context.
