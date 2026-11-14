import assert from 'node:assert/strict';
import test from 'node:test';
import {advance, newGame, overlaps, WIDTH} from './game.js';

test('speed is expressed per second, not per frame', () => {
  const run = frames => {
    let state = newGame();
    for (let i = 0; i < frames; i++) state = advance(state, {right: true}, 0.5 / frames);
    return state.player.x;
  };
  assert.ok(Math.abs(run(30) - run(60)) < 0.00001);
  assert.ok(Math.abs(run(30) - 440) < 0.00001);
});

test('player stays inside the canvas and input state is unchanged', () => {
  const before = newGame();
  before.player.x = 598;
  const after = advance(before, {right: true}, 0.05);
  assert.equal(after.player.x, WIDTH - after.player.w);
  assert.equal(before.player.x, 598);
});

test('touching edges is not overlap, crossing edges is', () => {
  const a = {x: 0, y: 0, w: 10, h: 10};
  assert.equal(overlaps(a, {...a, x: 10}), false);
  assert.equal(overlaps(a, {...a, x: 9}), true);
});

test('one bullet removes only one enemy and scores once', () => {
  const state = newGame();
  state.enemies = [{id: 1, x: 100, y: 100, w: 20, h: 20}, {id: 2, x: 100, y: 100, w: 20, h: 20}];
  state.bullets = [{x: 105, y: 125, w: 6, h: 14}];
  const after = advance(state, {}, 0.02);
  assert.equal(after.enemies.length, 1);
  assert.equal(after.bullets.length, 0);
  assert.equal(after.score, 10);
});

test('last hit wins and bonus is awarded only once', () => {
  const state = newGame();
  state.enemies = [{id: 1, x: 100, y: 100, w: 20, h: 20}];
  state.bullets = [{x: 105, y: 125, w: 6, h: 14}];
  state.score = 50;
  state.remaining = 8;
  const after = advance(state, {}, 0.02);
  assert.equal(after.status, 'won');
  assert.equal(after.score, 68);
  assert.deepEqual(advance(after, {fire: true}, 0.05), after);
});

test('timeout loses and a new game resets all previous state', () => {
  const state = newGame();
  state.remaining = 0.01;
  const after = advance(state, {}, 0.02);
  assert.equal(after.status, 'lost');
  const fresh = newGame();
  assert.equal(fresh.status, 'playing');
  assert.equal(fresh.score, 0);
  assert.equal(fresh.bullets.length, 0);
  assert.equal(fresh.enemies.length, 6);
});

test('a long suspended frame does not teleport the player', () => {
  const after = advance(newGame(), {right: true}, 10);
  assert.equal(after.player.x, 314);
  assert.equal(after.remaining, 29.95);
});

test('held fire respects its cooldown', () => {
  let state = newGame();
  for (let i = 0; i < 10; i++) state = advance(state, {fire: true}, 0.01);
  assert.equal(state.bullets.length, 1);
});
