# Client React de référence

Ce client respecte les appels de la todo du cours précédent, avec une URL configurable, des erreurs visibles et une vérification de `response.ok`.

```sh
npm ci
npm test
npm run dev
```

Ouvrir `http://127.0.0.1:5173`. Par défaut : Flask sur `http://localhost:5001`. Pour FastAPI : copier `.env.example` en `.env.local`, remplacer la valeur par `http://localhost:8000`, puis redémarrer Vite. On peut aussi utiliser `VITE_API_URL=http://localhost:8000 npm run dev` sous macOS/Linux ; sous PowerShell : `$env:VITE_API_URL="http://localhost:8000"` puis `npm run dev`.

Attendu : **4 tests passent**, `npm run build` produit `dist/`. Le navigateur doit créer, terminer, supprimer et relire les tasks avec chacun des deux backends. Le changement d'URL sélectionne aussi une autre database ; une liste vide est donc possible.

## Diagnostic visible

1. Le backend répond-il sur `/tasks/` dans un navigateur ?
2. Quelle URL React appelle-t-il dans Network ?
3. Le status code signale-t-il une erreur HTTP ?
4. Une erreur réseau/CORS apparaît-elle dans la console ?
5. `Content-Type` et le body correspondent-ils au contrat ?

Arrêter le backend après chargement, puis tenter DELETE : une erreur doit apparaître et la task rester visible. Un `204` réussi n'a pas de body JSON. Une erreur réseau après l'envoi d'une écriture peut laisser son résultat incertain ; recharger avant de retenter une création.

Le client utilise du CSS local et React, sans kit d'interface supplémentaire. `src/api.test.js` vérifie les cas où une mauvaise gestion de fetch ferait mentir l'interface.
