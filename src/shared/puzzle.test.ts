import assert from 'node:assert/strict';
import { test } from 'node:test';

import { dailySeed, generateTour, optimalRoute, routeLength, routeScore } from './puzzle.ts';

test('seed deterministe', () => {
  assert.equal(dailySeed('2026-12-01'), dailySeed('2026-12-01'));
});

test('la tournee du jour est deterministe', () => {
  const a = generateTour('2026-12-01');
  const b = generateTour('2026-12-01');
  assert.deepEqual(a.stops, b.stops);
  assert.equal(a.optimalLength, b.optimalLength);
});

test('la longueur optimale correspond a la meilleure permutation', () => {
  const puzzle = generateTour('2026-12-01');
  const best = optimalRoute(puzzle.depot, puzzle.stops);
  assert.equal(best.length, puzzle.optimalLength);
  assert.equal(routeLength(puzzle.depot, puzzle.stops, best.order), puzzle.optimalLength);
});

test('le score vaut 100 pour la route optimale', () => {
  const puzzle = generateTour('2026-12-02');
  const best = optimalRoute(puzzle.depot, puzzle.stops);
  assert.equal(routeScore(puzzle, best.order), 100);
  const worst = best.order.slice().reverse();
  assert.ok(routeScore(puzzle, worst) <= 100);
});
