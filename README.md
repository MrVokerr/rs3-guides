# RS3 Guides

> **Canonical repo:** [github.com/MrVokerr/rs3-guides](https://github.com/MrVokerr/rs3-guides) · `F:\Projects\RS3 guides`  
> **Live site:** [https://rs3-guides.pages.dev](https://rs3-guides.pages.dev)  
> **Stack:** VitePress → Cloudflare Pages (`rs3-guides`)

Mobile-ready RuneScape 3 leveling and money-making guides for fresh and returning players (2026 meta).

---

## Project structure

| File | Purpose | Live URL |
|------|---------|----------|
| `index.md` | Homepage (`layout: home`) | [/](https://rs3-guides.pages.dev/) |
| `necromancy.md` | Necromancy 1–120 | [/necromancy](https://rs3-guides.pages.dev/necromancy) |
| `ranged.md` | Ranged 1–120 | [/ranged](https://rs3-guides.pages.dev/ranged) |
| `sustain-and-tips.md` | Beginner survival & UI | [/sustain-and-tips](https://rs3-guides.pages.dev/sustain-and-tips) |
| `money-making.md` | Fresh-account gold making | [/money-making](https://rs3-guides.pages.dev/money-making) |
| `melee.md` | Melee 1–120 | [/melee](https://rs3-guides.pages.dev/melee) |
| `.vitepress/config.js` | Nav, sidebar, title | — |
| `docs/SPEC.md` | Project operating spec | — |
| `docs/specs/` | Feature specs | — |
| `AGENTS.md` | Agent / contributor rules | — |

---

## Commands

```powershell
cd "F:\Projects\RS3 guides"
npm install
npm run docs:dev
npm run docs:build
npm run docs:preview
```

### Deploy to Cloudflare Pages

Prerequisites: Node.js, Wrangler logged in (`npm install -g wrangler`).

```powershell
cd "F:\Projects\RS3 guides"
npm run docs:build
npx wrangler pages deploy .vitepress/dist --project-name=rs3-guides --branch=main
```

One-liner:

```powershell
cd "F:\Projects\RS3 guides"; npm run docs:build; npx wrangler pages deploy .vitepress/dist --project-name=rs3-guides --branch=main
```

### Daily GE price refresh (9:00 AM Pacific)

`money-making.md` can be refreshed automatically from [RS Wiki GE prices](https://runescape.wiki/w/Module:GEPrices/data.json) and wiki money-making method pages.

**Manual run:**

```powershell
cd "F:\Projects\RS3 guides"
npm run prices:update    # refresh money-making.md only
npm run prices:deploy    # refresh + build + deploy
```

**Option A — GitHub Actions (recommended for hands-off deploy)**

**One-time setup:**

1. Repo: [github.com/MrVokerr/rs3-guides](https://github.com/MrVokerr/rs3-guides) (already pushed).
2. GitHub secret `CLOUDFLARE_ACCOUNT_ID` — **already set** in repo secrets.
3. GitHub secret `CLOUDFLARE_API_TOKEN` — **add this once:**
   - Cloudflare Dashboard → **My Profile** → **API Tokens** → **Create Token**
   - Use template **Edit Cloudflare Workers** or custom token with **Account → Cloudflare Pages → Edit**
   - Then run:
   ```powershell
   cd "F:\Projects\RS3 guides"
   gh secret set CLOUDFLARE_API_TOKEN
   ```
   (paste token when prompted; input is hidden)
4. Test: GitHub **Actions** → **Daily GE price update** → **Run workflow**

Workflow `.github/workflows/daily-ge-price-update.yml` runs **every day at 9:00 AM America/Los_Angeles** (PST/PDT), commits price changes if any, builds, and deploys.

**Option B — Windows Task Scheduler (local machine)**

1. Open **Task Scheduler** → Create Basic Task → Daily → **9:00 AM**.
2. Action: Start a program → `powershell.exe`
3. Arguments: `-ExecutionPolicy Bypass -File "F:\Projects\RS3 guides\scripts\run-daily-price-update.ps1"`
4. Requires: Python 3, Node.js, and Wrangler logged in on that PC.

**Option C — Cursor Automation**

You can also schedule a Cursor Automation (cron trigger) to run the same audit prompt daily; it still needs Cloudflare credentials available in that environment to deploy.

---

## Content policy

- Prefer **RuneScape Wiki** and **official patch notes** for mechanics.
- PVME / Reddit / creators OK for practical tips **with attribution**, only when aligned with **2026+** changes (Combat Modernisation and later).
- Do not present pre–Combat Modernisation advice as current.
- New guides use a cleaner docs tone (minimal emoji). Legacy pages may still use the older style until refreshed.

---

## Key 2026 game changes (context)

| Update | Date | What changed |
|--------|------|----------------|
| Treasure Hunter removed | Jan 19, 2026 | Less P2W GP/XP injection; economy more organic |
| DailyScape overhaul | Mar 16, 2026 | Many dailies removed/changed; shop schedules shifted |
| Combat Modernisation | Mar 2026 | Combat skills to 120; abilities streamlined; thresholds removed; GCD changes |
| Havenhythe | Mar 2026 | Large expansion; new content and demand sinks |
| GE modernisation | Summer 2026 | Live prices, wider price shift cap, wiki integration |
| Mid-game rebalance | Jul 2026 | Fletching re-tier, ammo simplification, boss instance costs, GWD QoL |

Always re-check Wiki/patch notes before publishing — the year is still moving.

---

## Agent / contributor docs

- `AGENTS.md` — paths, commands, boundaries, style
- `docs/SPEC.md` — project operating spec
- `docs/specs/melee-1-120.md` — next feature (Melee guide)
- `tasks/plan.md` / `tasks/todo.md` — implementation plan after Melee spec approval
