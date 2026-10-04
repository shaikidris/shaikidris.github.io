#!/usr/bin/env python3
"""Generate assets/og-home.png, the 1200x630 social card for the research hub.

Counts are read from data/works.json so the card never disagrees with the page.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "data" / "works.json"
OUT = SITE / "assets" / "og-home.png"

W, H, S = 1200, 630, 2
PAPER, INK, SOFT, FAINT = (252, 251, 249), (26, 26, 28), (74, 74, 82), (126, 124, 136)
ACCENT, GOOD, RULE = (76, 59, 207), (28, 122, 74), (226, 221, 211)
SERIF_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size * S)


def main() -> None:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    works = d["works"]
    stats = [
        (str(sum(1 for w in works if w.get("preprint"))), "open preprints"),
        (str(len(works)), "Palomar entries"),
        (str(sum(w["palomar"]["declarations"] for w in works)), "verified declarations"),
    ]

    img = Image.new("RGB", (W * S, H * S), PAPER)
    dr = ImageDraw.Draw(img)
    pad = 72 * S
    dr.rectangle([0, 0, 10 * S, H * S], fill=ACCENT)

    dr.text((pad, 62 * S), "MATHEMATICS  ·  FORMAL VERIFICATION", font=font(SANS_B, 17), fill=ACCENT)
    dr.text((pad, 104 * S), d["author"]["name"], font=font(SERIF_B, 64), fill=INK)
    y = 196 * S
    for line in ["Quantitative number theory and combinatorics,",
                 "with selected results formalized in Lean 4."]:
        dr.text((pad, y), line, font=font(SERIF, 30), fill=SOFT)
        y += 42 * S

    # area tags
    x, y = pad, 316 * S
    tag = font(SANS_B, 16)
    for a in d["areas"]:
        tw = dr.textlength(a["name"], font=tag)
        dr.rounded_rectangle([x, y, x + tw + 28 * S, y + 36 * S], radius=18 * S, fill=(236, 233, 251))
        dr.text((x + 14 * S, y + 9 * S), a["name"], font=tag, fill=ACCENT)
        x += tw + 40 * S

    # stats
    y = 420 * S
    dr.line([pad, y - 22 * S, (W - 72) * S, y - 22 * S], fill=RULE, width=2 * S)
    x = pad
    for num, label in stats:
        dr.text((x, y), num, font=font(SERIF_B, 54), fill=INK)
        dr.text((x, y + 70 * S), label, font=font(SANS, 17), fill=FAINT)
        x += 300 * S
    dr.text(((W - 72) * S - dr.textlength("shaikidris.github.io", font=font(SANS_B, 18)), 556 * S),
            "shaikidris.github.io", font=font(SANS_B, 18), fill=GOOD)

    img.resize((W, H), Image.Resampling.LANCZOS).save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
