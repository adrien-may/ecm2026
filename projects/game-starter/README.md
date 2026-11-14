# Votre projet · Point de départ

Le jeu Canvas et son montage React fonctionnent. Le backend sait lire un classement vide. **L'enregistrement n'est pas encore implémenté** : c'est le premier trajet à terminer, avant d'ajouter des effets visuels.

## Lancer

Dans `backend/` : `uv sync --locked`, `uv run pytest -q` (1 passed), puis `uv run uvicorn scores:create_app --factory --reload --port 8001`.

Dans `frontend/` : `npm ci`, `npm test` (14 tests), puis `npm run dev`. Ouvrir `http://127.0.0.1:5175`. Chaque terminal reste dans son dossier.

## Premier trajet complet

1. Dans `backend/tests/test_scores.py`, écrire un test : POST un score, vérifier 201, puis GET et vérifier les données. Constater son échec.
2. Dans `backend/scores/__init__.py`, ajouter le POST en utilisant le schema et le modèle fournis. Faire passer le test, puis tester un score invalide sans écriture.
3. Dans `frontend/src/main.jsx`, ajouter le formulaire de pseudo après la fin, le POST, les états saving/saved/error puis la relecture du classement. `src/api.js` est fourni.
4. Redémarrer le backend et relire le score. Conserver un test de cette propriété.
5. Ajouter une modification personnelle limitée du jeu ou de la ressource ; adapter les tests et les limites du contrat si nécessaire.

Parcours commun : conserver le backend FastAPI + SQLAlchemy fourni. Le support séparé d’approfondissements propose ensuite l’option NestJS : utiliser le checkpoint `nest-01-memory` puis `nest-02-sqlite` comme support à la place du backend Python. Le frontend reçoit seulement une autre `VITE_API_URL`. Les comportements attendus restent les mêmes.

## Exactement deux markers Python

`backend/scores/__init__.py` contient le package applicatif. `backend/tests/__init__.py` est vide, à côté de `test_scores.py`. Il n'y a aucun marker dans `backend/`, `frontend/`, `instance/`, ni de second dossier `scores/` imbriqué. Les commandes Python sont lancées dans `backend/`, au niveau de `pyproject.toml`.

Le dossier `game-reference` montre un résultat complet. Vous pouvez le lire, mais devez expliquer et modifier ce que vous utilisez. Le brief et les attentes de présentation sont dans `assessments/02-game.md` du kit de cours.
