"""Crystal Badge Generator.

Emits a shields.io-compatible badge as SVG, JSON, or markdown snippet.
Drop-in for project READMEs: shows grade (A–F) and score (0–100),
linking back to crystalcodes.dev. Classic open-source growth hack.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


# Grade → colour (hex, works in shields.io custom badges)
GRADE_COLORS = {
    "A": "#2ecc71",   # green
    "B": "#9ccc65",   # light green
    "C": "#f1c40f",   # yellow
    "D": "#e67e22",   # orange
    "F": "#e74c3c",   # red
}


@dataclass
class BadgeSpec:
    label: str
    message: str
    color: str
    link: str = "https://crystalcodes.dev"


def build_spec(grade: str, score: int) -> BadgeSpec:
    color = GRADE_COLORS.get(grade, "#95a5a6")
    return BadgeSpec(
        label="crystal",
        message=f"{grade} {score}/100",
        color=color,
    )


def to_shields_json(spec: BadgeSpec) -> str:
    """shields.io dynamic endpoint format.

    Host this JSON anywhere; reference it via:
        https://img.shields.io/endpoint?url=<your-json-url>
    """
    return json.dumps({
        "schemaVersion": 1,
        "label": spec.label,
        "message": spec.message,
        "color": spec.color,
        "labelColor": "#2c3e50",
        "namedLogo": "gemstone",
    }, indent=2)


def to_shields_url(spec: BadgeSpec) -> str:
    """shields.io static badge URL (no hosting required)."""
    msg = spec.message.replace("-", "--").replace(" ", "%20").replace("/", "%2F")
    return f"https://img.shields.io/badge/{spec.label}-{msg}-{spec.color.lstrip('#')}"


def to_markdown(spec: BadgeSpec) -> str:
    """Markdown snippet ready to paste into a README."""
    return f"[![Crystal {spec.message}]({to_shields_url(spec)})]({spec.link})"


def to_svg(spec: BadgeSpec) -> str:
    """Minimal self-contained SVG (no external fetch).

    ~roughly matches shields.io visual style but renders offline.
    """
    label = spec.label
    msg = spec.message
    # Approximate width: 6.2px/char + padding
    label_w = max(len(label) * 7 + 10, 50)
    msg_w = max(len(msg) * 7 + 10, 50)
    total_w = label_w + msg_w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20" role="img" aria-label="{label}: {msg}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total_w}" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_w}" height="20" fill="#2c3e50"/>
    <rect x="{label_w}" width="{msg_w}" height="20" fill="{spec.color}"/>
    <rect width="{total_w}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{label_w / 2:.0f}" y="14">{label}</text>
    <text x="{label_w + msg_w / 2:.0f}" y="14">{msg}</text>
  </g>
</svg>'''
