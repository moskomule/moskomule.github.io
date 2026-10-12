# hataya.tokyo

Source of https://hataya.tokyo, built with [Hugo](https://gohugo.io) (≥ 0.165; CI uses 0.167.0) and the
in-repo theme `themes/hataya`. Pushing to `source` builds the site with GitHub Actions and deploys it
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
| Profile picture / cover photo | `hugo.toml` → `[params.profile]` (`avatar`, `cover`) |
| Short bio under the name | `content/<lang>/home/index.md` (body) |
| Top-page sections (About, Publications, …) | `content/<lang>/home/*.md`, ordered by `weight` |
| Photo band before a section | `image:` (or `band:`) in that section's front matter; `band: false` hides it |
| Contact section | `content/<lang>/home/contact.md` |
| Projects | `content/<lang>/projects/_index.md` + one bundle per project |
| Blog posts | `content/<lang>/blog/<slug>/index.md` |
| Publications | `publications.bib` |

## Add a publication

Edit `publications.bib`. Besides the usual BibTeX fields, the site reads:

- `abbr = {ICCV 2023}` — badge text
- `keywords = {selected}` — show in the "Selected" tab
- `category = {workshop}` — `journal` / `conference` / `workshop` / `preprint` / `other`
  (default: `@article` → journal, `@inproceedings` → conference, `@misc` → preprint)
- `equal = {1,2}` — equal-contribution authors (1-based)
- `note`, `arxiv`, `openreview`, `code`, `slides`, `pdf`, `project` — shown as text / links

Any markdown page can show the list with `{{< publications >}}`
(options: `filter="all"`, `tabs="false"`, `category="journal"`).

## Add a project

```sh
hugo new content en/projects/my-project/index.md
```

Add a picture next to `index.md`, write `description`, set `draft: false`.
The home page shows up to `params.home.numberOfProjectsToShow` projects.

## Add a blog post

```sh
hugo new content ja/blog/my-post/index.md
```

## Math

MathJax 4 is loaded only on pages that need it (`params.math = "auto"`: the top page and pages
whose source contains `$`, `\(` or `\[`). Force it per page with `math: true` / `math: false`
in front matter, or site-wide with `math = true` / `false` in `hugo.toml`.
