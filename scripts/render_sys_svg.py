#!/usr/bin/env python3
"""
Render an animated monochrome ASCII-art portrait of Rusdi's GitHub avatar
(the explosion cat!) that "types" itself in line-by-line like a CRT terminal scanner.
Directly inspired by avivashishta29's avi-ascii.svg.

Canvas size: 840 x 880 (matches stats.svg exactly for flawless side-by-side display).
Each row reveals with a left-to-right clip wipe plus a glowing cursor riding the wipe edge,
staggered top -> bottom, finishing with a steady blinking prompt cursor at the bottom.
"""
import html
import os
import sys
import urllib.request

try:
    from PIL import Image, ImageEnhance, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

HERE = os.path.dirname(os.path.abspath(__file__))
AVATAR_PATH = os.path.join(HERE, "..", "data", "avatar.png")
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "sys-info.svg")
USERNAME = os.environ.get("GH_PROFILE_USER", "RusdiEneri")

# Target dimensions matching stats.svg (840 x 880)
CANVAS_W = 840
CANVAS_H = 880
PAD = 20
TITLEBAR_H = 34

COLS = 160
ART_W = 800.0
CELL_W = ART_W / COLS                     # 5.0 px
CELL_H = CELL_W * 15.0 / 8.0              # 9.375 px
ROWS = 84
ART_H = ROWS * CELL_H                     # 787.5 px
art_top = TITLEBAR_H + 10                 # 44.0 px

# Color palette
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#c9d1d9"                           # Crisp terminal phosphor ASCII ink
CURSOR = "#39d353"                        # Glowing matrix-green wiping cursor
GREEN = "#39d353"
CYAN = "#58a6ff"

# ASCII ramp from sparse (dark) to dense (bright)
RAMP = " .`:-=+*cs#%@"

# Reveal timing: whole portrait streams in ~5.6s
TOTAL_DUR = 5.6
ROW_DUR = TOTAL_DUR / ROWS
STAGGER = ROW_DUR


def ensure_avatar():
    os.makedirs(os.path.dirname(AVATAR_PATH), exist_ok=True)
    url = f"https://github.com/{USERNAME}.png"
    print(f"Checking & downloading latest avatar from {url}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "profile-readme-bot/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if data and len(data) > 100:
                with open(AVATAR_PATH, "wb") as f:
                    f.write(data)
                print(f"Successfully refreshed avatar from {url} ({len(data)} bytes)")
    except Exception as e:
        print(f"Warning: could not refresh avatar (using existing if available): {e}", file=sys.stderr)


def prepare_ascii_lines():
    ensure_avatar()
    if not HAS_PIL or not os.path.exists(AVATAR_PATH):
        # Fallback placeholder if PIL not available or image missing
        return [" " * COLS for _ in range(ROWS)]

    im = Image.open(AVATAR_PATH).convert("L")
    # Enhance contrast and edge definition so the cat face and explosion flames stand out
    im = ImageEnhance.Contrast(im).enhance(1.35)
    im = ImageEnhance.Brightness(im).enhance(1.08)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.8, percent=130, threshold=2))
    im = im.resize((COLS, ROWS), Image.LANCZOS)
    px = im.load()

    lines = []
    ramp_len = len(RAMP)
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            lum = px[x, y] / 255.0
            # Force deep shadows to pure space for clean background
            if lum < 0.10:
                chars.append(" ")
            else:
                idx = int(lum * (ramp_len - 1) + 0.5)
                chars.append(RAMP[max(0, min(ramp_len - 1, idx))])
        lines.append("".join(chars))

    return lines


def render_svg():
    rows_txt = prepare_ascii_lines()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
        f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        # Base window
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="14" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="14" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    # Title bar buttons (Mac dots)
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i * 18}" cy="{TITLEBAR_H / 2}" r="5.5" fill="{dot}"/>')

    parts.append(
        f'<text x="{CANVAS_W / 2}" y="{TITLEBAR_H / 2 + 4.5}" fill="{TITLE_TEXT}" font-size="12.5" '
        f'text-anchor="middle">rusdi@github: ~$ ./portrait.sh --render-ascii</text>'
    )

    # ASCII rows with left-to-right clip wipe & scanning cursor
    font_size = CELL_H * 0.88
    for ry, line in enumerate(rows_txt):
        y = art_top + ry * CELL_H + CELL_H * 0.74
        row_y = art_top + ry * CELL_H
        delay = ry * STAGGER
        safe = html.escape(line)

        text = (
            f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
            f'font-size="{font_size:.1f}" textLength="{ART_W}" lengthAdjust="spacing">{safe}</text>'
        )

        parts.append(
            f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H:.2f}" width="0">'
            f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
        parts.append(
            f'<rect y="{row_y:.1f}" width="{CELL_W}" height="{CELL_H}" fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{PAD + ART_W}" begin="{delay:.3f}s" '
            f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.9" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay + ROW_DUR:.3f}s"/>'
            f'</rect>'
        )

    # Status bar with steady blinking prompt cursor
    status_line_y = art_top + ART_H + 8
    status_y = status_line_y + 24
    parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
    parts.append(
        f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
        f'rusdi@github:~$ whoami <tspan fill="{INK}" font-weight="600">Nuruddin Rusydi Ilham</tspan> '
        f'<tspan fill="{GREEN}">· Backend &amp; Network Engineer</tspan></text>'
    )

    # Blinking block cursor after command
    status_chars = len("rusdi@github:~$ whoami Nuruddin Rusydi Ilham · Backend & Network Engineer ")
    cursor_x = PAD + status_chars * 13 * 0.58
    parts.append(
        f'<rect x="{cursor_x:.1f}" y="{status_y - 12:.1f}" width="9" height="15" fill="{GREEN}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append("</svg>")
    return "".join(parts)


def main():
    svg = render_svg()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}: {CANVAS_W} x {CANVAS_H}, {len(svg)//1024} KB")


if __name__ == "__main__":
    main()
