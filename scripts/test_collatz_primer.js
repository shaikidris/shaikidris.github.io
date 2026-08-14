"use strict";

const assert = require("node:assert/strict");
const core = require("../assets/collatz-primer-core.js");

function values(run) {
  return run.values.map(record => record.value);
}

const standardSeven = core.compute(7n, "standard");
assert.deepEqual(values(standardSeven), [
  7n, 22n, 11n, 34n, 17n, 52n, 26n, 13n, 40n,
  20n, 10n, 5n, 16n, 8n, 4n, 2n, 1n
]);
assert.equal(standardSeven.status, "reached");
assert.equal(standardSeven.steps, 16);
assert.equal(standardSeven.peak, 52n);
assert.equal(standardSeven.peakStep, 5);

const shortcutSeven = core.compute(7n, "shortcut");
assert.deepEqual(values(shortcutSeven), [
  7n, 11n, 17n, 26n, 13n, 20n, 10n, 5n, 8n, 4n, 2n, 1n
]);
assert.equal(shortcutSeven.status, "reached");
assert.equal(shortcutSeven.steps, 11);
assert.equal(shortcutSeven.peak, 26n);

const one = core.compute(1n, "standard");
assert.equal(one.status, "reached");
assert.equal(one.steps, 0);
assert.equal(one.peak, 1n);

const standardTwentySeven = core.compute(27n, "standard");
assert.equal(standardTwentySeven.status, "reached");
assert.equal(standardTwentySeven.steps, 111);
assert.equal(standardTwentySeven.peak, 9232n);
assert.equal(standardTwentySeven.peakStep, 77);

const capped = core.compute(27n, "standard", { stepCap: 10 });
assert.equal(capped.status, "cap");
assert.equal(capped.steps, 10);

const oversized = core.compute(27n, "standard", { digitCap: 1 });
assert.equal(oversized.status, "size");
assert.equal(oversized.steps, 1);

assert.throws(() => core.compute(0n, "standard"), RangeError);

console.log("Collatz primer checks passed.");
