import {mountGame} from './canvas.js';
import './style.css';

const canvas = document.querySelector('canvas');
const context = canvas.getContext('2d');
const step = Number(4);
const title = document.querySelector('#step-title');
const instructions = document.querySelector('#instructions');
const status = document.querySelector('#status');
const controls = document.querySelector('.controls');
let cleanup = () => {};

function rectangle(x) {
  context.fillStyle = '#102b29'; context.fillRect(0, 0, 640, 400);
  context.fillStyle = '#a8e4c4'; context.fillRect(x, 350, 40, 20);
}

if (step === 1) {
  title.textContent = '01 · Dessiner un joueur';
  instructions.textContent = 'Origine en haut à gauche. x va vers la droite, y vers le bas.';
  rectangle(300);
  controls.hidden = true;
} else if (step === 2) {
  title.textContent = '02 · Déplacer avec le temps';
  instructions.textContent = 'Le joueur avance à 120 pixels par seconde et repart du bord.';
  controls.hidden = true;
  let x = 0, previous = null, frameId;
  function frame(now) {
    const dt = previous === null ? 0 : Math.min((now - previous) / 1000, 0.05);
    previous = now;
    x = (x + 120 * dt) % 600;
    rectangle(x);
    frameId = requestAnimationFrame(frame);
  }
  frameId = requestAnimationFrame(frame);
  cleanup = () => cancelAnimationFrame(frameId);
} else if (step === 3) {
  title.textContent = '03 · Lire le clavier';
  instructions.textContent = 'Cliquer dans le Canvas, puis maintenir une flèche. Le joueur reste dans les limites.';
  controls.hidden = true;
  let x = 300, previous = null, frameId;
  const keys = new Set();
  const down = event => { if (event.key.startsWith('Arrow')) { event.preventDefault(); keys.add(event.key); } };
  const up = event => keys.delete(event.key);
  const clear = () => keys.clear();
  canvas.addEventListener('keydown', down);
  canvas.addEventListener('keyup', up);
  canvas.addEventListener('blur', clear);
  function frame(now) {
    const dt = previous === null ? 0 : Math.min((now - previous) / 1000, 0.05);
    previous = now;
    x = Math.max(0, Math.min(600, x + (Number(keys.has('ArrowRight')) - Number(keys.has('ArrowLeft'))) * 280 * dt));
    rectangle(x);
    frameId = requestAnimationFrame(frame);
  }
  frameId = requestAnimationFrame(frame);
  cleanup = () => {
    cancelAnimationFrame(frameId);
    canvas.removeEventListener('keydown', down);
    canvas.removeEventListener('keyup', up);
    canvas.removeEventListener('blur', clear);
  };
} else {
  title.textContent = '04 · Une partie complète';
  instructions.textContent = 'Flèches pour bouger, espace pour tirer. 10 points par cible ; les secondes restantes donnent un bonus à la victoire.';
  const game = mountGame(canvas, state => {
    status.textContent = state.status === 'playing' ? 'Partie en cours.' : `${state.status === 'won' ? 'Victoire' : 'Fin de partie'} : ${state.score} points.`;
  });
  for (const key of ['left', 'right', 'fire']) {
    const button = document.querySelector(`#${key}`);
    button.addEventListener('pointerdown', event => { button.setPointerCapture(event.pointerId); game.setInput(key, true); });
    button.addEventListener('pointerup', () => game.setInput(key, false));
    button.addEventListener('pointercancel', () => game.setInput(key, false));
  }
  document.querySelector('#pause').onclick = () => { game.pause(); status.textContent = 'En pause.'; };
  document.querySelector('#resume').onclick = () => { game.resume(); status.textContent = 'Partie reprise.'; };
  document.querySelector('#restart').onclick = () => game.restart();
  cleanup = () => game.destroy();
}
window.addEventListener('pagehide', cleanup, {once: true});
if (import.meta.hot) import.meta.hot.dispose(cleanup);
