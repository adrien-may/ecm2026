# FastAPI · 00-app

```sh
uv sync --locked
uv run pytest -q
uv run uvicorn app:app --reload --port 8000
```

Attendu : **1 passed**. app.py est un module unique : aucun marker à la racine.

`tests/__init__.py` est vide, à côté de `conftest.py` ou `test_app.py`. Aucun marker à la racine, aucun `tests/tests/`. Lancer les commandes au niveau de `pyproject.toml`.

Ouvrir /health puis /docs.
