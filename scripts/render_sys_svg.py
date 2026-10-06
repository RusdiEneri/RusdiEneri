#!/usr/bin/env python3
"""
Render a terminal system info & HR candidate sheet card (sys-info.svg).
Canvas size: 840 x 880 (matches stats.svg exactly for flawless side-by-side alignment).
Highlights core competencies, production discipline, and hire status for HR / tech leads.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "sys-info.svg")

BG = "#0d1117"
BG2 = "#111722"
TILE = "#161b22"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
GREEN = "#39d353"
CYAN = "#58a6ff"
YELLOW = "#f0883e"
PURPLE = "#bc8cff"

W, H = 840, 880
PAD = 20
TITLEBAR_H = 34

ASCII_CAT = [
    r"     /\_____/\     ",
    r"    /  o   o  \    ",
    r"   ( ==  ^  == )   ",
    r"    )         (    ",
    r"   (           )   ",
    r"  ( (  )   (  ) )  ",
    r" (__(__)___(__)__) "
]

SPECS = [
    ("Candidate", "Nuruddin Rusydi Ilham", INK),
    ("Role Target", "Backend & Network Engineer", PURPLE),
    ("Hiring Status", "🟢 Available for Full-Time / Remote", GREEN),
    ("Engineering Cadence", "1,016+ Days Continuous Production", YELLOW),
    ("Core Architecture", "Scalable REST APIs · Microservices", CYAN),
    ("Primary Languages", "PHP (Laravel) · Go · Python · TS", GREEN),
    ("Database & Storage", "MySQL · Redis · Schema Optimization", INK),
    ("Infrastructure", "Docker · Linux SysAdmin · Nginx", YELLOW),
    ("Network Security", "iptables · OpenWRT · Wireshark · WireGuard", CYAN),
    ("Commit Integrity", "Cryptographic SSH Keypair Signing", GREEN),
]


def render():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>',
        '@keyframes fadeIn{0%{opacity:0;transform:translateY(12px)}100%{opacity:1;transform:translateY(0)}}',
        '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}',
        '.panel{opacity:0;animation:fadeIn 0.5s ease-out both}',
        '.cursor{animation:blink 1.1s infinite}',
        '@media (prefers-reduced-motion: reduce){.panel{opacity:1!important;transform:none!important;animation:none!important}}',
        '</style>',
        '<defs>',
        f'<linearGradient id="sysbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#sysbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    # Mac dots
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i * 18}" cy="{TITLEBAR_H / 2}" r="5.5" fill="{dot}"/>')

    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4.5}" fill="{MUTED}" font-size="12.5" '
        f'text-anchor="middle">rusdi@github: ~$ whoami --candidate-dossier</text>'
    )

    # Top Hero Box (ASCII Avatar + Fastfetch Header)
    hero_y = TITLEBAR_H + PAD + 4
    hero_h = 246
    hero_w = W - PAD * 2
    parts.append(f'<g class="panel" style="animation-delay:0.1s">')
    parts.append(
        f'<rect x="{PAD}" y="{hero_y}" width="{hero_w}" height="{hero_h}" rx="10" '
        f'fill="{TILE}" stroke="{FRAME}"/>'
    )

    # ASCII Cat Avatar on left
    ascii_x = PAD + 28
    ascii_start_y = hero_y + 44
    for i, line in enumerate(ASCII_CAT):
        parts.append(
            f'<text x="{ascii_x}" y="{ascii_start_y + i * 26}" fill="{CYAN}" font-size="18" '
            f'font-weight="700">{html.escape(line)}</text>'
        )

    # Candidate Dossier Header on right
    header_x = PAD + 270
    parts.append(f'<text x="{header_x}" y="{hero_y + 42}" fill="{GREEN}" font-size="24" font-weight="700">rusdi@production-lab</text>')
    parts.append(f'<text x="{header_x}" y="{hero_y + 68}" fill="{FRAME}" font-size="16">---------------------------------------------</text>')
    parts.append(f'<text x="{header_x}" y="{hero_y + 98}" fill="{MUTED}" font-size="16.5">Specialization: <tspan fill="{INK}" font-weight="600">Backend &amp; Network Infrastructure</tspan></text>')
    parts.append(f'<text x="{header_x}" y="{hero_y + 128}" fill="{MUTED}" font-size="16.5">Location: <tspan fill="{INK}">Tuban, Indonesia (UTC+7 · Remote-Ready)</tspan></text>')
    parts.append(f'<text x="{header_x}" y="{hero_y + 158}" fill="{MUTED}" font-size="16.5">HR Status: <tspan fill="{GREEN}" font-weight="700">🟢 Open for Full-Time &amp; Contracts</tspan></text>')
    parts.append(f'<text x="{header_x}" y="{hero_y + 188}" fill="{MUTED}" font-size="16.5">Consistency: <tspan fill="{YELLOW}">🔥 1,016+ Days Unbroken Work Ethic</tspan></text>')
    parts.append(f'<text x="{header_x}" y="{hero_y + 218}" fill="{MUTED}" font-size="16.5">Core Focus: <tspan fill="{PURPLE}">Building High-Throughput &amp; Secure Systems</tspan></text>')
    parts.append('</g>')

    # Middle Spec Panel (HR Tech Checklist)
    specs_y = hero_y + hero_h + 16
    specs_h = 360
    parts.append(f'<g class="panel" style="animation-delay:0.25s">')
    parts.append(
        f'<rect x="{PAD}" y="{specs_y}" width="{hero_w}" height="{specs_h}" rx="10" '
        f'fill="{TILE}" stroke="{FRAME}"/>'
    )
    parts.append(f'<text x="{PAD + 24}" y="{specs_y + 36}" fill="{MUTED}" font-size="18">$ cat /etc/candidate/competencies.conf</text>')

    spec_start_y = specs_y + 70
    col_w = (hero_w - 48) / 2
    for i, (k, v, color) in enumerate(SPECS):
        col = i // 5
        row = i % 5
        x_pos = PAD + 24 + col * col_w
        y_pos = spec_start_y + row * 56

        parts.append(
            f'<text x="{x_pos}" y="{y_pos}" fill="{MUTED}" font-size="15.5">● {html.escape(k)}:</text>'
        )
        parts.append(
            f'<text x="{x_pos}" y="{y_pos + 22}" fill="{color}" font-size="16.5" font-weight="600">{html.escape(v)}</text>'
        )
    parts.append('</g>')

    # Bottom Terminal Prompt Box (HR Match & Action)
    bot_y = specs_y + specs_h + 16
    bot_h = H - PAD - bot_y
    parts.append(f'<g class="panel" style="animation-delay:0.4s">')
    parts.append(
        f'<rect x="{PAD}" y="{bot_y}" width="{hero_w}" height="{bot_h}" rx="10" '
        f'fill="{TILE}" stroke="{FRAME}"/>'
    )
    parts.append(
        f'<text x="{PAD + 24}" y="{bot_y + 36}" fill="{MUTED}" font-size="16.5">'
        f'rusdi@production:~$ <tspan fill="{CYAN}">./evaluate-candidate.sh --verdict</tspan></text>'
    )
    parts.append(
        f'<text x="{PAD + 24}" y="{bot_y + 66}" fill="{GREEN}" font-size="16">'
        f'[HR MATCH 100%]: Backend Architecture + Network Ops + Relentless Discipline</text>'
    )
    parts.append(
        f'<text x="{PAD + 24}" y="{bot_y + 98}" fill="{MUTED}" font-size="16.5">'
        f'rusdi@production:~$ <tspan fill="{INK}">contact --mailto rusdieneri@gmail.com</tspan></text>'
    )
    # Blinking cursor after command
    cursor_x = PAD + 24 + 460
    parts.append(
        f'<rect class="cursor" x="{cursor_x}" y="{bot_y + 83}" width="10" height="18" fill="{GREEN}"/>'
    )
    parts.append('</g>')

    parts.append('</svg>')
    return "".join(parts)


def main():
    svg = render()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT}: {W} x {H}")


if __name__ == "__main__":
    main()
