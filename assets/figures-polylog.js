/* =========================================================================
   Figure engine for the root (v3.2.1) page. Preset values come from
   assets/figure-data-polylog.json, produced by
   scripts/make_figure_data_polylog.py from the actual shortcut Collatz map.

   Everything drawn here is a finite illustration. The theorem is asymptotic
   and holds in natural density; no figure is a proof input.
   ========================================================================= */

(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const resizers = [];

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

  /* ---------- canvas helpers ---------- */

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

    (opts.yTicks || []).forEach(t => {
      const y = opts.sy(t);
      ctx.beginPath();
      ctx.moveTo(x0, y); ctx.lineTo(x1, y);
      ctx.stroke();
      ctx.textAlign = "right"; ctx.textBaseline = "middle";
      ctx.fillText(opts.yFmt ? opts.yFmt(t) : String(t), x0 - 8, y);
    });
    (opts.xTicks || []).forEach(t => {
      const x = opts.sx(t);
      ctx.textAlign = "center"; ctx.textBaseline = "top";
      ctx.fillText(opts.xFmt ? opts.xFmt(t) : String(t), x, y0 + 8);
    });
    ctx.strokeStyle = p.rule;
    ctx.beginPath();
    ctx.moveTo(x0, y1); ctx.lineTo(x0, y0); ctx.lineTo(x1, y0);
    ctx.stroke();

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
      const X = sx(pt[0]);
      const Y = sy(pt[1]);
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    });
    ctx.stroke();
    ctx.restore();
  }

  function w0Aspect(canvas) {
    return canvas.parentElement.clientWidth < 560 ? 1.35 : 2.15;
  }

  function onVisible(el, fn) {
    if (!("IntersectionObserver" in window)) { fn(); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { fn(); io.unobserve(e.target); }
      });
    }, { threshold: 0.25 });
    io.observe(el);
  }

  function onResize(fn) { resizers.push(fn); }

  /* ---------- the real shortcut map, for user-supplied inputs ---------- */

  function shortcut(n) { return n % 2n === 0n ? n / 2n : (3n * n + 1n) / 2n; }

  function log2BigInt(x) {
    if (x <= 0n) return -Infinity;
    const bits = x.toString(2).length;
    if (bits <= 52) return Math.log2(Number(x));
    const head = Number(x >> BigInt(bits - 52));
    return Math.log2(head) + (bits - 52);
  }

  /* =====================================================================
     Figure 1 — one real orbit, its envelope, thresholds, and landings
     ===================================================================== */

  function figOrbit(data) {
    const canvas = document.getElementById("fig-orbit");
    if (!canvas) return;
    const d = data.orbit;
    let shown = reduceMotion ? d.series.length : 0;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 54, y0: h - 44, x1: w - 14, y1: 14 };
      const maxK = d.series.length - 1;
      const yMin = 0;
      const yMax = Math.ceil(d.log2n) + 1;
      const sx = k => box.x0 + (k / maxK) * (box.x1 - box.x0);
      const sy = v => box.y0 - ((v - yMin) / (yMax - yMin)) * (box.y0 - box.y1);

      const yTicks = [];
      for (let t = 0; t <= yMax; t += 5) yTicks.push(t);
      const xTicks = [];
      for (let t = 0; t <= maxK; t += Math.max(10, Math.round(maxK / 6 / 10) * 10)) xTicks.push(t);

      axes(ctx, box, {
        sx, sy, xTicks, yTicks,
        xLabel: "shortcut steps k",
        yLabel: "log₂ of the orbit value"
      });

      // mean-drift reference (slope a0 - 1), not a pointwise orbit bound
      path(ctx, d.driftReference.map(pt => [pt[0], pt[1]]), sx, sy, p.faint, [5, 4], 1.2);

      // landing markers on their dyadic thresholds
      ctx.save();
      d.landings.forEach(m => {
        if (m.k > shown) return;
        ctx.strokeStyle = p.rule;
        ctx.setLineDash([2, 3]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(box.x0, sy(m.threshold));
        ctx.lineTo(sx(m.k), sy(m.threshold));
        ctx.stroke();
      });
      ctx.restore();

      // the orbit itself
      const pts = d.series.slice(0, Math.max(2, shown)).map(s => [s[0], s[1]]);
      path(ctx, pts, sx, sy, p.accent, [], 1.6);

      // first-passage landing dots
      d.landings.forEach(m => {
        if (m.k > shown) return;
        ctx.fillStyle = p.good;
        ctx.beginPath();
        ctx.arc(sx(m.k), sy(m.log2v), 2.6, 0, Math.PI * 2);
        ctx.fill();
      });

      // clock marker
      const clockK = Math.min(maxK, d.clockBound);
      ctx.save();
      ctx.strokeStyle = p.warn;
      ctx.setLineDash([6, 4]);
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(sx(clockK), box.y1); ctx.lineTo(sx(clockK), box.y0);
      ctx.stroke();
      ctx.fillStyle = p.warn;
      ctx.font = "600 10px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "right"; ctx.textBaseline = "top";
      ctx.fillText("c⋆ log n reference", sx(clockK) - 6, box.y1 + 2);
      ctx.restore();
    }

    function animate() {
      shown += Math.max(1, Math.round(d.series.length / 90));
      if (shown >= d.series.length) { shown = d.series.length; draw(); return; }
      draw();
      requestAnimationFrame(animate);
    }

    onResize(draw);
    onVisible(canvas, () => { reduceMotion ? draw() : animate(); });
    draw();

    const replay = document.getElementById("orbit-replay");
    if (replay) replay.addEventListener("click", () => { shown = 0; animate(); });

    // user-supplied integer, evaluated locally under the same map
    const form = document.getElementById("orbit-form");
    const input = document.getElementById("orbit-input");
    const result = document.getElementById("orbit-result");
    if (form && input && result) {
      form.addEventListener("submit", ev => {
        ev.preventDefault();
        let n;
        try { n = BigInt(input.value.trim()); }
        catch (e) { result.textContent = "Enter a positive integer."; return; }
        if (n < 2n) { result.textContent = "Enter an integer of at least 2."; return; }
        if (n > 10n ** 24n) { result.textContent = "Keep it at or below 10²⁴ for a responsive local run."; return; }

        // Precise for big values: Number(n) would lose bits past 2^53.
        const lnN = log2BigInt(n) * Math.LN2;
        const delta = data.constants.illustrationDelta;
        // target = exp((log n)^(1-delta)); compare in log2 to stay exact.
        const targetLog2 = Math.pow(lnN, 1 - delta) / Math.LN2;
        const clock = data.constants.cStar * lnN;

        let cur = n, k = 0, peak = n;
        const cap = 20000;
        while (k < cap && log2BigInt(cur) > targetLog2) {
          cur = shortcut(cur); k++;
          if (cur > peak) peak = cur;
        }
        const reached = log2BigInt(cur) <= targetLog2;
        const peakRatio = log2BigInt(peak) / log2BigInt(n);
        if (!reached) {
          result.textContent =
            "Stopped after " + cap.toLocaleString() +
            " shortcut steps without reaching the displayed companion target. " +
            "This is the interactive safety cap, not a mathematical conclusion.";
          return;
        }
        const landed = cur.toString().length > 18
          ? "≈2^" + log2BigInt(cur).toFixed(1) : cur.toString();
        const withinClock = k < clock;
        result.innerHTML =
          "Reached <strong>" + landed + "</strong> after <strong>" + k +
          "</strong> shortcut steps, against a target of ≈2^" + targetLog2.toFixed(1) + ". " +
          "The reference \\(c_*\\log n\\) is " + clock.toFixed(0) + " — " +
          (withinClock ? "inside the reference" : "<strong>outside the reference</strong>") + ". " +
          "The highest iterate on the way was n^" + peakRatio.toFixed(3) + ". " +
          "<em>One finite run under the stretched-logarithmic companion target — an illustration, not evidence for the density theorem.</em>";
        if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
          window.MathJax.typesetPromise([result]).catch(() => {});
        }
      });
    }
  }

  /* =====================================================================
     Figure 2 — the quantitative pivot: linear horizon vs √(M log M)
     ===================================================================== */

  function figCompression(data) {
    const canvas = document.getElementById("fig-compression");
    if (!canvas) return;
    const pts = data.compression.points;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 54, y0: h - 44, x1: w - 14, y1: 14 };
      const maxM = pts[pts.length - 1].M;
      const maxY = pts[pts.length - 1].linear;
      const sx = m => box.x0 + (m / maxM) * (box.x1 - box.x0);
      const sy = v => box.y0 - (v / maxY) * (box.y0 - box.y1);

      axes(ctx, box, {
        sx, sy,
        xTicks: [0, 50, 100, 150, 200, 250],
        yTicks: [0, 50, 100, 150, 200, 250],
        xLabel: "shell rank M",
        yLabel: "number of possible cumulative passage times"
      });

      path(ctx, pts.map(q => [q.M, q.linear]), sx, sy, p.warn, [6, 4], 1.6);
      path(ctx, pts.map(q => [q.M, q.compressed]), sx, sy, p.accent, [], 2);

      ctx.font = "600 11px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "left"; ctx.textBaseline = "middle";
      ctx.fillStyle = p.warn;
      ctx.fillText("O(M) — direct union", sx(maxM * 0.42), sy(maxM * 0.52));
      ctx.fillStyle = p.accent;
      ctx.fillText("O(√(M log M)) — proved", sx(maxM * 0.44), sy(pts[Math.floor(pts.length * 0.55)].compressed) + 14);
    }

    onResize(draw);
    onVisible(canvas, draw);
    draw();
  }

  /* =====================================================================
     Figure 3 — how the targets compare as n grows
     ===================================================================== */

  function figTargets(data) {
    const canvas = document.getElementById("fig-targets");
    if (!canvas) return;
    const rows = data.targets.curves;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 58, y0: h - 44, x1: w - 14, y1: 14 };
      const maxD = rows[rows.length - 1].D;
      const maxY = Math.max(rows[rows.length - 1].powerHalf, rows[rows.length - 1].stretched);
      const sx = D => box.x0 + (D / maxD) * (box.x1 - box.x0);
      const sy = v => box.y0 - (v / maxY) * (box.y0 - box.y1);

      axes(ctx, box, {
        sx, sy,
        xTicks: [0, 100, 200, 300, 400],
        yTicks: [0, 50, 100, 150, 200],
        xLabel: "decimal digits of n",
        yLabel: "decimal digits of the target"
      });

      path(ctx, rows.map(r => [r.D, r.powerHalf]), sx, sy, p.faint, [6, 4], 1.4);
      path(ctx, rows.map(r => [r.D, r.powerTenth]), sx, sy, p.warn, [3, 3], 1.4);
      path(ctx, rows.map(r => [r.D, r.stretched]), sx, sy, p.good, [], 1.6);
      path(ctx, rows.map(r => [r.D, r.polylog]), sx, sy, p.accent, [], 2.2);

      const legend = [
        ["n^(1/2)", p.faint],
        ["n^(1/10)", p.warn],
        ["exp((log n)^0.75)", p.good],
        ["C(log n)^" + data.targets.A.toFixed(0) + " — fixed-exponent theorem", p.accent]
      ];
      ctx.font = "600 10.5px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "left"; ctx.textBaseline = "middle";
      legend.forEach((item, i) => {
        const y = box.y1 + 12 + i * 15;
        ctx.fillStyle = item[1];
        ctx.fillRect(box.x0 + 12, y - 4, 16, 2.5);
        ctx.fillText(item[0], box.x0 + 34, y);
      });
    }

    onResize(draw);
    onVisible(canvas, draw);
    draw();
  }

  /* =====================================================================
     Figure 4 — "almost all", drawn from real orbits in one dyadic shell
     ===================================================================== */

  function figEnsemble(data) {
    const canvas = document.getElementById("fig-ensemble");
    if (!canvas) return;
    const d = data.ensemble;
    let shown = reduceMotion ? d.tracks.length : 0;

    function draw() {
      const { ctx, w, h } = setup(canvas, w0Aspect(canvas));
      const p = palette();
      const box = { x0: 54, y0: h - 44, x1: w - 14, y1: 14 };
      const maxK = Math.max(d.maxK, Math.ceil(d.clockLimit)) * 1.05;
      const n = d.tracks.length;
      const sx = k => box.x0 + (k / maxK) * (box.x1 - box.x0);
      const sy = i => box.y1 + (i / n) * (box.y0 - box.y1);

      axes(ctx, box, {
        sx, sy: v => box.y0 - (v / n) * (box.y0 - box.y1),
        xTicks: [0, 50, 100, 150, 200, 250, 300],
        yTicks: [],
        xLabel: "shortcut steps to the stretched-logarithmic companion target",
        yLabel: "sampled starts in shell 2²⁶"
      });

      d.tracks.slice(0, shown).forEach((t, i) => {
        if (t.k < 0) return;
        ctx.strokeStyle = t.k < d.clockLimit ? p.accent : p.warn;
        ctx.globalAlpha = 0.5;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(box.x0, sy(i));
        ctx.lineTo(sx(t.k), sy(i));
        ctx.stroke();
        ctx.globalAlpha = 1;
      });

      // the clock
      ctx.save();
      ctx.strokeStyle = p.warn;
      ctx.setLineDash([6, 4]);
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(sx(d.clockLimit), box.y1); ctx.lineTo(sx(d.clockLimit), box.y0);
      ctx.stroke();
      ctx.fillStyle = p.warn;
      ctx.font = "600 10px ui-sans-serif, system-ui, sans-serif";
      ctx.textAlign = "left"; ctx.textBaseline = "top";
      ctx.fillText("c⋆ log n reference = " + d.clockLimit.toFixed(0), sx(d.clockLimit) + 5, box.y1 + 2);
      ctx.restore();
    }

    function animate() {
      shown += Math.max(1, Math.round(d.tracks.length / 60));
      if (shown >= d.tracks.length) { shown = d.tracks.length; draw(); return; }
      draw();
      requestAnimationFrame(animate);
    }

    onResize(draw);
    onVisible(canvas, () => { reduceMotion ? draw() : animate(); });
    draw();
  }

  /* =====================================================================
     Theorem lab — the quantifier order, made movable
     ===================================================================== */

  function theoremLab(data) {
    const aEl = document.getElementById("lab-A");
    if (!aEl) return;
    const cEl = document.getElementById("lab-c");
    const bEl = document.getElementById("lab-beta");
    const gEl = document.getElementById("lab-gamma");
    const dEl = document.getElementById("lab-size");

    const aOut = document.getElementById("lab-A-value");
    const cOut = document.getElementById("lab-c-value");
    const bOut = document.getElementById("lab-beta-value");
    const gOut = document.getElementById("lab-gamma-value");
    const dOut = document.getElementById("lab-size-value");

    const status = document.getElementById("lab-status");
    const gammaCap = document.getElementById("lab-gamma-cap");
    const mTarget = document.getElementById("metric-target-digits");
    const mClock = document.getElementById("metric-clock");
    const mSaving = document.getElementById("metric-saving");

    const K = data.constants.kappaStar;
    const AFP = data.constants.A_FP;
    const CSTAR = data.constants.cStar;

    function update() {
      const A = parseFloat(aEl.value);
      const c = parseFloat(cEl.value);
      const beta = parseFloat(bEl.value);
      const gamma = parseFloat(gEl.value);
      const D = parseFloat(dEl.value);

      const cap = K * (A - AFP);
      const admissible = gamma > 0 && gamma < cap && A > AFP && c > CSTAR;

      aOut.textContent = "A = " + A.toFixed(3);
      cOut.textContent = "c = " + c.toFixed(3);
      bOut.textContent = "β = " + beta.toFixed(2);
      gOut.textContent = "γ = " + gamma.toFixed(4);
      dOut.textContent = "n ≈ 10^" + D;

      if (gammaCap) {
        gammaCap.textContent =
          "κ⋆(A − A_FP) = " + cap.toFixed(4) + (cap <= 0 ? "  (no admissible γ)" : "");
      }

      if (status) {
        status.classList.toggle("valid", admissible);
        status.classList.toggle("invalid", !admissible);
        status.textContent = admissible
          ? "Admissible. The exceptional set is O(X/(log X)^" + gamma.toFixed(4) + ")."
          : (A <= AFP
              ? "A must exceed A_FP = " + AFP.toFixed(10) + "."
              : (c <= CSTAR
                  ? "c must exceed c⋆ = " + CSTAR.toFixed(10) + "."
                  : "γ must lie strictly between 0 and κ⋆(A − A_FP) = " + cap.toFixed(4) + "."));
      }

      // scale readout for n = 10^D
      const lnN = D * Math.log(10);
      const targetDigits = A * Math.log10(lnN);
      const clockSteps = c * lnN;
      if (mTarget) mTarget.textContent = targetDigits < 1e4
        ? targetDigits.toFixed(1) : targetDigits.toExponential(2);
      if (mClock) mClock.textContent = clockSteps < 1e5
        ? clockSteps.toFixed(0) : clockSteps.toExponential(2);
      if (mSaving) mSaving.textContent = (targetDigits / D).toExponential(2);
    }

    [aEl, cEl, bEl, gEl, dEl].forEach(el => el && el.addEventListener("input", update));

    document.querySelectorAll("[data-lab-preset]").forEach(btn => {
      btn.addEventListener("click", () => {
        const preset = btn.dataset.labPreset;
        if (preset === "comfortable") {
          aEl.value = 14; cEl.value = 8; gEl.value = 0.15;
        } else if (preset === "near-critical") {
          aEl.value = 10.2; cEl.value = 7.0; gEl.value = 0.008;
        } else if (preset === "inadmissible") {
          aEl.value = 10.5; cEl.value = 7.5; gEl.value = 0.09;
        }
        update();
      });
    });

    update();
  }

  /* ---------- witness table ---------- */

  function witnessTable(data) {
    const body = document.getElementById("witness-body");
    if (!body) return;
    body.innerHTML = data.witnesses.map(r => {
      const landed = r.k >= 0;
      return "<tr>" +
        "<td>10^" + (r.digits - 1) + "<span class='sub'> (" + r.digits + " digits)</span></td>" +
        "<td>" + (landed ? r.k : "—") + "</td>" +
        "<td>" + r.clock.toFixed(0) + "</td>" +
        "<td>" + (landed ? "n^" + r.peakRatioLog.toFixed(3) : "—") + "</td>" +
        "</tr>";
    }).join("");
  }

  /* ---------- guided proof lab ---------- */

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
        if (trigger.dataset.proofStep === id) trigger.setAttribute("aria-current", "step");
        else trigger.removeAttribute("aria-current");
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
          behavior: reduceMotion ? "auto" : "smooth", block: "start"
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
        panels.forEach((other, i) => { if (i !== index) other.open = false; });
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
      if (section && !seen.has(id)) { seen.add(id); sections.push(section); }
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
      if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
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
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -8% 0px" });
    els.forEach(e => io.observe(e));
  }

  /* ---------- boot ---------- */

  function boot() {
    proofFlowLab();
    sectionNavigation();
    reveal();
    fetch("/assets/figure-data-polylog.json")
      .then(r => r.json())
      .then(data => {
        window.__figdata = data;
        figOrbit(data);
        figCompression(data);
        figTargets(data);
        figEnsemble(data);
        theoremLab(data);
        witnessTable(data);
        const mo = new MutationObserver(() => resizers.forEach(f => f()));
        mo.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
      })
      .catch(err => {
        console.error("figure data failed to load", err);
      });

    let t;
    window.addEventListener("resize", () => {
      clearTimeout(t);
      t = setTimeout(() => resizers.forEach(f => f()), 150);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
