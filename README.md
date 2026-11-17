# 01-flask : Une application Flask

Branche : `flask-01-flask`. Ce dossier contient le code complet à la fin de cette étape.

## Démarrer

Python 3.12 et uv sont nécessaires. Depuis la racine de ce dossier :

```sh
uv sync --locked
uv run python --version
uv run flask --app app:app run --debug --port 5001
```

Résultat attendu : **GET /bonjour renvoie 404 : aucune route ne traite encore cette URL.**

Fichiers introduits ou modifiés : app.py, pyproject.toml, uv.lock.

## Se repérer

L’atelier avance dans cet ordre : 00-ready, 01-flask, 02-pytest, 03-route, 04-template, 05-name, 06-fixtures, 07-test-quality, 08-json.

Depuis un clone du [dépôt GitHub](https://github.com/adrien-may/ecm2026), `git log --oneline` affiche l’historique. Comparer deux étapes : `git diff origin/flask-00-ready origin/flask-01-flask`.
Une archive ZIP contient la même étape sans historique Git.

Pour reprendre une étape dans un dossier indépendant sans effacer le travail en cours, depuis le dépôt cloné :

```sh
git worktree add --detach ../reprise-01-flask origin/flask-01-flask
cd ../reprise-01-flask
uv sync --locked
```

## Étape suivante

Installer pytest et tester la construction de l’application.
