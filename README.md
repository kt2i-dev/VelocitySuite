# Velocity Suite mockups

Clickable HTML mockups and build notes for the Velocity Suite: applications for different
industries and sectors, built to one shared standard. The first is **Quality Assurance** for
**Manufacturing**.

Everything here is public and all data in the mockups is fictional.

## Viewing

Locally: open `docs/index.html` in a browser, or serve the folder:

```bash
python3 -m http.server -d docs 8000
```

Live site: GitHub Pages serves the `docs/` folder of `main` (repo **Settings → Pages → Deploy from a
branch → main / docs**). No build step and no workflow.

## Layout

| Path | What it is |
|---|---|
| `docs/index.html` | Start page: the standards (Button standard, Details/Edit Screen Template, Custom widgets), a tile per sector, then the review checklist and recent updates |
| `docs/updates.html` | **Recent updates**, newest first. Add a dated entry with each change and update the "last updated" date on the start page's tile |
| `docs/<sector>/index.html` | A sector's page: a tile per application |
| `docs/<sector>/<app>/…` | An application's screens (none yet) |
| `docs/assets/site.css` | Shared styles for every page |

## Coming soon

A page without enough detail yet is a disabled tile (`<div class="tile disabled" aria-disabled="true">`
with a `<span class="soon">Coming soon</span>` badge) rather than a link. When its page is built, turn
the `div` back into an `<a class="tile" href="…">` and drop the badge.
