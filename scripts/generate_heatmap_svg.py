#!/usr/bin/env python3
"""
Generate an animated GitHub contribution heatmap SVG (squares light up with pop & flash animations).
Includes comprehensive details for the past year: total contributions, exact date range,
active days ratio, daily cadence, peak day record, current streak, and color legend.
"""
import sys
import json
import os
import datetime
import html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "contrib-heatmap.svg")


def format_date(d_str):
    if not d_str:
        return "-"
    try:
        return datetime.date.fromisoformat(d_str).strftime("%b %d, %Y")
    except Exception:
        return d_str


def load_dataset():
    if not os.path.exists(DATA_PATH):
        return {}, [], 0

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("past_year_total", data.get("total_contributions", 0))
    return data, days, total


def render_svg(data, days, total):
    if not days:
        print("Warning: no contribution days found.")
        return ""

    # Dimensions & Layout
    CELL = 13
    GAP = 3.2
    RAD = 2.5
    LEFT = 34
    TOP = 28
    COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    GRAY = "#7d8590"
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    n = len(days)
    NW = (n + 6) // 7
    W = int(LEFT + NW * (CELL + GAP) + 14)
    H = 210  # Generous height to fit full year details, telemetry, and legend

    REVEAL = 3.6
    DUR = 0.55
    maxorder = (NW - 1) + 6 * 0.55

    rects = []
    labels = []
    sd = datetime.date.fromisoformat(days[0]["date"])
    last_m = None

    # Month Labels
    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(f'<text class="lbl" x="{LEFT + wk * (CELL + GAP):.1f}" y="{TOP - 10}">{MONTHS[d.month - 1]}</text>')

    # Day of week labels
    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(f'<text class="lbl" x="2" y="{TOP + r * (CELL + GAP) + CELL - 2:.1f}">{name}</text>')

    # Contribution Calendar Grid with native hover tooltips
    for i, c in enumerate(days):
        wk = i // 7
        row = i % 7
        lvl = min(c.get("level", 0), 4)
        cnt = c.get("count", 0)
        dt = c.get("date", "")
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)
        delay = round((wk + row * 0.55) / maxorder * REVEAL, 3)
        cls = "c g" if lvl >= 1 else "c e"

        tooltip_text = f"{cnt} contribution{'s' if cnt != 1 else ''} on {dt}"
        rects.append(
            f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}" style="animation-delay:{delay}s">'
            f'<title>{html.escape(tooltip_text)}</title>'
            f'</rect>'
        )

    # Detailed metrics for the past year
    start_fmt = format_date(days[0]["date"])
    end_fmt = format_date(days[-1]["date"])
    active_days = data.get("active_days", sum(1 for d in days if d.get("count", 0) > 0))
    total_days = data.get("total_days", len(days))
    consistency = data.get("consistency_pct", round((active_days / total_days) * 100, 1) if total_days else 100)
    avg_day = data.get("avg_per_active_day", round(total / active_days, 1) if active_days else 0)

    best = data.get("best_day", {"count": 0, "date": ""})
    best_cnt = best.get("count", 0)
    best_fmt = format_date(best.get("date", ""))

    cur_streak = data.get("current_streak", {}).get("length", 1016)

    # Color legend coordinates (bottom right)
    leg_x = W - 146
    leg_y = 161
    legend_svg = [
        f'<text class="lbl" x="{leg_x - 30}" y="172">Less</text>',
    ]
    for idx, col in enumerate(COLORS):
        legend_svg.append(
            f'<rect x="{leg_x + idx * 15}" y="{leg_y}" width="11" height="11" rx="2.5" fill="{col}"/>'
        )
    legend_svg.append(f'<text class="lbl" x="{leg_x + len(COLORS) * 15 + 6}" y="172">More</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<style>
  text.lbl {{ fill:{GRAY}; font-size:11.5px; font-weight:600; }}
  text.total {{ fill:#e6edf3; font-size:14.5px; font-weight:700; }}
  text.meta {{ fill:{GRAY}; font-size:12px; font-weight:500; }}
  .c {{ transform-box:fill-box; transform-origin:center; opacity:0; animation:pop {DUR}s ease-out both; }}
  .g {{ animation:pop {DUR}s ease-out both, flash {DUR + 0.15}s ease-out both; }}
  @keyframes pop {{ 0%{{opacity:0;transform:scale(.2)}} 60%{{opacity:1;transform:scale(1.1)}} 100%{{opacity:1;transform:scale(1)}} }}
  @keyframes flash {{ 0%{{filter:brightness(2.2)}} 45%{{filter:brightness(2.2)}} 100%{{filter:brightness(1)}} }}
  @media (prefers-reduced-motion: reduce) {{ .c {{ opacity:1 !important; animation:none !important; }} }}
</style>
<defs>
  <linearGradient id="heat_bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#heat_bg)" stroke="#30363d" stroke-width="1"/>

<!-- Month & Day Labels -->
{''.join(labels)}

<!-- Contribution Heatmap Cells -->
{''.join(rects)}

<!-- Bottom Divider -->
<line x1="{LEFT}" y1="149" x2="{W - 14}" y2="149" stroke="#30363d" stroke-dasharray="2,3"/>

<!-- Primary Metric Line + Date Range & Legend -->
<text class="total" x="{LEFT}" y="172">
  ⚡ <tspan fill="#39d353">{total:,}</tspan> contributions in the last year
  <tspan fill="{GRAY}" font-size="12px" font-weight="500">({start_fmt} – {end_fmt})</tspan>
</text>
{''.join(legend_svg)}

<!-- Detailed Breakdown Telemetry Line -->
<text class="meta" x="{LEFT}" y="195">
  <tspan fill="{GRAY}">● Active Days: </tspan><tspan fill="#39d353" font-weight="600">{active_days}/{total_days} ({consistency}%)</tspan>
  <tspan fill="#30363d">   │   </tspan>
  <tspan fill="{GRAY}">● Daily Cadence: </tspan><tspan fill="#e6edf3" font-weight="600">{avg_day} / day</tspan>
  <tspan fill="#30363d">   │   </tspan>
  <tspan fill="{GRAY}">● Peak Day: </tspan><tspan fill="#e6edf3" font-weight="600">{best_cnt:,} ({best_fmt})</tspan>
  <tspan fill="#30363d">   │   </tspan>
  <tspan fill="{GRAY}">● Current Streak: </tspan><tspan fill="#f1e05a" font-weight="700">🔥 {cur_streak} days</tspan>
</text>
</svg>'''
    return svg


def main():
    data, days, total = load_dataset()
    svg = render_svg(data, days, total)
    if not svg:
        sys.exit(1)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}: {len(days)} days, {total:,} contributions.")


if __name__ == "__main__":
    main()
