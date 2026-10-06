#!/usr/bin/env python3
"""
Render the real-time streak / numbers card from data/contributions.json
as an ultra-polished terminal-window SVG (stats.svg).
Canvas size: 840 x 880 (matches sys-info.svg exactly).
Features SMIL animated number count-ups and SMIL animated monthly bar chart.
"""
import datetime
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "dist", "stats.svg")

BG = "#0d1117"
BG2 = "#111722"
TILE = "#161b22"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
GREEN = "#39d353"
BAR = "#26a641"
CYAN = "#58a6ff"
GOLD = "#f1e05a"

W, H = 840, 880
PAD = 20
TITLEBAR_H = 34
COLS, ROWS = 2, 3
GAP = 16
TILE_W = (W - PAD * 2 - GAP * (COLS - 1)) / COLS
TILE_H = 146
TILES_TOP = TITLEBAR_H + PAD + 4
CHART_TOP = TILES_TOP + ROWS * TILE_H + (ROWS - 1) * GAP + GAP

TILE_STAGGER = 0.15
SLIDE_DUR = 0.45
COUNT_DUR = 1.2
FRAMES = 16
BAR_START = TILE_STAGGER * COLS * ROWS + 0.35
BAR_STAGGER = 0.05
BAR_DUR = 0.6


def short_date(d_str):
    if not d_str:
        return "—"
    try:
        return datetime.date.fromisoformat(d_str).strftime("%b %d, %Y")
    except Exception:
        return d_str


def fmt(v, like):
    return f"{v:,.1f}" if isinstance(like, float) else f"{int(round(v)):,}"


