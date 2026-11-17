# 02-pytest : Notre premier test

Branche : `flask-02-pytest`. Ce dossier contient le code complet à la fin de cette étape.

## Démarrer

Python 3.12 et uv sont nécessaires. Depuis la racine de ce dossier :

```sh
uv sync --locked
uv run python --version
uv run pytest -q
uv run flask --app app:app run --debug --port 5001
```

Résultat attendu : **1 passed. Ce test vérifie la construction de Flask, pas une page web.**

Fichiers introduits ou modifiés : tests/test_app.py, pyproject.toml, uv.lock.

## Se repérer

L’atelier avance dans cet ordre : 00-ready, 01-flask, 02-pytest, 03-route, 04-template, 05-name, 06-fixtures, 07-test-quality, 08-json.

Depuis un clone du [dépôt GitHub](https://github.com/adrien-may/ecm2026), `git log --oneline` affiche l’historique. Comparer deux étapes : `git diff origin/flask-01-flask origin/flask-02-pytest`.
Une archive ZIP contient la même étape sans historique Git.

Pour reprendre une étape dans un dossier indépendant sans effacer le travail en cours, depuis le dépôt cloné :

```sh
git worktree add --detach ../reprise-02-pytest origin/flask-02-pytest
cd ../reprise-02-pytest
uv sync --locked
```

## Étape suivante

Écrire le test de GET /bonjour : il doit échouer avec 404.

## Où placer `__init__.py` ?

Le fichier vide `tests/__init__.py` se trouve directement dans `tests/`, à côté de `test_app.py` et, à partir de 06, de `conftest.py`. Il fait de `tests/` un package Python explicite. Ne pas créer `tests/tests/__init__.py`.

`app.py` est un module, pas un dossier package : aucun `__init__.py` à la racine du projet. Le dossier HTML `templates/` n’en a pas besoin. Pytest peut découvrir des tests sans ce fichier ; l’atelier utilise un package explicite pour que ses imports soient prévisibles.
