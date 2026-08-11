"""Shared state and rendering for the README canvas.

The canvas is a small grid of pixels that anyone on GitHub can paint by opening
an issue. This module owns three things:

  * the palette and grid geometry
  * loading / saving the JSON state
  * rendering that state into the swatch files, an SVG, and the README block

No third-party dependencies — this runs on a bare `python:3` in Actions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "canvas" / "state.json"
SWATCH_DIR = ROOT / "assets" / "px"
SVG_PATH = ROOT / "assets" / "canvas.svg"
README_PATH = ROOT / "README.md"

REPO = os.environ.get("GITHUB_REPOSITORY", "AbdullahKaddoura/AbdullahKaddoura")

WIDTH = 20
HEIGHT = 12
CELL = 20  # rendered px per cell in the README grid

# Palette. Keys are what a user types in an issue title; values are hex.
PALETTE = {
    # "empty" is the unpainted default: a neutral slate that recedes in both
    # GitHub themes. White as a *default* reads as a bright slab in dark mode.
    "empty": "#7d8590",
    "white": "#ffffff",
    "black": "#1b1f23",
    "red": "#e5484d",
    "orange": "#f76b15",
    "yellow": "#ffc53d",
    "green": "#30a46c",
    "blue": "#3e63dd",
    "purple": "#8e4ec6",
}
DEFAULT_COLOR = "empty"

# How long a single user must wait between placements.
COOLDOWN_SECONDS = 30

START_MARKER = "<!-- CANVAS:START -->"
END_MARKER = "<!-- CANVAS:END -->"


# --------------------------------------------------------------------------- state


def blank_state() -> dict:
    return {
        "width": WIDTH,
        "height": HEIGHT,
        "pixels": {},        # "x,y" -> {"color": str, "by": str, "at": iso8601}
        "placements": 0,
        "contributors": [],  # unique logins, most recent last
        "last_placed_at": {},  # login -> unix seconds
    }


def load_state() -> dict:
    if not STATE_PATH.exists():
        return blank_state()
    with STATE_PATH.open(encoding="utf-8") as fh:
        state = json.load(fh)
    # Tolerate older/partial files so a hand-edit can't wedge the workflow.
    base = blank_state()
    base.update(state)
    return base


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STATE_PATH.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
        fh.write("\n")


def color_at(state: dict, x: int, y: int) -> str:
    pixel = state["pixels"].get(f"{x},{y}")
    return pixel["color"] if pixel else DEFAULT_COLOR


# ------------------------------------------------------------------------ rendering


def write_swatches() -> None:
    """One tiny SVG per colour, used as the <img> for every cell."""
    SWATCH_DIR.mkdir(parents=True, exist_ok=True)
    for name, hex_code in PALETTE.items():
        stroke = "#d8dee4" if name == "white" else "rgba(0,0,0,0.18)"
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">'
            f'<rect width="20" height="20" rx="3" fill="{hex_code}" '
            f'stroke="{stroke}" stroke-width="1"/>'
            "</svg>"
        )
        (SWATCH_DIR / f"{name}.svg").write_text(svg, encoding="utf-8")


def render_svg(state: dict) -> str:
    """A single contiguous image of the canvas — no gaps, good for sharing."""
    pad, cell = 8, 22
    w = WIDTH * cell + pad * 2
    h = HEIGHT * cell + pad * 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="Community pixel canvas">',
        f'<rect width="{w}" height="{h}" rx="10" fill="#0d1117"/>',
    ]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            fill = PALETTE[color_at(state, x, y)]
            parts.append(
                f'<rect x="{pad + x * cell}" y="{pad + y * cell}" '
                f'width="{cell - 2}" height="{cell - 2}" rx="3" fill="{fill}"/>'
            )
    parts.append("</svg>")
    return "".join(parts)


def issue_url(x: int, y: int) -> str:
    # Deliberately no `&body=` — it would be repeated once per cell and bloat
    # the README by ~80KB. The instructions live in the rendered block instead.
    return f"https://github.com/{REPO}/issues/new?title=place%20{x},{y}%20red"


def render_grid(state: dict) -> str:
    """The clickable canvas: rows of <img> links, no whitespace between cells."""
    lines = []
    for y in range(HEIGHT):
        row = "".join(
            f'<a href="{issue_url(x, y)}" title="{x},{y}">'
            f'<img src="assets/px/{color_at(state, x, y)}.svg" '
            f'width="{CELL}" height="{CELL}" alt=""></a>'
            for x in range(WIDTH)
        )
        lines.append(row)
    return "<br>".join(lines)


def render_block(state: dict) -> str:
    people = len(state["contributors"])
    placements = state["placements"]
    swatches = " ".join(
        f'<img src="assets/px/{name}.svg" width="14" height="14" alt="{name}"> `{name}`'
        for name in PALETTE
    )
    recent = ""
    if state["contributors"]:
        tail = list(reversed(state["contributors"][-8:]))
        recent = (
            "\n<sub>Most recent painters: "
            + " · ".join(f"[@{login}](https://github.com/{login})" for login in tail)
            + "</sub>\n"
        )

    return f"""{START_MARKER}
## The Canvas

**Click any pixel to paint it.** That opens a pre-filled issue — submit it and a
GitHub Action paints your pixel, redraws this grid and closes the issue. No account
setup, no fork, nothing to install. Everyone shares one canvas.

<p align="center">
{render_grid(state)}
</p>

<p align="center">
{swatches}
</p>

<p align="center">
<strong>{placements}</strong> pixels placed by <strong>{people}</strong> {"person" if people == 1 else "people"}
</p>
{recent}
<sub>Change the colour word in the issue title before submitting. One pixel every
{COOLDOWN_SECONDS} seconds per person. How it works:
[`canvas/`](canvas/) · [`.github/workflows/canvas.yml`](.github/workflows/canvas.yml)</sub>
{END_MARKER}"""


def update_readme(state: dict) -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    block = render_block(state)

    if START_MARKER in readme and END_MARKER in readme:
        head, _, rest = readme.partition(START_MARKER)
        _, _, tail = rest.partition(END_MARKER)
        readme = head + block + tail
    else:
        readme = readme.rstrip() + "\n\n---\n\n" + block + "\n"

    README_PATH.write_text(readme, encoding="utf-8")


def render_all(state: dict) -> None:
    write_swatches()
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(render_svg(state), encoding="utf-8")
    update_readme(state)


if __name__ == "__main__":
    render_all(load_state())
