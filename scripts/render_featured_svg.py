#!/usr/bin/env python3
"""
Render an animated, flowing terminal simulation of `./featured.sh` as an SVG (featured.svg).
Matches the sleek dark CLI aesthetic of contrib-heatmap.svg, sys-info.svg, and stats.svg.
Features:
- macOS terminal titlebar with traffic light buttons and deployment indicator
- Animated cascading entrance with fluid translateY + opacity timing
- Periodic ambient flowing light sweep (shimmer wave) across the cards
- Dynamic pulsing status indicators (LIVE / PROD)
- Rich tech stack pill badges for each featured repository
- Blinking shell cursor at bottom
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "featured.svg")

CANVAS_W = 860
CANVAS_H = 460
PAD = 20
TITLEBAR_H = 36

# Color palette
BG = "#0d1117"
BG_TOP = "#161b22"
CARD_BG = "#13171f"
CARD_STROKE = "#30363d"
CARD_HOVER = "#1c2128"
MUTED = "#7d8590"
TEXT_DIM = "#9ca3af"
INK = "#e6edf3"
GREEN = "#39d353"
GREEN_GLOW = "#238636"
CYAN = "#58a6ff"
YELLOW = "#f0883e"
PURPLE = "#bc8cff"

PROJECTS = [
    {
        "num": "01",
        "icon": "🧠",
        "name": "MahasigMind",
        "accent": CYAN,
        "desc": "Mental Health SPA Platform · Secure health records & reflective journaling",
        "tags": ["Laravel 11", "React 19", "TypeScript", "Inertia.js"],
        "status": "LIVE",
        "repo": "RusdiEneri/MahasigMind",
        "url": "https://github.com/RusdiEneri/MahasigMind",
    },
    {
        "num": "02",
        "icon": "🛒",
        "name": "Cuanin",
        "accent": GREEN,
        "desc": "Preloved Multi-Vendor Marketplace · RBAC & WhatsApp price negotiation",
        "tags": ["Laravel 12", "MySQL", "Vite", "Tailwind CSS"],
        "status": "LIVE",
        "repo": "RusdiEneri/Cuanin",
        "url": "https://github.com/RusdiEneri/Cuanin",
    },
    {
        "num": "03",
        "icon": "🚚",
        "name": "J&T Scheduling",
        "accent": YELLOW,
        "desc": "Algorithmic Shift Optimizer · Genetic Algorithm for complex constraints",
        "tags": ["Python", "Genetic Algorithm", "Streamlit", "Pandas"],
        "status": "LIVE",
        "repo": "RusdiEneri/jt-express-scheduling",
        "url": "https://github.com/RusdiEneri/jt-express-scheduling",
    },
    {
        "num": "04",
        "icon": "🏢",
        "name": "Alam Makmur Jaya",
        "accent": PURPLE,
        "desc": "Centralized ERP & Retail System · Real-time inventory & automated PDF reporting",
        "tags": ["Express.js", "Vite", "REST API", "Vanilla JS"],
        "status": "LIVE",
        "repo": "RusdiEneri/alam-makmur-jaya",
        "url": "https://github.com/RusdiEneri/alam-makmur-jaya",
    },
]


def render_svg():
    card_w = CANVAS_W - (PAD + 10) * 2
    card_h = 70
    card_gap = 10
    start_y = TITLEBAR_H + 58

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        "<style>",
        """
        @keyframes cascadeIn {
            0% { opacity: 0; transform: translateY(14px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes flowSweep {
            0% { transform: translateX(-900px); }
            35%, 100% { transform: translateX(900px); }
        }
        @keyframes blinkCursor {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }
        @keyframes breatheGlow {
            0%, 100% { opacity: 0.9; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
        .flow-row {
            opacity: 0;
            animation: cascadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .cursor {
            animation: blinkCursor 1.05s infinite;
        }
        .sweep-beam {
            animation: flowSweep 5.5s ease-in-out infinite;
        }
        .pulse-light {
            transform-origin: center;
            animation: breatheGlow 2.2s ease-in-out infinite;
        }
        @media (prefers-reduced-motion: reduce) {
            .flow-row { opacity: 1 !important; transform: none !important; animation: none !important; }
            .sweep-beam { display: none !important; }
            .pulse-light { animation: none !important; }
        }
        """,
        "</style>",
        "<defs>",
        f'<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">',
        f'  <stop offset="0%" stop-color="{BG_TOP}"/>',
        f'  <stop offset="100%" stop-color="{BG}"/>',
        f"</linearGradient>",
        # Ambient flowing light beam gradient
        f'<linearGradient id="sweepGrad" x1="0" y1="0" x2="1" y2="0">',
        f'  <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>',
        f'  <stop offset="50%" stop-color="#ffffff" stop-opacity="0.07"/>',
        f'  <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>',
        f"</linearGradient>",
        # Clip path for cards area so sweep beam doesn't bleed outside
        f'<clipPath id="cardsClip">',
        f'  <rect x="{PAD + 10}" y="{start_y}" width="{card_w}" height="{4 * card_h + 3 * card_gap}" rx="8"/>',
        f"</clipPath>",
        "</defs>",
        # Main Window
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bgGrad)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" fill="none" stroke="{CARD_STROKE}" stroke-width="1"/>',
        # Titlebar
        f'<path d="M 0,12 Q 0,0 12,0 L {CANVAS_W-12},0 Q {CANVAS_W},0 {CANVAS_W},12 L {CANVAS_W},{TITLEBAR_H} L 0,{TITLEBAR_H} Z" fill="{BG_TOP}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{CARD_STROKE}" stroke-width="1"/>',
    ]

    # Traffic lights
    for i, (col, stroke) in enumerate([("#ff5f56", "#e0443e"), ("#ffbd2e", "#dea123"), ("#27c93f", "#1aab29")]):
        cx = PAD + 10 + i * 18
        cy = TITLEBAR_H / 2
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{col}" stroke="{stroke}" stroke-width="0.5"/>')

    # Titlebar text
    parts.append(
        f'<text x="{CANVAS_W / 2}" y="{TITLEBAR_H / 2 + 4.5}" fill="{MUTED}" font-size="12" '
        f'font-weight="500" text-anchor="middle">rusdi@github: ~/portfolio $ ./featured.sh</text>'
    )
    # Right-aligned status pill
    status_x = CANVAS_W - PAD - 10
    parts.append(
        f'<g transform="translate({status_x - 120}, {TITLEBAR_H / 2 - 9})">'
        f'<rect width="120" height="18" rx="9" fill="#13231b" stroke="{GREEN}" stroke-width="0.8"/>'
        f'<circle class="pulse-light" cx="12" cy="9" r="3.5" fill="{GREEN}"/>'
        f'<text x="64" y="12.5" fill="{GREEN}" font-size="10.5" font-weight="700" text-anchor="middle">4/4 VERIFIED</text>'
        f'</g>'
    )

    # Shell execution banner
    parts.append(f'<g class="flow-row" style="animation-delay: 0.08s;">')
    parts.append(
        f'<text x="{PAD + 10}" y="{TITLEBAR_H + 24}" font-size="13.5">'
        f'<tspan fill="{MUTED}">rusdi@github</tspan> '
        f'<tspan fill="{CYAN}">~ $</tspan> '
        f'<tspan fill="{INK}" font-weight="700">./featured.sh</tspan>'
        f'</text>'
    )
    parts.append(
        f'<text x="{PAD + 10}" y="{TITLEBAR_H + 44}" fill="{MUTED}" font-size="11.5">'
        f'🚀 Initializing featured production stack &amp; microservices matrix...'
        f'</text>'
    )
    parts.append(f'</g>')

    # The 4 flowing project cards
    for idx, p in enumerate(PROJECTS):
        ry = start_y + idx * (card_h + card_gap)
        delay = 0.22 + idx * 0.16

        parts.append(f'<g class="flow-row" style="animation-delay: {delay:.2f}s;">')

        # Card container with anchor link for interactive SVG support
        parts.append(f'<a xlink:href="{p["url"]}" target="_blank" style="cursor: pointer;">')
        parts.append(
            f'<rect x="{PAD + 10}" y="{ry}" width="{card_w}" height="{card_h}" rx="8" '
            f'fill="{CARD_BG}" stroke="{CARD_STROKE}" stroke-width="0.9"/>'
        )

        # Left accent colored pill bar
        parts.append(
            f'<rect x="{PAD + 10}" y="{ry + 10}" width="3.5" height="{card_h - 20}" rx="1.75" fill="{p["accent"]}"/>'
        )

        # Index badge: e.g. [01]
        parts.append(
            f'<text x="{PAD + 24}" y="{ry + 29}" fill="{MUTED}" font-size="12" font-weight="600">[{p["num"]}]</text>'
        )

        # Icon and Title
        title_x = PAD + 62
        parts.append(
            f'<text x="{title_x}" y="{ry + 29}" font-size="15" font-weight="700">'
            f'{p["icon"]} <tspan fill="{p["accent"]}">{html.escape(p["name"])}</tspan>'
            f'</text>'
        )

        # Tech stack pill badges
        name_px = len(p["name"]) * 9 + 42
        pill_x = title_x + name_px
        for tag in p["tags"]:
            tag_w = len(tag) * 6.8 + 14
            # Keep safely within bounds before right-hand LIVE badge
            if pill_x + tag_w < PAD + 10 + card_w - 92:
                parts.append(
                    f'<rect x="{pill_x:.1f}" y="{ry + 15}" width="{tag_w:.1f}" height="19" rx="4" '
                    f'fill="#1c2128" stroke="{CARD_STROKE}" stroke-width="0.75"/>'
                )
                parts.append(
                    f'<text x="{pill_x + tag_w / 2:.1f}" y="{ry + 28}" fill="{TEXT_DIM}" '
                    f'font-size="10.5" text-anchor="middle">{html.escape(tag)}</text>'
                )
                pill_x += tag_w + 6

        # LIVE status badge on the right
        badge_w = 68
        badge_x = PAD + 10 + card_w - badge_w - 12
        parts.append(
            f'<rect x="{badge_x}" y="{ry + 15}" width="{badge_w}" height="19" rx="4" '
            f'fill="#13231b" stroke="{GREEN_GLOW}" stroke-width="0.8"/>'
        )
        parts.append(
            f'<circle class="pulse-light" cx="{badge_x + 11}" cy="{ry + 24.5}" r="3" fill="{GREEN}"/>'
        )
        parts.append(
            f'<text x="{badge_x + 38}" y="{ry + 28}" fill="{GREEN}" font-size="10.5" '
            f'font-weight="700" text-anchor="middle">{p["status"]}</text>'
        )

        # Second row: Description + Repo slug
        desc_x = PAD + 24
        parts.append(
            f'<text x="{desc_x}" y="{ry + 52}" font-size="12">'
            f'<tspan fill="{MUTED}">{html.escape(p["desc"])}</tspan> '
            f'<tspan fill="{CYAN}">· {html.escape(p["repo"])} ↗</tspan>'
            f'</text>'
        )

        parts.append(f'</a>')
        parts.append(f'</g>')

    # Ambient light sweep beam across the cards
    parts.append(f'<g clip-path="url(#cardsClip)">')
    parts.append(
        f'<rect class="sweep-beam" x="{PAD + 10}" y="{start_y}" width="400" '
        f'height="{4 * card_h + 3 * card_gap}" fill="url(#sweepGrad)"/>'
    )
    parts.append(f'</g>')

    # Bottom Terminal Prompt
    bot_y = start_y + 4 * (card_h + card_gap) + 12
    parts.append(f'<g class="flow-row" style="animation-delay: 0.95s;">')
    parts.append(
        f'<line x1="{PAD + 10}" y1="{bot_y}" x2="{CANVAS_W - PAD - 10}" y2="{bot_y}" '
        f'stroke="{CARD_STROKE}" stroke-width="0.8" stroke-dasharray="3,3"/>'
    )
    parts.append(
        f'<text x="{PAD + 10}" y="{bot_y + 24}" font-size="13">'
        f'<tspan fill="{MUTED}">rusdi@github</tspan> '
        f'<tspan fill="{CYAN}">~ $</tspan> '
        f'<tspan fill="{GREEN}">open-selected --interactive</tspan>'
        f'</text>'
    )
    # Cursor
    cursor_x = PAD + 10 + 350
    parts.append(
        f'<rect class="cursor" x="{cursor_x}" y="{bot_y + 11}" width="7.5" height="15" fill="{GREEN}"/>'
    )
    parts.append(f'</g>')

    parts.append(f'</svg>')
    return "".join(parts)


def main():
    svg = render_svg()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}: {CANVAS_W} x {CANVAS_H}, {len(svg)//1024} KB")


if __name__ == "__main__":
    main()
