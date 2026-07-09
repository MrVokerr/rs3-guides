# Spec: RS3 Guides (project operating spec)

> Status: **Approved decisions recorded 2026-07-09**  
> Related: `AGENTS.md` (agent context), `README.md` (human ops), `docs/specs/` (feature specs)

## Objective

Maintain a **mobile-ready VitePress site** of RS3 guides for fresh and returning players, kept current with **2026+ game changes** (Combat Modernisation, economy, DailyScape overhaul, Havenhythe, GE modernisation, mid-game rebalance, and patches through end of 2026).

**Users:** New/returning RS3 accounts who want a single clear path (combat style, sustain, or GP) without wiki archaeology.

**Success looks like:**
- Guides are phased, actionable, and internally consistent with nav/sidebar/home
- Mechanical claims match current game behavior (or are clearly dated)
- Site builds cleanly and deploys to https://rs3-guides.pages.dev
- Agents edit a single canonical repo without dual-path confusion

## Decisions (resolved)

| Question | Decision |
|----------|----------|
| Repo layout | VitePress source lives in `F:\Projects\RS3 guides`; Cursor root points here |
| Next deliverable | **Melee 1–120** combat style guide (approved; implementing) |
| Tone | **Cleaner docs look** — minimize emoji; clear headings/tables |
| Sources | Wiki + official patch notes primary; PVME / Reddit / creators allowed **with attribution** if they align with 2026 changes |
| Git | **This workspace is the canonical repo** |

## Tech stack

| Piece | Choice |
|-------|--------|
| SSG | VitePress (`vitepress` ^1.0.0 in package.json) |
| Hosting | Cloudflare Pages project `rs3-guides` |
| Deploy | Wrangler `pages deploy` of `.vitepress/dist` |
| Content | Markdown + VitePress theme config in JS |

## Commands

```powershell
cd "F:\Projects\RS3 guides"
npm run docs:dev
npm run docs:build
npm run docs:preview
npx wrangler pages deploy .vitepress/dist --project-name=rs3-guides --branch=main
```

## Project structure

```
F:\Projects\RS3 guides\
  *.md                     → Published guides + home
  .vitepress/config.js     → Nav + sidebars
  docs/SPEC.md             → This file
  docs/specs/              → Feature specs
  AGENTS.md                → Agent rules
  README.md                → Ops / deploy
  package.json             → npm scripts
```

## Code / content style

- Home uses `layout: home` with hero + feature cards
- New/rewritten guides: phased sections, tables, VitePress callouts; **minimal emoji**
- Prefer concrete names (NPCs, items, locations) over vague advice
- See `AGENTS.md` for the canonical snippet and new-page checklist

## Testing strategy

| Level | When | How |
|-------|------|-----|
| Build | Every content/config change | `npm run docs:build` must succeed |
| Local preview | Nav/layout/home changes | `npm run docs:dev` or `docs:preview` |
| Content accuracy | Meta-sensitive claims | Wiki / patch notes; attribute community sources; reject pre-2026 outdated meta |
| Deploy smoke | After deploy | Open live URL; spot-check new/changed page + nav |

## Boundaries

- **Always:** Build before deploy; update config + home when adding pages; source-check game facts against 2026+ reality
- **Ask first:** New top-level guides beyond approved Melee work, theme/custom components, CI, domain changes
- **Never:** Secrets in git; fabricated rates/meta; deploy broken builds; present obsolete combat/economy advice as current

## Success criteria (project baseline)

- [x] Dual-path resolved — source consolidated into this workspace
- [x] Decisions recorded (Melee next, cleaner tone, source policy, canonical git)
- [ ] `AGENTS.md` / this spec acknowledged by human as living baseline
- [ ] `npm run docs:build` passes on canonical source
- [ ] Melee feature spec approved → plan/tasks → implement
- [ ] Live site eventually includes Melee alongside existing guides

## Open questions

_None blocking. Optional later: Magic guide, CI, emoji cleanup pass on legacy pages._

---

## Feature specs

See `docs/specs/melee-1-120.md` for the next deliverable. Do not implement until that feature spec is approved.
