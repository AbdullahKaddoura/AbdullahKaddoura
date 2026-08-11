"""Generate the animated profile header.

One source, two themes. The animation is pure CSS inside the SVG, which keeps
working when GitHub serves the file through its image proxy — no JS, no
external requests, no build step.

    python3 header.py     # writes assets/header-dark.svg and header-light.svg
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

W, H = 880, 250
LINE_Y = 178
X0, X1 = 62, 818

STAGES = ["capture", "normalise", "reason", "ship"]

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "panel": "#161b22",
        "edge": "#30363d",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "accent": "#4d8bf0",
        "accent2": "#3fb950",
    },
    "light": {
        "bg": "#ffffff",
        "panel": "#f6f8fa",
        "edge": "#d8dee4",
        "text": "#1f2328",
        "muted": "#636c76",
        "accent": "#2f6feb",
        "accent2": "#2da44e",
    },
}


def build(theme: dict) -> str:
    n = len(STAGES)
    span = X1 - X0
    xs = [X0 + round(i * span / (n - 1)) for i in range(n)]

    nodes, labels, rings = [], [], []
    for i, (x, name) in enumerate(zip(xs, STAGES)):
        delay = f"{i * 0.55:.2f}s"
        rings.append(
            f'<circle class="ring" cx="{x}" cy="{LINE_Y}" r="10" '
            f'style="animation-delay:{delay}"/>'
        )
        nodes.append(
            f'<circle class="node" cx="{x}" cy="{LINE_Y}" r="7" '
            f'style="animation-delay:{delay}"/>'
        )
        labels.append(
            f'<text class="stage" x="{x}" y="{LINE_Y + 34}" text-anchor="middle">'
            f"{name}</text>"
        )

    # Three packets, evenly offset in time, sliding the length of the track.
    packets = "".join(
        f'<circle class="packet" cx="{X0}" cy="{LINE_Y}" r="4" '
        f'style="animation-delay:{i * 1.83:.2f}s"/>'
        for i in range(3)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img"
     aria-label="Abdullah Kaddoura — AI systems, health data pipelines, Dubai">
  <style>
    .bg     {{ fill: {theme['bg']}; }}
    .name   {{ fill: {theme['text']}; font: 700 40px ui-monospace, 'SFMono-Regular',
              'JetBrains Mono', Menlo, Consolas, monospace; letter-spacing: -0.5px; }}
    .role   {{ fill: {theme['muted']}; font: 400 16px ui-monospace, 'SFMono-Regular',
              'JetBrains Mono', Menlo, Consolas, monospace; }}
    .stage  {{ fill: {theme['muted']}; font: 400 13px ui-monospace, 'SFMono-Regular',
              'JetBrains Mono', Menlo, Consolas, monospace; letter-spacing: 0.4px; }}
    .track  {{ stroke: {theme['edge']}; stroke-width: 2; }}
    .node   {{ fill: {theme['panel']}; stroke: {theme['accent']}; stroke-width: 2;
              animation: pulse 2.2s ease-in-out infinite; }}
    .ring   {{ fill: none; stroke: {theme['accent']}; stroke-width: 2;
              opacity: 0; animation: halo 2.2s ease-out infinite; }}
    .packet {{ fill: {theme['accent2']};
              animation: flow 5.5s linear infinite; }}
    .caret  {{ fill: {theme['accent2']}; animation: blink 1.1s step-end infinite; }}

    @keyframes flow {{
      0%   {{ transform: translateX(0);      opacity: 0; }}
      6%   {{ opacity: 1; }}
      94%  {{ opacity: 1; }}
      100% {{ transform: translateX({span}px); opacity: 0; }}
    }}
    @keyframes pulse {{
      0%, 100% {{ r: 7; }}
      50%      {{ r: 8.5; }}
    }}
    @keyframes halo {{
      0%   {{ r: 8;  opacity: 0.55; }}
      70%  {{ r: 20; opacity: 0; }}
      100% {{ r: 20; opacity: 0; }}
    }}
    @keyframes blink {{
      0%, 50%   {{ opacity: 1; }}
      50.01%, 100% {{ opacity: 0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .packet, .node, .ring, .caret {{ animation: none; }}
      .ring {{ opacity: 0; }}
    }}
  </style>

  <rect class="bg" width="{W}" height="{H}" rx="14"/>

  <text class="name" x="62" y="86">Abdullah Kaddoura</text>
  <rect class="caret" x="62" y="112" width="11" height="19" rx="1.5"/>
  <text class="role" x="84" y="128">AI systems · wearable health data · Dubai</text>

  <line class="track" x1="{X0}" y1="{LINE_Y}" x2="{X1}" y2="{LINE_Y}"/>
  {packets}
  {''.join(rings)}
  {''.join(nodes)}
  {''.join(labels)}
</svg>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, theme in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote assets/header-{name}.svg")


if __name__ == "__main__":
    main()
