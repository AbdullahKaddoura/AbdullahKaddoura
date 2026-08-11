"""Apply one pixel placement requested through a GitHub issue.

Everything untrusted (issue title, actor login) arrives via environment
variables — never interpolated into the workflow's shell — so a title like
`place 1,1 red"; rm -rf /` is just a string that fails to parse.

Writes `status` and `message` to $GITHUB_OUTPUT for the workflow to act on.
"""

from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime, timezone

from canvas import (
    COOLDOWN_SECONDS,
    HEIGHT,
    PALETTE,
    WIDTH,
    load_state,
    render_all,
    save_state,
)

# "place 3,7 red" — tolerant about spacing, case and an optional colon.
PATTERN = re.compile(
    r"^\s*place\s*:?\s*(\d{1,3})\s*,\s*(\d{1,3})\s+([a-z]+)\s*$",
    re.IGNORECASE,
)


def emit(status: str, message: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"status={status}\n")
            # Multi-line safe delimiter form.
            fh.write(f"message<<CANVAS_EOF\n{message}\nCANVAS_EOF\n")
    print(f"[{status}] {message}")


def fail(message: str) -> None:
    emit("error", message)
    sys.exit(0)  # handled, not a workflow failure


def main() -> None:
    title = os.environ.get("ISSUE_TITLE", "")
    actor = os.environ.get("ISSUE_ACTOR", "")

    if not actor:
        fail("Could not determine who opened this issue.")

    match = PATTERN.match(title)
    if not match:
        fail(
            "I couldn't read that title. It needs to look like `place 3,7 red` — "
            "click a pixel on the canvas and submit the issue it pre-fills for you."
        )

    x, y, color = int(match.group(1)), int(match.group(2)), match.group(3).lower()

    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        fail(
            f"`{x},{y}` is off the canvas. Valid coordinates are "
            f"`0,0` to `{WIDTH - 1},{HEIGHT - 1}`."
        )

    if color not in PALETTE:
        fail(
            f"`{color}` isn't in the palette. Pick one of: "
            + ", ".join(f"`{c}`" for c in PALETTE)
            + "."
        )

    state = load_state()

    now = time.time()
    last = state["last_placed_at"].get(actor)
    if last is not None:
        waited = now - float(last)
        if waited < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - waited) + 1
            fail(
                f"Easy — one pixel every {COOLDOWN_SECONDS} seconds. "
                f"Try again in {remaining}s."
            )

    state["pixels"][f"{x},{y}"] = {
        "color": color,
        "by": actor,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    state["placements"] += 1
    state["last_placed_at"][actor] = now

    # Keep contributors unique but ordered by most recent placement.
    if actor in state["contributors"]:
        state["contributors"].remove(actor)
    state["contributors"].append(actor)

    save_state(state)
    render_all(state)

    emit(
        "ok",
        f"Painted **{x},{y}** {color}. That's placement #{state['placements']} — "
        "thanks for adding to it.",
    )


if __name__ == "__main__":
    main()
