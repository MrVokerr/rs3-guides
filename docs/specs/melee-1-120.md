# Spec: Melee 1–120 Guide

> Status: **Approved 2026-07-09** — implement  
> Parent: `docs/SPEC.md`

## Objective

Ship a **Melee 1–120 leveling guide** for fresh/returning RS3 players that is accurate for **post–Combat Modernisation (March 2026)** and later 2026 patches, matching the usefulness of the existing Ranged / Necromancy guides but with a **cleaner docs tone** (minimal emoji).

## Approved decisions

| Question | Decision |
|----------|----------|
| Audience | Fresh-account-first with optional upgrades |
| Style focus | Both dual-wield and 2H tracks called out |
| Endgame depth | 120 unlocks + gear table **and** short boss starter (GWD2 / Melee notes) |
| Deploy | Deploy to Cloudflare in the same session once build passes |

## In scope

- `melee.md`, nav/sidebar, home feature, README update
- Overview, 1–120 route, gear (DW + 2H), abilities/Bloodlust, perks, supporting skills, short boss starter
- Wiki + official patch notes primary; community sources only with attribution and 2026 alignment

## Success criteria

- [x] `melee.md` live with approved scope
- [x] Nav, sidebar, home link to Melee
- [x] No known pre–Combat Modernisation obsolete advice as current
- [x] `npm run docs:build` succeeds
- [x] Deployed to https://rs3-guides.pages.dev/melee
