# hataya.tokyo

Source of https://hataya.tokyo, built with [Hugo](https://gohugo.io) (≥ 0.158; CI uses 0.167.0) and the
in-repo theme `themes/hataya_theme`. Pushing to `source` builds the site with GitHub Actions and deploys it
to GitHub Pages (`.github/workflows/publish.yml`, following the Hugo docs). Pull requests are built but not deployed.

Repository setting: **Settings → Pages → Source = GitHub Actions**, custom domain `hataya.tokyo`.

## Local preview

```sh
python3 scripts/bib2json.py   # publications.bib -> data/publications.json
hugo server
```

## Where things live

| What | File |
| --- | --- |
| Name, tagline, affiliations (per language) | `hugo.toml` → `[languages.*.params]` |
| Profile picture / cover photos | `assets/images/profile.png`, `assets/images/covers/` (one is picked at random on each page load); see `hugo.toml` → `[params.profile]` |
| Short bio under the name | `content/<lang>/home/index.md` (body) |
| Top-page sections (About, Publications, …) | `content/<lang>/home/*.md`, ordered by `weight` |
| Photo band before a section | `assets/images/`, chosen with `image: "images/xxx.jpg"` (or `band:`) in that section's front matter; `band: false` hides it |
| Contact section | `content/<lang>/home/contact.md` |
| Projects | `content/<lang>/projects/_index.md` + one bundle per project |
| Blog posts | `content/<lang>/blog/<slug>/index.md` |
| Publications | `publications.bib` |

## Photos

| Photo | Where to put it | Recommended size | Notes |
| --- | --- | --- | --- |
| Profile picture | `assets/images/`, set `params.profile.avatar` | 600 × 600 px, square | Shown as a 168 px circle (104 px on phones); keep the face centered |
| Cover photo | `assets/images/covers/` (all photos there rotate at random), or one file set in `params.profile.cover` | 2400 × 800 px (3 : 1) | Shown 1280 × 320 on PCs, about 390 × 150 on phones. Top and bottom are cropped; adjust with `coverPosition` (e.g. `"center 30%"`) |
| Section photo band | `assets/images/`, `image: "images/xxx.jpg"` (or `band:`) in the section's front matter | 2400 × 600 px (4 : 1) | Shown up to 320 px tall across the full width; the left and right edges are cropped on phones |
| Project thumbnail | next to the project's `index.md` | 1600 × 900 px (16 : 9) | Cropped to 16 : 9 from the center |

- JPEG (quality ~85) or WebP; landscape photos rather than portrait.
- Larger images are resized automatically (cover/bands to 2400 px wide), so camera originals are fine.
- `assets/images/` is shared by both languages. Images used by one blog post or project go next to its `index.md` instead.
- The bottom-left of the cover sits behind the profile picture, and the top-right behind the language switch.

## Add a publication

Edit `publications.bib` (entries are grouped by year, newest first; the page is sorted automatically, so the order in the file is only for readability). Besides the usual BibTeX fields, the site reads:

- `abbr = {ICCV 2023}` — badge text
- `keywords = {selected}` — show in the "Selected" tab
- `category = {workshop}` — `journal` / `conference` / `workshop` / `preprint` / `other`
  (default: `@article` → journal, `@inproceedings` → conference, `@misc` → preprint)
- `equal = {1,2}` — equal-contribution authors (1-based)
- `note`, `arxiv`, `openreview`, `code`, `slides`, `pdf`, `poster`, `video`, `project` — shown as text / links

Any markdown page can show the list with `{{< publications >}}`
(options: `filter="all"` to start on "All", `category="journal"` for one category without filter buttons).

## Add a project

```sh
hugo new content content/en/projects/my-project/index.md
```

Add a picture next to `index.md`, write `description`, set `draft: false`.
The home page shows up to `params.home.numberOfProjectsToShow` projects.

## Add a blog post

```sh
hugo new content content/ja/blog/my-post/index.md
```

## Math

MathJax 4 is loaded only on pages that need it (`params.math = "auto"`: the top page and pages
whose source contains `$`, `\(` or `\[`). Force it per page with `math: true` / `math: false`
in front matter, or site-wide with `math = true` / `false` in `hugo.toml`.

## Theme files (`themes/hataya_theme`)

| File | Role |
| --- | --- |
| `layouts/baseof.html` | page skeleton |
| `layouts/home.html` | top page: cover, profile, section tabs, sections with photo bands |
| `layouts/list.html`, `single.html` | blog / tag lists and posts |
| `layouts/projects/` | project list and project pages |
| `layouts/_partials/` | header, footer, head (CSS, JS, MathJax), small helpers in `funcs/` |
| `layouts/_shortcodes/publications.html` | publication list |
| `assets/css/main.css` | all styles; colors and widths are variables at the top |
| `assets/js/main.js` | publication filter buttons (the random cover is a two-line inline script in `home.html`) |
| `i18n/*.yaml` | English / Japanese labels |
