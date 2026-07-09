#!/usr/bin/env python3
"""
Refresh money-making.md GE prices and GP/hr figures from the RS Wiki.

Sources:
  - Module:GEPrices/data.json (item prices)
  - Money making guide method pages (hourly profit where listed)

Run from repo root:
  python scripts/update-money-making-prices.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "money-making.md"
GE_URL = "https://runescape.wiki/w/Module:GEPrices/data.json?action=raw"
WIKI_API = "https://runescape.wiki/api.php"
USER_AGENT = "RS3-Guides-PriceBot/1.0 (github.com/rs3-guides; wiki GE sync)"
TAX = 0.02
TAN_FEE = 20
ONYX_ALCH = 8179

# Wiki MMG hourly profits (fallback when HTML parse is ambiguous).
MMG_FALLBACKS: dict[str, int] = {
    "cows": 957_000,
    "cabbages": 1_528_000,
    "clay": 934_000,
    "bomb_vials": 2_524_000,
    "onyx_ge": 9_642_000,
    "starbloom": 8_590_000,
    "refined_magic": 4_649_000,
    "refined_elder": 5_275_000,
    "necrotic_spirit": 51_812_000,
    "necrotic_bone": 40_610_000,
    "necrotic_flesh": 39_065_000,
    "necrotic_miasma": 36_359_000,
    "incense_spirit": 12_230_000,
    "incense_kwuarm": 5_826_000,
    "incense_lantadyme": 8_024_000,
    "incense_torstol": 9_314_000,
}


def safe_profit(parsed: int | None, key: str) -> int:
    fallback = MMG_FALLBACKS[key]
    if parsed is None:
        return fallback
    if fallback and abs(parsed - fallback) / fallback > 0.35:
        return fallback
    return parsed


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode())


def parse_large_profits(
    html: str,
    *,
    min_val: int = 1_000_000,
    max_val: int = 200_000_000,
) -> list[int]:
    seen: set[int] = set()
    profits: list[int] = []
    for match in re.finditer(r"\b([\d,]{6,})\b", html):
        value = int(match.group(1).replace(",", ""))
        if min_val <= value <= max_val and value not in seen:
            seen.add(value)
            profits.append(value)
    return profits


def fetch_wiki_page_html(title: str) -> str:
    params = (
        f"?action=parse&page={urllib.parse.quote(title.replace(' ', '_'))}"
        "&prop=text&formatversion=2&format=json"
    )
    req = urllib.request.Request(WIKI_API + params, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode())
    return data["parse"]["text"]


def fmt_money_gp(n: float) -> str:
    """Format coin amounts: 957k, 1.5M, 51.8M."""
    if n >= 1_000_000:
        m = n / 1_000_000
        if m >= 10:
            return f"{m:.0f}M"
        s = f"{m:.1f}".rstrip("0").rstrip(".")
        return f"{s}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}k"
    return str(int(n))


def profit_display(value: float | None, fallback: float | None = None) -> str:
    amount = value if value is not None else fallback
    if amount is None:
        return "~?"
    return f"~{fmt_money_gp(amount)}"


def parse_profit_after_tax(html: str) -> int | None:
    """Extract main hourly profit from a wiki MMG page."""
    idx = html.lower().find("profit")
    if idx == -1:
        return None
    chunk = html[idx : idx + 8000]
    for match in re.finditer(r"([\d,]+)\s*after\s*tax", chunk, re.I):
        value = int(match.group(1).replace(",", ""))
        if value >= 10_000:
            return value
    return None


def parse_all_profits_after_tax(html: str) -> list[int]:
    idx = html.lower().find("profit")
    if idx == -1:
        return []
    chunk = html[idx : idx + 20000]
    values = []
    for match in re.finditer(r"([\d,]+)\s*after\s*tax", chunk, re.I):
        value = int(match.group(1).replace(",", ""))
        if value >= 10_000:
            values.append(value)
    return values


def load_ge_prices() -> dict[str, int]:
    return fetch_json(GE_URL)


def fetch_mmg_profit(
    page: str,
    index: int = 0,
    *,
    min_val: int = 1_000_000,
) -> int | None:
    try:
        html = fetch_wiki_page_html(f"Money making guide/{page}")
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        print(f"warn: could not fetch MMG/{page}: {exc}", file=sys.stderr)
        return None

    # Prefer large unique totals on multi-method template pages.
    profits = parse_large_profits(html, min_val=min_val)
    if profits and index < len(profits):
        return profits[index]

    # Fallback for simple pages with a single Results profit row.
    single = parse_profit_after_tax(html)
    if single is not None and index == 0:
        return single
    return None


def tanning_row(color: str, prices: dict[str, int]) -> str:
    hide = prices[f"{color} dragonhide"]
    leather = prices[f"{color} dragon leather"]
    profit_ea = leather * (1 - TAX) - hide - TAN_FEE
    return (
        f"| {color} | {hide:,} | {leather:,} | ~{profit_ea:.0f} "
        f"| ~{fmt_money_gp(profit_ea * 40_000)} | ~{fmt_money_gp(profit_ea * 60_000)} |"
    )


def build_snapshot_table(prices: dict[str, int]) -> str:
    rows = [
        ("Cowhide", prices["Cowhide"]),
        ("Raw beef", prices["Raw beef"]),
        ("Sinew", prices["Sinew"]),
        ("Cabbage", prices["Cabbage"]),
        ("Impious ashes", prices["Impious ashes"]),
        ("Third Age iron", prices["Third Age iron"]),
        ("Zarosian insignia", prices["Zarosian insignia"]),
        ("Clay / Soft clay", f"{prices['Clay']:,} / {prices['Soft clay']:,}"),
        (
            "Green / Blue / Black dragonhide",
            f"{prices['Green dragonhide']:,} / {prices['Blue dragonhide']:,} / {prices['Black dragonhide']:,}",
        ),
        (
            "Green / Blue / Black dragon leather",
            f"{prices['Green dragon leather']:,} / {prices['Blue dragon leather']:,} / {prices['Black dragon leather']:,}",
        ),
        (
            "Molten glass / Bomb vial",
            f"{prices['Molten glass']:,} / {prices['Bomb vial']:,}",
        ),
        ("Impure essence", prices["Impure essence"]),
        (
            "Spirit / Bone / Flesh / Miasma rune",
            f"{prices['Spirit rune']:,} / {prices['Bone rune']:,} / {prices['Flesh rune']:,} / {prices['Miasma rune']:,}",
        ),
        (
            "Onyx bolt tips / Onyx bolts",
            f"{prices['Onyx bolt tips']:,} / {prices['Onyx bolts']:,}",
        ),
        (
            "Starbloom flower / thread / cloth",
            f"{prices['Starbloom flower']:,} / {prices['Starbloom thread']:,} / {prices['Starbloom cloth']:,}",
        ),
        (
            "Apex sinew / Apex leather",
            f"{prices['Apex sinew']:,} / {prices['Apex leather']:,}",
        ),
    ]
    lines = ["| Item | GE Price |", "|---|---|"]
    for name, val in rows:
        lines.append(f"| {name} | {val} |")
    return "\n".join(lines)


def update_guide(prices: dict[str, int], mmg: dict[str, int | None]) -> str:
    today = date.today()
    today_long = today.strftime("%B %-d, %Y") if sys.platform != "win32" else today.strftime("%B %d, %Y").replace(" 0", " ")
    # Windows-friendly date without leading zero on day
    today_long = today.strftime("%B ") + str(today.day) + today.strftime(", %Y")

    text = GUIDE.read_text(encoding="utf-8")

    # Header date
    text = re.sub(
        r"> Last updated: \*\*[^*]+\*\*",
        f"> Last updated: **{today_long}**",
        text,
        count=1,
    )

    # Phase 1 inline prices
    text = re.sub(r"Cowhides \(~[\d,]+ GP\)", f"Cowhides (~{prices['Cowhide']:,} GP)", text)
    text = re.sub(r"Raw Beef \(~[\d,]+ GP\)", f"Raw Beef (~{prices['Raw beef']:,} GP)", text)
    text = re.sub(r"Bones \(~[\d,]+ GP\)", f"Bones (~{prices['Bones']:,} GP)", text)
    text = re.sub(
        r"### 1\. Slaying Cows in Burthorpe \(~[^)]+\)",
        f"### 1. Slaying Cows in Burthorpe ({profit_display(mmg.get('cows'), 957_000)} GP/hour)",
        text,
    )
    if mmg.get("cows"):
        text = re.sub(
            r"\* \*\*Wiki rate:\*\* ~540 kills/hr ≈ \*\*~[\d.]+[Mk]+ GP/hr\*\*",
            f"* **Wiki rate:** ~540 kills/hr ≈ **{profit_display(mmg['cows'])} GP/hr** after tax.",
            text,
        )

    text = re.sub(
        r"Harvest cabbages \(~[\d,]+ GP each\)",
        f"Harvest cabbages (~{prices['Cabbage']:,} GP each)",
        text,
    )
    if mmg.get("cabbages"):
        text = re.sub(
            r"\* \*\*Wiki rate:\*\* ~1,100 cabbages/hr ≈ \*\*~[\d.]+M GP/hr\*\*",
            f"* **Wiki rate:** ~1,100 cabbages/hr ≈ **{profit_display(mmg['cabbages'])} GP/hr** after tax.",
            text,
        )

    text = re.sub(
        r"\*\*Impious Ashes\*\* \(~[\d,]+ GP each\)",
        f"**Impious Ashes** (~{prices['Impious ashes']:,} GP each)",
        text,
    )

    text = re.sub(
        r"\*\*Third Age Iron\*\* \(~[\d,]+ GP\), \*\*Goldrune\*\* \(~[\d,]+ GP\), \*\*Samite Silk\*\* \(~[\d,]+ GP\), and \*\*Zarosian Insignia\*\* \(~[\d,]+ GP\)",
        (
            f"**Third Age Iron** (~{prices['Third Age iron']:,} GP), "
            f"**Goldrune** (~{prices['Goldrune']:,} GP), "
            f"**Samite Silk** (~{prices['Samite silk']:,} GP), and "
            f"**Zarosian Insignia** (~{prices['Zarosian insignia']:,} GP)"
        ),
        text,
    )

    text = re.sub(
        r"Mine clay \(~[\d,]+ GP\).*?soft clay \(~[\d,]+ GP\)",
        f"Mine clay (~{prices['Clay']:,} GP) and sell on the GE. Equip a **Bracelet of Clay** to automatically soften it into soft clay (~{prices['Soft clay']:,} GP)",
        text,
        flags=re.S,
    )
    if mmg.get("clay"):
        text = re.sub(
            r"\* \*\*Wiki rate:\*\* ~940 clay/hr ≈ \*\*~[\d.]+[Mk]+ GP/hr\*\*",
            f"* **Wiki rate:** ~940 clay/hr ≈ **{profit_display(mmg['clay'])} GP/hr**",
            text,
        )

    # Tanning section
    green_p = prices["Green dragon leather"] * (1 - TAX) - prices["Green dragonhide"] - TAN_FEE
    black_p = prices["Black dragon leather"] * (1 - TAX) - prices["Black dragonhide"] - TAN_FEE
    text = re.sub(
        r"### 1\. Tanning Dragonhides \(~[^)]+\)",
        f"### 1. Tanning Dragonhides ({profit_display(green_p * 40_000)} – {profit_display(black_p * 60_000)} GP/hour)",
        text,
    )
    text = re.sub(
        r"\* \*\*Current margins \(July [^)]+\):\*\*",
        f"* **Current margins ({today_long}):**",
        text,
    )

    tanning_table = "\n".join(
        [
            "| Hide | Hide Price | Leather Price | Profit/ea (after tax + tan fee) | ~40k/hr | ~60k/hr |",
            "|---|---|---|---|---|---|",
            tanning_row("Green", prices),
            tanning_row("Blue", prices),
            tanning_row("Black", prices),
        ]
    )
    text = re.sub(
        r"\| Hide \| Hide Price \| Leather Price \| Profit/ea \(after tax \+ tan fee\) \| ~40k/hr \| ~60k/hr \|\n\|---\|---\|---\|---\|---\|---\|\n(?:\| [^\n]+\n){3}",
        tanning_table + "\n",
        text,
    )

    # Sinew
    sinew_profit = prices["Sinew"] * (1 - TAX) - prices["Raw beef"]
    sinew_lo = sinew_profit * 1500
    sinew_hi = sinew_profit * 1800
    text = re.sub(
        r"\*\*Current prices:\*\* Raw Beef ~[\d,]+ GP → Sinew ~\*\*[\d,]+ GP\*\* \(~[\d,]+ GP profit after tax\)\.",
        (
            f"**Current prices:** Raw Beef ~{prices['Raw beef']:,} GP → Sinew ~**{prices['Sinew']:,} GP** "
            f"(~{sinew_profit:,.0f} GP profit after tax)."
        ),
        text,
    )
    text = re.sub(
        r"\* \*\*Rate:\*\* ~1,500–1,800 sinews/hr ≈ \*\*~[\d.]+M – [\d.]+M GP/hr\*\*",
        f"* **Rate:** ~1,500–1,800 sinews/hr ≈ **~{fmt_money_gp(sinew_lo)} – {fmt_money_gp(sinew_hi)} GP/hr**",
        text,
    )

    # Bomb vials / beer glass
    bv_profit = prices["Bomb vial"] * (1 - TAX) - prices["Molten glass"]
    bg_profit = prices["Beer glass"] * (1 - TAX) - prices["Molten glass"]
    if mmg.get("bomb_vials"):
        text = re.sub(
            r"### 3\. Molten Glass → Bomb Vials \(~[^)]+\)",
            f"### 3. Molten Glass → Bomb Vials ({profit_display(mmg['bomb_vials'])} GP/hour + Crafting XP)",
            text,
        )
    text = re.sub(
        r"\*\*Current prices:\*\* Molten Glass ~[\d,]+ GP → Bomb Vial ~\*\*[\d,]+ GP\*\* \(~[\d,]+ GP profit after tax\)\.",
        (
            f"**Current prices:** Molten Glass ~{prices['Molten glass']:,} GP → Bomb Vial ~**{prices['Bomb vial']:,} GP** "
            f"(~{bv_profit:,.0f} GP profit after tax)."
        ),
        text,
    )
    if mmg.get("bomb_vials"):
        text = re.sub(
            r"\* \*\*Wiki rate:\*\* ~1,830 vials/hr ≈ \*\*[^*]+\*\*\.+",
            f"* **Wiki rate:** ~1,830 vials/hr ≈ **{profit_display(mmg['bomb_vials'])} GP/hr**.",
            text,
        )
    text = re.sub(
        r"Beer Glasses \(~[\d,]+ GP\) only clear ~[\d,]+ GP each after tax",
        f"Beer Glasses (~{prices['Beer glass']:,} GP) only clear ~{bg_profit:.0f} GP each after tax",
        text,
    )

    # Incense table
    incense_rows = [
        ("Spirit weed", 35, mmg.get("incense_spirit")),
        ("Kwuarm", 54, mmg.get("incense_kwuarm")),
        ("Lantadyme", 67, mmg.get("incense_lantadyme")),
        ("Torstol", 75, mmg.get("incense_torstol")),
    ]
    incense_vals = [p for _, _, p in incense_rows if p]
    if incense_vals:
        text = re.sub(
            r"### 4\. Incense Sticks \(~[^)]+\)",
            f"### 4. Incense Sticks ({profit_display(min(incense_vals))} – {profit_display(max(incense_vals))} GP/hour)",
            text,
        )
    incense_table = "\n".join(
        [
            "| Stick | Level | Approx. GP/hr |",
            "|---|---|---|",
            *[
                f"| {name} | {lvl} | {profit_display(p) if p else '~?'} |"
                for name, lvl, p in incense_rows
            ],
        ]
    )
    text = re.sub(
        r"\| Stick \| Level \| Approx\. GP/hr \|\n\|---\|---\|---\|\n(?:\| [^\n]+\n){4}",
        incense_table + "\n",
        text,
    )

    # Refined planks
    if mmg.get("refined_magic") and mmg.get("refined_elder"):
        text = re.sub(
            r"Refined Magic planks ~\*\*[\d.]+M/hr\*\* \| Refined Elder planks ~\*\*[\d.]+M/hr\*\*",
            (
                f"Refined Magic planks ~**{fmt_money_gp(mmg['refined_magic'])}** "
                f"| Refined Elder planks ~**{fmt_money_gp(mmg['refined_elder'])}**"
            ),
            text,
        )

    # Necrotic runes
    necrotic = [
        ("Spirit", mmg.get("necrotic_spirit")),
        ("Bone", mmg.get("necrotic_bone")),
        ("Flesh", mmg.get("necrotic_flesh")),
        ("Miasma", mmg.get("necrotic_miasma")),
    ]
    nec_vals = [p for _, p in necrotic if p]
    if nec_vals:
        text = re.sub(
            r"### 1\. Necrotic Rune Crafting \(~[^)]+\)",
            f"### 1. Necrotic Rune Crafting ({profit_display(min(nec_vals))} – {profit_display(max(nec_vals))} GP/hour optimised)",
            text,
        )
    nec_table = "\n".join(
        [
            "| Rune | Approx. GP/hr after tax |",
            "|---|---|",
            *[f"| {name} | ~**{fmt_money_gp(p)}** |" if p else f"| {name} | ~**?** |" for name, p in necrotic],
        ]
    )
    text = re.sub(
        r"\| Rune \| Approx\. GP/hr after tax \|\n\|---\|---\|\n(?:\| [^\n]+\n){4}",
        nec_table + "\n",
        text,
    )
    text = re.sub(
        r"Impure Essence \(~[\d,]+ GP\)",
        f"Impure Essence (~{prices['Impure essence']:,} GP)",
        text,
    )

    # Onyx bolts
    text = re.sub(
        r"Onyx Bolt Tips ~\*\*[\d,]+\*\* \+ Rune Bolts ~\*\*[\d,]+\*\* → Onyx Bolts ~\*\*[\d,]+\*\* GE",
        (
            f"Onyx Bolt Tips ~**{prices['Onyx bolt tips']:,}** + Rune Bolts ~**{prices['Rune bolts']:,}** "
            f"→ Onyx Bolts ~**{prices['Onyx bolts']:,}** GE"
        ),
        text,
    )
    if mmg.get("onyx_ge"):
        text = re.sub(
            r"\* \*\*Wiki GE rate:\*\* ~\*\*[\d.]+M GP/hr\*\*",
            f"* **Wiki GE rate:** ~**{fmt_money_gp(mmg['onyx_ge'])} GP/hr**",
            text,
        )
    prefer_alch = ONYX_ALCH > prices["Onyx bolts"] * (1 - TAX)
    text = re.sub(
        r"4\. \*\*Prefer High Alch\*\* right now — GE guide price sits below alch value\.",
        (
            "4. **Prefer High Alch** right now — GE guide price sits below alch value."
            if prefer_alch
            else "4. **Prefer GE sell** right now — GE after-tax beats alch value."
        ),
        text,
    )

    # Starbloom
    cloth_hr = 605 * prices["Starbloom cloth"] * (1 - TAX) - 1210 * prices["Starbloom flower"]
    thread_loss = prices["Starbloom thread"] * (1 - TAX) - prices["Starbloom flower"]
    text = re.sub(
        r"### 3\. Spinning Starbloom Flowers into Cloth \(~[^)]+\)",
        f"### 3. Spinning Starbloom Flowers into Cloth ({profit_display(cloth_hr)} GP/hour, Fully AFK)",
        text,
    )
    text = re.sub(
        r"Starbloom Flower ~\*\*[\d,]+\*\* \| Starbloom Thread ~\*\*[\d,]+\*\* \| Starbloom Cloth ~\*\*[\d,]+\*\*",
        (
            f"Starbloom Flower ~**{prices['Starbloom flower']:,}** | "
            f"Starbloom Thread ~**{prices['Starbloom thread']:,}** | "
            f"Starbloom Cloth ~**{prices['Starbloom cloth']:,}**"
        ),
        text,
    )
    text = re.sub(
        r"3\. Sell cloth\. Wiki rate: 1,210 flowers → 605 cloth/hr ≈ \*\*[^*]+\*\*(?: after tax\.)*",
        f"3. Sell cloth. Wiki rate: 1,210 flowers → 605 cloth/hr ≈ **{profit_display(cloth_hr)} GP/hr** after tax.",
        text,
    )
    loss_note = (
        "**loses money** (thread GE price is below flower price)"
        if thread_loss < 0
        else "**may profit** if thread GE price stays above flower price"
    )
    text = re.sub(
        r"selling the \*\*thread\*\* currently \*\*loses money\*\* \(thread GE price is below flower price\)",
        f"selling the **thread** currently {loss_note}",
        text,
    )

    # Bob shirts
    text = re.sub(
        r"Bob shirts ~\*\*[^*]+\*\* each",
        f"Bob shirts ~**{prices['Bob shirt (black)'] / 1000:.0f}k** each",
        text,
    )

    text = re.sub(
        r"Wooden Frames \(~[\d.]+k each\)",
        f"Wooden Frames (~{prices['Wooden frame'] / 1000:.1f}k each)",
        text,
    )

    # Price snapshot block
    snapshot = build_snapshot_table(prices)
    text = re.sub(
        r"## 📊 Price Snapshot — [^\n]+\n\nQuick reference for items cited in this guide \(wiki GE guide prices\):\n\n\| Item \| GE Price \|\n\|---\|---\|\n(?:\| [^\n]+\n)+",
        f"## 📊 Price Snapshot — {today_long}\n\nQuick reference for items cited in this guide (wiki GE guide prices):\n\n{snapshot}\n",
        text,
    )

    return text


def main() -> int:
    if not GUIDE.exists():
        print(f"error: guide not found at {GUIDE}", file=sys.stderr)
        return 1

    print("Fetching GE prices...")
    prices = load_ge_prices()

    required = [
        "Cowhide", "Raw beef", "Sinew", "Cabbage", "Impious ashes", "Bones",
        "Third Age iron", "Goldrune", "Samite silk", "Zarosian insignia",
        "Clay", "Soft clay", "Green dragonhide", "Blue dragonhide", "Black dragonhide",
        "Green dragon leather", "Blue dragon leather", "Black dragon leather",
        "Molten glass", "Beer glass", "Bomb vial",
        "Impure essence", "Spirit rune", "Bone rune", "Flesh rune", "Miasma rune",
        "Onyx bolt tips", "Rune bolts", "Onyx bolts",
        "Starbloom flower", "Starbloom thread", "Starbloom cloth",
        "Apex sinew", "Apex leather", "Wooden frame", "Bob shirt (black)",
        "Magic plank", "Refined Magic planks", "Elder plank", "Refined Elder planks",
    ]
    missing = [k for k in required if k not in prices]
    if missing:
        print(f"error: missing GE prices: {', '.join(missing)}", file=sys.stderr)
        return 1

    print("Fetching wiki money-making rates...")
    mmg: dict[str, int | None] = {
        "cows": safe_profit(fetch_mmg_profit("Killing_cows", min_val=100_000), "cows"),
        "cabbages": safe_profit(fetch_mmg_profit("Picking_cabbages", min_val=100_000), "cabbages"),
        "clay": safe_profit(fetch_mmg_profit("Mining_clay", min_val=100_000), "clay"),
        "bomb_vials": safe_profit(fetch_mmg_profit("Making_bomb_vials", min_val=100_000), "bomb_vials"),
        "onyx_ge": safe_profit(fetch_mmg_profit("Fletching_onyx_bolts", min_val=1_000_000), "onyx_ge"),
        "starbloom": safe_profit(fetch_mmg_profit("Spinning_starbloom_flowers_into_cloth", min_val=1_000_000), "starbloom"),
        "refined_magic": safe_profit(
            fetch_mmg_profit("Making_refined_planks_at_Fort_Forinthry", 0, min_val=4_000_000),
            "refined_magic",
        ),
        "refined_elder": safe_profit(
            fetch_mmg_profit("Making_refined_planks_at_Fort_Forinthry", 1, min_val=4_000_000),
            "refined_elder",
        ),
        "necrotic_spirit": MMG_FALLBACKS["necrotic_spirit"],
        "necrotic_bone": MMG_FALLBACKS["necrotic_bone"],
        "necrotic_flesh": MMG_FALLBACKS["necrotic_flesh"],
        "necrotic_miasma": MMG_FALLBACKS["necrotic_miasma"],
        "incense_spirit": safe_profit(
            fetch_mmg_profit("Adding_herbs_to_incense_sticks", 0, min_val=5_000_000),
            "incense_spirit",
        ),
        "incense_kwuarm": safe_profit(
            fetch_mmg_profit("Adding_herbs_to_incense_sticks", 1, min_val=5_000_000),
            "incense_kwuarm",
        ),
        "incense_lantadyme": safe_profit(
            fetch_mmg_profit("Adding_herbs_to_incense_sticks", 2, min_val=5_000_000),
            "incense_lantadyme",
        ),
        "incense_torstol": safe_profit(
            fetch_mmg_profit("Adding_herbs_to_incense_sticks", 3, min_val=5_000_000),
            "incense_torstol",
        ),
    }

    original = GUIDE.read_text(encoding="utf-8")
    updated = update_guide(prices, mmg)

    if updated == original:
        print("No changes — guide already up to date.")
        return 0

    GUIDE.write_text(updated, encoding="utf-8")
    print(f"Updated {GUIDE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
