#!/usr/bin/env python3
"""
Generate an animated GitHub contribution heatmap SVG (squares light up with pop & flash animations).
Works standalone or as part of automated GitHub Action pipeline.
"""
import sys
import json
import os
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "contrib-heatmap.svg")


def load_contributions():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("days", []), data.get("total_contributions", 0)
    return [], 0


def render_svg(days, total):
    if not days:
        print("Warning: no contribution days found.")
        return ""

    # Dimensions & Layout
    CELL = 13
    GAP = 3.2
    RAD = 2.5
    LEFT = 34
    TOP = 26
    COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    GRAY = "#7d8590"
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    n = len(days)
    NW = (n + 6) // 7
    W = int(LEFT + NW * (CELL + GAP) + 10)
    H = int(TOP + 7 * (CELL + GAP) + 26)

    REVEAL = 3.6
    DUR = 0.55
    maxorder = (NW - 1) + 6 * 0.55

    rects = []
    labels = []
    sd = datetime.date.fromisoformat(days[0]["date"])
    last_m = None

    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(f'<text class="lbl" x="{LEFT + wk * (CELL + GAP):.1f}" y="{TOP - 8}">{MONTHS[d.month - 1]}</text>')

    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(f'<text class="lbl" x="2" y="{TOP + r * (CELL + GAP) + CELL - 2:.1f}">{name}</text>')

    for i, c in enumerate(days):
        wk = i // 7
        row = i % 7
        lvl = min(c.get("level", 0), 4)
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"
        rects.append(
            f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}" style="animation-delay:{delay}s"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<style>
  text.lbl {{ fill:{GRAY}; font-size:12px; font-weight:600; }}
  text.total {{ fill:#e6edf3; font-size:14px; font-weight:700; }}
  text.total span {{ fill:#39d353; }}
  .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
  .g {{ animation:pop {DUR}s ease-out both, flash {DUR + 0.15}s ease-out both; }}
  @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.1)}} 100%{{opacity:1;transform:scale(1)}} }}
  @keyframes flash {{ 0%{{filter:brightness(2.2)}} 45%{{filter:brightness(2.2)}} 100%{{filter:brightness(1)}} }}
  @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
</style>
<rect width="{W}" height="{H}" fill="none"/>
{''.join(labels)}
{''.join(rects)}
<text class="total" x="{LEFT}" y="{H - 7}">⚡ <span>{total:,}</span> contributions in the last year</text>
</svg>'''
    return svg


def main():
    days, total = load_contributions()
    svg = render_svg(days, total)
    if not svg:
        sys.exit(1)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}: {len(days)} days, {total:,} contributions.")


if __name__ == "__main__":
    main()
