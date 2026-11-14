import assert from 'node:assert/strict';
import test from 'node:test';
import {mountGame} from './canvas.js';

function environment(t) {
  const previous = Object.fromEntries(['window', 'requestAnimationFrame', 'cancelAnimationFrame'].map(key => [key, globalThis[key]]));
  const canvas = new EventTarget();
  canvas.focus = () => {};
  let frame;
  let state;
  globalThis.window = new EventTarget();
  globalThis.requestAnimationFrame = callback => {frame = callback; return 1;};
  globalThis.cancelAnimationFrame = () => {};
  const game = mountGame(canvas, () => {}, next => {state = next;});
  t.after(() => {
    game.destroy();
    for (const [key, value] of Object.entries(previous)) {
      if (value === undefined) delete globalThis[key];
      else globalThis[key] = value;
    }
  });
  return {canvas, game, tick: now => frame(now), state: () => state};
}

test('a pointer press survives focus leaving the canvas for a control', t => {
  const {canvas, game, tick, state} = environment(t);
  tick(0);
  game.setInput('right', true);
  canvas.dispatchEvent(new Event('blur'));
  tick(50);
  assert.equal(state().player.x, 314);
});

test('a brief fire click between frames still produces one bullet', t => {
  const {canvas, game, tick, state} = environment(t);
  tick(0);
  game.setInput('fire', true);
  canvas.dispatchEvent(new Event('blur'));
  game.setInput('fire', false);
  tick(16);
  assert.equal(state().bullets.length, 1);
  tick(32);
  assert.equal(state().bullets.length, 1);
});
