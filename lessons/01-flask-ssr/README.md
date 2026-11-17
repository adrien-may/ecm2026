# Atelier 01 : construire un backend avec Flask

Nous partons d’un projet Python sans Flask ni pytest. Nous construisons une page, décrivons ses comportements par des tests, puis exposons les mêmes données en JSON. Explications en français, termes techniques en anglais.

**Ce dossier est la solution finale de l’enseignant (`08-json`).** Pour suivre la progression, créer son propre dossier ou commencer à `00-ready` avec les téléchargements ci-dessous.

## Déroulement et points de reprise

À chaque point de synchronisation, lancer la commande, comparer les résultats et les fichiers avec ceux de l’enseignant. Le nombre de tests annoncé est celui de l’état complet.

| Étape | Slides | Ce qui arrive maintenant | Résultat à vérifier | Code complet |
| --- | --- | --- | --- | --- |
| `00-ready` | 10 | Projet Python et uv | Python 3.12.x, aucun package applicatif | [ZIP](../../slides/public/checkpoints/00-ready.zip) |
| `01-flask` | 11–12 | Flask, app.py, serveur local | /bonjour renvoie 404 | [ZIP](../../slides/public/checkpoints/01-flask.zip) |
| `02-pytest` | 13–16 | pytest et une assertion de construction | 1 passed | [ZIP](../../slides/public/checkpoints/02-pytest.zip) |
| `03-route` | 17–20 | Test d’une request, @app.get, première route | 2 passed, page « Bonjour ECM » | [ZIP](../../slides/public/checkpoints/03-route.zip) |
| `04-template` | 21–24 | Jinja et render_template | Toujours 2 passed, même page | [ZIP](../../slides/public/checkpoints/04-template.zip) |
| `05-name` | 25–30 | Query string, variable Jinja, escaping, SSR | 5 passed, prénom selon l’URL | [ZIP](../../slides/public/checkpoints/05-name.zip) |
| `06-fixtures` | 31–38 | @pytest.fixture, puis application factory | Toujours 5 passed | [ZIP](../../slides/public/checkpoints/06-fixtures.zip) |
| `07-test-quality` | 39–47 | @pytest.mark.parametrize, comparaison, template signal et régression | 7 passed après restauration | [ZIP](../../slides/public/checkpoints/07-test-quality.zip) |
| `08-json` | 48–52 | Une seconde route, avec une response JSON | 8 passed, deux représentations | [ZIP](../../slides/public/checkpoints/08-json.zip) |

Ce sont de vraies branches Git nommées `flask-00-ready`, `flask-01-flask`, etc. Chaque ZIP contient aussi un README, un `pyproject.toml` et un `uv.lock` adaptés à cette étape.

## Partir de zéro

Prérequis : Python 3.12, uv, Git et un éditeur. Créer un dossier indépendant du dépôt des supports :

```sh
mkdir ecm26-flask-ssr
cd ecm26-flask-ssr
uv init --bare --python 3.12
uv python pin 3.12
uv run python --version
```

À l’étape 01 seulement :

```sh
uv add flask==3.1.3
```

À l’étape 02 seulement :

```sh
uv add --dev pytest==9.2.0
```

Ajouter alors à `pyproject.toml` :

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

Flask installe ses propres dependencies, dont Jinja. Il n’y a pas d’installation supplémentaire pour les fixtures, le SSR ou la response JSON.

## Où placer `__init__.py` ?

À partir de l’étape 02, créer un fichier **vide**, exactement ici :

```text
ecm26-flask-ssr/
├── app.py
├── pyproject.toml
└── tests/
    ├── __init__.py
    └── test_app.py
```

Les deux fichiers Python sont directement dans `tests/`. Ne pas ajouter un deuxième dossier `tests/`. À l’étape 06, `conftest.py` se place à côté d’eux.

Ce fichier marque un package Python explicite. Pytest peut découvrir des tests sans lui, mais nous utilisons cette structure pour rendre les imports prévisibles. `app.py` reste un module autonome : pas de `__init__.py` à la racine du projet. Le dossier HTML `templates/` n’est pas un package Python et n’en a pas besoin.

Quand nous créerons un package de code `todo/`, son marker sera `todo/__init__.py`, directement à côté des modules qu’il contient. Les éventuels sous-packages auront leur propre marker. Les namespace packages sont une autre possibilité de Python, hors de cet atelier.

## Reprendre sans perdre son travail

