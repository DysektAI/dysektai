#!/usr/bin/env python3
"""Generate the profile README graphics (light and dark variants).

Edit the content below, then run:  python3 assets/generate.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "panel": "#0d1117",
        "border": "#30363d",
        "grid": "#ffffff",
        "grid_opacity": 0.035,
        "title": "#f0f6fc",
        "text": "#9198a1",
        "muted": "#6e7681",
        "chip_bg": "#151b23",
        "chip_text": "#d1d7e0",
        "accent": "#ff4d4f",
    },
    "light": {
        "bg": "#ffffff",
        "panel": "#ffffff",
        "border": "#d1d9e0",
        "grid": "#1f2328",
        "grid_opacity": 0.045,
        "title": "#1f2328",
        "text": "#59636e",
        "muted": "#818b98",
        "chip_bg": "#f6f8fa",
        "chip_text": "#1f2328",
        "accent": "#d1242f",
    },
}

LANG_COLORS = {
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "C#": "#178600",
    "Python": "#3572a5",
}

# ---------------------------------------------------------------- content

HEADER = {
    "eyebrow": "DYSEKTAI",
    "location": "FLORIDA, US",
    "name": "Dys",
    "tagline": [
        "Software developer building open-source tools for the",
        "Escape from Tarkov community and developer tooling for AI coding agents.",
    ],
    "roles": [
        ("Owner", "DysektAI"),
        ("Core maintainer", "TarkovTracker"),
        ("Maintainer", "RatScanner"),
    ],
}

CARDS = [
    {
        "slug": "tarkovtracker",
        "name": "TarkovTracker",
        "tag": "OWNER · CORE MAINTAINER",
        "desc": "Quest, hideout, item, and progression tracker for Escape from Tarkov PvP and PvE, with squad sync.",
        "lang": "TypeScript",
        "tech": ["Nuxt 4", "Supabase"],
    },
    {
        "slug": "ratscanner",
        "name": "RatScanner",
        "tag": "MAINTAINER",
        "desc": "Desktop companion for Escape from Tarkov that scans in-game items and shows their details instantly.",
        "lang": "C#",
        "tech": [".NET"],
    },
    {
        "slug": "pi-lsp",
        "name": "pi-lsp",
        "tag": "AI TOOLING",
        "desc": "Managed, cross-platform language-server integration for the Pi coding agent, with first-class C#/.NET support.",
        "lang": "TypeScript",
        "tech": ["LSP", "Vitest"],
    },
    {
        "slug": "pi-extensions",
        "name": "pi-extensions",
        "tag": "AI TOOLING",
        "desc": "Extensions for the Pi coding agent: tasks, search, LSP, goal loops, and UX helpers.",
        "lang": "TypeScript",
        "tech": ["Pi"],
    },
    {
        "slug": "ai-api-monitor",
        "name": "ai-api-monitor",
        "tag": "MONITORING",
        "desc": "Zero-dependency monitor for AI API endpoints. Tracks availability, latency, and uptime across providers.",
        "lang": "JavaScript",
        "tech": ["Node.js"],
    },
    {
        "slug": "wardogs-sitrep",
        "name": "wardogs-sitrep",
        "tag": "GAMING",
        "desc": "SITREP, a companion app for WARDOGS with a built-in mortar solver.",
        "lang": "C#",
        "tech": [".NET"],
    },
]

STACK = [
    ("LANGUAGES", ["TypeScript", "JavaScript", "Python", "C#", "Bash", "Lua", "Go", "Rust"]),
    ("AI & AGENTS", ["OpenAI API", "Anthropic API", "MCP", "LSP", "vLLM"]),
    ("WEB", ["React", "Next.js", "Nuxt", "Vite", "Tailwind CSS", "Supabase"]),
    ("INFRA", ["Node.js", "Docker", "GitHub Actions", "Cloudflare", "pnpm", "Vitest"]),
]

# ---------------------------------------------------------------- text metrics

# Helvetica/Arial advance widths (per 1000 em) for printable ASCII.
_W = dict(zip(
    " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
    [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278,
     556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556,
     1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
     667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556,
     333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
     556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584],
))


def text_width(s, size, bold=False, spacing=0.0):
    w = sum(_W.get(c, 556) for c in s) * size / 1000
    if bold:
        w *= 1.08
    # System UI fonts run a little wider than Helvetica.
    return w * 1.04 + spacing * len(s)


def wrap(s, size, max_width):
    lines, line = [], ""
    for word in s.split():
        trial = f"{line} {word}".strip()
        if line and text_width(trial, size) > max_width:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    return lines


def t(x, y, s, *, size, fill, weight=400, spacing=0, anchor="start", family=FONT, opacity=None):
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
    extra += f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}"{extra}>{escape(s)}</text>')


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">\n'
            f'<title>{escape(title)}</title>\n{body}\n</svg>\n')


def grid(w, h, c, step=24):
    lines = [f'<path d="M{x} 0V{h}" />' for x in range(step, w, step)]
    lines += [f'<path d="M0 {y}H{w}" />' for y in range(step, h, step)]
    return (f'<g stroke="{c["grid"]}" stroke-opacity="{c["grid_opacity"]}" stroke-width="1">'
            + "".join(lines) + "</g>")


def corners(x, y, w, h, color, size=10, inset=0):
    x0, y0, x1, y1 = x + inset, y + inset, x + w - inset, y + h - inset
    d = (f"M{x0} {y0 + size}V{y0}H{x0 + size} "
         f"M{x1 - size} {y0}H{x1}V{y0 + size} "
         f"M{x1} {y1 - size}V{y1}H{x1 - size} "
         f"M{x0 + size} {y1}H{x0}V{y1 - size}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="0.7" stroke-width="1.5" stroke-linecap="square" />'


# ---------------------------------------------------------------- header

def header(c):
    W, H = 880, 280
    a = c["accent"]
    out = [
        f'<defs><clipPath id="clip"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" /></clipPath>'
        f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{a}" stop-opacity="0.16" />'
        f'<stop offset="1" stop-color="{a}" stop-opacity="0" /></radialGradient></defs>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}" />',
        f'<g clip-path="url(#clip)">{grid(W, H, c)}</g>',
    ]

    # Reticle, echoing the DysektAI mark.
    cx, cy = 728, 140
    out.append(f'<circle cx="{cx}" cy="{cy}" r="120" fill="url(#glow)" />')
    out.append(f'<g fill="none" stroke="{a}">'
               f'<circle cx="{cx}" cy="{cy}" r="92" stroke-opacity="0.55" stroke-width="1.5" />'
               f'<circle cx="{cx}" cy="{cy}" r="64" stroke-opacity="0.25" />'
               f'<circle cx="{cx}" cy="{cy}" r="30" stroke-opacity="0.35" stroke-dasharray="3 5" />'
               f'<path d="M{cx - 118} {cy}H{cx - 72} M{cx + 72} {cy}H{cx + 118} '
               f'M{cx} {cy - 118}V{cy - 72} M{cx} {cy + 72}V{cy + 118}" stroke-opacity="0.6" />'
               '</g>')
    for dx, dy in ((0, -92), (0, 92), (-92, 0), (92, 0)):
        x, y = cx + dx, cy + dy
        out.append(f'<path d="M{x} {y - 6}L{x + 6} {y}L{x} {y + 6}L{x - 6} {y}Z" '
                   f'fill="{c["panel"]}" stroke="{a}" stroke-width="1.25" />')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{a}" />')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{a}" stroke-opacity="0.5" />')

    # Text block.
    x = 48
    eyebrow = HEADER["eyebrow"]
    out.append(t(x, 62, eyebrow, size=12, fill=a, weight=600, spacing=3.5))
    ex = x + text_width(eyebrow, 12, True, 3.5) + 10
    out.append(f'<path d="M{ex:.1f} 58H{ex + 18:.1f}" stroke="{c["muted"]}" />')
    out.append(t(ex + 28, 62, HEADER["location"], size=12, fill=c["muted"], weight=500, spacing=3.5))

    out.append(t(x - 3, 128, HEADER["name"], size=60, fill=c["title"], weight=700, spacing=-1))
    for i, line in enumerate(HEADER["tagline"]):
        out.append(t(x, 164 + i * 24, line, size=16, fill=c["text"]))

    cx0, cy0, ch = x, 212, 30
    for role, org in HEADER["roles"]:
        label_w = text_width(role, 12.5)
        org_w = text_width(org, 12.5, True)
        w = 14 + 6 + 10 + label_w + 6 + org_w + 14
        out.append(f'<rect x="{cx0}" y="{cy0}" width="{w:.1f}" height="{ch}" rx="15" '
                   f'fill="{c["chip_bg"]}" stroke="{c["border"]}" />')
        out.append(f'<circle cx="{cx0 + 17}" cy="{cy0 + ch / 2}" r="3" fill="{a}" />')
        out.append(t(cx0 + 30, cy0 + 19.5, role, size=12.5, fill=c["text"]))
        out.append(t(cx0 + 30 + label_w + 6, cy0 + 19.5, org, size=12.5, fill=c["chip_text"], weight=600))
        cx0 += w + 10

    return svg(W, H, "\n".join(out),
               "Dys. Software developer. Owner of DysektAI, core maintainer of TarkovTracker, maintainer of RatScanner.")


# ---------------------------------------------------------------- project cards

def card(p, c):
    W, H = 430, 164
    a = c["accent"]
    out = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="{c["panel"]}" stroke="{c["border"]}" />',
        corners(0, 0, W, H, a, size=9, inset=8),
    ]
    x = 28
    out.append(t(x, 48, p["name"], size=19, fill=c["title"], weight=600))

    tag = p["tag"]
    tw = text_width(tag, 10, True, 1.6) + 20
    tx = W - 26 - tw
    out.append(f'<rect x="{tx:.1f}" y="30" width="{tw:.1f}" height="22" rx="11" fill="none" '
               f'stroke="{a}" stroke-opacity="0.55" />')
    out.append(t(tx + tw / 2 + 0.8, 45, tag, size=10, fill=a, weight=600, spacing=1.6, anchor="middle"))

    for i, line in enumerate(wrap(p["desc"], 14, W - 2 * x)[:3]):
        out.append(t(x, 80 + i * 21, line, size=14, fill=c["text"]))

    fy = H - 26
    out.append(f'<circle cx="{x + 6}" cy="{fy - 4.5}" r="6" fill="{LANG_COLORS[p["lang"]]}" />')
    lx = x + 18
    out.append(t(lx, fy, p["lang"], size=12.5, fill=c["chip_text"]))
    lx += text_width(p["lang"], 12.5)
    for tech in p["tech"]:
        out.append(t(lx + 8, fy, "·", size=12.5, fill=c["muted"]))
        out.append(t(lx + 18, fy, tech, size=12.5, fill=c["muted"]))
        lx += 18 + text_width(tech, 12.5)

    return svg(W, H, "\n".join(out), f'{p["name"]}: {p["desc"]}')


# ---------------------------------------------------------------- stack

def stack(c):
    W = 880
    row_h, top = 46, 34
    H = top * 2 + row_h * len(STACK) - 14
    a = c["accent"]
    out = [
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["panel"]}" stroke="{c["border"]}" />',
    ]
    for i, (label, items) in enumerate(STACK):
        y = top + i * row_h
        out.append(t(40, y + 20, label, size=11, fill=a, weight=600, spacing=2.4))
        x = 190
        for item in items:
            w = text_width(item, 13) + 26
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="30" rx="6" '
                       f'fill="{c["chip_bg"]}" stroke="{c["border"]}" />')
            out.append(t(x + w / 2, y + 20, item, size=13, fill=c["chip_text"], anchor="middle"))
            x += w + 8
        if i < len(STACK) - 1:
            out.append(f'<path d="M40 {y + row_h - 8}H{W - 40}" stroke="{c["border"]}" stroke-opacity="0.5" />')
    title = "Stack: " + "; ".join(f"{label.title()}: {', '.join(items)}" for label, items in STACK)
    return svg(W, H, "\n".join(out), title)


def main():
    for name, c in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(c))
        (OUT / f"stack-{name}.svg").write_text(stack(c))
        cards = OUT / "cards"
        cards.mkdir(exist_ok=True)
        for p in CARDS:
            (cards / f'{p["slug"]}-{name}.svg').write_text(card(p, c))


if __name__ == "__main__":
    main()
