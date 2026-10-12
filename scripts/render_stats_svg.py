#!/usr/bin/env python3
"""
Render real-time GitHub telemetry stats card (stats.svg)
Styled in Rusdi's signature portfolio aesthetic (mangrusdi.my.id):
- Deep dark canvas (#0a0a0a) with refined surface cards (#141414)
- Warm taupe accents (#b38b6d / #d4a373)
- Swiss neo-minimalist typography with clean metrics
- Lightweight GPU-accelerated micro-animations (0 CPU lag, no SMIL frame hacks)
"""
import datetime
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "dist", "stats.svg")

# Design tokens matching mangrusdi.my.id
BG = "#0a0a0a"
SURFACE = "#141414"
SURFACE_RAISED = "#1a1a1a"
BORDER = "#262626"
BORDER_STRONG = "#333333"
TEXT_PRIMARY = "#f5f5f5"
TEXT_MUTED = "#9e9e9e"
TEXT_SUBTLE = "#6e6e6e"
TAUPE = "#b38b6d"
TAUPE_LIGHT = "#d4a373"
GREEN_LIVE = "#3fb950"

W, H = 840, 316
PAD = 20
TITLEBAR_H = 36


def short_date(d_str):
    if not d_str:
        return "-"
    try:
        return datetime.date.fromisoformat(d_str).strftime("%b %d, %Y")
    except Exception:
        return d_str


