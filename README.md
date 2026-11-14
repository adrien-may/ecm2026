# flask-07-test-quality

Parametrize, test de comparaison, template signal et régression volontaire.

## Lancer ce checkpoint

Ouvrir ce dossier dans l’éditeur. Lancer depuis la racine qui contient `pyproject.toml` :

```sh
uv sync --locked
uv run pytest -q
uv run flask --app app:create_app run --debug --port 5001
```

Résultat attendu : **7 passed**. La page `/bonjour?name=Samira` reste disponible.

## Fichiers et packages

`app.py` est un module autonome ; aucun package todo à ce stade. `tests/__init__.py` existe et reste vide. Les fichiers de tests sont directement dans `tests/`, y compris `conftest.py` et `test_template_signal.py`. Aucun `__init__.py` à la racine du projet, dans `templates/` ou dans `instance/`.

`captured_templates` écoute `template_rendered` pour cette app pendant le test, puis se désabonne dans finally. Le test vérifie le template choisi et son context ; il ne remplace pas les assertions sur le HTML reçu. Blinker est déjà une dépendance de Flask.

Les étapes 09–12 stockent les tasks en mémoire. À partir de 13, `init-db` crée les tables absentes dans `instance/flask-todo.sqlite`, sans effacer les données existantes. Les tests utilisent des fichiers temporaires isolés. Aux étapes 15 et 16, les mêmes 33 tests restent verts.

Pour reprendre, décompresser un ZIP dans un nouveau dossier ou créer un worktree depuis le bundle. Ne pas écraser un travail en cours. Après tout changement de checkpoint, relancer `uv sync --locked`.

## Expérience de régression

Dans `templates/hello.html`, remplacer `<h1>Bonjour {{ name }}</h1>` par `<h1>Bonjour</h1>`. `uv run pytest -q -k matches_its_template` et `uv run pytest -q -k uses_expected_template` restent verts (1 passed chacun). `uv run pytest -q -k displays_requested_name` donne 2 failed : le HTML ne satisfait plus le besoin du visiteur. Restaurer la ligne initiale pour retrouver 7 passed.
