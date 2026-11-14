# Jour 2 · Canvas, une règle à la fois

```sh
npm ci
npm run dev
```

Ouvrir `http://127.0.0.1:5174`. Les liens montrent quatre états complets. Les ZIPs et branches permettent de ne télécharger que le code déjà étudié.

| Branche | Fichier à lire | Observation |
| --- | --- | --- |
| `canvas-01-draw` | `src/main.js`, `rectangle()` | Un rectangle à x=300, y=350 |
| `canvas-02-animation` | `frame(now)` | 120 pixels par seconde |
| `canvas-03-input` | keydown/keyup + `frame()` | Mouvement limité au Canvas |
| `canvas-04-game` | `game.js`, puis `canvas.js` | Tirs, collisions, fin, pause, restart |

Le projet complet possède **10 tests** (8 de simulation et 2 sur les controls) (`npm test`). Les trois premiers checkpoints n'ont pas de test automatique artificiel : leur résultat se vérifie visuellement. Au quatrième, la logique pure mérite des tests indépendants du rendu.

## Atelier de 90 minutes

10 min : coordonnées et rectangle. 15 min : boucle et `dt`. 15 min : clavier et limites. 20 min : balle, collision et un test rouge. 15 min : états de jeu, score, restart. 15 min : intégration React dans le starter et checkpoint.

À chaque étape, prédire le résultat avant de lancer. Une erreur volontaire `x += 5` par frame permet de discuter de la fréquence d'affichage ; remplacer par `speed * dt`. Le cap à 0,05 seconde évite un saut après suspension et ralentit volontairement le temps simulé en cas de très gros retard. Ce n'est pas une horloge de compétition.

`game.js` contient `newGame`, `advance` et `overlaps`. `advance` ne touche ni DOM ni réseau : mêmes entrées, même résultat. `canvas.js` dessine et gère les events. Une balle ne touche qu'une cible, puis disparaît. Les bords qui se touchent ne comptent pas comme une collision.

Le score donne 10 points par cible, plus les secondes restantes arrondies au-dessus après la dernière cible. Il est compris entre 0 et 90. Une partie dure au maximum 30 secondes de simulation. Le joueur gagne en retirant les six cibles, perd si le temps expire ou si une cible arrive à sa hauteur.

Cliquer dans le Canvas pour les flèches et espace. Les boutons permettent aussi de jouer au pointeur. Une perte de focus de la fenêtre met le jeu en pause : cliquer Reprendre. Le cleanup annule `requestAnimationFrame` et retire les listeners ; le vérifier en démontant puis remontant le composant React.

## Passage à React

Le starter et la référence copient le même `game.js` et le même `canvas.js` pour rester téléchargeables séparément. Un `useEffect` appelle `mountGame(canvas, setState)` et retourne `destroy()`. `useRef` conserve le Canvas et l'instance de jeu. React affiche les formulaires, le résultat et le classement ; il ne reçoit pas 60 mises à jour de state par seconde.

Démo 3D préparée dans `../three-demo`, hors du parcours obligatoire. Elle réutilise exactement les mêmes règles.
