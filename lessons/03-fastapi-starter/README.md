# FastAPI · 01-create

```sh
uv sync --locked
uv run python -m todo.init_db
uv run pytest -q
uv run uvicorn todo:create_app --factory --reload --port 8000
```

Attendu : **14 passed**. todo/__init__.py contient la factory, à côté de schemas.py, models.py, database.py et init_db.py. Aucun todo/todo/ supplémentaire.

`tests/__init__.py` est vide, à côté de `conftest.py` ou `test_app.py`. Aucun marker à la racine, aucun `tests/tests/`. Lancer les commandes au niveau de `pyproject.toml`.

Ce starter sait lister et créer. Lancer `uv run pytest tests/exercise_contract.py -q` pour observer le test rouge, puis ajouter GET individuel, PATCH et DELETE. Compléter avec des tests invalides et manquants. Le contrat est conservé, la database est indépendante de Flask.
