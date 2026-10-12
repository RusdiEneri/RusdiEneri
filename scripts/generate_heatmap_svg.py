#!/usr/bin/env python3
"""
Generate GitHub contribution heatmap SVG (contrib-heatmap.svg)
Styled in Rusdi's signature portfolio aesthetic (mangrusdi.my.id):
- Deep dark canvas (#0a0a0a) with crisp borders (#262626)
- Warm taupe & bronze contribution spectrum (#161616 -> #b38b6d)
- Comprehensive metrics: total contributions, consistency, streak
- Feather-light rendering (removed heavy GPU CSS brightness filters)
"""
import datetime
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "contrib-heatmap.svg")

# Design tokens matching mangrusdi.my.id
BG = "#0a0a0a"
SURFACE = "#141414"
BORDER = "#262626"
TEXT_PRIMARY = "#f5f5f5"
TEXT_MUTED = "#9e9e9e"
TEXT_SUBTLE = "#6e6e6e"
TAUPE = "#b38b6d"
TAUPE_LIGHT = "#d4a373"

# Taupe gradient scale from empty to peak
COLORS = [
    "#161616",  # Level 0 (Empty)
    "#3d2f23",  # Level 1 (Light)
    "#6e523c",  # Level 2 (Medium)
    "#9c7453",  # Level 3 (High)
    "#b38b6d",  # Level 4 (Peak)
]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


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
    CELL = 12.0
    GAP = 3.0
    RAD = 2.0
    LEFT = 36.0
    TOP = 46.0

    n = len(days)
    NW = (n + 6) // 7
    W = int(LEFT + NW * (CELL + GAP) + 16)
    H = 206

    rects = []
    labels = []
    sd = datetime.date.fromisoformat(days[0]["date"])
    last_m = None

    # Month Labels
    for wk in range(NW):
        d = sd + datetime.timedelta(days=wk * 7)
        if d.month != last_m:
            last_m = d.month
            labels.append(
                f'<text class="lbl" x="{LEFT + wk * (CELL + GAP):.1f}" y="{TOP - 10:.1f}">'
                f'{MONTHS[d.month - 1]}</text>'
            )

    # Day of week labels
    for name, r in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        labels.append(f'<text class="lbl" x="4" y="{TOP + r * (CELL + GAP) + CELL - 2:.1f}">{name}</text>')

    # Contribution Calendar Grid
    for i, c in enumerate(days):
        wk = i // 7
        row = i % 7
        lvl = min(c.get("level", 0), 4)
        cnt = c.get("count", 0)
        dt = c.get("date", "")
        x = LEFT + wk * (CELL + GAP)
        y = TOP + row * (CELL + GAP)

        tooltip_text = f"{cnt:,} contribution{'s' if cnt != 1 else ''} on {dt}"
        rects.append(
            f'<rect class="c" x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="{RAD}" '
            f'fill="{COLORS[lvl]}">'
            f'<title>{html.escape(tooltip_text)}</title>'
            f'</rect>'
        )

    # Header Telemetry
    start_fmt = format_date(days[0]["date"])
    end_fmt = format_date(days[-1]["date"])
    active_days = data.get("active_days", sum(1 for d in days if d.get("count", 0) > 0))
    total_days = data.get("total_days", len(days))
    consistency = data.get("consistency_pct", round((active_days / total_days) * 100, 1) if total_days else 100)
    cur_streak = data.get("current_streak", {}).get("length", 1021)

    # Color legend coordinates (bottom right)
    leg_x = W - 142
    leg_y = H - 28
    legend_svg = [
        f'<text class="lbl" x="{leg_x - 30}" y="{leg_y + 9}">Less</text>',
    ]
    for idx, col in enumerate(COLORS):
        legend_svg.append(
            f'<rect x="{leg_x + idx * 14}" y="{leg_y}" width="10" height="10" rx="2" fill="{col}"/>'
        )
    legend_svg.append(f'<text class="lbl" x="{leg_x + len(COLORS) * 14 + 6}" y="{leg_y + 9}">More</text>')

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="\'Space Grotesk\', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, sans-serif">',
        "<style>",
        f"""
        text.lbl {{ fill: {TEXT_SUBTLE}; font-size: 10px; font-weight: 500; font-family: ui-monospace, SFMono-Regular, monospace; }}
        text.head-prompt {{ fill: {TEXT_MUTED}; font-size: 11.5px; font-family: ui-monospace, SFMono-Regular, monospace; }}
        text.head-stat {{ fill: {TAUPE}; font-size: 11.5px; font-weight: 600; }}
        text.meta-range {{ fill: {TEXT_SUBTLE}; font-size: 10px; font-family: ui-monospace, SFMono-Regular, monospace; }}
        .c {{ transition: opacity 0.15s ease; }}
        .c:hover {{ opacity: 0.8; stroke: {TAUPE_LIGHT}; stroke-width: 1px; }}
        .grid-fade {{ animation: gridFade 0.4s ease-out both; }}
        @keyframes gridFade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        @media (prefers-reduced-motion: reduce) {{ .grid-fade {{ animation: none !important; opacity: 1 !important; }} }}
        """,
        "</style>",
        # Window Canvas Background
        f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{BORDER}" stroke-width="1"/>',
        # Header Bar
        f'<line x1="0" y1="32" x2="{W}" y2="32" stroke="{BORDER}" stroke-width="1"/>',
        f'<circle cx="16" cy="16" r="4" fill="#ff5f56"/>',
        f'<circle cx="28" cy="16" r="4" fill="#ffbd2e"/>',
        f'<circle cx="40" cy="16" r="4" fill="#27c93f"/>',
        f'<text class="head-prompt" x="54" y="20">rusdi@github:~$ git-contrib-matrix --annual</text>',
        f'<text class="head-stat" x="{W - 16}" y="20" text-anchor="end">{total:,} contributions in past year · 🔥 {cur_streak:,}d streak</text>',
        # Calendar Grid
        f'<g class="grid-fade">',
        "".join(labels),
        "".join(rects),
        f'</g>',
        # Footer
        f'<text class="meta-range" x="{LEFT}" y="{H - 19}">{start_fmt} – {end_fmt} ({consistency:.1f}% unbroken consistency)</text>',
        "".join(legend_svg),
        "</svg>",
    ]

    return "\n".join(parts)


def main():
    data, days, total = load_dataset()
    svg = render_svg(data, days, total)
    if svg:
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Rendered {OUT_PATH}: size={len(svg)} bytes")


if __name__ == "__main__":
    main()