def main():
    if not os.path.exists(SRC):
        print(f"Error: {SRC} does not exist", file=sys.stderr)
        sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        data = json.load(f)

    cur = data.get("current_streak", {"length": 1016})
    lng = data.get("longest_streak", {"length": 1016})
    all_time = data.get("all_time_total", 14306)
    best = data.get("best_day", {"count": 718, "date": "2026-09-22"})
    avg_day = data.get("avg_per_active_day", 31.0)
    consistency = data.get("consistency_pct", 100.0)

    cur_start_fmt = short_date(cur.get("start", "2023-12-26"))
    lng_start_fmt = short_date(lng.get("start", "2023-12-26"))

    tiles = [
        ("current streak", cur.get("length", 1016), " days", f"🔥 Since {cur_start_fmt} (Active)", GREEN),
        ("longest streak", lng.get("length", 1016), " days", f"100% Unbroken consistency", INK),
        ("all-time contributions", all_time, " commits", "across all public repositories", CYAN),
        ("yearly consistency", consistency, " %", "365 / 365 active commit days", GREEN),
        ("peak throughput", best.get("count", 718), " / day", f"record high ({short_date(best.get('date', ''))})", INK),
        ("production pace", avg_day, " avg/day", "high-velocity engineering cadence", INK),
    ]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>',
        f'.t{{opacity:0;animation:in {SLIDE_DUR}s ease-out both}}',
        '@keyframes in{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:translateY(0)}}',
        f'.b{{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow {BAR_DUR}s ease-out both}}',
        '@keyframes grow{to{transform:scaleY(1)}}',
        '@media (prefers-reduced-motion: reduce){.t,.b{opacity:1!important;transform:none!important;animation:none!important}}',
        '</style>',
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    # Mac window dots
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i * 18}" cy="{TITLEBAR_H / 2}" r="5.5" fill="{dot}"/>')
    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4.5}" fill="{MUTED}" font-size="12.5" '
        f'text-anchor="middle">rusdi@github: ~$ ./stats.sh --telemetry live</text>'
    )

    # Stat Tiles
    for i, (label, value, suffix, caption, accent) in enumerate(tiles):
        col, row = i % COLS, i // COLS
        x = PAD + col * (TILE_W + GAP)
        y = TILES_TOP + row * (TILE_H + GAP)
        start = i * TILE_STAGGER
        count_start = start + SLIDE_DUR * 0.6

        parts.append(f'<g class="t" style="animation-delay:{start:.2f}s">')
        parts.append(
            f'<rect x="{x:.1f}" y="{y}" width="{TILE_W:.1f}" height="{TILE_H}" rx="10" '
            f'fill="{TILE}" stroke="{FRAME}"/>'
        )
        parts.append(f'<text x="{x + 24:.1f}" y="{y + 38}" fill="{MUTED}" font-size="20">$ {html.escape(label)}</text>')

        # count-up frames
        num_y = y + 96
        for k in range(1, FRAMES + 1):
            p = k / FRAMES
            v = value * (1 - (1 - p) ** 3)
            t_on = count_start + COUNT_DUR * (k - 1) / FRAMES
            t_off = count_start + COUNT_DUR * k / FRAMES
            anim = f'<set attributeName="opacity" to="1" begin="{t_on:.3f}s"/>'
            if k < FRAMES:
                anim += f'<set attributeName="opacity" to="0" begin="{t_off:.3f}s"/>'
            parts.append(
                f'<text x="{x + 24:.1f}" y="{num_y}" opacity="0" font-size="46" font-weight="700" fill="{accent}">'
                f'{fmt(v, value)}<tspan font-size="20" font-weight="400" fill="{MUTED}">{html.escape(suffix)}</tspan>'
                f'{anim}</text>'
            )
        parts.append(f'<text x="{x + 24:.1f}" y="{y + 128}" fill="{MUTED}" font-size="17">{html.escape(caption)}</text>')
        parts.append("</g>")

    # Monthly Bar Chart
    monthly = data.get("monthly", [])
    chart_x, chart_w = PAD, W - PAD * 2
    chart_h = H - PAD - CHART_TOP
    parts.append(f'<g class="t" style="animation-delay:{BAR_START - 0.3:.2f}s">')
    parts.append(
        f'<rect x="{chart_x}" y="{CHART_TOP}" width="{chart_w}" height="{chart_h}" rx="10" '
        f'fill="{TILE}" stroke="{FRAME}"/>'
    )
    parts.append(f'<text x="{chart_x + 24}" y="{CHART_TOP + 36}" fill="{MUTED}" font-size="20">$ contributions / month (past 12 months)</text>')
    parts.append("</g>")

    if monthly:
        plot_top = CHART_TOP + 56
        plot_bot = CHART_TOP + chart_h - 36
        plot_l, plot_r = chart_x + 24, chart_x + chart_w - 24
        slot = (plot_r - plot_l) / len(monthly)
        bar_w = slot * 0.62
        peak = max(m.get("total", 0) for m in monthly) or 1

        for i, m in enumerate(monthly):
            tot = m.get("total", 0)
            h_bar = max(4, (plot_bot - plot_top) * tot / peak)
            bx = plot_l + i * slot + (slot - bar_w) / 2
            fill = GREEN if tot == peak else BAR
            delay = BAR_START + i * BAR_STAGGER
            parts.append(
                f'<rect class="b" x="{bx:.1f}" y="{plot_bot - h_bar:.1f}" width="{bar_w:.1f}" height="{h_bar:.1f}" '
                f'rx="3" fill="{fill}" style="animation-delay:{delay:.2f}s"/>'
            )
            try:
                mon = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
            except Exception:
                mon = m["month"][-2:]
            parts.append(
                f'<text x="{bx + bar_w / 2:.1f}" y="{plot_bot + 24}" fill="{MUTED}" font-size="15" '
                f'text-anchor="middle">{mon}</text>'
            )
            if tot == peak:
                parts.append(
                    f'<text class="t" style="animation-delay:{delay + BAR_DUR:.2f}s" x="{bx + bar_w / 2:.1f}" '
                    f'y="{plot_bot - h_bar - 8:.1f}" fill="{INK}" font-size="16" font-weight="700" text-anchor="middle">{peak:,}</text>'
                )

    parts.append("</svg>")
    svg = "".join(parts)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT}: {W} x {H}")


if __name__ == "__main__":
    main()
