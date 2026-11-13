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

window.addEventListener('pagehide', cleanup, {once:true});
if (import.meta.hot) import.meta.hot.dispose(cleanup);
