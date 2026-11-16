import * as THREE from 'three';
import {mountGame} from './canvas.js';
import {WIDTH, HEIGHT} from './game.js';
import './style.css';

const canvas = document.querySelector('canvas');
const status = document.querySelector('#status');
const renderer = new THREE.WebGLRenderer({canvas, antialias: true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(WIDTH, HEIGHT, false);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#102b29');
const camera = new THREE.PerspectiveCamera(45, WIDTH / HEIGHT, 1, 2000);
const viewpoint = document.querySelector('#viewpoint');
function updateCamera() {
  const offset = Number(viewpoint.value) / 100;
  camera.position.set(330 * offset, -220 * offset, 650);
  camera.lookAt(0, 0, 0);
}
viewpoint.addEventListener('input', updateCamera);
updateCamera();
scene.add(new THREE.AmbientLight(0xffffff, 2));
const light = new THREE.DirectionalLight(0xffffff, 3);
light.position.set(-200, 300, 500);
scene.add(light);
const geometry = new THREE.BoxGeometry(1, 1, 1);
const materials = ['#a8e4c4', '#f4be70', '#ffffff'].map(color => new THREE.MeshStandardMaterial({color}));
const pools = [[], [], []];

function show(items, pool, material, depth) {
  while (pool.length < items.length) {
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
    pool.push(mesh);
  }
  pool.forEach((mesh, index) => {
    const item = items[index];
    mesh.visible = Boolean(item);
    if (!item) return;
    mesh.position.set(item.x + item.w / 2 - WIDTH / 2, HEIGHT / 2 - item.y - item.h / 2, depth / 2);
    mesh.scale.set(item.w, item.h, depth);
  });
}

const game = mountGame(canvas, () => {}, state => {
  show([state.player], pools[0], materials[0], 22);
  show(state.enemies, pools[1], materials[1], 28);
  show(state.bullets, pools[2], materials[2], 8);
  status.textContent = `${state.score} points · ${Math.ceil(state.remaining)} s · ${state.status === 'playing' ? 'En cours' : state.status === 'won' ? 'Victoire' : 'Fin de partie'}`;
  renderer.render(scene, camera);
});
document.querySelector('#restart').onclick = () => game.restart();
document.querySelector('#resume').onclick = () => game.resume();
document.querySelector('#pause').onclick = () => game.pause();
function cleanup() {
  game.destroy();
  viewpoint.removeEventListener('input', updateCamera);
  geometry.dispose();
  materials.forEach(material => material.dispose());
  renderer.dispose();
}
window.addEventListener('pagehide', cleanup, {once: true});
if (import.meta.hot) import.meta.hot.dispose(cleanup);
