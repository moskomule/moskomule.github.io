# hataya.tokyo

Source of https://hataya.tokyo, built with [Hugo](https://gohugo.io) (≥ 0.128, CI uses 0.145.0) and the
in-repo theme `themes/hataya`. Pushing to `source` builds the site and publishes it to `master`.

## Local preview

```sh
python3 scripts/bib2json.py   # publications.bib -> data/publications.json
hugo server
```

## Where things live

| What | File |
| --- | --- |
| Name, tagline, affiliations (per language) | `config.toml` → `[languages.*.params]` |
| Profile picture / cover photo | `config.toml` → `[params.profile]` (`avatar`, `cover`) |
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
