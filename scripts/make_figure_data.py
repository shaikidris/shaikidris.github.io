#!/usr/bin/env python3
"""Compute figure data for the public site from the actual shortcut Collatz map.

Every number plotted on the site comes from this script. Nothing is drawn by
hand and nothing is a proof input; the figures are illustrations of statements
proved in the manuscript.

Shortcut map:  T(n) = n/2 for even n,  (3n+1)/2 for odd n.

Outputs assets/figure-data.json.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "figure-data.json"

# Constants fixed by the public v2.0.3 article.
A0 = math.log2(3) / 2                      # a_0 = log_2(3)/2
RHO = math.sqrt(3) / 2                     # heuristic one-step rate
CLOCK = 6.953                              # literal public theorem bound
DELTA_0 = math.log(1 / A0) / math.log(2 / A0)       # public strict endpoint


def require_public_delta(delta: float) -> None:
    """Reject figure parameters outside the strict public theorem range."""
    if not 0 < delta < DELTA_0:
        raise ValueError(f"delta={delta} is outside 0 < delta < {DELTA_0}")


def shortcut_orbit(n: int, max_steps: int = 4000) -> list[int]:
    """Iterate T from n until reaching 1, or until max_steps."""
    orbit = [n]
    x = n
    for _ in range(max_steps):
        if x == 1:
            break
        x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
        orbit.append(x)
    return orbit


def orbit_min_index(orbit: list[int], threshold: float) -> int | None:
    """First index k with T^k(n) <= threshold."""
    for k, v in enumerate(orbit):
        if v <= threshold:
            return k
    return None


def figure_orbit() -> dict:
    """One example orbit, its heuristic trend, target, and first witness.

    The trend is the logarithmic-block motivation from Section 1.1 of the
    public article. It is not asserted as a pointwise orbit envelope.
    """
    n = 1_234_567
    delta = 0.15
    require_public_delta(delta)
    orbit = shortcut_orbit(n)
    log2n = math.log2(n)
    threshold = math.exp(math.log(n) ** (1 - delta))
    kstar = orbit_min_index(orbit, threshold)

    # Plot only the certified segment plus a little beyond the witness.
    kmax = min(len(orbit) - 1, (kstar or 0) + 12)

    series = [{"k": k, "y": math.log2(v)} for k, v in enumerate(orbit[: kmax + 1])]
    trend = [{"k": k, "y": k * math.log2(RHO) + log2n} for k in range(kmax + 1)]

    return {
        "n": n,
        "delta": delta,
        "M": int(math.log2(n)),
        "log2n": log2n,
        "thresholdLog2": math.log2(threshold),
        "kstar": kstar,
        "clockBound": CLOCK * math.log(n),
        "kmax": kmax,
        "series": series,
        "trend": trend,
    }


def figure_threshold_comparison() -> dict:
    """Why the stretched-logarithmic threshold is below every fixed power.

    Plotting both thresholds directly is useless: the crossovers happen at
    absurd sizes, so over any plottable range the stretched-log threshold looks
    LARGER than n^eps and the picture contradicts the statement.

    The honest quantity is the *effective exponent*. Write

        exp((log n)^(1-delta)) = n^(eps(n)),    eps(n) = (log n)^(-delta),

    so the stretched-log threshold is a power of n whose exponent decays to
    zero. A fixed power is a horizontal line. The curve crossing below each
    line is exactly "smaller than every fixed power", and on a logarithmic
    axis in log n the crossings are visible.

    x-axis is log10(log n); we also report the digit count for labelling.
    """
    curves = []
    # log10(log n) from 0.5 (log n ~ 3, n ~ 20) to 10 (log n = 10^10).
    xs = [0.5 + i * (10 - 0.5) / 300 for i in range(301)]

    # Both displayed exponents lie strictly below the public endpoint DELTA_0.
    deltas = (0.15, 0.2)
    for delta in deltas:
        require_public_delta(delta)
        pts = []
        for x in xs:
            log_n = 10 ** x
            pts.append({"x": x, "y": log_n ** (-delta)})
        curves.append({"kind": "stretched", "delta": delta, "points": pts})

    levels = [0.5, 0.2, 0.05]

    # eps(n) = eps  <=>  (log n)^delta = 1/eps  <=>  log n = (1/eps)^(1/delta)
    crossovers = []
    for delta in deltas:
        for eps in levels:
            log_n = (1 / eps) ** (1 / delta)
            crossovers.append({
                "delta": delta,
                "eps": eps,
                "x": math.log10(log_n),
                "log10digits": math.log10(log_n / math.log(10)),
            })

    return {"curves": curves, "levels": levels, "crossovers": crossovers,
            "xRange": [xs[0], xs[-1]]}


def figure_descent_ensemble() -> dict:
    """Many orbits at once: the 'almost all' picture.

    For a sample of starting values in one dyadic shell, record log2 of the
    running minimum against step count. Animating these together shows the
    ensemble collapsing while individual orbits stay ragged.
    """
    shell_lo, shell_hi = 2**19, 2**20
    step = (shell_hi - shell_lo) // 60
    tracks = []
    for i in range(60):
        n = shell_lo + i * step + 1
        if n % 2 == 0:
            n += 1
        orbit = shortcut_orbit(n)
        running = []
        cur = orbit[0]
        for v in orbit[:140]:
            cur = min(cur, v)
            running.append(round(math.log2(cur), 4))
        tracks.append({"n": n, "y": running})
    return {"shell": [shell_lo, shell_hi], "tracks": tracks, "maxK": 140}


def figure_exceptional_count() -> dict:
    """Normalized shape of the public exceptional-fraction estimate.

    The pair delta=0.1, sigma=0.5 is admissible because
    sigma < 1 - delta / DELTA_0. The value c=1 normalizes the drawing only;
    it is not the article's unoptimized proof constant.
    """
    delta, sigma, c = 0.1, 0.5, 1.0
    require_public_delta(delta)
    if not 0 < sigma < 1 - delta / DELTA_0:
        raise ValueError("exceptional-rate exponents are outside Theorem 1.1")
    pts = []
    for i in range(201):
        log10x = 2 + i * (400 - 2) / 200
        log_x = log10x * math.log(10)
        frac = 5 * math.exp(-c * (log_x**sigma))
        pts.append({"x": log10x, "y": max(frac, 1e-300)})
    return {"delta": delta, "sigma": sigma, "c": c, "points": pts}


def _witness_row(n: int, delta: float = 0.15) -> dict:
    orbit = shortcut_orbit(n)
    threshold = math.exp(math.log(n) ** (1 - delta))
    kstar = orbit_min_index(orbit, threshold)
    bound = CLOCK * math.log(n)
    return {
        "n": n,
        "kstar": kstar,
        "bound": round(bound, 1),
        "threshold": round(threshold, 1),
        "peak": max(orbit),
        "withinClock": (kstar is not None and kstar < bound),
    }


def witness_table() -> dict:
    """Typical behaviour versus the known extremal small cases.

    IMPORTANT framing: Theorem 1.1, part 2, is an almost-all statement about
    sufficiently large n. The celebrated small record-holders (27, 703, 9663,
    63728127, ...) are exactly the sparse, small exceptional values the theorem
    permits, and several of them do miss the 6.953 log n clock. Showing only
    those would misrepresent the result; showing only a typical sample would
    hide them. We report both, plus the measured rate over a large sample.
    """
    delta = 0.15
    require_public_delta(delta)

    # Typical behaviour: a deterministic stride across one large dyadic shell.
    shell_lo, shell_hi = 2**26, 2**27
    sample_n, hits, kratios = 0, 0, []
    stride = (shell_hi - shell_lo) // 2000
    for i in range(2000):
        n = shell_lo + i * stride
        if n % 2 == 0:
            n += 1
        row = _witness_row(n, delta)
        sample_n += 1
        if row["withinClock"]:
            hits += 1
        if row["kstar"] is not None:
            kratios.append(row["kstar"] / row["bound"])
    kratios.sort()

    typical = [_witness_row(n, delta) for n in
               (67_108_865, 74_000_001, 90_000_001, 110_000_001, 130_000_001)]
    extremal = [_witness_row(n, delta) for n in
                (27, 703, 9_663, 63_728_127, 670_617_279)]

    return {
        "delta": delta,
        "typical": typical,
        "extremal": extremal,
        "sample": {
            "shell": [shell_lo, shell_hi],
            "count": sample_n,
            "withinClock": hits,
            "rate": hits / sample_n,
            "medianRatio": kratios[len(kratios) // 2] if kratios else None,
            "maxRatio": kratios[-1] if kratios else None,
        },
    }


def main() -> None:
    data = {
        "constants": {
            "a0": A0,
            "rho": RHO,
            "clock": CLOCK,
            "delta0": DELTA_0,
        },
        "orbit": figure_orbit(),
        "comparison": figure_threshold_comparison(),
        "ensemble": figure_descent_ensemble(),
        "exceptional": figure_exceptional_count(),
        "witnesses": witness_table(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1))
    print(f"wrote {OUT}  ({OUT.stat().st_size} bytes)")
    print(f"  a0={A0:.12f} rho={RHO:.12f} clock={CLOCK:.10f}")
    for c in data["comparison"]["crossovers"]:
        d10 = 10 ** c["log10digits"]
        print(f"  crossover delta={c['delta']} eps={c['eps']}: "
              f"n needs ~10^{c['log10digits']:.1f} digits ({d10:.3g})")
    print(f"  orbit: n={data['orbit']['n']} k*={data['orbit']['kstar']} "
          f"bound={data['orbit']['clockBound']:.1f}")
    s = data["witnesses"]["sample"]
    print(f"  sample: {s['withinClock']}/{s['count']} within clock "
          f"(rate {s['rate']:.4f}), median k*/bound={s['medianRatio']:.3f}, "
          f"max={s['maxRatio']:.3f}")
    for label in ("typical", "extremal"):
        print(f"  -- {label} --")
        for r in data["witnesses"][label]:
            print(f"  n={r['n']:>12}  k*={r['kstar']:>4}  clock<{r['bound']:>6}  ok={r['withinClock']}")


if __name__ == "__main__":
    main()
