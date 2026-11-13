# 00-ready : Un projet Python

Branche : `flask-00-ready`. Ce dossier contient le code complet à la fin de cette étape.

## Démarrer

Python 3.12 et uv sont nécessaires. Depuis la racine de ce dossier :

```sh
uv sync --locked
uv run python --version
```

Résultat attendu : **Python 3.12.x ; aucune dépendance applicative.**

Fichiers introduits ou modifiés : pyproject.toml, .python-version.

## Se repérer

L’atelier avance dans cet ordre : 00-ready, 01-flask, 02-pytest, 03-route, 04-template, 05-name, 06-fixtures, 07-test-quality, 08-json.

Avec le bundle Git, `git log --oneline` et `git diff HEAD~1` montrent la modification depuis l’étape précédente (sauf 00-ready, qui est le point de départ).
Une archive ZIP contient la même étape sans historique Git.

Pour reprendre une étape dans un dossier indépendant sans effacer le travail en cours, depuis le dépôt cloné :

```sh
git worktree add --detach ../reprise-00-ready origin/flask-00-ready
cd ../reprise-00-ready
uv sync --locked
```

## Étape suivante

Installer Flask, puis créer app.py.
