# Velocity Suite mockups

Clickable HTML mockups and build notes for KT2i's **Velocity Suite for Manufacturing**: Manufacturing
Operations Management applications on OutSystems, in five sectors (Quality / Engineering, Supply Chain /
Logistics, Production / Maintenance, Safety / Environment, Workforce / Training). The first solution is
**Quality Event & Corrective Action Management** (CAPA / SCAR / MRB / NCR) in Quality / Engineering.

Page content comes from the solution documents (overview deck, executive summary, solution brief, case
study, functional specification, UI/UX specification), not from new wording.

Everything here is public and all data in the mockups is fictional.

## Viewing

Locally: open `docs/index.html` in a browser, or serve the folder:

```bash
python3 -m http.server -d docs 8000
```

**Live site (no login): https://kt2i-dev.github.io/VelocitySuite/** — GitHub Pages serves the `docs/` folder of `main` (repo **Settings → Pages → Deploy from a
branch → main / docs**). No build step and no workflow.

## Layout

| Path | What it is |
|---|---|
| `docs/index.html` | Start page: the standards (About, Button standard, Details/Edit Screen Template, Custom widgets), a tile per sector, then the review checklist and recent updates |
| `docs/updates.html` | **Recent updates**, newest first. Add a dated entry with each change and update the "last updated" date on the start page's tile |
| `docs/about.html` | About Velocity Suite |
| `docs/<sector>/index.html` | A sector's page: its About tile, then a tile per solution. Sectors: `quality-engineering`, `supply-chain-logistics`, `production-maintenance`, `safety-environment`, `workforce-training` |
| `docs/<sector>/about.html` | About the sector (Quality / Engineering and Supply Chain / Logistics so far) |
| `docs/<sector>/<solution>/index.html` | A solution's page: its About tile, then its screens |
| `docs/quality-engineering/quality-event-capa/` | Quality Event & Corrective Action Management: its page, About, and data model |
| `docs/manufacturing/` | Redirects only: the site's first links, before the sectors were set up |
| `docs/assets/site.css` | Shared styles for every page |
| `tools/build_data_model.py` | Builds the Quality Event & CAPA data model page. Edit the entity list there and rerun it, rather than editing `data-model.html` |

## Coming soon

A page without enough detail yet is a disabled tile (`<div class="tile disabled" aria-disabled="true">`
with a `<span class="soon">Coming soon</span>` badge) rather than a link. When its page is built, turn
the `div` back into an `<a class="tile" href="…">` and drop the badge.
