#!/usr/bin/env python3
"""Generate assets/figure-data-polylog.json for the root (v3.2.0) page.

Every number written here is computed from the real shortcut Collatz map or
from the paper's closed-form constants. Nothing is hand-typed, and nothing
produced here is a proof input: these are finite illustrations of an
asymptotic, natural-density theorem.

Source of truth: Zenodo 10.5281/zenodo.21931194 (article v3.2.0).
Run:  python3 scripts/make_figure_data_polylog.py
"""

import json
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "figure-data-polylog.json"

# --------------------------------------------------------------------------
# Constants, exactly as defined in the article
# --------------------------------------------------------------------------

LOG2 = math.log(2.0)
LOG3 = math.log(3.0)


def h2(p: float) -> float:
    """Binary entropy in bits."""
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


A0 = math.log2(3.0) / 2.0                 # a_0 = (log_2 3)/2
P_STAR = LOG2 / LOG3                      # p_* = log_3 2
KAPPA_STAR = 1.0 - h2(P_STAR)             # kappa_* = 1 - H_2(p_*)
A_FP = 1.0 / (2.0 * KAPPA_STAR)           # A_FP = 1/(2 kappa_*)
C_STAR = 2.0 / math.log(4.0 / 3.0)        # c_*   = 2/log(4/3)
C_RAW = 3.0 / math.log(4.0 / 3.0)         # raw   = 3/log(4/3)

# Guard: these must match the published article to the digits it prints.
# If a future edit changes a definition, this fails loudly instead of
# quietly shipping a figure that contradicts the theorem.
_PUBLISHED = {
    "A_FP": 9.9911133419,
    "c_star": 6.9521189935,
    "c_raw": 10.42817849,
    "a0": 0.7924812503,
}
for _name, _value, _want in (
    ("A_FP", A_FP, _PUBLISHED["A_FP"]),
    ("c_star", C_STAR, _PUBLISHED["c_star"]),
    ("c_raw", C_RAW, _PUBLISHED["c_raw"]),
    ("a0", A0, _PUBLISHED["a0"]),
):
    if abs(_value - _want) > 5e-10:
        raise SystemExit(
            f"constant drift: {_name} computed {_value!r}, article prints {_want!r}"
        )


# --------------------------------------------------------------------------
# The real shortcut Collatz map
# --------------------------------------------------------------------------

def shortcut(n: int) -> int:
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def orbit_log2(n: int, max_steps: int):
    """Return [(k, log2(T^k n))] until the orbit reaches 1 or runs out."""
    out, cur = [], n
    for k in range(max_steps + 1):
        out.append([k, math.log2(cur)])
        if cur == 1:
            break
        cur = shortcut(cur)
    return out


def first_passages(n: int, max_steps: int):
    """First time the orbit lands at or below each descending power of two."""
    marks, cur, seen = [], n, set()
    top = int(math.floor(math.log2(n)))
    for k in range(max_steps + 1):
        lg = math.log2(cur)
        q = int(math.floor(lg))
        for level in range(top, q - 1, -1):
            if level not in seen and lg <= level:
                seen.add(level)
                marks.append({"k": k, "log2v": lg, "threshold": level})
        if cur == 1:
            break
        cur = shortcut(cur)
    return marks


def steps_to_below(n: int, bound: float, cap: int) -> int:
    """Least k with T^k(n) <= bound, or -1 if not reached within cap."""
    cur = n
    for k in range(cap + 1):
        if cur <= bound:
            return k
        cur = shortcut(cur)
    return -1


# --------------------------------------------------------------------------
# Figure 1 — one real orbit, its thresholds and landings
# --------------------------------------------------------------------------

ORBIT_N = 27_000_001
ORBIT_CAP = 400
orbit_series = orbit_log2(ORBIT_N, ORBIT_CAP)
orbit_marks = first_passages(ORBIT_N, ORBIT_CAP)
orbit_log2n = math.log2(ORBIT_N)
orbit_M = int(math.floor(orbit_log2n))

# The deterministic high-rank envelope slope is a_0 - 1 per shortcut step.
orbit_envelope = [
    [0, orbit_log2n],
    [len(orbit_series) - 1, orbit_log2n + (A0 - 1.0) * (len(orbit_series) - 1)],
]

figure_orbit = {
    "n": ORBIT_N,
    "M": orbit_M,
    "log2n": orbit_log2n,
    "series": orbit_series,
    "landings": orbit_marks,
    "envelope": orbit_envelope,
    "clockBound": C_STAR * math.log(ORBIT_N),
    "steps": len(orbit_series) - 1,
}

# --------------------------------------------------------------------------
# Figure 2 — the quantitative pivot: linear horizon vs sqrt(M log M)
# --------------------------------------------------------------------------

compression = []
for M in range(8, 261, 4):
    linear = float(M)
    sqrt_term = math.sqrt(M * math.log(M))
    compression.append({
        "M": M,
        "linear": linear,
        "compressed": sqrt_term,
        "ratio": sqrt_term / linear,
    })

figure_compression = {
    "points": compression,
    "note": "orders only; the unspecified constant in the time-support lemmas is not modelled",
}

# --------------------------------------------------------------------------
# Figure 3 — how the targets compare as n grows
# --------------------------------------------------------------------------

# log10 of each target, as a function of D = log10(n).
targets_curves = []
for D in range(2, 401, 2):
    ln_n = D * math.log(10.0)
    polylog = A_FP * math.log10(ln_n)              # (log n)^{A_FP}
    stretched_25 = (ln_n ** (1.0 - 0.25)) / math.log(10.0)
    power_half = 0.5 * D                            # n^{1/2}
    power_tenth = 0.1 * D                           # n^{1/10}
    targets_curves.append({
        "D": D,
        "polylog": polylog,
        "stretched": stretched_25,
        "powerHalf": power_half,
        "powerTenth": power_tenth,
        "n": D,
    })

