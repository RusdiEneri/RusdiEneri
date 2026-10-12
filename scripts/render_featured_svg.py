#!/usr/bin/env python3
"""
Generate minimalist, high-fidelity SVG cards for featured repositories.
Styled in Rusdi's signature portfolio aesthetic (mangrusdi.my.id):
- Neo-card surface (#141414) on dark canvas (#0a0a0a) with crisp borders (#262626)
- Warm taupe accents (#b38b6d) and clean tech tags
- Subtle GPU-accelerated breathing pulse (0 CPU lag, no heavy beam translation)
- Directly clickable to repositories
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(HERE, "..", "dist")

CARD_W = 420
CARD_H = 126

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

PROJECTS = [
    {
        "key": "wa-full-pfp",
        "filename": "featured-wa-full-pfp.svg",
        "name": "wa-full-pfp",
        "badge": "PROTOCOL UTILITY",
        "desc": "Full-resolution WhatsApp profile picture without crop via binary protobuf.",
        "tags": ["Go", "whatsmeow", "WebSockets"],
        "accent": TAUPE,
        "url": "https://github.com/RusdiEneri/wa-full-pfp",
    },
    {
        "key": "jt-scheduling",
        "filename": "featured-jt-scheduling.svg",
        "name": "J&T Express Shift Optimizer",
        "badge": "HEURISTIC SEARCH",
        "desc": "Automated courier schedule optimization via custom Genetic Algorithm.",
        "tags": ["Python", "Streamlit", "NumPy"],
        "accent": TAUPE_LIGHT,
        "url": "https://github.com/RusdiEneri/jt-express-scheduling",
    },
    {
        "key": "cuanin",
        "filename": "featured-cuanin.svg",
        "name": "Cuanin",
        "badge": "RELATIONAL COMMERCE",
        "desc": "Preloved marketplace with ACID transaction locking & price bargaining.",
        "tags": ["Laravel 12", "MySQL", "Tailwind CSS"],
        "accent": TAUPE,
        "url": "https://github.com/RusdiEneri/Cuanin",
    },
    {
        "key": "mahasigmind",
        "filename": "featured-mahasigmind.svg",
        "name": "MahasigMind",
        "badge": "MENTAL HEALTH SPA",
        "desc": "Single Page Application for student consultations & reflective tracking.",
        "tags": ["Laravel 11", "React 19", "Inertia.js"],
        "accent": TAUPE_LIGHT,
        "url": "https://github.com/RusdiEneri/MahasigMind",
    },
    {
        "key": "alam-makmur",
        "filename": "featured-alam-makmur.svg",
        "name": "Alam Makmur Jaya",
        "badge": "CENTRALIZED ERP",
        "desc": "Enterprise retail backend for multi-branch inventory & sales accounting.",
        "tags": ["Express.js", "Node.js", "REST API"],
        "accent": TAUPE,
        "url": "https://github.com/RusdiEneri/alam-makmur-jaya",
    },
]


def render_card(p):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" '
        f'font-family="\'Space Grotesk\', ui-monospace, SFMono-Regular, -apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif">',
        "<style>",
        """
        .card-bg {
            transition: stroke 0.2s ease, fill 0.2s ease;
        }
        .card-bg:hover {
            stroke: #404040;
            fill: #171717;
        }
        .pulse-dot {
            animation: pulseDot 2.4s ease-in-out infinite;
        }
        @keyframes pulseDot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        @media (prefers-reduced-motion: reduce) {
            .pulse-dot { animation: none !important; opacity: 1 !important; }
        }
        """,
        "</style>",
        # Clickable Link
        f'<a xlink:href="{p["url"]}" target="_blank" style="text-decoration:none; cursor:pointer;">',
        # Background card
        f'<rect class="card-bg" width="{CARD_W}" height="{CARD_H}" rx="4" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>',
        # Subtle top accent border line
        f'<line x1="0" y1="0" x2="{CARD_W}" y2="0" stroke="{p["accent"]}" stroke-width="2"/>',
        # Category Badge
        f'<text x="18" y="24" fill="{p["accent"]}" font-size="9" font-weight="700" letter-spacing="0.8">'
        f'{html.escape(p["badge"])}</text>',
        # Live status dot
        f'<circle cx="{CARD_W - 24}" cy="20" r="3.5" fill="{p["accent"]}" class="pulse-dot"/>',
        # Project Title + Arrow
        f'<text x="18" y="47" fill="{TEXT_PRIMARY}" font-size="14.5" font-weight="700">'
        f'{html.escape(p["name"])} '
        f'<tspan fill="{TEXT_SUBTLE}" font-size="12">↗</tspan></text>',
        # Description
        f'<text x="18" y="68" fill="{TEXT_MUTED}" font-size="10.5" font-weight="400">'
        f'{html.escape(p["desc"])}</text>',
    ]

    # Tags along bottom
    tag_x = 18
    tag_y = 90
    tag_h = 20

    for tag in p["tags"]:
        # Estimate width roughly based on characters
        tag_w = max(38, len(tag) * 6.5 + 14)
        parts.append(
            f'<g transform="translate({tag_x}, {tag_y})">'
            f'<rect width="{tag_w:.1f}" height="{tag_h}" rx="2" fill="{SURFACE_RAISED}" stroke="{BORDER}" stroke-width="1"/>'
            f'<text x="{tag_w/2:.1f}" y="13.5" fill="{TEXT_PRIMARY}" font-size="9.5" font-weight="500" text-anchor="middle">'
            f'{html.escape(tag)}</text>'
            f'</g>'
        )
        tag_x += tag_w + 6

    parts.append("</a>")
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    for p in PROJECTS:
        svg = render_card(p)
        out_path = os.path.join(DIST_DIR, p["filename"])
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Rendered {out_path} ({len(svg)} bytes)")

    # Also write dist/featured.svg as default flagship card
    flagship = render_card(PROJECTS[0])
    master_path = os.path.join(DIST_DIR, "featured.svg")
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(flagship)
    print(f"Rendered master {master_path}")


if __name__ == "__main__":
    main()
