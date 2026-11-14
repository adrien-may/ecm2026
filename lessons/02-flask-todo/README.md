# Jour 1 · Une todo API persistante et structurée

Continuer après `flask-08-json`. Nous conservons `/bonjour`, son template et les huit tests du premier atelier. Le nouveau besoin vient du client React : gérer des tasks.

## Démarrer le résultat final

Depuis ce dossier :

```sh
uv sync --locked
uv run flask --app todo:create_app init-db
uv run flask --app todo:create_app run --debug --port 5001
```

Dans un second terminal, au même endroit : `uv run pytest -q` → **35 passed**. Ouvrir `http://localhost:5001/bonjour` puis `http://localhost:5001/tasks/`. `init-db` crée les tables absentes sans effacer les tasks. Le fichier de développement est `instance/flask-todo.sqlite`. Les tests créent chacun un autre fichier dans un dossier temporaire.

## Avancer ensemble

| Branche | Besoin / changement | Vérification |
| --- | --- | --- |
| `flask-09-list` | GET collection vide, aucun nouveau package | 9 passed |
| `flask-10-create` | POST, validation explicite, erreurs JSON | 20 passed |
| `flask-11-crud` | Lire une task, PATCH partiel, DELETE | 31 passed |
| `flask-12-package` | Déplacer le code sans changer le comportement | 31 passed |
| `flask-13-sqlite` | Installer Flask-SQLAlchemy, conserver les tasks | 32 passed |
| `flask-14-cors` | Installer Flask-CORS, connecter React | 33 passed |
| `flask-15-marshmallow` | Installer Marshmallow, remplacer validation et serialization | Les mêmes 33 tests |
| `flask-16-blueprint` | Regrouper les routes avec Blueprint et les enregistrer | Les mêmes 33 tests |
| `flask-17-openapi` | Flask-smorest, arguments/response, OpenAPI et Swagger UI | 35 passed |

Les ZIPs sont liés dans les slides et dans le catalogue des checkpoints. Chaque branche contient le projet entier et son `uv.lock`. Après chaque changement de checkpoint : `uv sync --locked`, puis les commandes de son README. Pour récupérer sans écraser un travail local, utiliser un nouveau dossier depuis le ZIP ou `git worktree add ../reprise origin/flask-11-crud` depuis un clone du bundle.

Les checkpoints en mémoire perdent les tasks à chaque redémarrage. Ce défaut est volontaire et motive SQLite. Ne pas lancer plusieurs workers avec cette version en mémoire.

## `__init__.py` : le déplacement du checkpoint 12

Avant, `app.py` était un module unique. Après le refactor :

```text
ecm26-flask-todo/          ← dossier du projet, PAS de __init__.py ici
├── pyproject.toml
├── todo/                 ← package Python importé par « from todo import … »
│   ├── __init__.py        ← contient create_app ; pas un second todo/ imbriqué
│   ├── models.py         ← ajouté seulement au checkpoint 13
│   ├── schemas.py        ← ajouté au checkpoint 15, même niveau
│   ├── tasks.py          ← ajouté au checkpoint 16, même niveau
│   └── templates/        ← fichiers HTML ; PAS de __init__.py ici
│       └── hello.html
└── tests/
    ├── __init__.py        ← vide ; convention explicite de ce cours
    ├── conftest.py
    ├── test_app.py
    ├── test_template_signal.py
    ├── test_openapi.py      ← ajouté au checkpoint 17
    ├── test_tasks.py
    └── test_persistence.py
```

Déplacer `app.py` vers `todo/__init__.py`, déplacer `templates/` dans `todo/`, changer l'import de la fixture en `from todo import create_app`. Ne pas garder un ancien `app.py` qui continuerait à lancer une autre application. Lancer les commandes depuis le dossier qui contient `pyproject.toml`, **pas depuis `todo/`**.

Nous utilisons des packages Python classiques : chaque dossier importable choisi comme package porte son `__init__.py`. Python possède aussi des namespace packages sans ce fichier ; ils ne sont pas utilisés ici. pytest peut découvrir des tests sans marker, mais notre `tests/__init__.py` rend la convention d'import explicite. Un fichier nommé `__init__py`, `_init_.py` ou `__init__.py.txt` ne convient pas.

## SQLite, ORM et transaction

Le modèle `Task` décrit une table, ses attributs des colonnes, son `id` une primary key. L'ORM traduit les opérations Python en SQL. `db.session.add()` prépare une écriture ; `commit()` termine la transaction et rend l'écriture durable. La session de Flask-SQLAlchemy est retirée à la fin du contexte ; une écriture non validée n'est pas un succès à annoncer au client.

