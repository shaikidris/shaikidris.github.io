/* Exact finite Collatz trajectories for the beginner orbit primer.
   Browser-global and CommonJS compatible so the arithmetic can be tested
   without a DOM. A capped run is a software outcome, not a theorem claim. */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.CollatzPrimerCore = Object.freeze(api);
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  function standardStep(n) {
    return n % 2n === 0n ? n / 2n : 3n * n + 1n;
  }

  function shortcutStep(n) {
    return n % 2n === 0n ? n / 2n : (3n * n + 1n) / 2n;
  }

  function operation(n, map) {
    if (n % 2n === 0n) return "÷2";
    return map === "shortcut" ? "(3n+1)/2" : "3n+1";
  }

  function compute(start, map, options) {
    const selectedMap = map === "shortcut" ? "shortcut" : "standard";
    const config = options || {};
    const stepCap = Number.isInteger(config.stepCap) && config.stepCap >= 0
      ? config.stepCap : 2000;
    const digitCap = Number.isInteger(config.digitCap) && config.digitCap >= 1
      ? config.digitCap : 320;
    const initial = typeof start === "bigint" ? start : BigInt(start);
    if (initial < 1n) throw new RangeError("The starting value must be positive.");

    const values = [{ value: initial, operation: "start", step: 0 }];
    const seen = new Set([initial.toString()]);
    let current = initial;
    let peak = initial;
    let peakStep = 0;
    let status = initial === 1n ? "reached" : "running";

    for (let step = 1; status === "running" && step <= stepCap; step++) {
      const op = operation(current, selectedMap);
      const next = selectedMap === "shortcut" ? shortcutStep(current) : standardStep(current);
      values.push({ value: next, operation: op, step });
      if (next > peak) { peak = next; peakStep = step; }

      if (next === 1n) {
        status = "reached";
      } else if (next.toString().length > digitCap) {
        status = "size";
      } else if (seen.has(next.toString())) {
        status = "cycle";
      } else {
        seen.add(next.toString());
        current = next;
      }
    }
    if (status === "running") status = "cap";

    return {
      start: initial,
      map: selectedMap,
      values,
      status,
      peak,
      peakStep,
      steps: values.length - 1
    };
  }

  return { standardStep, shortcutStep, compute };
});