figure_targets = {
    "curves": targets_curves,
    "A": A_FP,
    "delta": 0.25,
    "note": "vertical axis is log10 of the target; the landing constant C_tar is not modelled",
}

# --------------------------------------------------------------------------
# Which target can a finite illustration honestly use?
#
# The headline target (log n)^A_FP is asymptotic: it is only SMALLER than n
# once n passes a crossover far beyond anything a browser can iterate. Below
# that point every orbit satisfies it vacuously at k = 0, which would make
# the figures look like a descent when nothing has happened.
#
# So the finite illustrations use the paper's stretched-logarithmic
# companion, exp((log n)^(1-delta)) -- a genuine theorem of the same paper
# (every fixed 0 < delta < 1) that IS a real descent at these scales. The
# crossover below is computed, displayed on the page, and used to explain why.
# --------------------------------------------------------------------------

def polylog_crossover() -> float:
    """Least n with (log n)^A_FP < n, by bisection."""
    lo, hi = 1e10, 1e30
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if math.log(mid) ** A_FP < mid:
            hi = mid
        else:
            lo = mid
    return hi


CROSSOVER = polylog_crossover()
DELTA_ILL = 0.25  # the illustrated stretched-logarithmic exponent


def stretched_target(n: float) -> float:
    return math.exp(math.log(n) ** (1.0 - DELTA_ILL))


# --------------------------------------------------------------------------
# Figure 4 — 'almost all', drawn: real orbits from one dyadic shell
# --------------------------------------------------------------------------

random.seed(20260814)
SHELL_M = 26
shell_lo, shell_hi = 2 ** SHELL_M, 2 ** (SHELL_M + 1) - 1
SAMPLE = 220
ENSEMBLE_CAP = 900

ensemble_target = stretched_target(shell_lo)
if ensemble_target >= shell_lo:
    raise SystemExit("illustrated target is not a descent at this shell")

tracks, reached, clock_ok = [], 0, 0
clock_limit = C_STAR * math.log(shell_lo)
for _ in range(SAMPLE):
    n = random.randint(shell_lo, shell_hi)
    k = steps_to_below(n, ensemble_target, ENSEMBLE_CAP)
    if k >= 0:
        reached += 1
        if k < clock_limit:
            clock_ok += 1
    tracks.append({"n": n, "k": k})

figure_ensemble = {
    "shellM": SHELL_M,
    "sample": SAMPLE,
    "delta": DELTA_ILL,
    "target": ensemble_target,
    "targetLog2": math.log2(ensemble_target),
    "clockLimit": clock_limit,
    "reached": reached,
    "withinClock": clock_ok,
    "tracks": tracks,
    "maxK": max((t["k"] for t in tracks if t["k"] >= 0), default=0),
}

# --------------------------------------------------------------------------
# Witness table — real (n, k, T^k n) triples at several scales
# --------------------------------------------------------------------------

witness_rows = []
for exp10 in (6, 9, 12, 15, 18):
    n = random.randint(10 ** exp10, 10 ** exp10 * 2)
    target = stretched_target(n)
    k = steps_to_below(n, target, 5000)
    if k <= 0:
        raise SystemExit(f"illustrated target is vacuous at 10^{exp10}")
    cur, peak = n, n
    for _ in range(k):
        cur = shortcut(cur)
        peak = max(peak, cur)
    witness_rows.append({
        "n": n,
        "digits": len(str(n)),
        "k": k,
        "clock": C_STAR * math.log(n),
        "target": target,
        "landing": cur,
        "peakRatioLog": math.log(peak) / math.log(n),
    })

# --------------------------------------------------------------------------

payload = {
    "_source": "Zenodo 10.5281/zenodo.21931194 (article v3.2.0)",
    "_disclaimer": (
        "Finite illustrations computed from the real shortcut Collatz map. "
        "Not proof inputs; the theorem is asymptotic and holds in natural density."
    ),
    "constants": {
        "a0": A0,
        "pStar": P_STAR,
        "kappaStar": KAPPA_STAR,
        "A_FP": A_FP,
        "cStar": C_STAR,
        "cRaw": C_RAW,
        "polylogCrossover": CROSSOVER,
        "illustrationDelta": DELTA_ILL,
    },
    "orbit": figure_orbit,
    "compression": figure_compression,
    "targets": figure_targets,
    "ensemble": figure_ensemble,
    "witnesses": witness_rows,
}

OUT.write_text(json.dumps(payload, indent=1), encoding="utf-8")
print(f"wrote {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT}")
print(f"  kappa_* = {KAPPA_STAR!r}")
print(f"  A_FP    = {A_FP!r}   (article prints 9.9911133419...)")
print(f"  c_*     = {C_STAR!r}   (article prints 6.9521189935...)")
print(f"  c_raw   = {C_RAW!r}   (article prints 10.42817849...)")
print(f"  polylog crossover: (log n)^A_FP < n only for n > {CROSSOVER:.3e}")
print(f"  illustrations use exp((log n)^{1 - DELTA_ILL:.2f}) instead")
_ks = [t["k"] for t in tracks if t["k"] >= 0]
print(f"  ensemble: {reached}/{SAMPLE} reached target, {clock_ok} within the clock, "
      f"k ranges {min(_ks)}–{max(_ks)}")
print(f"  witnesses: k = {[r['k'] for r in witness_rows]}")
