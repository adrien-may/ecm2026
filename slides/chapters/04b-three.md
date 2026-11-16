# Le même jeu, vu autrement

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px">
<div><p><strong>De face</strong></p><img src="/screenshots/three-front-view.png" alt="Le jeu en volume vu de face, avec son joueur et ses cibles." style="height: 215px; width: 100%; object-fit: contain" /></div>
<div><p><strong>En déplaçant la caméra</strong></p><img src="/screenshots/three-side-view.png" alt="Le même instant vu de côté : la profondeur des cibles devient visible." style="height: 215px; width: 100%; object-fit: contain" /></div>
</div>

Three.js affiche notre jeu en volume. **La caméra change ce que l’on voit.**

Le jeu reste sur un plan : les collisions et le score suivent les mêmes règles.

<!--
2 min. Ouverture visuelle dans le parcours commun, après Canvas. Les captures montrent exactement le même état en pause. Déplacer la caméra dans la démo prête à lancer, puis demander ce qui a changé. Garder l’explication sur le résultat visible : même jeu, nouveau rendu. Ne pas détailler les paramètres de projection, shaders ou matrices. Three.js est déjà installé dans la démo préparée avant la séance.
-->

---

# Une caméra à déplacer

**Extraire <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/three-demo.zip" download>la démo prête à lancer (.zip)</a> dans un nouveau dossier.**

Terminal : **`canvas-05-three/`**, au niveau du fichier fourni `package.json`.

```sh
npm ci
npm run dev
```

Ouvrir **http://127.0.0.1:5176**. Mettre en pause, déplacer **Point de vue**, puis reprendre et tirer.

Branche **`canvas-05-three`**.

**La suite reprend `game-starter/` : enregistrer et relire le score avec le backend.**

<!--
3 min. L’enseignant prépare la démo avant le cours ; les étudiants peuvent la relancer après. Aucun bloc Three.js à recopier dans l’atelier. Les flèches du clavier peuvent déplacer le slider lorsqu’il a le focus ; cliquer dans le jeu ou sur Reprendre pour rejouer. Montrer deux points de vue du même jeu en pause, puis reprendre la partie. Cette démo sert d’ouverture vers d’autres interfaces possibles ; elle n’ajoute aucune obligation au projet. Revenir explicitement au dossier game-starter pour conserver le fil rouge.
-->
