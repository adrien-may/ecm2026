# Option · Pourquoi passer au rendu 3D ?

**Objectif : séparer les règles du jeu de leur représentation.**

Le moteur 2D garde les positions, déplacements et collisions testés. Three.js transforme cet état en objets éclairés vus par une caméra.

L’exercice porte sur **scene, mesh, camera et projection** : un rendu 3D avec un gameplay en 2D, souvent appelé **2.5D**.

Une vraie simulation 3D demanderait aussi un axe de déplacement, des collisions et des tests en 3D. Ce n’est pas l’objectif de cette option.

---

# Option · Lancer le rendu en volume

**Extraire le ZIP dans un nouveau dossier** ; `src/` et ses fichiers sont fournis.

<a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/three-demo.zip" download>Démo Three.js prête à lancer (.zip)</a>

```sh
npm ci
npm run dev
```

`Scene` + `Camera` + `Mesh` + `Renderer` remplacent le dessin Canvas.

**10 tests restent verts** : huit pour les règles, deux pour les controls.

<!--
Hors des90minutes, seulement si le groupe a du temps. Ouvrir le port5176. Montrer les mêmes coordonnées transformées en positions de Mesh. Les géométries, matériaux et renderer doivent être libérés. Ne pas faire de cette démo un prérequis du projet final.
-->

---

# Option · Changer le point de vue

**Dans le fichier fourni `src/main.js`**, remplacer la déclaration de `camera` et ses deux lignes de position/orientation par :

```javascript
const camera = new THREE.PerspectiveCamera(
  50, WIDTH / HEIGHT, 1, 2000,
);
camera.position.set(300, -300, 650);
camera.lookAt(0, 0, 0);
```

`50` est le field of view vertical ; `WIDTH / HEIGHT` est l’aspect ratio. `1` et `2000` bornent les distances visibles.

**Observer la profondeur et la taille apparente**, puis lancer `npm test` : les règles du jeu n’ont pas changé.

---

# Option · Mêmes règles, deux projections

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">
<div><p><strong>OrthographicCamera</strong></p><img src="/screenshots/three-orthographic.png" alt="Caméra orthographique : les cibles gardent la même taille apparente." /></div>
<div><p><strong>PerspectiveCamera</strong></p><img src="/screenshots/three-perspective.png" alt="Caméra en perspective et décalée : volume visible et tailles apparentes différentes avec la distance." /></div>
</div>

**À expliquer :** pourquoi la caméra change-t-elle l’image sans changer une collision dans `game.js` ?

<!--
Les captures illustrent deux projections et positions de caméra à des instants différents de la démo ; elles ne constituent pas une comparaison pixel à pixel du même état. Pour apprendre les règles d’un jeu 3D, cet exercice ne suffit pas. Son intérêt ici est l’adaptateur de rendu : réutiliser la logique testée, changer la représentation et discuter de sa lisibilité.
-->
