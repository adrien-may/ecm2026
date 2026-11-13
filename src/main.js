import './style.css';
const canvas = document.querySelector('canvas');
const context = canvas.getContext('2d');
const title = document.querySelector('#step-title');
const instructions = document.querySelector('#instructions');
const status = document.querySelector('#status');
const controls = document.querySelector('.controls');
let cleanup = () => {};

function rectangle(x) {
  context.fillStyle = '#102b29'; context.fillRect(0, 0, 640, 400);
  context.fillStyle = '#a8e4c4'; context.fillRect(x, 350, 40, 20);
}


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

window.addEventListener('pagehide', cleanup, {once:true});
if (import.meta.hot) import.meta.hot.dispose(cleanup);
