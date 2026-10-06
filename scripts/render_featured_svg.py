#!/usr/bin/env python3
"""
Generate individual, flowing animated terminal SVG cards for each featured repository:
- dist/featured-mahasigmind.svg
- dist/featured-cuanin.svg
- dist/featured-jt-scheduling.svg
- dist/featured-alam-makmur.svg
- dist/featured.svg (master index)

Each card is a standalone, spacious terminal window with:
- macOS titlebar, path slug, and glowing LIVE status badge
- Terminal command invocation ($ ./start.sh) with blinking cursor
- Project identity with custom accent color, emoji, and tagline
- Clear tech stack pill badges
- Ambient flowing shimmer wave ("animasi mengalir") sweeping across the card
- Interactive link footer with target repository URL
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(HERE, "..", "dist")

CARD_W = 420
CARD_H = 210
TITLEBAR_H = 32

BG = "#0d1117"
BG_TOP = "#161b22"
PILL_BG = "#1c2128"
STROKE = "#30363d"
MUTED = "#7d8590"
TEXT_DIM = "#8b949e"
TEXT_MAIN = "#e6edf3"
GREEN = "#39d353"
GREEN_BOX = "#13231b"
GREEN_STROKE = "#238636"
CYAN = "#58a6ff"
YELLOW = "#f0883e"
PURPLE = "#bc8cff"

PROJECTS = [
    {
        "key": "mahasigmind",
        "filename": "featured-mahasigmind.svg",
        "num": "01",
        "icon": "🧠",
        "name": "MahasigMind",
        "slug": "mahasigmind.sh",
        "cmd": "./launch.sh --service=spa",
        "accent": CYAN,
        "tagline": "Mental Health SPA Platform",
        "desc": "Secure health records & reflective journaling",
        "tags": ["Laravel 11", "React 19", "Inertia.js", "TypeScript"],
        "repo": "RusdiEneri/MahasigMind",
        "url": "https://github.com/RusdiEneri/MahasigMind",
    },
    {
        "key": "cuanin",
        "filename": "featured-cuanin.svg",
        "num": "02",
        "icon": "🛒",
        "name": "Cuanin",
        "slug": "cuanin.sh",
        "cmd": "php artisan serve --port=8080",
        "accent": GREEN,
        "tagline": "Preloved Multi-Vendor Marketplace",
        "desc": "RBAC security & WhatsApp price negotiation",
        "tags": ["Laravel 12", "MySQL", "Vite", "Tailwind CSS"],
        "repo": "RusdiEneri/Cuanin",
        "url": "https://github.com/RusdiEneri/Cuanin",
    },
    {
        "key": "jt-scheduling",
        "filename": "featured-jt-scheduling.svg",
        "num": "03",
        "icon": "🚚",
        "name": "J&T Scheduling",
        "slug": "jt-scheduler.py",
        "cmd": "python optimize.py --genetic-algo",
        "accent": YELLOW,
        "tagline": "Algorithmic Shift Optimizer",
        "desc": "Genetic Algorithm for complex work constraints",
        "tags": ["Python", "Genetic Algo", "Streamlit", "Pandas"],
        "repo": "RusdiEneri/jt-express-scheduling",
        "url": "https://github.com/RusdiEneri/jt-express-scheduling",
    },
    {
        "key": "alam-makmur",
        "filename": "featured-alam-makmur.svg",
        "num": "04",
        "icon": "🏢",
        "name": "Alam Makmur Jaya",
        "slug": "alam-makmur.js",
        "cmd": "node server.js --cluster-mode",
        "accent": PURPLE,
        "tagline": "Centralized ERP & Retail System",
        "desc": "Real-time inventory & automated PDF reporting",
        "tags": ["Express.js", "Vite", "REST API", "Vanilla JS"],
        "repo": "RusdiEneri/alam-makmur-jaya",
        "url": "https://github.com/RusdiEneri/alam-makmur-jaya",
    },
]


def render_single_card(p):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        "<style>",
        f"""
        @keyframes flowSweep {{
            0% {{ transform: translateX(-350px) skewX(-20deg); }}
            40%, 100% {{ transform: translateX(500px) skewX(-20deg); }}
        }}
        @keyframes pulseDot {{
            0%, 100% {{ r: 3; opacity: 1; }}
            50% {{ r: 4.5; opacity: 0.5; }}
        }}
        @keyframes blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}
        @keyframes accentBreathe {{
            0%, 100% {{ opacity: 0.95; }}
            50% {{ opacity: 0.55; }}
        }}
        .sweep-beam {{
            animation: flowSweep 4.8s ease-in-out infinite;
        }}
        .pulse-dot {{
            animation: pulseDot 2.2s ease-in-out infinite;
        }}
        .cursor {{
            animation: blink 1.05s infinite;
        }}
        .accent-bar {{
            animation: accentBreathe 3s ease-in-out infinite;
        }}
        @media (prefers-reduced-motion: reduce) {{
            .sweep-beam {{ display: none !important; }}
            .pulse-dot {{ animation: none !important; }}
        }}
        """,
        "</style>",
        "<defs>",
        f'<linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">',
        f'  <stop offset="0%" stop-color="{BG_TOP}"/>',
        f'  <stop offset="100%" stop-color="{BG}"/>',
        f"</linearGradient>",
        # Ambient flowing light beam gradient
        f'<linearGradient id="sweepGrad" x1="0" y1="0" x2="1" y2="0">',
        f'  <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>',
        f'  <stop offset="50%" stop-color="{p["accent"]}" stop-opacity="0.12"/>',
        f'  <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>',
        f"</linearGradient>",
        # Clip path for card window
        f'<clipPath id="windowClip">',
        f'  <rect width="{CARD_W}" height="{CARD_H}" rx="10"/>',
        f"</clipPath>",
        "</defs>",
        # Root clickable anchor for interactive SVG support
        f'<a xlink:href="{p["url"]}" target="_blank" style="text-decoration: none; cursor: pointer;">',
        # Background window
        f'<rect width="{CARD_W}" height="{CARD_H}" rx="10" fill="url(#cardBg)"/>',
        f'<rect x="0.5" y="0.5" width="{CARD_W-1}" height="{CARD_H-1}" rx="10" fill="none" stroke="{STROKE}" stroke-width="1"/>',
        # Titlebar
        f'<path d="M 0,10 Q 0,0 10,0 L {CARD_W-10},0 Q {CARD_W},0 {CARD_W},10 L {CARD_W},{TITLEBAR_H} L 0,{TITLEBAR_H} Z" fill="{BG_TOP}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CARD_W}" y2="{TITLEBAR_H}" stroke="{STROKE}" stroke-width="1"/>',
    ]

    # Traffic light buttons
    for i, (col, strk) in enumerate([("#ff5f56", "#e0443e"), ("#ffbd2e", "#dea123"), ("#27c93f", "#1aab29")]):
        cx = 16 + i * 16
        cy = TITLEBAR_H / 2
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{col}" stroke="{strk}" stroke-width="0.5"/>')

    # Titlebar centered slug
    parts.append(
        f'<text x="{CARD_W / 2}" y="{TITLEBAR_H / 2 + 4}" fill="{MUTED}" font-size="11.5" '
        f'font-weight="500" text-anchor="middle">~/{html.escape(p["slug"])}</text>'
    )

    # Top-right LIVE status badge
    badge_w = 62
    badge_h = 18
    badge_x = CARD_W - badge_w - 12
    badge_y = (TITLEBAR_H - badge_h) / 2
    parts.append(
        f'<rect x="{badge_x}" y="{badge_y}" width="{badge_w}" height="{badge_h}" rx="9" '
        f'fill="{GREEN_BOX}" stroke="{GREEN_STROKE}" stroke-width="0.75"/>'
    )
    parts.append(
        f'<circle class="pulse-dot" cx="{badge_x + 11}" cy="{badge_y + badge_h/2}" r="3" fill="{GREEN}"/>'
    )
    parts.append(
        f'<text x="{badge_x + 36}" y="{badge_y + badge_h/2 + 3.5}" fill="{GREEN}" font-size="10" '
        f'font-weight="700" text-anchor="middle">LIVE</text>'
    )

    # Left colored vertical accent line
    parts.append(
        f'<rect class="accent-bar" x="0.5" y="{TITLEBAR_H}" width="3.5" height="{CARD_H - TITLEBAR_H - 1}" '
        f'fill="{p["accent"]}"/>'
    )

    # Command line invocation
    cmd_y = TITLEBAR_H + 20
    parts.append(
        f'<text x="18" y="{cmd_y}" font-size="12">'
        f'<tspan fill="{MUTED}">rusdi@github:~$</tspan> '
        f'<tspan fill="{p["accent"]}">{html.escape(p["cmd"])}</tspan>'
        f'</text>'
    )
    # Cursor after command
    cmd_len = len(p["cmd"]) * 7.3
    cursor_x = 18 + 105 + cmd_len
    if cursor_x < CARD_W - 20:
        parts.append(f'<rect class="cursor" x="{cursor_x:.1f}" y="{cmd_y - 10}" width="6.5" height="13" fill="{p["accent"]}"/>')

    # Project Header: Emoji + Name
    name_y = cmd_y + 28
    parts.append(
        f'<text x="18" y="{name_y}" font-size="17" font-weight="700">'
        f'{p["icon"]} <tspan fill="{p["accent"]}">{html.escape(p["name"])}</tspan>'
        f'</text>'
    )

    # Tagline
    tagline_y = name_y + 19
    parts.append(
        f'<text x="18" y="{tagline_y}" fill="{TEXT_MAIN}" font-size="12" font-weight="600">'
        f'{html.escape(p["tagline"])}'
        f'</text>'
    )

    # Description
    desc_y = tagline_y + 17
    parts.append(
        f'<text x="18" y="{desc_y}" fill="{TEXT_DIM}" font-size="11">'
        f'{html.escape(p["desc"])}'
        f'</text>'
    )

    # Tech stack pill badges
    pills_y = desc_y + 14
    curr_x = 18
    for tag in p["tags"]:
        tag_w = len(tag) * 6.5 + 14
        if curr_x + tag_w < CARD_W - 14:
            parts.append(
                f'<rect x="{curr_x:.1f}" y="{pills_y}" width="{tag_w:.1f}" height="19" rx="4" '
                f'fill="{PILL_BG}" stroke="{STROKE}" stroke-width="0.75"/>'
            )
            parts.append(
                f'<text x="{curr_x + tag_w / 2:.1f}" y="{pills_y + 13}" fill="{MUTED}" '
                f'font-size="10" font-weight="500" text-anchor="middle">{html.escape(tag)}</text>'
            )
            curr_x += tag_w + 6

    # Bottom bar separator
    bot_sep_y = CARD_H - 30
    parts.append(
        f'<line x1="16" y1="{bot_sep_y}" x2="{CARD_W - 16}" y2="{bot_sep_y}" '
        f'stroke="{STROKE}" stroke-width="0.8" stroke-dasharray="3,3"/>'
    )

    # Bottom link row
    link_y = bot_sep_y + 18
    parts.append(
        f'<text x="18" y="{link_y}" fill="{MUTED}" font-size="10.5">'
        f'github.com/<tspan fill="{CYAN}">{html.escape(p["repo"])}</tspan>'
        f'</text>'
    )
    parts.append(
        f'<text x="{CARD_W - 18}" y="{link_y}" fill="{GREEN}" font-size="10.5" font-weight="700" text-anchor="end">'
        f'OPEN REPO ↗'
        f'</text>'
    )

    # Flowing light sweep beam
    parts.append(f'<g clip-path="url(#windowClip)">')
    parts.append(
        f'<rect class="sweep-beam" x="0" y="0" width="220" height="{CARD_H}" fill="url(#sweepGrad)"/>'
    )
    parts.append(f'</g>')

    parts.append(f'</a>')
    parts.append(f'</svg>')
    return "".join(parts)


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    generated = []

    for p in PROJECTS:
        out_file = os.path.join(DIST_DIR, p["filename"])
        svg_content = render_single_card(p)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(svg_content)
        generated.append(p["filename"])
        print(f"Wrote {out_file}: {CARD_W} x {CARD_H}, {len(svg_content)//1024} KB")

    # Also update master featured.svg (if requested as fallback or single file)
    master_path = os.path.join(DIST_DIR, "featured.svg")
    # For master, we point it to the first project or keep a concise banner
    with open(os.path.join(DIST_DIR, PROJECTS[0]["filename"]), "r", encoding="utf-8") as f:
        master_content = f.read()
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_content)
    print(f"Synced master fallback {master_path}")


if __name__ == "__main__":
    main()
