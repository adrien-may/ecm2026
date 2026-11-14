export const WIDTH = 640;
export const HEIGHT = 400;

export function newGame() {
  return {
    player: {x: 300, y: 350, w: 40, h: 20},
    enemies: Array.from({length: 6}, (_, i) => ({id: i, x: 70 + i * 90, y: 45, w: 32, h: 24})),
    bullets: [], score: 0, remaining: 30, cooldown: 0, status: 'playing',
  };
}

export function overlaps(a, b) {
  return a.x < b.x + b.w && a.x + a.w > b.x &&
    a.y < b.y + b.h && a.y + a.h > b.y;
}

// Pure function: the same state, input and dt produce the same next state.
export function advance(previous, input, seconds) {
  if (previous.status !== 'playing') return previous;
  const dt = Math.max(0, Math.min(seconds, 0.05));
  const state = {
    ...previous,
    player: {...previous.player},
    enemies: previous.enemies.map(enemy => ({...enemy})),
    bullets: previous.bullets.map(bullet => ({...bullet})),
  };
  const direction = Number(Boolean(input.right)) - Number(Boolean(input.left));
  state.player.x = Math.max(0, Math.min(WIDTH - state.player.w, state.player.x + direction * 280 * dt));
  state.remaining = Math.max(0, state.remaining - dt);
  state.cooldown = Math.max(0, state.cooldown - dt);
  if (input.fire && state.cooldown === 0) {
    state.bullets.push({x: state.player.x + 17, y: state.player.y, w: 6, h: 14});
    state.cooldown = 0.22;
  }
  for (const enemy of state.enemies) enemy.y += 8 * dt;
  for (const bullet of state.bullets) bullet.y -= 420 * dt;
  const remainingBullets = [];
  for (const bullet of state.bullets) {
    const hit = state.enemies.findIndex(enemy => overlaps(bullet, enemy));
    if (hit !== -1) {
      state.enemies.splice(hit, 1);
      state.score += 10;
    } else if (bullet.y + bullet.h >= 0) {
      remainingBullets.push(bullet);
    }
  }
  state.bullets = remainingBullets;
  if (state.enemies.length === 0) {
    state.status = 'won';
    state.score += Math.ceil(state.remaining);
  } else if (state.remaining === 0 || state.enemies.some(enemy => enemy.y + enemy.h >= state.player.y)) {
    state.status = 'lost';
  }
  return state;
}