La configuration de test arrive **avant** `db.init_app(app)`. Le test de persistance ferme la première connexion, recrée une application puis relit le fichier. Le test de PATCH vérifie aussi une seconde task : modifier la mauvaise ligne ferait échouer le test.

`create_all()` crée des tables absentes, il ne fait pas de migration de schéma. Si l'on modifie les colonnes d'une application déjà utilisée, il faudra introduire un outil de migration. Ne pas supprimer la database de développement pour faire passer des tests.

## Brancher React

Dans `projects/todo-client`, démarrer avec `VITE_API_URL=http://localhost:5001`. CORS autorise les origins de développement sur le port 5173. Origin = scheme + host + port ; `localhost` et `127.0.0.1` sont deux origins. CORS est une règle appliquée par le navigateur, pas une authentification ni une protection contre curl.

Essai attendu : créer deux tasks, terminer la première, supprimer la seconde, recharger la page, redémarrer Flask et relire. Arrêter Flask doit afficher une erreur dans React sans faire disparaître artificiellement les données.

## Marshmallow puis Blueprint

`todo/schemas.py` décrit les champs HTTP. Flask parse le JSON avec `request.get_json()`, puis `TaskSchema.load()` valide et prépare les données avant toute mutation. `dump()` transforme le modèle en dictionnaire ; il ne valide pas la sortie. `dump_only` réserve les champs attribués par le backend. `TaskPatchSchema(partial=True)` accepte les champs absents mais refuse une modification vide ; le hook du boolean empêche la conversion de `0` ou `"false"`.

`todo/tasks.py` contient les cinq routes et leur helper de recherche. `tasks_blueprint` utilise le prefix `/tasks`. Au checkpoint 16, dans `todo/__init__.py`, `app.register_blueprint(tasks_blueprint)` les ajoute à l’app ; les handlers d’erreurs, CORS, la commande `init-db` et les routes SSR/JSON de salutation restent dans la factory. Ce premier Blueprint fait partie de Flask : aucune dépendance supplémentaire au checkpoint 16.

Les fichiers `schemas.py` et `tasks.py` sont des modules dans le package `todo` existant. Ne pas créer `schemas/`, `tasks/`, ni de nouveaux `__init__.py`. Les 33 tests de `flask-14-cors` sont conservés à l’identique aux checkpoints 15 et 16. Le même fichier SQLite est réutilisé sans migration ni suppression.

Le parcours reprend les patterns de l’ancien support : serialization, validation, regroupement et registration du CRUD. `SQLAlchemyAutoSchema` reste une piste de recherche. Flask-smorest est installé au checkpoint 17, après la version explicite du CRUD.

Contrat complet : [todo.md](../../contracts/todo.md). Étape suivante : remplacer Flask par FastAPI en conservant ce contrat.

## OpenAPI et Swagger UI au checkpoint 17

Installer maintenant `uv add flask-smorest==0.47.0`. Le Blueprint vient alors de `flask_smorest`. `@arguments` valide le body et fournit les champs à la fonction ; `@response` appelle `dump()` et décrit le status. `Api` enregistre le Blueprint dans la factory avec `api.register_blueprint()`. Il reste placé avant nos error handlers pour conserver notre format d’erreurs et les headers HTTP.

Le hook `before_request` conserve les règles déjà testées : un PATCH vers un ID absent renvoie 404 avant de lire le body ; un Content-Type incorrect renvoie 415. Les 33 tests précédents restent verts, auxquels s’ajoutent deux tests de documentation.

Après les commandes de lancement ci-dessus, ouvrir <http://localhost:5001/openapi/swagger>. OpenAPI est la specification, accessible sur <http://localhost:5001/openapi/openapi.json>. Swagger UI la présente et permet d’envoyer des requests avec **Try it out**, puis **Execute**. Ces essais écrivent dans la database de développement. Les fichiers UI viennent du CDN jsDelivr (version 5.32.0), donc prévoir Internet au premier chargement. La specification JSON est servie localement.

## Lire une query SQLAlchemy

`db.session` suit les objets et la transaction de l’app courante. `db.select(Task).order_by(Task.id)` décrit la lecture ; `db.session.scalars(query)` l’exécute et fournit les objets Task ; `.all()` les rassemble en liste. La forme `session.query()` appartient à l’API legacy. Notre choix reste la syntaxe actuelle, avec son vocabulaire expliqué avant le GET.

## Distinguer JSON et schema

L’expérience de serialization manuelle montre les guillemets cassés et le boolean Python `False`. `json.dumps` règle l’encodage JSON, mais nous devons encore choisir les attributs. Marshmallow décrit ce choix dans un schema. Le parse JSON de Flask transforme `true` en `True` et `null` en `None` ; `load()` applique ensuite les règles du schema. Notre code construit `Task(**data)`, et `dump()` transforme les attributs d’une Task en dictionnaire.
