# Jour 2 · Le même contrat avec FastAPI

Cette solution complète remplace les routes JSON de Flask. Le client et le contrat `/tasks/` restent identiques. Le SSR a été étudié et conservé dans le projet Flask ; il n'est pas réimplémenté ici.

```sh
uv sync --locked
uv run python -m todo.init_db
uv run pytest -q
uv run uvicorn todo:create_app --factory --reload --port 8000
```

Attendu : **25 passed**. Ouvrir `http://localhost:8000/docs` pour essayer les requests, puis utiliser le client React avec `VITE_API_URL=http://localhost:8000`. Redémarrer Vite après ce changement. La nouvelle database `instance/fastapi-todo.sqlite` ne contient pas les tasks créées sous Flask.

## Checkpoints

| Branche | Livré | Attendu |
| --- | --- | --- |
| `fastapi-00-app` | Installer FastAPI/Uvicorn puis pytest/HTTPX ; route `/health` | 1 passed |
| `fastapi-01-create` | Package, SQLAlchemy fourni, GET collection et POST validé | 14 passed |
| `fastapi-02-crud` | GET individuel, PATCH partiel et DELETE | 25 passed |

Le starter de l'exercice est aussi dans `../03-fastapi-starter`. Depuis le checkpoint 01 : `uv run pytest tests/exercise_contract.py -q` lance explicitement le premier test à faire passer. Écrire également des cas invalides et manquants. Le corrigé n'est pas le point de départ de l'évaluation.

## `__init__.py` : emplacement exact

```text
projet/                  ← lancer les commandes ici ; aucun marker ici
├── pyproject.toml
├── todo/
│   ├── __init__.py       ← create_app ; rend todo importable comme package
│   ├── database.py
│   ├── init_db.py
│   ├── models.py
│   └── schemas.py
└── tests/
    ├── __init__.py       ← vide, convention explicite du cours
    ├── conftest.py
    ├── test_tasks.py
    └── test_persistence.py
```

Ne pas créer `todo/todo/`, `tests/tests/` ou un marker à la racine. `python -m todo.init_db` permet à Python de résoudre les imports relatifs du package. Ne pas lancer `python todo/init_db.py`. pytest pourrait découvrir des tests sans marker, mais nous gardons ici un package de tests explicite. Les namespace packages ne sont pas utilisés dans cet atelier.

## Lire les responsabilités

- `schemas.py` valide les bodies et décrit les responses. Les annotations Python seules ne valident pas n'importe quel appel de fonction : Pydantic intervient à la frontière HTTP.
- `models.py` décrit la table SQLAlchemy. Ce modèle ORM n'est pas le schema de request.
- `database.py` crée l'engine. La factory reçoit un autre URL SQLite pendant les tests, avant toute connexion.
- `Depends(get_session)` fournit une session par request. `with Session(...)` assure sa fermeture. Les routes restent `def` car les opérations SQLAlchemy utilisées sont synchrones.
- `exclude_unset=True` conserve la différence entre champ omis et champ fourni. Le validator de `TaskPatch` rejette un objet vide et les valeurs explicitement `null`.
- Le client HTTPX utilise `response.json()` ; le client Flask utilisait la propriété `response.json`.

Le pin Starlette stabilise l'API du test client utilisée dans le cours. Les lockfiles fixent aussi les versions transitives. Une deprecation warning provenant d'AnyIO/Starlette peut apparaître avec ce jeu de versions ; elle ne correspond pas à un test échoué.

Pour reprendre sans écraser son code : extraire le ZIP dans un nouveau dossier, ou `git worktree add ../reprise origin/fastapi-01-create` depuis le clone du bundle du cours.
