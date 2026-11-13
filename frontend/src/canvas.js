import {advance, newGame, WIDTH, HEIGHT} from './game.js';

export function draw(context, state) {
  context.fillStyle = '#102b29';
  context.fillRect(0, 0, WIDTH, HEIGHT);
  context.fillStyle = '#a8e4c4';
  const player = state.player;
  context.fillRect(player.x, player.y, player.w, player.h);
  context.fillStyle = '#f4be70';
  for (const enemy of state.enemies) context.fillRect(enemy.x, enemy.y, enemy.w, enemy.h);
  context.fillStyle = '#ffffff';
  for (const bullet of state.bullets) context.fillRect(bullet.x, bullet.y, bullet.w, bullet.h);
  context.font = '16px Arial';
  context.fillText(`${state.score} points`, 18, 25);
  context.fillText(`${Math.ceil(state.remaining)} s`, WIDTH - 65, 25);
  if (state.status !== 'playing') {
    context.fillStyle = '#102b29e8';
    context.fillRect(0, 130, WIDTH, 120);
    context.fillStyle = '#ffffff';
    context.textAlign = 'center';
    context.font = 'bold 30px Arial';
    context.fillText(state.status === 'won' ? 'Objectif atteint !' : 'Temps écoulé', WIDTH / 2, 183);
    context.font = '18px Arial';
    context.fillText(`${state.score} points · Rejouer pour recommencer`, WIDTH / 2, 220);
    context.textAlign = 'left';
  }
}

export function mountGame(canvas, onState = () => {}, render = null) {
  const context = render ? null : canvas.getContext('2d');
  let state = newGame();
  let previous = null;
  let frameId;
  let paused = false;
  let fireQueued = false;
  let lastStatus = '';
  const input = {left: false, right: false, fire: false};
  const keyboard = {left: false, right: false, fire: false};
  const keys = {ArrowLeft: 'left', ArrowRight: 'right', ' ': 'fire'};
  const paint = render || (state => draw(context, state));
  function clearInput() {
    input.left = input.right = input.fire = false;
    fireQueued = false;
    clearKeyboard();
  }
  function clearKeyboard() {
    keyboard.left = keyboard.right = keyboard.fire = false;
  }
  function keydown(event) {
    if (keys[event.key]) {
      event.preventDefault();
      keyboard[keys[event.key]] = true;
      if (event.key === ' ') fireQueued = true;
    }
  }
  function keyup(event) {
    if (keys[event.key]) { event.preventDefault(); keyboard[keys[event.key]] = false; }
  }
  function blur() { clearInput(); paused = true; previous = null; }
  function frame(now) {
    const dt = previous === null ? 0 : (now - previous) / 1000;
    previous = now;
    if (!paused) {
      state = advance(state, {
        left: input.left || keyboard.left,
        right: input.right || keyboard.right,
        fire: input.fire || keyboard.fire || fireQueued,
      }, dt);
      fireQueued = false;
    }
    paint(state);
    if (state.status !== lastStatus) {
      lastStatus = state.status;
      onState({...state});
    }
    frameId = requestAnimationFrame(frame);
  }
  canvas.addEventListener('keydown', keydown);
  canvas.addEventListener('keyup', keyup);
  canvas.addEventListener('blur', clearKeyboard);
  window.addEventListener('blur', blur);
  frameId = requestAnimationFrame(frame);
  return {
    setInput(key, value) {
      input[key] = value;
      if (key === 'fire' && value) fireQueued = true;
    },
    pause() { paused = true; clearInput(); },
    resume() { paused = false; previous = null; canvas.focus(); },
    restart() { state = newGame(); lastStatus = ''; clearInput(); paused = false; previous = null; canvas.focus(); },
    destroy() {
      cancelAnimationFrame(frameId);
      canvas.removeEventListener('keydown', keydown);
      canvas.removeEventListener('keyup', keyup);
      canvas.removeEventListener('blur', clearKeyboard);
      window.removeEventListener('blur', blur);
    },
  };
}
