#!/usr/bin/env python3
"""
Render Developer Identity & System Telemetry SVG (sys-info.svg)
Styled in Rusdi's signature portfolio aesthetic (mangrusdi.my.id):
- Deep dark canvas (#0a0a0a) with refined surface cards (#141414)
- Warm taupe accents (#b38b6d / #d4a373)
- Embedded crisp avatar thumbnail (clean, lightweight base64)
- Neofetch-style system architecture specs (Linux, Network, Backend)
- Feather-light CSS blinking prompt cursor (0 lag, 0 CPU overhead)
Canvas size: 840 x 316 (matches stats.svg exactly).
"""
import base64
import html
import io
import json
import os
import sys

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

HERE = os.path.dirname(os.path.abspath(__file__))
AVATAR_PATH = os.path.join(HERE, "..", "data", "avatar.png")
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "sys-info.svg")

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


def get_avatar_base64():
    if not HAS_PIL or not os.path.exists(AVATAR_PATH):
        return None
    try:
        im = Image.open(AVATAR_PATH)
        im = im.convert("RGB")
        im = im.resize((96, 96), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=85, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Warning: could not process avatar image: {e}", file=sys.stderr)
        return None


def render_svg():
    avatar_b64 = get_avatar_base64()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
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
        .cursor-blink {
            animation: cursorBlink 1.1s steps(2, start) infinite;
        }
        @keyframes cursorBlink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        @media (prefers-reduced-motion: reduce) {
            .pulse-dot { animation: none !important; opacity: 1 !important; }
            .cursor-blink { animation: none !important; opacity: 1 !important; }
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
        f'rusdi@server:~$ neofetch --system-specs</text>'
    )

    # Status indicator on right
    status_x = W - PAD - 80
    parts.append(
        f'<g transform="translate({status_x}, {TITLEBAR_H / 2 - 8})">'
        f'<circle cx="8" cy="8" r="4" fill="{GREEN_LIVE}" class="pulse-dot" transform-origin="8 8"/>'
        f'<text x="18" y="11.5" fill="{TEXT_MUTED}" font-size="10.5" font-weight="600" letter-spacing="0.6">ONLINE</text>'
        f'</g>'
    )

    body_top = TITLEBAR_H + 14
    body_h = H - body_top - 14

    # Left Card: Identity & Profile (Width: 260)
    left_w = 260
    left_x = PAD
    parts.append(
        f'<g>'
        f'<rect x="{left_x}" y="{body_top}" width="{left_w}" height="{body_h}" rx="4" '
        f'fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # Avatar area
    av_size = 72
    av_x = left_x + (left_w - av_size) / 2
    av_y = body_top + 18

    # Avatar clip path & image
    parts.append(
        f'<defs>'
        f'<clipPath id="avatar-clip">'
        f'<rect x="{av_x}" y="{av_y}" width="{av_size}" height="{av_size}" rx="36"/>'
        f'</clipPath>'
        f'</defs>'
    )

    if avatar_b64:
        parts.append(
            f'<image xlink:href="{avatar_b64}" x="{av_x}" y="{av_y}" width="{av_size}" height="{av_size}" '
            f'clip-path="url(#avatar-clip)"/>'
        )
    else:
        # Fallback monogram
        parts.append(
            f'<rect x="{av_x}" y="{av_y}" width="{av_size}" height="{av_size}" rx="36" fill="{SURFACE_RAISED}"/>'
            f'<text x="{av_x + av_size/2}" y="{av_y + av_size/2 + 7}" fill="{TAUPE}" font-size="24" '
            f'font-weight="700" text-anchor="middle">RI</text>'
        )

    # Avatar ring border
    parts.append(
        f'<circle cx="{av_x + av_size/2}" cy="{av_y + av_size/2}" r="{av_size/2}" '
        f'fill="none" stroke="{TAUPE}" stroke-width="1.5"/>'
    )

    # Profile Text in Left Card
    text_center_x = left_x + left_w / 2
    parts.append(
        f'<text x="{text_center_x}" y="{av_y + av_size + 24}" fill="{TEXT_PRIMARY}" font-size="14.5" '
        f'font-weight="700" text-anchor="middle">Nuruddin Rusydi Ilham</text>'
        f'<text x="{text_center_x}" y="{av_y + av_size + 42}" fill="{TAUPE}" font-size="11.5" '
        f'font-weight="600" text-anchor="middle">Backend &amp; Network Engineer</text>'
        f'<text x="{text_center_x}" y="{av_y + av_size + 60}" fill="{TEXT_MUTED}" font-size="10.5" '
        f'text-anchor="middle">📍 Tuban, Jawa Timur, Indonesia</text>'
    )

    # Availability Badge
    badge_w = 216
    badge_h = 26
    badge_x = left_x + (left_w - badge_w) / 2
    badge_y = body_top + body_h - 38
    parts.append(
        f'<rect x="{badge_x}" y="{badge_y}" width="{badge_w}" height="{badge_h}" rx="3" '
        f'fill="{SURFACE_RAISED}" stroke="{BORDER}" stroke-width="1"/>'
        f'<circle cx="{badge_x + 12}" cy="{badge_y + badge_h/2}" r="3.5" fill="{GREEN_LIVE}"/>'
        f'<text x="{badge_x + 22}" y="{badge_y + badge_h/2 + 3.5}" fill="{TEXT_PRIMARY}" font-size="9.5" '
        f'font-weight="600">Available for Backend / DevOps</text>'
        f'</g>'
    )

    # Right Card: System Architecture Specs (Width: 528)
    right_x = left_x + left_w + 12
    right_w = W - PAD - right_x
    parts.append(
        f'<g>'
        f'<rect x="{right_x}" y="{body_top}" width="{right_w}" height="{body_h}" rx="4" '
        f'fill="{SURFACE}" stroke="{BORDER}" stroke-width="1"/>'
        f'<text x="{right_x + 18}" y="{body_top + 24}" fill="{TEXT_SUBTLE}" font-size="9.5" '
        f'font-weight="600" letter-spacing="0.8">INFRASTRUCTURE &amp; STACK SPECIFICATIONS</text>'
    )

    streak_days = 1022
    contrib_path = os.path.join(HERE, "..", "data", "contributions.json")
    if os.path.exists(contrib_path):
        try:
            with open(contrib_path, "r", encoding="utf-8") as f:
                cdata = json.load(f)
                streak_days = cdata.get("current_streak", {}).get("length", 1022)
        except Exception:
            pass

    specs = [
        ("OS", "Debian GNU/Linux 12 (Bookworm) · MikroTik RouterOS"),
        ("Host", "Production Edge Node · Tuban, East Java (ID)"),
        ("Uptime", f"{streak_days:,} days unbroken engineering cadence"),
        ("Core Stack", "Go (Golang) · Laravel 12 · Python · Node.js"),
        ("Storage", "PostgreSQL · MySQL · Redis · SQLite (ACID)"),
        ("Networking", "Nginx Reverse Proxy · Docker · WireGuard · AdGuard DNS"),
        ("Philosophy", "Zero-Bloat · Low Latency · Explicit Protocols"),
    ]

    start_y = body_top + 48
    row_gap = 21

    for idx, (label, val) in enumerate(specs):
        sy = start_y + idx * row_gap
        parts.append(
            f'<text x="{right_x + 18}" y="{sy}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11">'
            f'<tspan fill="{TAUPE}" font-weight="600">{html.escape(label):<11}</tspan>'
            f'<tspan fill="{TEXT_SUBTLE}"> : </tspan>'
            f'<tspan fill="{TEXT_PRIMARY}">{html.escape(val)}</tspan>'
            f'</text>'
        )

    # Bottom Terminal Prompt with blinking cursor
    prompt_y = body_top + body_h - 18
    parts.append(
        f'<line x1="{right_x}" y1="{prompt_y - 18}" x2="{right_x + right_w}" y2="{prompt_y - 18}" stroke="{BORDER}" stroke-width="1"/>'
        f'<text x="{right_x + 18}" y="{prompt_y}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11">'
        f'<tspan fill="{TAUPE}">rusdi@node01:~$</tspan> '
        f'<tspan fill="{TEXT_MUTED}">ready for production deployment</tspan>'
        f'</text>'
        f'<rect x="{right_x + 368}" y="{prompt_y - 10}" width="7" height="13" fill="{TAUPE}" class="cursor-blink"/>'
        f'</g>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg = render_svg()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Rendered {OUT_PATH}: {W}x{H}, size={len(svg)} bytes")


if __name__ == "__main__":
    main()