Cloner le [dépôt GitHub du cours](https://github.com/adrien-may/ecm2026) à la première étape :

```sh
git clone -b flask-00-ready https://github.com/adrien-may/ecm2026.git mon-backend
cd mon-backend
uv sync --locked
```

Pour changer d’étape lorsque ses modifications sont enregistrées et que `git status` indique un arbre propre :

```sh
git switch flask-03-route
uv sync --locked
uv run pytest -q
```

Si du travail est en cours, créer un dossier indépendant. Le préfixe `origin/` désigne la branche disponible dans le clone :

```sh
git worktree add --detach ../reprise-route origin/flask-03-route
cd ../reprise-route
uv sync --locked
uv run pytest -q
```

Les fichiers précédents restent dans leur dossier. Aucun `reset --hard`, `clean` ou effacement global n’est nécessaire. Pour comparer deux checkpoints : `git diff origin/flask-02-pytest origin/flask-03-route`. Cette comparaison porte sur les deux étapes nommées, même si leur documentation a reçu des commits supplémentaires.

Sans Git : télécharger le ZIP de l’étape, le décompresser dans un **nouveau dossier**, l’ouvrir dans l’éditeur et y lancer `uv sync --locked`. Ne pas écraser son travail avec l’archive.

## Les cycles « rouge, puis vert »

| Changement | Avant l’implémentation | Après l’implémentation |
| --- | --- | --- |
| Première route /bonjour | 1 passed, 1 failed : 404 au lieu de 200 | 2 passed |
| Prénom Samira | 2 passed, 1 failed : « Bonjour ECM » au lieu du prénom demandé | 3 passed |
| Route /api/bonjour | 7 passed, 1 failed : nouvelle URL absente | 8 passed |

Les tests pour Élodie et l’escaping complètent ensuite les comportements. Ils peuvent être verts immédiatement : ce n’est pas du TDD strict pour chaque ligne de l’atelier.

Le passage au template conserve les deux tests précédents. Le passage aux fixtures conserve les cinq cas précédents. Il s’agit de refactors, pas de nouveaux comportements du produit.

## Trois decorators, trois rôles

- `@app.get` enregistre une fonction pour une route HTTP.
- `@pytest.fixture` déclare une préparation que pytest peut fournir aux tests.
- `@pytest.mark.parametrize` exécute un même test avec plusieurs valeurs.

Dans `test_page_displays_requested_name(client, name)`, `client` vient d’une fixture et `name` vient de `parametrize`. Tous les arguments de tests ne sont donc pas des fixtures.

## Expérience de régression à l’étape 07

Les **sept cas** passent avant la manipulation. Dans `templates/hello.html`, remplacer uniquement :

```html
<h1>Bonjour {{ name }}</h1>
```

par :

```html
<h1>Bonjour</h1>
```

Prédire les résultats, puis exécuter les commandes séparément :

```sh
uv run pytest -q -k matches_its_template
uv run pytest -q -k uses_expected_template
uv run pytest -q -k displays_requested_name
```

Le test de comparaison passe : la route et son résultat attendu utilisent le même template modifié. Les deux cas du test de prénom échouent : ils expriment le besoin du visiteur indépendamment du template.

Le test `template_rendered` passe lui aussi : le bon template reçoit encore le bon context, même si le template n’affiche plus le prénom. Il vérifie la liaison route/template ; les assertions sur le HTML vérifient le résultat reçu par le visiteur. Le test de construction de Flask est lui aussi utile à son niveau, mais ne vérifie aucune page.

Restaurer exactement la ligne contenant `{{ name }}`, puis relancer les sept cas. Après l’étape JSON, la suite complète contient **huit cas**.

## Lancer la solution finale de l’enseignant

Depuis ce dossier :

```sh
uv sync --locked
uv run pytest -q
uv run flask --app app:create_app run --debug --port 5001
```

Attendu : **8 passed**. Comparer dans le browser et dans l’onglet Network :

- <http://127.0.0.1:5001/bonjour?name=Samira> : response HTML.
- <http://127.0.0.1:5001/api/bonjour?name=Samira> : response JSON.

Changer le prénom, lire le `Content-Type` et le `body`, puis afficher le code source du document HTML : le serveur a déjà remplacé la variable Jinja. C’est du server-side rendering.

Avant l’étape 06 : `uv run flask --app app:app run --debug --port 5001`.
À partir de 06 : `create_app` construit une application par appel et les fixtures en créent une par test.

## Suite

Une liste de tâches remplacera la salutation. Nous garderons Flask pour le CRUD, la validation, SQLite, les tests isolés et la connexion au frontend React. Cette introduction ne contient pas encore de persistance.

## Capturer le template et son context

Après les fixtures, ajouter `captured_templates` dans `tests/conftest.py` et créer `tests/test_template_signal.py`. Le signal `template_rendered` appelle notre fonction `record` ; elle conserve le template et son context dans une liste fournie au test. `connect(record, app)` limite l’écoute à cette app. Le `finally` appelle `disconnect`, même si une assertion échoue. Blinker est déjà installé avec Flask : aucun nouveau package. Garder `tests/__init__.py` vide, ne pas créer de sous-dossier de tests.
