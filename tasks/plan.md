# Plan: Melee 1–120 Guide

> Depends on approval of `docs/specs/melee-1-120.md`  
> Created: 2026-07-09

## Approach

1. Research current Melee meta against RS Wiki + 2026 patch notes (Combat Modernisation, mid-game rebalance, Havenhythe-related Melee gear if any). Optionally cross-check PVME with attribution.
2. Draft `melee.md` using cleaner docs tone (minimal emoji), structured like `ranged.md`: overview → 1–120 route → gear → abilities → perks → supporting skills → short endgame pointer.
3. Wire nav, sidebar, and home feature card.
4. Update `README.md` structure table.
5. Verify with `npm run docs:build` + local preview; deploy only if requested.

## Order (sequential)

1. Research notes (sources list) → content outline freeze
2. Write `melee.md`
3. Config + home + README wiring
4. Build / preview verification
5. Optional deploy

## Risks

| Risk | Mitigation |
|------|------------|
| Outdated community guides | Wiki/patch notes win; date-stamp; attribute community only when aligned |
| DW vs 2H ambiguity | Cover both; call out bracket winners |
| Scope creep into full PvM | Stick to short endgame pointer per feature spec |
| Legacy emoji style bleed | Follow AGENTS cleaner pattern for this page only |

## Verification checkpoints

- After research: source list reviewed (human can skim)
- After draft: human content review before deploy
- After wiring: `npm run docs:build` green; Melee in nav
