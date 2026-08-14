/* =========================================================================
   Figure engine. Preset values come from assets/figure-data.json, produced by
   scripts/make_figure_data.py from the actual shortcut Collatz map. The orbit
   lab can also evaluate a user-supplied integer locally with the same map.
   ========================================================================= */

(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- theme ---------- */

  function css(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function palette() {
    return {
      ink: css("--ink"), soft: css("--ink-soft"), faint: css("--ink-faint"),
      rule: css("--rule"), accent: css("--accent"), good: css("--good"),
      warn: css("--warn"), paper: css("--paper-raised")
    };
  }

  /* ---------- canvas helper ---------- */

  function setup(canvas, aspect) {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.parentElement.clientWidth;
    const h = Math.round(w / aspect);
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.height = h + "px";
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    return { ctx, w, h };
  }

  function axes(ctx, box, opts) {
    const p = palette();
    const { x0, y0, x1, y1 } = box;
    ctx.strokeStyle = p.rule;
    ctx.lineWidth = 1;
    ctx.font = "11px ui-sans-serif, -apple-system, system-ui, sans-serif";
    ctx.fillStyle = p.faint;

    // horizontal gridlines + y labels
    (opts.yTicks || []).forEach(t => {
      const y = opts.sy(t);
      ctx.beginPath();
      ctx.moveTo(x0, y); ctx.lineTo(x1, y);
      ctx.stroke();
      ctx.textAlign = "right"; ctx.textBaseline = "middle";
      ctx.fillText(opts.yFmt ? opts.yFmt(t) : String(t), x0 - 8, y);
    });
    // x labels
    (opts.xTicks || []).forEach(t => {
      const x = opts.sx(t);
      ctx.textAlign = "center"; ctx.textBaseline = "top";
      ctx.fillText(opts.xFmt ? opts.xFmt(t) : String(t), x, y0 + 8);
    });
    // axis lines
    ctx.strokeStyle = p.rule;
    ctx.beginPath();
    ctx.moveTo(x0, y1); ctx.lineTo(x0, y0); ctx.lineTo(x1, y0);
    ctx.stroke();

    // axis titles
    ctx.fillStyle = p.soft;
    ctx.font = "600 11px ui-sans-serif, -apple-system, system-ui, sans-serif";
    if (opts.xLabel) {
      ctx.textAlign = "center"; ctx.textBaseline = "bottom";
      ctx.fillText(opts.xLabel, (x0 + x1) / 2, y0 + 34);
    }
    if (opts.yLabel) {
      ctx.save();
      ctx.translate(14, (y0 + y1) / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.textAlign = "center"; ctx.textBaseline = "top";
      ctx.fillText(opts.yLabel, 0, 0);
      ctx.restore();
    }
  }

  function path(ctx, pts, sx, sy, style, dash, width) {
    ctx.save();
    ctx.strokeStyle = style;
    ctx.lineWidth = width || 1.5;
    ctx.setLineDash(dash || []);
    ctx.lineJoin = "round"; ctx.lineCap = "round";
    ctx.beginPath();
    pts.forEach((pt, i) => {
      const X = sx(pt.k !== undefined ? pt.k : pt.x);
      const Y = sy(pt.y);
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    });
    ctx.stroke();
    ctx.restore();
  }

  /* =====================================================================
     Figure 1 — one orbit, its heuristic trend, and the descent witness.
     ===================================================================== */

  function log2BigInt(x) {
    const bits = x.toString(2).length;
    if (bits <= 53) return Math.log2(Number(x));
    const shift = bits - 53;
    const leading = Number(x >> BigInt(shift));
    return Math.log2(leading) + shift;
  }

  function customOrbit(start, delta, maxSteps) {
    let x = BigInt(start);
    const full = [];
    const thresholdLog2 = Math.pow(Math.log(start), 1 - delta) / Math.log(2);
    let kstar = null;

    for (let k = 0; k <= maxSteps; k += 1) {
      const y = log2BigInt(x);
      full.push({ k, y });
      if (kstar === null && y <= thresholdLog2) kstar = k;
      if (x === 1n) break;
      x = x % 2n === 0n ? x / 2n : (3n * x + 1n) / 2n;
    }

    const kmax = Math.max(1, Math.min(
      full.length - 1,
      kstar === null ? 160 : kstar + 12
    ));
    const log2n = Math.log2(start);
    const rho = Math.sqrt(3) / 2;
    const trend = Array.from({ length: kmax + 1 }, (_, k) => ({
      k,
      y: k * Math.log2(rho) + log2n
    }));

    return {
      n: start,
      delta,
      log2n,
      thresholdLog2,
      kstar,
      clockBound: 6.953 * Math.log(start),
      kmax,
      series: full.slice(0, kmax + 1),
      trend,
      computedSteps: full.length - 1
    };
  }

  function figOrbit(data) {
    const canvas = document.getElementById("fig-orbit");
    if (!canvas) return;
    let d = data.orbit;
    let progress = reduceMotion ? 1 : 0;
    let raf = null;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 46, y0: h - 42, x1: w - 12, y1: 12 };
      const kMax = d.kmax;
      const plottedMax = Math.max(
        d.log2n,
        d.thresholdLog2,
        ...d.series.map(pt => pt.y),
        ...d.trend.map(pt => pt.y)
      );
      const yLo = 0, yHi = Math.max(5, Math.ceil(plottedMax / 5) * 5);

      const sx = k => box.x0 + (k / kMax) * (box.x1 - box.x0);
      const sy = y => box.y0 - ((y - yLo) / (yHi - yLo)) * (box.y0 - box.y1);

      const yTicks = [];
      for (let t = yLo; t <= yHi; t += 5) yTicks.push(t);
      const xTicks = [];
      for (let t = 0; t <= kMax; t += 10) xTicks.push(t);

      axes(ctx, box, {
        sx, sy, yTicks, xTicks,
        xLabel: "step k", yLabel: "log₂ Tᵏ(n)"
      });

      const n = Math.max(2, Math.round(progress * (kMax + 1)));
      const cut = a => a.slice(0, n);

      path(ctx, cut(d.trend), sx, sy, p.soft, [7, 5], 1.25);

      // threshold
      ctx.save();
      ctx.strokeStyle = p.good; ctx.lineWidth = 1.5; ctx.setLineDash([6, 3, 2, 3]);
      ctx.beginPath();
      ctx.moveTo(box.x0, sy(d.thresholdLog2)); ctx.lineTo(box.x1, sy(d.thresholdLog2));
      ctx.stroke();
      ctx.restore();
      ctx.fillStyle = p.good;
      ctx.font = "600 10px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "right"; ctx.textBaseline = "bottom";
      ctx.fillText(
        "exp((log n)^" + (1 - d.delta).toFixed(2) + ")",
        box.x1 - 4,
        sy(d.thresholdLog2) - 4
      );

      // the orbit
      path(ctx, cut(d.series), sx, sy, p.ink, [], 1.9);

      // witness marker
      if (d.kstar !== null && n > d.kstar) {
        const wx = sx(d.kstar), wy = sy(d.series[d.kstar].y);
        ctx.save();
        ctx.fillStyle = p.good;
        ctx.beginPath(); ctx.arc(wx, wy, 5, 0, 2 * Math.PI); ctx.fill();
        ctx.strokeStyle = p.paper; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(wx, wy, 5, 0, 2 * Math.PI); ctx.stroke();
        ctx.fillStyle = p.good;
        ctx.font = "600 11px ui-sans-serif, system-ui, sans-serif";
        ctx.textAlign = "left"; ctx.textBaseline = "top";
        ctx.fillText("k* = " + d.kstar, wx + 9, wy - 2);
        ctx.restore();
      }
    }

    function animate() {
      progress = Math.min(1, progress + 0.014);
      draw();
      if (progress < 1) raf = requestAnimationFrame(animate);
    }

    function start() {
      if (reduceMotion) { progress = 1; draw(); return; }
      cancelAnimationFrame(raf);
      progress = 0;
      raf = requestAnimationFrame(animate);
    }

    draw();
    onVisible(canvas, start);
    const replay = document.getElementById("fig-orbit-replay");
    if (replay) replay.addEventListener("click", start);

    const form = document.getElementById("orbit-form");
    const input = document.getElementById("orbit-input");
    const delta = document.getElementById("orbit-delta");
    const deltaOut = document.getElementById("orbit-delta-value");
    const result = document.getElementById("orbit-result");

    function loadCustom(animateResult) {
      const startValue = Number(input && input.value);
      const deltaValue = Number(delta && delta.value);
      if (!Number.isSafeInteger(startValue) || startValue < 3 || startValue > 1e12) {
        if (result) result.textContent = "Enter an integer from 3 through 1,000,000,000,000.";
        if (input) input.setAttribute("aria-invalid", "true");
        return;
      }
      if (input) input.removeAttribute("aria-invalid");
      d = customOrbit(startValue, deltaValue, 2000);
      if (deltaOut) deltaOut.textContent = deltaValue.toFixed(2);
      canvas.setAttribute(
        "aria-label",
        "Shortcut Collatz orbit of " + startValue.toLocaleString() +
        " with delta " + deltaValue.toFixed(2) +
        (d.kstar === null
          ? "; the target was not reached in the computed window."
          : "; first target witness at step " + d.kstar + ".")
      );
      if (result) {
        const witness = d.kstar === null
          ? "target not reached in the first " + d.computedSteps.toLocaleString() + " steps"
          : "witness k* = " + d.kstar;
        const clockVerdict = d.kstar === null
          ? ""
          : d.kstar < d.clockBound ? " · inside the displayed clock" : " · outside the displayed clock";
        result.textContent =
          "n = " + startValue.toLocaleString() +
          " · δ = " + deltaValue.toFixed(2) +
          " · " + witness +
          " · clock bound ≈ " + d.clockBound.toFixed(1) +
          clockVerdict;
      }
      progress = 1;
      draw();
      if (animateResult) start();
    }

    if (delta) {
      delta.addEventListener("input", () => {
        if (deltaOut) deltaOut.textContent = Number(delta.value).toFixed(2);
        loadCustom(false);
      });
    }
    if (form) {
      form.addEventListener("submit", event => {
        event.preventDefault();
        loadCustom(true);
      });
    }
    onResize(draw);
  }

  /* =====================================================================
     Figure 2 — stretched-logarithmic vs every fixed power.
     ===================================================================== */

  function figComparison(data) {
    const canvas = document.getElementById("fig-comparison");
    if (!canvas) return;
    const d = data.comparison;
    let deltaSel = 0.15;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 54, y0: h - 46, x1: w - 14, y1: 14 };
      const xLo = d.xRange[0], xHi = d.xRange[1];
      const yLo = 0, yHi = 1;

      const sx = x => box.x0 + ((x - xLo) / (xHi - xLo)) * (box.x1 - box.x0);
      const sy = y => box.y0 - ((y - yLo) / (yHi - yLo)) * (box.y0 - box.y1);

      axes(ctx, box, {
        sx, sy,
        yTicks: [0, 0.2, 0.4, 0.6, 0.8, 1.0],
        xTicks: [1, 2, 4, 6, 8, 10],
        // x is log10(log n); convert to a digit count for the label
        xFmt: t => "10" + supr(Math.round(t - 0.36)),
        yFmt: t => t.toFixed(1),
        xLabel: "digits of n",
        yLabel: "effective exponent ε(n)"
      });

      // fixed powers are horizontal lines
      d.levels.forEach(eps => {
        ctx.save();
        ctx.strokeStyle = p.faint; ctx.setLineDash([5, 4]); ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(box.x0, sy(eps)); ctx.lineTo(box.x1, sy(eps));
        ctx.stroke();
        ctx.restore();
        ctx.fillStyle = p.faint;
        ctx.font = "10px ui-monospace, monospace";
        ctx.textAlign = "right"; ctx.textBaseline = "bottom";
        ctx.fillText("n^" + eps, box.x1 - 4, sy(eps) - 3);
      });

      d.curves.forEach(c => {
        const on = Math.abs(c.delta - deltaSel) < 1e-9;
        path(ctx, c.points, sx, sy, on ? p.accent : p.rule, [], on ? 2.4 : 1.2);
      });

      // crossings of the selected curve with each fixed power
      d.crossovers.filter(c => Math.abs(c.delta - deltaSel) < 1e-9).forEach(c => {
        if (c.x < xLo || c.x > xHi) return;
        const X = sx(c.x), Y = sy(c.eps);
        ctx.save();
        ctx.strokeStyle = p.good; ctx.setLineDash([2, 3]); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(X, box.y0); ctx.lineTo(X, Y); ctx.stroke();
        ctx.restore();
        ctx.fillStyle = p.good;
        ctx.beginPath(); ctx.arc(X, Y, 3.5, 0, 2 * Math.PI); ctx.fill();
      });

      ctx.fillStyle = p.accent;
      ctx.font = "600 11px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "left"; ctx.textBaseline = "top";
      ctx.fillText("δ = " + deltaSel, box.x0 + 8, box.y1 + 2);
    }

    function supr(t) {
      const map = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³",
        4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
      return String(t).split("").map(c => map[c] || c).join("");
    }

    const slider = document.getElementById("fig-comparison-delta");
    const out = document.getElementById("fig-comparison-delta-val");
    if (slider) {
      slider.addEventListener("input", () => {
        deltaSel = parseFloat(slider.value) === 0 ? 0.15 : 0.2;
        if (out) out.textContent = "δ = " + deltaSel;
        draw();
      });
    }
    draw();
    onResize(draw);
  }

  /* =====================================================================
     Figure 3 — the ensemble. Many orbits' running minima collapsing.
     ===================================================================== */

  function figEnsemble(data) {
    const canvas = document.getElementById("fig-ensemble");
    if (!canvas) return;
    const d = data.ensemble;
    let frame = reduceMotion ? d.maxK : 0;
    let raf = null, running = false;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 40, y0: h - 42, x1: w - 12, y1: 12 };
      const yHi = 21, yLo = 0;
      const sx = k => box.x0 + (k / d.maxK) * (box.x1 - box.x0);
      const sy = y => box.y0 - ((y - yLo) / (yHi - yLo)) * (box.y0 - box.y1);

      axes(ctx, box, {
        sx, sy,
        yTicks: [0, 5, 10, 15, 20],
        xTicks: [0, 20, 40, 60, 80, 100, 120, 140],
        xLabel: "step k",
        yLabel: "log₂ of running min"
      });

      const n = Math.max(2, Math.round(frame));
      ctx.save();
      ctx.globalAlpha = 0.42;
      d.tracks.forEach((t, i) => {
        const pts = t.y.slice(0, n).map((y, k) => ({ k, y }));
        path(ctx, pts, sx, sy, i % 7 === 0 ? p.accent : p.soft, [], i % 7 === 0 ? 1.5 : 0.9);
      });
      ctx.restore();

      // count how many are below each of a few marks
      ctx.fillStyle = p.faint;
      ctx.font = "10px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "left"; ctx.textBaseline = "top";
      ctx.fillText(d.tracks.length + " starting values in [2¹⁹, 2²⁰)", box.x0 + 8, box.y1 + 4);
    }

    function animate() {
      frame += 1.1;
      if (frame >= d.maxK) { frame = d.maxK; running = false; draw(); return; }
      draw();
      raf = requestAnimationFrame(animate);
    }
    function start() {
      if (reduceMotion) { frame = d.maxK; draw(); return; }
      cancelAnimationFrame(raf);
      frame = 0; running = true;
      raf = requestAnimationFrame(animate);
    }

    draw();
    onVisible(canvas, start);
    const replay = document.getElementById("fig-ensemble-replay");
    if (replay) replay.addEventListener("click", start);
    onResize(draw);
  }

  /* =====================================================================
     Figure 4 — how sparse the exceptional set is.
     ===================================================================== */

  function figExceptional(data) {
    const canvas = document.getElementById("fig-exceptional");
    if (!canvas) return;
    const d = data.exceptional;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 56, y0: h - 42, x1: w - 12, y1: 12 };
      const xLo = 2, xHi = 400;
      const yLo = -30, yHi = 1;   // log10 of the fraction

      const sx = x => box.x0 + ((x - xLo) / (xHi - xLo)) * (box.x1 - box.x0);
      const sy = y => box.y0 - ((y - yLo) / (yHi - yLo)) * (box.y0 - box.y1);

      axes(ctx, box, {
        sx, sy,
        yTicks: [0, -5, -10, -15, -20, -25, -30],
        xTicks: [2, 100, 200, 300, 400],
        yFmt: t => t === 0 ? "1" : "10" + sup(t),
        xLabel: "digits of X",
        yLabel: "normalized rate shape"
      });

      const pts = d.points.map(pt => ({ x: pt.x, y: Math.log10(pt.y) }));
      // area under the curve
      ctx.save();
      ctx.globalAlpha = .12; ctx.fillStyle = p.accent;
      ctx.beginPath();
      pts.forEach((pt, i) => i ? ctx.lineTo(sx(pt.x), sy(pt.y)) : ctx.moveTo(sx(pt.x), sy(pt.y)));
      ctx.lineTo(sx(pts[pts.length - 1].x), box.y0);
      ctx.lineTo(sx(pts[0].x), box.y0);
      ctx.closePath(); ctx.fill();
      ctx.restore();

      path(ctx, pts, sx, sy, p.accent, [], 2.2);
    }
    function sup(t) {
      const map = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³",
        4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
      return String(t).split("").map(c => map[c] || c).join("");
    }
    draw();
    onResize(draw);
  }

  /* ---------- shared helpers ---------- */

  function w0Aspect(canvas) {
    const a = parseFloat(canvas.dataset.aspect || "1.9");
    return window.innerWidth < 560 ? Math.min(a, 1.35) : a;
  }

  function onVisible(el, fn) {
    if (!("IntersectionObserver" in window)) { fn(); return; }
    let fired = false;
    new IntersectionObserver((entries, obs) => {
      entries.forEach(e => {
        if (e.isIntersecting && !fired) { fired = true; fn(); }
      });
    }, { threshold: 0.35 }).observe(el);
  }

  const resizers = [];
  function onResize(fn) { resizers.push(fn); }
  let rt = null;
  window.addEventListener("resize", () => {
    clearTimeout(rt);
    rt = setTimeout(() => resizers.forEach(f => f()), 150);
  });

  /* ---------- theorem parameter + scale lab ---------- */

  function superscript(value) {
    const map = { "-": "⁻", ".": "·", 0: "⁰", 1: "¹", 2: "²", 3: "³",
      4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
    return String(value).split("").map(c => map[c] || c).join("");
  }

  function compactNumber(value) {
    if (!Number.isFinite(value)) return "—";
    if (value < 1e5) {
      return value.toLocaleString(undefined, { maximumFractionDigits: value < 10 ? 3 : 0 });
    }
    const exponent = Math.floor(Math.log10(value));
    const mantissa = value / Math.pow(10, exponent);
    return mantissa.toFixed(2) + " × 10" + superscript(exponent);
  }

  function theoremLab(data) {
    const deltaInput = document.getElementById("theorem-delta");
    const sigmaInput = document.getElementById("theorem-sigma");
    const sizeInput = document.getElementById("theorem-size");
    if (!deltaInput || !sigmaInput || !sizeInput) return;

    const deltaOut = document.getElementById("theorem-delta-value");
    const sigmaOut = document.getElementById("theorem-sigma-value");
    const sizeOut = document.getElementById("theorem-size-value");
    const status = document.getElementById("theorem-status");
    const admissibility = document.getElementById("theorem-admissibility");
    const capOut = document.getElementById("theorem-sigma-cap");
    const epsilonOut = document.getElementById("metric-epsilon");
    const targetOut = document.getElementById("metric-target-digits");
    const clockOut = document.getElementById("metric-clock");
    const delta0 = data.constants.delta0;

    function update() {
      const delta = Number(deltaInput.value);
      const sigma = Number(sigmaInput.value);
      const sizeExponent = Number(sizeInput.value);
      const sigmaCap = 1 - delta / delta0;
      const valid = sigma > 0 && sigma < sigmaCap;

      deltaOut.textContent = "δ = " + delta.toFixed(3);
      sigmaOut.textContent = "σ = " + sigma.toFixed(3);
      sizeOut.textContent = "D = 10" + superscript(sizeExponent.toFixed(1).replace(".0", ""));

      status.className = "lab-status " + (valid ? "valid" : "invalid");
      status.textContent = valid
        ? "Admissible: the quantitative exceptional-count conclusion applies."
        : "Outside the theorem: this σ is not below the strict upper bound.";
      sigmaInput.setAttribute("aria-invalid", valid ? "false" : "true");
      admissibility.textContent =
        sigma.toFixed(3) + (valid ? " < " : " ≥ ") + sigmaCap.toFixed(3);
      capOut.textContent =
        "For this δ, the paper requires 0 < σ < " + sigmaCap.toFixed(6) + ".";

      const D = Math.pow(10, sizeExponent);
      const logN = D * Math.log(10);
      const epsilon = Math.pow(logN, -delta);
      const targetDigits = Math.pow(logN, 1 - delta) / Math.log(10);
      const clock = data.constants.clock * logN;

      epsilonOut.textContent = epsilon < 0.001
        ? epsilon.toExponential(3)
        : epsilon.toFixed(4);
      targetOut.textContent = "≈ " + compactNumber(targetDigits);
      clockOut.textContent = "≈ " + compactNumber(clock);
    }

    [deltaInput, sigmaInput, sizeInput].forEach(el => {
      el.addEventListener("input", update);
    });
    document.querySelectorAll("[data-theorem-preset]").forEach(button => {
      button.addEventListener("click", () => {
        const preset = button.dataset.theoremPreset;
        if (preset === "interior") {
          deltaInput.value = "0.10";
          sigmaInput.value = "0.50";
        } else if (preset === "endpoint") {
          deltaInput.value = "0.245";
          sigmaInput.value = "0.01";
        } else {
          deltaInput.value = "0.20";
          sigmaInput.value = "0.40";
        }
        update();
      });
    });
    update();
  }

  /* ---------- witness table ---------- */

  function witnessTable(data) {
    const host = document.getElementById("witness-table");
    if (!host) return;
    const w = data.witnesses;
    const row = r => `<tr>
      <td class="num">${r.n.toLocaleString()}</td>
      <td class="num">${r.kstar}</td>
      <td class="num">${r.bound}</td>
      <td><span class="pill ${r.withinClock ? "yes" : "no"}">${r.withinClock ? "within clock" : "misses clock"}</span></td>
    </tr>`;
    host.innerHTML = `
      <div class="tablewrap"><table>
        <thead><tr><th>n</th><th>witness k*</th><th>clock bound 6.953·log n</th><th></th></tr></thead>
        <tbody>
          <tr><td colspan="4" style="background:var(--paper-sunk);font-weight:650;color:var(--ink-faint);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase">Typical values</td></tr>
          ${w.typical.map(row).join("")}
          <tr><td colspan="4" style="background:var(--paper-sunk);font-weight:650;color:var(--ink-faint);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase">Known extremal small cases</td></tr>
          ${w.extremal.map(row).join("")}
        </tbody>
      </table></div>`;
    const rate = document.getElementById("witness-rate");
    if (rate) {
      const s = w.sample;
      rate.textContent = (s.rate * 100).toFixed(1) + "%";
    }
    const med = document.getElementById("witness-median");
    if (med) med.textContent = w.sample.medianRatio.toFixed(2);
  }

  /* ---------- guided proof architecture ---------- */

  function proofFlowLab() {
    const panels = Array.from(document.querySelectorAll("[data-proof-panel]"));
    const triggers = Array.from(document.querySelectorAll("[data-proof-step]"));
    const previous = document.getElementById("proof-prev");
    const next = document.getElementById("proof-next");
    const progress = document.getElementById("proof-lab-progress");
    if (!panels.length) return;

    let current = Math.max(0, panels.findIndex(panel => panel.open));

    function sync(index) {
      current = Math.max(0, Math.min(panels.length - 1, index));
      const id = panels[current].id;
      triggers.forEach(trigger => {
        if (trigger.dataset.proofStep === id) {
          trigger.setAttribute("aria-current", "step");
        } else {
          trigger.removeAttribute("aria-current");
        }
      });
      if (progress) {
        const title = panels[current].querySelector("summary").textContent.trim();
        progress.textContent = "Stage " + (current + 1) + " of " + panels.length + " · " + title;
      }
      if (previous) previous.disabled = current === 0;
      if (next) next.disabled = current === panels.length - 1;
    }

    function openStage(index, scroll) {
      index = Math.max(0, Math.min(panels.length - 1, index));
      panels.forEach((panel, i) => { panel.open = i === index; });
      sync(index);
      if (scroll) {
        panels[index].scrollIntoView({
          behavior: reduceMotion ? "auto" : "smooth",
          block: "start"
        });
      }
    }

    triggers.forEach(trigger => {
      trigger.addEventListener("click", () => {
        const index = panels.findIndex(panel => panel.id === trigger.dataset.proofStep);
        if (index >= 0) openStage(index, false);
      });
    });
    panels.forEach((panel, index) => {
      panel.addEventListener("toggle", () => {
        if (!panel.open) return;
        panels.forEach((other, i) => {
          if (i !== index) other.open = false;
        });
        sync(index);
      });
    });
    if (previous) previous.addEventListener("click", () => openStage(current - 1, true));
    if (next) next.addEventListener("click", () => openStage(current + 1, true));

    const hashIndex = panels.findIndex(panel => "#" + panel.id === window.location.hash);
    openStage(hashIndex >= 0 ? hashIndex : current, false);
  }

  /* ---------- in-page section navigation ---------- */

  function sectionNavigation() {
    const links = Array.from(document.querySelectorAll('.section-links a[href^="#"]'));
    if (!links.length) return;

    const sections = [];
    const seen = new Set();
    links.forEach(link => {
      const id = link.getAttribute("href").slice(1);
      const section = document.getElementById(id);
      if (section && !seen.has(id)) {
        seen.add(id);
        sections.push(section);
      }
      link.addEventListener("click", () => {
        const menu = link.closest(".section-menu");
        if (menu) menu.removeAttribute("open");
      });
    });

    let scheduled = false;
    function update() {
      scheduled = false;
      const marker = Math.min(220, window.innerHeight * 0.3);
      let current = sections[0];
      sections.forEach(section => {
        if (section.getBoundingClientRect().top <= marker) current = section;
      });
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) {
        current = sections[sections.length - 1];
      }
      links.forEach(link => {
        const active = current && link.getAttribute("href") === "#" + current.id;
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    }
    function schedule() {
      if (!scheduled) {
        scheduled = true;
        requestAnimationFrame(update);
      }
    }

    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    update();
  }

  /* ---------- reveal ---------- */

  function reveal() {
    const els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || reduceMotion) {
      els.forEach(e => e.classList.add("in")); return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -8% 0px" });
    els.forEach(e => io.observe(e));
  }

  /* ---------- boot ---------- */

  function boot() {
    proofFlowLab();
    sectionNavigation();
    reveal();
    fetch("/assets/figure-data.json")
      .then(r => r.json())
      .then(data => {
        window.__figdata = data;
        figOrbit(data);
        figComparison(data);
        figEnsemble(data);
        figExceptional(data);
        theoremLab(data);
        witnessTable(data);
        // redraw on theme change
        const mo = new MutationObserver(() => resizers.forEach(f => f()));
        mo.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
        window.matchMedia("(prefers-color-scheme: dark)")
          .addEventListener("change", () => resizers.forEach(f => f()));
      })
      .catch(err => {
        console.error("figure data failed to load", err);
        document.querySelectorAll(".figbox").forEach(b => {
          b.innerHTML = '<p style="font-family:var(--sans);font-size:.8125rem;color:var(--ink-faint);margin:0">Figure data could not be loaded.</p>';
        });
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }
})();
