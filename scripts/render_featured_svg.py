#!/usr/bin/env python3
"""
Generate minimalist, sleek SVG cards for each featured repository:
- dist/featured-mahasigmind.svg
- dist/featured-cuanin.svg
- dist/featured-jt-scheduling.svg
- dist/featured-alam-makmur.svg
- dist/featured.svg (master fallback)

Minimalist design principles:
- Spacious layout with zero unnecessary clutter (no fake terminals or verbose shells)
- Clean typography matching GitHub native system font stack
- Subtle flowing accent beam animation ("animasi mengalir") along the top edge
- Soft ambient light sheen across the card surface
- Language dot with breathing pulse
- Clickable directly to the repository
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(HERE, "..", "dist")

CARD_W = 420
CARD_H = 125

BG = "#0d1117"
BG_CARD = "#161b22"
BORDER = "#30363d"
TEXT_TITLE = "#f0f6fc"
TEXT_MUTED = "#8b949e"
TEXT_DIM = "#6e7681"

PROJECTS = [
    {
        "key": "mahasigmind",
        "filename": "featured-mahasigmind.svg",
        "icon": "🧠",
        "name": "MahasigMind",
        "desc": "Mental Health SPA Platform",
        "primary_tech": "Laravel 11",
        "stack": "React 19 · Inertia.js",
        "accent": "#58a6ff",  # Cyan
        "url": "https://github.com/RusdiEneri/MahasigMind",
    },
    {
        "key": "cuanin",
        "filename": "featured-cuanin.svg",
        "icon": "🛒",
        "name": "Cuanin",
        "desc": "Preloved Multi-Vendor Marketplace",
        "primary_tech": "Laravel 12",
        "stack": "MySQL · Vite",
        "accent": "#3fb950",  # Emerald Green
        "url": "https://github.com/RusdiEneri/Cuanin",
    },
    {
        "key": "jt-scheduling",
        "filename": "featured-jt-scheduling.svg",
        "icon": "🚚",
        "name": "J&T Scheduling",
        "desc": "Algorithmic Shift Optimizer",
        "primary_tech": "Python",
        "stack": "Genetic Algorithm",
        "accent": "#d29922",  # Amber / Gold
        "url": "https://github.com/RusdiEneri/jt-express-scheduling",
    },
    {
        "key": "alam-makmur",
        "filename": "featured-alam-makmur.svg",
        "icon": "🏢",
        "name": "Alam Makmur Jaya",
        "desc": "Centralized ERP & Retail System",
        "primary_tech": "Express.js",
        "stack": "Vite · REST API",
        "accent": "#a371f7",  # Purple
        "url": "https://github.com/RusdiEneri/alam-makmur-jaya",
    },
]


def render_card(p):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" '
        f'font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', \'Noto Sans\', Helvetica, Arial, sans-serif">',
        "<style>",
        f"""
        @keyframes flowBeam {{
            0% {{ transform: translateX(-400px); }}
            40%, 100% {{ transform: translateX(450px); }}
        }}
        @keyframes pulseDot {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.45; }}
        }}
        @keyframes cardGlow {{
            0%, 100% {{ opacity: 0.8; }}
            50% {{ opacity: 0.5; }}
        }}
        .flowing-beam {{
            animation: flowBeam 4.5s ease-in-out infinite;
        }}
        .pulse-dot {{
            animation: pulseDot 2.4s ease-in-out infinite;
        }}
        .top-accent {{
            animation: cardGlow 3s ease-in-out infinite;
        }}
        @media (prefers-reduced-motion: reduce) {{
            .flowing-beam {{ display: none !important; }}
            .pulse-dot {{ animation: none !important; }}
            .top-accent {{ animation: none !important; }}
        }}
        """,
        "</style>",
        "<defs>",
        # Top flowing beam gradient
        f'<linearGradient id="beamGrad-{p["key"]}" x1="0" y1="0" x2="1" y2="0">',
        f'  <stop offset="0%" stop-color="{p["accent"]}" stop-opacity="0"/>',
        f'  <stop offset="50%" stop-color="{p["accent"]}" stop-opacity="0.95"/>',
        f'  <stop offset="100%" stop-color="{p["accent"]}" stop-opacity="0"/>',
        f"</linearGradient>",
        # Ambient soft surface sheen
        f'<linearGradient id="sheenGrad-{p["key"]}" x1="0" y1="0" x2="1" y2="0">',
        f'  <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>',
        f'  <stop offset="50%" stop-color="{p["accent"]}" stop-opacity="0.06"/>',
        f'  <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>',
        f"</linearGradient>",
        # Card clip path
        f'<clipPath id="cardClip-{p["key"]}">',
        f'  <rect width="{CARD_W}" height="{CARD_H}" rx="8"/>',
        f"</clipPath>",
        "</defs>",
        # Clickable root link
        f'<a xlink:href="{p["url"]}" target="_blank" style="text-decoration: none; cursor: pointer;">',
        # Background card
        f'<rect width="{CARD_W}" height="{CARD_H}" rx="8" fill="{BG_CARD}"/>',
        f'<rect x="0.5" y="0.5" width="{CARD_W-1}" height="{CARD_H-1}" rx="8" fill="none" stroke="{BORDER}" stroke-width="1"/>',
        # Ambient flowing surface sheen (clipped)
        f'<g clip-path="url(#cardClip-{p["key"]})">',
        f'<rect class="flowing-beam" x="0" y="0" width="260" height="{CARD_H}" fill="url(#sheenGrad-{p["key"]})"/>',
        f'</g>',
        # Top static accent border
        f'<line x1="0" y1="1" x2="{CARD_W}" y2="1" stroke="{BORDER}" stroke-width="1"/>',
        # Top animated glowing flowing beam line
        f'<g clip-path="url(#cardClip-{p["key"]})">',
        f'<rect class="flowing-beam top-accent" x="0" y="0" width="180" height="2" fill="url(#beamGrad-{p["key"]})"/>',
        f'</g>',
        # Row 1: Emoji + Title + Arrow (y = 38)
        f'<text x="20" y="38" fill="{TEXT_TITLE}" font-size="15" font-weight="600">',
        f'{p["icon"]}  {html.escape(p["name"])}',
        f'</text>',
        f'<text x="{CARD_W - 20}" y="38" fill="{TEXT_DIM}" font-size="13" font-weight="600" text-anchor="end">↗</text>',
        # Row 2: Description (y = 66)
        f'<text x="20" y="68" fill="{TEXT_MUTED}" font-size="12.5" font-weight="400">',
        f'{html.escape(p["desc"])}',
        f'</text>',
        # Row 3: Language dot + Primary Tech + Stack (y = 98)
        f'<circle class="pulse-dot" cx="24" cy="98" r="3.5" fill="{p["accent"]}"/>',
        f'<text x="34" y="102" font-size="11.5">',
        f'<tspan fill="{p["accent"]}" font-weight="500">{html.escape(p["primary_tech"])}</tspan> ',
        f'<tspan fill="{TEXT_DIM}">·  {html.escape(p["stack"])}</tspan>',
        f'</text>',
        f'</a>',
        f'</svg>',
    ]
    return "".join(parts)


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    for p in PROJECTS:
        out_file = os.path.join(DIST_DIR, p["filename"])
        svg_content = render_card(p)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Wrote {out_file}: {CARD_W} x {CARD_H}")

    # Update master fallback featured.svg
    master_path = os.path.join(DIST_DIR, "featured.svg")
    with open(os.path.join(DIST_DIR, PROJECTS[0]["filename"]), "r", encoding="utf-8") as f:
        master_content = f.read()
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_content)
    print(f"Synced {master_path}")


if __name__ == "__main__":
    main()
