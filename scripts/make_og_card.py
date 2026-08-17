#!/usr/bin/env python3
"""Generate the 1200x630 social card for the root v3.2.3 paper page."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "assets" / "figure-data-polylog.json"
OUT = SITE / "assets" / "og-card.png"

W, H = 1200, 630
SCALE = 2

PAPER = (252, 251, 249)
INK = (26, 26, 28)
SOFT = (74, 74, 82)
FAINT = (126, 124, 136)
ACCENT = (76, 59, 207)
WARN = (168, 100, 26)
RULE = (226, 221, 211)

SERIF_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size * SCALE)
    except OSError:
        return ImageFont.load_default()


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    compression = data["compression"]["points"]

    image = Image.new("RGB", (W * SCALE, H * SCALE), PAPER)
    draw = ImageDraw.Draw(image)
    pad = 72 * SCALE

    draw.rectangle([0, 0, 10 * SCALE, H * SCALE], fill=ACCENT)

    eyebrow = font(SANS_B, 17)
    draw.text(
        (pad, 58 * SCALE),
        "NUMBER THEORY  ·  NATURAL DENSITY  ·  LEAN 4",
        font=eyebrow,
        fill=ACCENT,
    )

    badge_font = font(SANS_B, 13)
    badge = "ALMOST-ALL THEOREM"
    badge_box = draw.textbbox((0, 0), badge, font=badge_font)
    badge_width = badge_box[2] - badge_box[0]
    bx = (W - 72) * SCALE - badge_width - 20 * SCALE
    by = 48 * SCALE
    draw.rounded_rectangle(
        [bx, by, bx + badge_width + 20 * SCALE, by + 32 * SCALE],
        radius=16 * SCALE,
        fill=(236, 233, 251),
    )
    draw.text((bx + 10 * SCALE, by + 8 * SCALE), badge, font=badge_font, fill=ACCENT)

    title_font = font(SERIF_B, 52)
    title_lines = [
        "Polylogarithmic Descent for",
        "Almost All Collatz Orbits",
        "in Natural Density",
    ]
    y = 106 * SCALE
    for line in title_lines:
        draw.text((pad, y), line, font=title_font, fill=INK)
        y += 62 * SCALE

    tagline_font = font(SERIF, 24)
    y += 12 * SCALE
    for line in [
        "An explicit first-passage exponent, quantitative exceptional rates,",
        "a logarithmic clock, and a same-witness orbit ceiling.",
    ]:
        draw.text((pad, y), line, font=tagline_font, fill=SOFT)
        y += 34 * SCALE

    # A compact order-of-growth picture of the paper's quantitative pivot.
    gx0, gy0 = pad, 485 * SCALE
    gw, gh = 520 * SCALE, 72 * SCALE
    max_m = compression[-1]["M"]
    max_y = compression[-1]["linear"]

    def sx(value: float) -> float:
        return gx0 + value / max_m * gw

    def sy(value: float) -> float:
        return gy0 + gh - value / max_y * gh

    draw.line([gx0, gy0 + gh, gx0 + gw, gy0 + gh], fill=RULE, width=2 * SCALE)
    linear = [(sx(row["M"]), sy(row["linear"])) for row in compression]
    compressed = [(sx(row["M"]), sy(row["compressed"])) for row in compression]
    draw.line(linear, fill=WARN, width=3 * SCALE)
    draw.line(compressed, fill=ACCENT, width=4 * SCALE)

    small = font(SANS, 14)
    draw.text((gx0, gy0 - 25 * SCALE), "time support", font=small, fill=FAINT)
    draw.text((gx0 + 110 * SCALE, gy0 + 4 * SCALE), "O(M)", font=small, fill=WARN)
    draw.text(
        (gx0 + 255 * SCALE, gy0 + 38 * SCALE),
        "O(√(M log M))",
        font=small,
        fill=ACCENT,
    )

    rx = 730 * SCALE
    draw.line(
        [rx - 38 * SCALE, 476 * SCALE, rx - 38 * SCALE, 575 * SCALE],
        fill=RULE,
        width=2 * SCALE,
    )
    name_font = font(SANS_B, 20)
    meta_font = font(SANS, 16)
    draw.text((rx, 478 * SCALE), "Idris Ali Shaik", font=name_font, fill=INK)
    draw.text(
        (rx, 511 * SCALE),
        "doi:10.5281/zenodo.21984038  ·  v3.2.3",
        font=meta_font,
        fill=ACCENT,
    )
    draw.text((rx, 538 * SCALE), "Lean 4 · Mathlib · CC BY 4.0", font=meta_font, fill=FAINT)
    draw.text((rx, 565 * SCALE), "shaikidris.github.io", font=meta_font, fill=FAINT)

    image = image.resize((W, H), Image.Resampling.LANCZOS)
    image.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
