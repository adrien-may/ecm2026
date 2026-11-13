# Projet de référence · Six cibles

Un jeu court, une ressource persistante et des tests lisibles. Ce dossier montre le niveau de finition attendu, pas une invitation à rendre une copie inchangée.

## Deux terminaux

Depuis `backend/` :

```sh
uv sync --locked
uv run pytest -q
uv run uvicorn scores:create_app --factory --reload --port 8001
```

Depuis `frontend/` :

```sh
npm ci
npm test
npm run dev
```

Ouvrir `http://127.0.0.1:5175`. Attendu : 11 tests backend, 14 tests frontend (8 de simulation, 2 sur les controls et 4 du client HTTP). Jouer, attendre une fin, saisir un pseudo et enregistrer. Recharger puis redémarrer le backend : le classement doit conserver le score.

Pour utiliser NestJS, démarrer `lessons/04-nest-scores` sur le port 8002, puis renseigner `VITE_API_URL=http://127.0.0.1:8002` dans `frontend/.env.local` et redémarrer Vite. Le contrat de succès est identique ; NestJS possède sa propre database. Aucun changement de composant n'est nécessaire.

## Arbre Python exact

```text
backend/                 ← commandes ici ; pas de __init__.py ici
├── pyproject.toml
├── scores/
│   └── __init__.py       ← factory, schemas, modèle et routes du petit exemple
└── tests/
    ├── __init__.py       ← vide, convention explicite du cours
    └── test_scores.py
```

Ne pas créer `backend/scores/scores/`. Le dossier `frontend/` n'est pas un package Python. `instance/` contient la database et n'a pas de marker. Cette petite référence garde le backend dans un fichier pour que le trajet entier se lise ; un domaine plus grand motiverait une séparation comme celle du projet todo.

## Contrat des scores

`POST /scores/` reçoit `{"player":"Samira","points":60}` et renvoie `201` avec `id`, `player`, `points`, `created_at`. Le pseudo est nettoyé, de 1 à 24 caractères. Les points sont un integer de 0 à 90 ; booleans, strings numériques et champs supplémentaires sont refusés. `GET /scores/` renvoie au maximum dix scores, par points décroissants puis ID croissant. Les timestamps sont en ISO 8601 UTC. FastAPI renvoie `422` pour une entrée invalide, NestJS `400`.

La database Python est `backend/instance/scores.sqlite`. Les tables absentes sont créées au démarrage de ce petit projet fourni ; ce n'est pas un système de migrations. Les tests utilisent un fichier temporaire par cas, et un test ferme l'application avant de relire les mêmes données.

## Ce que la référence montre

- Jeu au clavier et au pointeur ; pause, fin de partie, restart.
- Séparation simulation / rendu / interface React / HTTP / stockage.
- Un enregistrement explicite après la partie ; chargement et erreur visibles.
- Une écriture confirmée avant d'afficher « enregistré » ; classement relu après succès.
- Validation des entrées, tri, limite et persistance testés.

## Limites à expliquer à l'oral

Le serveur reçoit un score déclaré par le client. Il ne peut pas vérifier que la partie a eu lieu. La validation de format n'est pas un mécanisme anti-cheat. Il n'y a ni comptes, ni rate limiting, ni clé d'idempotence. Après une erreur réseau incertaine, relire le classement avant de retenter pour éviter un doublon. SQLite synchrone convient à cette démonstration locale ; ce choix n'est pas une promesse de capacité en production.
