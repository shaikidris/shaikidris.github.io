#!/usr/bin/env python3
"""Generate assets/og-card.png, the 1200x630 social preview card.

The orbit drawn on the card is the real orbit of 1,234,567 under the shortcut
Collatz map, read from assets/figure-data.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "assets" / "figure-data.json"
OUT = SITE / "assets" / "og-card.png"

W, H = 1200, 630
SCALE = 2                                  # supersample, then downsample

PAPER = (252, 251, 249)
INK = (26, 26, 28)
SOFT = (74, 74, 82)
FAINT = (150, 148, 158)
ACCENT = (76, 59, 207)
GOOD = (28, 122, 74)
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
    data = json.loads(DATA.read_text())
    orbit = data["orbit"]

    img = Image.new("RGB", (W * SCALE, H * SCALE), PAPER)
    d = ImageDraw.Draw(img)

    pad = 72 * SCALE

    # accent rule down the left edge
    d.rectangle([0, 0, 10 * SCALE, H * SCALE], fill=ACCENT)

    # eyebrow
    f_eyebrow = font(SANS_B, 17)
    d.text((pad, 68 * SCALE), "NUMBER THEORY  ·  FORMALIZED MATHEMATICS",
           font=f_eyebrow, fill=ACCENT)

    # title
    f_title = font(SERIF_B, 54)
    title = ["Natural-density Collatz descent", "to a stretched-logarithmic scale"]
    y = 112 * SCALE
    for line in title:
        d.text((pad, y), line, font=f_title, fill=INK)
        y += 66 * SCALE

    # tagline
    f_tag = font(SERIF, 27)
    y += 16 * SCALE
    for line in ["For every 0 < δ < 0.251245…, almost every orbit falls below",
                 "exp((log n)^(1−δ)); the principal chain is formalized in Lean 4."]:
        d.text((pad, y), line, font=f_tag, fill=SOFT)
        y += 39 * SCALE

    # ---- inline orbit sparkline ----
    gx0, gy0 = pad, 470 * SCALE
    gw, gh = 560 * SCALE, 96 * SCALE
    series = orbit["series"]
    kmax = max(p["k"] for p in series)
    ylo, yhi = 0.0, orbit["log2n"] * 1.25

    def sx(k): return gx0 + (k / kmax) * gw
    def sy(v): return gy0 + gh - ((v - ylo) / (yhi - ylo)) * gh

    # threshold line
    ty = sy(orbit["thresholdLog2"])
    for x in range(int(gx0), int(gx0 + gw), 12 * SCALE):
        d.line([x, ty, x + 6 * SCALE, ty], fill=GOOD, width=2 * SCALE)

    pts = [(sx(p["k"]), sy(p["y"])) for p in series]
    d.line(pts, fill=INK, width=3 * SCALE, joint="curve")

    ks = orbit["kstar"]
    wx, wy = sx(ks), sy(series[ks]["y"])
    r = 8 * SCALE
    d.ellipse([wx - r, wy - r, wx + r, wy + r], fill=GOOD)
    d.ellipse([wx - r, wy - r, wx + r, wy + r], outline=PAPER, width=3 * SCALE)

    f_small = font(SANS, 15)
    d.text((gx0, gy0 + gh + 14 * SCALE),
           f"orbit of n = 1,234,567   ·   witness k* = {ks}   ·   clock bound ≈ {orbit['clockBound']:.1f}",
           font=f_small, fill=FAINT)

    # ---- right column: identity ----
    rx = 760 * SCALE
    d.line([rx - 40 * SCALE, 450 * SCALE, rx - 40 * SCALE, 560 * SCALE],
           fill=RULE, width=2 * SCALE)
    f_name = font(SANS_B, 21)
    f_meta = font(SANS, 17)
    d.text((rx, 458 * SCALE), "Idris Ali Shaik", font=f_name, fill=INK)
    d.text((rx, 490 * SCALE), "doi:10.5281/zenodo.21851173", font=f_meta, fill=ACCENT)
    d.text((rx, 516 * SCALE), "Lean 4 · Mathlib · CC BY 4.0", font=f_meta, fill=FAINT)
    d.text((rx, 542 * SCALE), "shaikidris.github.io", font=f_meta, fill=FAINT)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