def main():
    if not os.path.exists(SRC):
        print(f"Error: {SRC} does not exist", file=sys.stderr)
        sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        data = json.load(f)

    cur = data.get("current_streak", {"length": 1021})
    lng = data.get("longest_streak", {"length": 1021})
    all_time = data.get("all_time_total", 14778)
    consistency = data.get("consistency_pct", 100.0)
    avg_day = data.get("avg_per_active_day", 32.2)
    cur_start_fmt = short_date(cur.get("start", "2023-12-26"))

    tiles = [
        ("CURRENT STREAK", f"{cur.get('length', 1021):,}", " DAYS", f"Unbroken since {cur_start_fmt}", TAUPE),
        ("TOTAL COMMITS", f"{all_time:,}", "", "All-time public contributions", TEXT_PRIMARY),
        ("YEARLY CONSISTENCY", f"{consistency:.1f}%", "", "365 / 365 active commit days", TAUPE_LIGHT),
        ("VELOCITY PACE", f"{avg_day:.1f}", " /day", "High-throughput cadence", TEXT_PRIMARY),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="\'Space Grotesk\', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, sans-serif">',
        "<style>",
        """
        .pulse-dot {
            animation: pulseGlow 2.4s ease-in-out infinite;
        }
        @keyframes pulseGlow {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.35; transform: scale(0.92); }
        }
        .bar-item {
            transition: opacity 0.2s ease;
        }
        .bar-item:hover {
            opacity: 0.85;
        }
        @media (prefers-reduced-motion: reduce) {
            .pulse-dot { animation: none !important; opacity: 1 !important; }
        }
        """,
        "</style>",
        # Window Canvas Background
        f'<rect width="{W}" height="{H}" rx="6" fill="{BG}"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{BORDER}" stroke-width="1"/>',
        # Title bar divider
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{BORDER}" stroke-width="1"/>',
    ]

    # Title bar controls (Mac dots)
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i * 16}" cy="{TITLEBAR_H / 2}" r="4.5" fill="{dot}"/>')

    # Title bar prompt
    parts.append(
        f'<text x="{PAD + 58}" y="{TITLEBAR_H / 2 + 4}" fill="{TEXT_MUTED}" font-size="12" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace">'
        f'rusdi@server:~$ telemetry --profile RusdiEneri</text>'
    )

    # Live status indicator on right
    live_x = W - PAD - 84
    parts.append(
        f'<g transform="translate({live_x}, {TITLEBAR_H / 2 - 8})">'
        f'<circle cx="8" cy="8" r="4" fill="{GREEN_LIVE}" class="pulse-dot" transform-origin="8 8"/>'
        f'<text x="18" y="11.5" fill="{TEXT_MUTED}" font-size="10.5" font-weight="600" letter-spacing="0.6">LIVE METRICS</text>'
        f'</g>'
    )

    # Top Metric Tiles (4 columns)
    tile_top = TITLEBAR_H + 14
    tile_h = 92
    cols = 4
    gap = 12
    tile_w = (W - PAD * 2 - gap * (cols - 1)) / cols

    for i, (label, val_str, suffix, caption, accent) in enumerate(tiles):
        x = PAD + i * (tile_w + gap)
        y = tile_top
        parts.append(
            f'<g>'
            f'<rect x="{x:.1f}" y="{y}" width="{tile_w:.1f}" height="{tile_h}" rx="4" '
            f'fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
            f'<text x="{x + 14:.1f}" y="{y + 22}" fill="{TEXT_SUBTLE}" font-size="9.5" font-weight="600" '
            f'letter-spacing="0.8">{html.escape(label)}</text>'
            f'<text x="{x + 14:.1f}" y="{y + 56}" fill="{accent}" font-size="25" font-weight="700">'
            f'{html.escape(val_str)}'
            f'<tspan font-size="12" font-weight="500" fill="{TEXT_MUTED}">{html.escape(suffix)}</tspan>'
            f'</text>'
            f'<text x="{x + 14:.1f}" y="{y + 78}" fill="{TEXT_MUTED}" font-size="10.5">{html.escape(caption)}</text>'
            f'</g>'
        )

    # Bottom Velocity Chart (12 Months)
    chart_y = tile_top + tile_h + 12
    chart_h = 138
    chart_w = W - PAD * 2
    parts.append(
        f'<g>'
        f'<rect x="{PAD}" y="{chart_y}" width="{chart_w}" height="{chart_h}" rx="4" '
        f'fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'<text x="{PAD + 14}" y="{chart_y + 22}" fill="{TEXT_SUBTLE}" font-size="9.5" font-weight="600" '
        f'letter-spacing="0.8">MONTHLY COMMIT VELOCITY (PAST 12 MONTHS)</text>'
    )

    monthly = data.get("monthly", [])
    if monthly:
        monthly_12 = monthly[-12:]
        max_val = max((m.get("total", 0) for m in monthly_12), default=1)
        if max_val == 0:
            max_val = 1

        n_bars = len(monthly_12)
        inner_w = chart_w - 28
        bar_w = min(42.0, (inner_w - (n_bars - 1) * 14) / n_bars)
        actual_gap = (inner_w - bar_w * n_bars) / max(1, n_bars - 1)
        plot_bottom = chart_y + chart_h - 30
        plot_max_h = 62.0

        for idx, m in enumerate(monthly_12):
            val = m.get("total", 0)
            month_key = m.get("month", "")
            try:
                m_label = datetime.datetime.strptime(month_key, "%Y-%m").strftime("%b")
            except Exception:
                m_label = month_key[-2:]

            bh = max(4.0, (val / max_val) * plot_max_h) if max_val > 0 else 4.0
            bx = PAD + 14 + idx * (bar_w + actual_gap)
            by = plot_bottom - bh

            is_peak = (val == max_val and val > 0)
            fill_col = TAUPE_LIGHT if is_peak else TAUPE
            fill_opacity = "1" if is_peak else "0.85"

            tooltip = f"{month_key}: {val:,} commits"
            parts.append(
                f'<g class="bar-item">'
                f'<title>{html.escape(tooltip)}</title>'
                f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="2" '
                f'fill="{fill_col}" fill-opacity="{fill_opacity}"/>'
                f'<text x="{bx + bar_w / 2:.1f}" y="{by - 5:.1f}" fill="{TEXT_SUBTLE}" font-size="9.5" '
                f'text-anchor="middle">{val:,}</text>'
                f'<text x="{bx + bar_w / 2:.1f}" y="{plot_bottom + 17:.1f}" fill="{TEXT_MUTED}" '
                f'font-size="10.5" font-weight="500" text-anchor="middle">{html.escape(m_label)}</text>'
                f'</g>'
            )

    parts.append("</g>")
    parts.append("</svg>")

    svg_content = "\n".join(parts)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Rendered {OUT}: {W}x{H}, size={len(svg_content)} bytes")


if __name__ == "__main__":
    main()
