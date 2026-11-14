# Démo optionnelle · Le rendu 3D

À utiliser seulement si le groupe a de l'avance. Cette démo ajoute Three.js à un projet séparé ; il n'est pas nécessaire pour l'atelier Canvas ou le projet final.

```sh
npm ci
npm test
npm run dev
```

Ouvrir `http://127.0.0.1:5176`. Cliquer dans le jeu, utiliser les flèches et espace. Reprendre après une perte de focus. `npm run build` produit la version autonome ; 10 tests vérifient la simulation et les controls.

`game.js` conserve des coordonnées et collisions 2D. `main.js` les affiche avec une `Scene`, une `OrthographicCamera`, des `Mesh`, une géométrie partagée et des matériaux éclairés. La caméra inclinée montre le volume. Ce changement de rendu ne crée pas une physique 3D.

Question à faire expliquer : quelle responsabilité change et quelles assertions restent valables ? Comparer le rectangle Canvas et le Mesh. Inspecter le cleanup : boucle annulée, géométrie, matériaux et renderer libérés. Aucun asset distant ni texture à télécharger pendant la démo.

## Objectif et exercice de caméra (10–15 minutes, optionnel)

Cette démo enseigne un changement de représentation, pas une simulation 3D. Les positions et collisions restent dans game.js en 2D ; main.js transforme l’état en volumes éclairés. C’est un rendu 3D avec un gameplay en 2D (2.5D). Une simulation 3D exigerait de nouveaux déplacements, collisions et tests sur trois axes.

Dans le fichier existant `src/main.js`, remplacer la déclaration de camera et ses deux lignes de position/orientation par :

```javascript
const camera = new THREE.PerspectiveCamera(
  50, WIDTH / HEIGHT, 1, 2000,
);
camera.position.set(300, -300, 650);
camera.lookAt(0, 0, 0);
```

50 est le field of view vertical en degrés, WIDTH/HEIGHT l’aspect ratio, 1 et 2000 les distances de clipping. Comparer au rendu OrthographicCamera initial : les volumes et tailles apparentes changent avec la distance. Les mêmes 10 tests restent verts (`npm test`), car aucune règle du jeu n’a changé. Expliquer pourquoi la caméra ne change pas la collision ; cela montre la séparation entre état, règles et rendu. Pour revenir, reprendre les trois lignes du checkpoint. Aucun nouveau fichier ou asset externe n’est nécessaire.
