# Ouverture 3D · Déplacer la caméra

Une démo de cinq minutes après le jeu Canvas : voir le même jeu en volume, changer le point de vue et reprendre la partie. Le projet est fourni dans le checkpoint `canvas-05-three` ; aucune intégration Three.js n’est à écrire pendant le cours.

## Lancer la démo

Extraire `three-demo.zip` à part et ouvrir un terminal dans le dossier `three-demo/`, celui qui contient le fichier fourni `package.json`.

```sh
npm ci
npm test
npm run dev
```

Ouvrir http://127.0.0.1:5176. Mettre en pause, déplacer le slider **Point de vue**, puis reprendre. Cliquer dans le jeu pour utiliser les flèches et espace. Après une perte de focus, cliquer sur Reprendre. Le slider fonctionne aussi avec les flèches lorsqu’il a le focus.

Comparer les deux vues pendant la pause : les objets gardent leurs positions et le score reste le même. Reprendre et tirer pour retrouver le jeu connu. La caméra ne bouge que lorsqu’on déplace le slider.

## Se repérer dans le code fourni

- `src/game.js` : les mêmes règles et collisions que dans le jeu Canvas, sur un plan.
- `src/main.js` : le rendu Three.js, les volumes éclairés et la caméra. `updateCamera()` déplace et oriente la caméra à partir du slider.
- `index.html` : le slider et les boutons de la démo.

Les **10 tests** vérifient les règles et les controls. Vérifier dans le navigateur que le slider change bien l’image, y compris en pause, sans changer le score. `npm run build` produit la version autonome. Aucun asset distant ni texture à télécharger pendant la démo.

Le rendu est en 3D ; les règles du jeu restent sur un plan. Cette ouverture montre qu’on peut changer la représentation d’un jeu déjà fonctionnel. Ensuite, reprendre `game-starter/` pour construire l’aller-retour du score avec le backend ; la démo reste un projet séparé.
