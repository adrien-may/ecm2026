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


  title.textContent = '01 · Dessiner un joueur';
  instructions.textContent = 'Origine en haut à gauche. x va vers la droite, y vers le bas.';
  rectangle(300);
  controls.hidden = true;

window.addEventListener('pagehide', cleanup, {once:true});
if (import.meta.hot) import.meta.hot.dispose(cleanup);
