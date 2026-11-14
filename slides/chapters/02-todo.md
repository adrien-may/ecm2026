# Jour 1 · Notre React a besoin de tasks

La salutation nous a appris le trajet d’une request.

Nous allons maintenant **lister → créer → modifier → supprimer**.

Puis conserver les données au redémarrage, et connecter React.

Même cycle : besoin, test, implémentation, checkpoint.

<!--
3 min. Revenir au client React des trois premiers jours. Faire nommer une action visible et la request correspondante. Continuer à partir de flask-08-json ; aucune nouvelle installation.
-->

---

# 09 · Lister une collection vide

<div class="lesson-step">09-list</div>

**Créer le fichier** `tests/test_tasks.py`, à côté de `test_app.py` et `conftest.py`.

```python
def test_list_starts_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json == []
```

**ROUGE : 8 passed, 1 failed**, car la route n’existe pas.

<!--
4 min. Créer le fichier directement dans tests/, à côté du marker existant. Les sept tests de la salutation restent présents.
-->

---

# 09 · Le premier GET

<div class="lesson-step">09-list</div>

**Modifier** `app.py` : ajouter ce bloc dans `create_app()`, avant `return app`.

```python
tasks = {}

@app.get("/tasks/")
def list_tasks():
    return list(tasks.values())
```

La factory crée un dictionnaire neuf. **9 tests passent.**

<!--
4 min. Flask convertit la liste en JSON. Le dictionnaire est temporaire ; nous observerons sa limite avant SQLite. Ne pas prétendre que ce GET prouve la persistance.
-->

---

# flask-09-list · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
```

**Résultat attendu : 9 passed.**

Branche `flask-09-list` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/09-list.zip" download>Projet complet (.zip)</a>

Prochain besoin : ajouter une task depuis un body JSON.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# 10 · Créer puis relire

<div class="lesson-step">10-create</div>

**Modifier** `tests/test_tasks.py` : ajouter ce test après le test de liste vide.

```python
def test_create_and_read(client):
    response = client.post("/tasks/", json={"title": "Lire"})
    assert response.status_code == 201
    task = response.json
    assert task["title"] == "Lire"
    assert task["done"] is False
    assert client.get("/tasks/").json == [task]
```

La route manque : le nouveau test échoue. `201` signifie « créé ».

<!--
5 min. Écrire cette version courte d’abord. Le checkpoint étend le test avec un titre nettoyé, un ID integer et un timestamp UTC. json= encode le body et fixe Content-Type.
-->

---

# 10 · D’où viennent les valeurs ?

| Valeur | Responsabilité |
| --- | --- |
| `title` | Le client propose ; le backend valide |
| `id` | Le backend génère un integer |
| `done` | Le backend initialise à `false` |
| `creation_date` | Le backend fixe l’instant en UTC |

Le client ne choisit pas son ID. Deux tasks peuvent avoir le même titre.

<!--
4 min. Montrer le JSON du contrat. Le frontend est contrôlable par son utilisateur : une validation dans un formulaire ne remplace pas celle du backend.
-->

---

# 10 · Préparer la validation du body

<div class="lesson-step">10-create</div>

Avant de créer une task, il faut **lire le body JSON, vérifier ses champs et nettoyer le titre**.

Regroupons ces vérifications dans une fonction que nous appellerons **`read_fields()`**. Elle renverra les champs validés.

**Modifier** `app.py` : compléter les imports tout en haut du fichier.

```python
from datetime import datetime, timezone
from flask import Flask, abort, render_template, request
from werkzeug.exceptions import HTTPException
```

<!--
Partir du besoin avant de nommer la fonction. read_fields est un nom choisi pour notre code, pas une fonction de Flask. request lit le body, abort interrompt une request invalide ; HTTPException permettra ensuite de conserver le format JSON pour les erreurs.
-->

---

# 10 · Écrire read_fields(), première partie

<div class="lesson-step">10-create</div>

**Modifier** `app.py` : ajouter cette fonction après les imports, **avant `create_app()`**, sans l'imbriquer dedans.

```python
def read_fields():
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Expected a JSON object")
    if set(data) != {"title"}:
        abort(400, description="Expected only title")
    return data
```

Pour POST, le body doit être un objet JSON avec le seul champ `title`.

---

# 10 · Compléter la validation du titre

<div class="lesson-step">10-create</div>

**Modifier** `app.py` : dans `read_fields()`, insérer ce bloc **juste avant `return data`**.

```python
    if not isinstance(data["title"], str):
        abort(400, description="title must be a string")
    data["title"] = data["title"].strip()
    if not 1 <= len(data["title"]) <= 255:
        abort(400, description=
              "title must contain 1 to 255 characters")
```

Garder la première partie et le `return data` final. **Une seule fonction `read_fields()`**.


---

# 10 · Préparer des erreurs JSON

<div class="lesson-step">10-create</div>

**Modifier** `app.py` : dans `create_app()`, ajouter **`next_id = 1`** après `tasks = {}`, puis ce handler :

```python
@app.errorhandler(HTTPException)
def http_error(error):
    response = error.get_response()
    response.data = app.json.dumps({"error": error.description})
    response.content_type = "application/json"
    return response
```

`HTTPException` est déjà importé. Le handler conserve les headers de l’erreur.

<!--
5 min. Dans create_app, comme les routes. Nous gardons le status code et les headers de l’erreur, dont Allow pour 405. Ce decorator gère des erreurs HTTP ; ce n’est pas une route et il ne masque pas les exceptions Python ordinaires. Werkzeug est déjà une dépendance de Flask.
-->

---

# 10 · Écrire la route POST complète

<div class="lesson-step">10-create</div>

**Modifier** `app.py` : ajouter cette route dans `create_app()`, après GET et avant `return app`.

```python
@app.post("/tasks/")
def create_task():
    nonlocal next_id
    data = read_fields()
    task = {"id": next_id, "title": data["title"], "done": False,
            "creation_date": datetime.now(timezone.utc).isoformat()}
    tasks[next_id] = task
    next_id += 1
    return task, 201
```

<!--
Indenter tout le bloc de quatre espaces dans create_app. next_id appartient à la factory ; nonlocal permet de l'incrémenter depuis cette route. Le helper read_fields est au niveau du fichier et est maintenant défini avant son premier appel.
-->

---

# 10 · Vérifier aussi les body invalides

**Modifier** `tests/test_tasks.py` : ajouter `import pytest` en haut, puis ce test à la fin.

```python
@pytest.mark.parametrize("data", [
    {}, {"title": " "}, {"title": "x" * 256}, {"title": 1},
    {"title": None}, {"title": "x", "done": True}, [], None,
])
def test_invalid_create_leaves_list_empty(client, data):
    response = client.post("/tasks/", json=data)
    assert 400 <= response.status_code < 500
    assert response.is_json
    assert client.get("/tasks/").json == []
```

<!--
Ce test ajoute huit cas. Avec les huit tests du premier atelier, le GET vide et la création, on obtient 18 cas. Le checkpoint ajoute deux tests et renforce le test de création, annoncés sur la slide suivante.
-->

---

# 10 · Comparer les tests avec le checkpoint

**Ouvrir le fichier fourni** `tests/test_tasks.py` dans <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/10-create.zip" download>flask-10-create (.zip)</a>, extrait dans un autre dossier.

Notre parcours contient maintenant **18 cas**. Le checkpoint en contient **20** :

1. Le test de création vérifie aussi le titre nettoyé, le type de l’ID et la date UTC.
2. Un test crée deux titres identiques avec des ID différents.
3. Un test couvre JSON malformé, mauvais Content-Type et méthode interdite.

**Modifier notre `tests/test_tasks.py`** : reprendre ces ajouts et leurs imports, puis relancer pytest.

---

# flask-10-create · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
```

**Résultat attendu : 20 passed.**

Branche `flask-10-create` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/10-create.zip" download>Projet complet (.zip)</a>

Les cas invalides doivent aussi laisser la liste vide. Ensuite : agir sur un ID.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# 11 · Une URL, une task

| Action | Request | Succès |
| --- | --- | --- |
| Lire | `GET /tasks/7` | `200` + task |
| Modifier un champ | `PATCH /tasks/7` | `200` + task modifiée |
| Supprimer | `DELETE /tasks/7` | `204`, body vide |

`/tasks/` finit par `/`. Une ressource `/tasks/7` n’en a pas.

Un ID absent donne une erreur JSON **404**.

<!--
5 min. Le client inspecté n’utilise pas PUT. Expliquer oralement remplacement complet vs modification partielle. Ne pas compter sur un redirect implicite pour corriger toutes les URL.
-->

---

# 11 · PATCH doit préserver les autres champs

<div class="lesson-step">11-crud</div>

**Modifier** `tests/test_tasks.py` : ajouter ce test complet.

```python
def test_patch_preserves_fields(client):
    task = client.post("/tasks/", json={"title": "Lire"}).json
    other = client.post("/tasks/", json={"title": "Garder"}).json
    url = f"/tasks/{task['id']}"
    response = client.patch(url, json={"done": True})
    assert response.status_code == 200
    assert response.json == {**task, "done": True}
    assert client.get(f"/tasks/{other['id']}").json == other
```

Le nouveau test échoue : nous n'avons encore écrit ni GET par ID, ni PATCH.

---

# 11 · Retrouver une task par son ID

GET, PATCH et DELETE doivent chercher une task et répondre **404** si elle manque. Regroupons cette recherche dans une fonction nommée **`find_task()`**.

**Modifier** `app.py` : ajouter ces fonctions dans `create_app()`, avant `return app`.

```python
def find_task(task_id):
    if task_id not in tasks:
        abort(404, description="Task not found")
    return tasks[task_id]

@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    return find_task(task_id)
```

---

# 11 · Adapter read_fields() pour PATCH

**Modifier** `app.py` : remplacer `read_fields()` par la version complète fournie dans <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/11-crud.zip" download>flask-11-crud (.zip)</a>.

Lire les changements avant de poursuivre :

- Signature : `def read_fields(*, partial=False):`.
- POST garde `partial=False` : seul `title` est accepté.
- PATCH passe `partial=True` : `title` et/ou `done` sont acceptés.
- `{}`, `null`, champs inconnus et valeurs invalides sont refusés.
- Tous les champs sont validés **avant** de modifier la task.

La fonction reste **après les imports, avant `create_app()`**.

---

# 11 · Un paramètre dans le path

<div class="lesson-step">11-crud</div>

**Modifier** `app.py` : ajouter cette route dans `create_app()`, avant `return app`.

```python
@app.patch("/tasks/<int:task_id>")
def update_task(task_id):
    task = find_task(task_id)
    task.update(read_fields(partial=True))
    return task
```

`find_task()` renvoie la task ou appelle `abort(404)`.

Valider **tous** les champs avant de modifier le dictionnaire.

<!--
6 min. Le converter int fournit un integer au paramètre task_id. Lire read_fields(partial=True) : objet non vide, seulement title/done, bool strict ; la string "false" n’est pas False. Montrer le cas done=True et title vide qui ne doit rien modifier.
-->

---

# 11 · DELETE termine sans JSON

<div class="lesson-step">11-crud</div>

**Modifier** `app.py` : ajouter cette route dans `create_app()`, après PATCH.

```python
@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    find_task(task_id)
    del tasks[task_id]
    return "", 204
```

Dans le test : vérifier `204`, le body vide, puis **relire la collection**.

Un test limité au status code pourrait manquer une suppression incorrecte.

<!--
5 min. Ne pas appeler response.json() sur un body vide dans le frontend. Faire ajouter GET individuel avec le même find_task, puis exécuter les tests invalides et les cas 404.
-->

---

# flask-11-crud · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
```

**Reprendre les tests complets** de `tests/test_tasks.py` dans le ZIP : ils couvrent aussi les ID absents, les body invalides et DELETE. **Attendu : 31 passed.**

Branche `flask-11-crud` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/11-crud.zip" download>Projet complet (.zip)</a>

Créer une task puis redémarrer Flask : elle disparaît. Nous allons corriger cette limite.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# 12 · Créer todo/ et déplacer les fichiers

**Créer le dossier** `todo/` à la racine, à côté de `pyproject.toml`.

1. **Déplacer et renommer** `app.py` en **`todo/__init__.py`**. Conserver tout son contenu.
2. **Déplacer le dossier** `templates/` entier dans `todo/`, avec `hello.html`.
3. Garder `tests/` à la racine, avec tous ses fichiers.

Il ne doit plus rester de `app.py` ni de `templates/` à la racine.

La slide suivante montre l'arbre obtenu. Aucun fichier de code n'est jeté.

---

# 12 · Un package, un niveau précis

<div class="lesson-step">12-package</div>

```text
projet/                 ← pas de __init__.py ici
├── pyproject.toml
├── todo/
│   ├── __init__.py      ← l’ancien app.py, avec create_app
│   └── templates/
│       └── hello.html   ← pas de marker dans templates/
└── tests/
    ├── __init__.py      ← vide, à ce niveau exact
    └── conftest.py
```

Ni `todo/todo/`, ni `tests/tests/`. Le nom exact : **`__init__.py`**.

<!--
6 min. Ce slide est un refactor distinct de la database. Déplacer le fichier app.py et le dossier templates, ne pas en garder une copie qui lancerait l’ancienne application. Le marker de todo contient le code, celui de tests est vide. Les autres fichiers test restent directement dans tests/.
-->

---

# 12 · L’import suit le déplacement

<div class="lesson-step">12-package</div>

**Modifier** `tests/conftest.py` : remplacer `from app import create_app` par :

```python
from todo import create_app
```

Depuis le dossier de `pyproject.toml` :

```sh
uv run pytest -q
uv run flask --app todo:create_app run --debug --port 5001
```

Les assertions restent identiques. Aucun nouveau package externe.

<!--
4 min. todo est notre package local, pas un téléchargement. Python a aussi des namespace packages sans marker, hors de ce cours. pytest peut découvrir des tests sans marker ; nous conservons une convention explicite ici. Ne pas lancer la commande depuis todo/.
-->

---

# flask-12-package · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
```

**Résultat attendu : 31 passed.**

Branche `flask-12-package` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/12-package.zip" download>Projet complet (.zip)</a>

Même comportement, nouvelle organisation. Maintenant seulement : SQLite.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# 13 · Constater la perte des données

**Créer le fichier** `tests/test_persistence.py`, dans le dossier `tests/` existant.

```python
from todo import create_app

def test_new_application_reads_committed_data():
    first_app = create_app()
    task = first_app.test_client().post(
        "/tasks/", json={"title": "Persistée"}
    ).json
    second_app = create_app()
    assert second_app.test_client().get("/tasks/").json == [task]
```

<!--
Demander de prédire le résultat. Deux apps neuves simulent le redémarrage : la deuxième possède un dictionnaire vide. Le test ne dépend pas encore de SQLite.
-->

---

# 13 · Un test rouge pour la persistance

**Terminal à la racine du projet** : lancer le nouveau test.

```sh
uv run pytest tests/test_persistence.py -q
```

**Attendu : 1 failed**. La deuxième app renvoie `[]`.

Le besoin : retrouver une task après le redémarrage du backend.

Nous allons conserver les données dans un fichier SQLite.

<!--
Lancer les autres tests reste possible : ils vérifient le contrat HTTP, mais aucun ne prouvait encore la persistance entre deux apps.
-->

---

# 13 · Une table et des transactions

| Python / ORM | Database |
| --- | --- |
| Classe `Task` | Table `task` |
| Une instance | Une row |
| Attribut `title` | Une colonne |
| `id` | Primary key |

`add()` prépare l’écriture ; **`commit()` termine la transaction**.

SQLite stocke les données dans un fichier local.

<!--
Dessiner deux rows. SQLite ne nécessite pas de serveur séparé. Un ORM traduit nos opérations en SQL ; il ne remplace pas la compréhension des transactions.
-->

---

# 13 · Créer le fichier des modèles

**Terminal à la racine** : installer le package devenu nécessaire.

```sh
uv add flask-sqlalchemy==3.1.1
```

**Créer le fichier** `todo/models.py`, à côté de **`todo/__init__.py`**.

Le dossier `todo/` existe déjà. Aucun nouveau dossier, aucun nouveau `__init__.py`.

Les deux slides suivantes remplissent ce nouveau fichier.

---

# 13 · Préparer SQLAlchemy

**Modifier** `todo/models.py`, encore vide : écrire ces imports et définitions.

```python
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
```

`db` décrit l’accès ORM. La connexion à notre app viendra dans la factory.

<!--
Base est la base commune des modèles déclaratifs. db est créé sans app pour pouvoir connecter plusieurs apps, notamment dans les tests. Pas encore de connexion ni de table à cette ligne.
-->

---

# 13 · Décrire la table Task

**Modifier** `todo/models.py` : ajouter cette classe après `db = ...`.

```python
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False)
    creation_date: Mapped[str] = mapped_column(
        default=lambda: datetime.now(timezone.utc).isoformat()
    )
```

La database attribuera l’ID ; le backend choisit la date et `done=False`.

<!--
Mapped indique le type de l’attribut ORM. mapped_column ajoute des options de colonne. lambda reporte le calcul de la date à chaque insertion. La date reste une string ISO UTC, car SQLite ne conserve pas simplement les timezones. Ces types ne valident pas le body HTTP.
-->

---

# 13 · Convertir une task en dictionnaire

**Modifier** `todo/models.py` : ajouter cette méthode **dans `Task`**, sous les champs.

```python
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "creation_date": self.creation_date,
        }
```

Flask sait produire du JSON depuis un dictionnaire. Nous nommons cette conversion `to_dict()`.

<!--
Cette méthode est notre code, pas une fonction fournie par Flask. Elle prépare la représentation de sortie ; elle ne valide aucune request. Garder quatre espaces avant def, huit dans la méthode.
-->

---

# 13 · Préparer les imports de la factory

**Modifier** `todo/__init__.py` : remplacer ses imports par ceux-ci.

```python
from pathlib import Path
from flask import Flask, abort, render_template, request
from werkzeug.exceptions import HTTPException
from .models import Task, db
```

`Path` permet de créer le dossier de données.

`.models` désigne `models.py` dans le package `todo`.

Garder `read_fields()` : la validation du body ne change pas.

---

# 13 · Configurer avant de connecter

**Modifier** `todo/__init__.py` : remplacer le début de `create_app()`, jusqu’à `next_id = 1` inclus.

```python
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///flask-todo.sqlite",
    )
    if test_config:
        app.config.update(test_config)
```

Le dictionnaire `tasks` et le compteur `next_id` disparaissent. Garder les routes en dessous pour les adapter.

<!--
test_config est un argument que nous ajoutons à notre factory. La configuration des tests doit être appliquée avant init_app. Les anciennes routes utilisent encore tasks : attendre leur remplacement avant de relancer le serveur.
-->

---

# 13 · Créer le dossier et connecter l’ORM

**Modifier** `todo/__init__.py` : ajouter ces lignes dans `create_app()`, après le bloc `if test_config`.

```python
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
```

**Le code crée le dossier `instance/`** à la racine du projet.

La commande suivante créera `instance/flask-todo.sqlite`.

`instance/` contient des données, **aucun `__init__.py`**.

<!--
Avec cette URI SQLite relative, Flask-SQLAlchemy utilise app.instance_path. exist_ok=True permet de relancer la factory. Le dossier de développement est ignoré par Git ; les tests pointeront ailleurs.
-->

---

# 13 · Ajouter notre commande init-db

**Modifier** `todo/__init__.py` : ajouter ce bloc dans `create_app()`, juste après `db.init_app(app)`.

```python
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database ready")
```

`@app.cli.command` enregistre une **commande terminal**.

`create_all()` crée les tables absentes, sans modifier les anciennes colonnes.

<!--
Nouveau decorator, distinct de @app.get et @pytest.fixture. Flask fournit automatiquement le contexte de l’app à sa commande. Ce n’est pas une migration. Ne pas effacer les données pour changer un schéma.
-->

---

# 13 · Créer les tables

**Terminal à la racine**, après avoir enregistré les fichiers :

```sh
uv run flask --app todo:create_app init-db
```

**Attendu : `Database ready`**.

Observer le nouveau fichier `instance/flask-todo.sqlite`.

La table existe. Nous allons maintenant adapter chaque opération CRUD.

<!--
La commande peut être relancée : elle ne vide pas la table. Le serveur HTTP attend encore le refactor des routes, mais la commande ne les exécute pas.
-->

---

# 13 · Une session suit notre travail

**`db.session`** relie nos objets Python au travail en database.

- Elle charge et suit les objets `Task` utilisés pendant la request.
- `add()`, les modifications d’attributs et `delete()` préparent des écritures.
- `commit()` termine la transaction et rend ces écritures durables.

Flask-SQLAlchemy retire la session à la fin du contexte de l’app.

Ce n’est ni la session de connexion d’un utilisateur, ni un cookie.

<!--
Une session ORM n’est pas exactement une connexion : elle utilise le moteur pour obtenir une connexion au besoin. Le contexte de request fournit normalement celui de l’app. Dans nos tests hors request, with app.app_context() donne ce contexte explicitement.
-->

---

# 13 · Écrire une task dans SQLite

**Modifier** `todo/__init__.py` : dans `create_app()`, remplacer toute la route POST.

```python
    @app.post("/tasks/")
    def create_task():
        task = Task(**read_fields())
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201
```

`read_fields()` valide avant l’écriture. `commit()` attribue l’ID avant la response.

<!--
Retirer tout l’ancien body, y compris nonlocal next_id. ** déplie le dictionnaire validé en arguments nommés du modèle. Le status code reste 201.
-->

---

# 13 · Lire select, scalars et all

**Ouvrir** `todo/__init__.py` : lire la route de collection que nous allons écrire.

| Expression | Rôle |
| --- | --- |
| `db.select(Task)` | Décrire quelles données lire |
| `.order_by(Task.id)` | Demander un ordre stable |
| `db.session.scalars(query)` | Exécuter et extraire les objets `Task` |
| `.all()` | Rassembler tous les résultats dans une liste |

`execute()` produit des rows ; `scalars()` prend leur première valeur.

<!--
Avec select(Task), chaque row contient un objet Task : scalars extrait cet objet, ce qui évite une liste de tuples à un élément. Il ne force pas la lecture d’un seul résultat. session.query(Task).order_by(Task.id).all() existe encore, mais fait partie de l’API legacy. Nous gardons la forme actuelle commune aux deux frameworks.
-->

---

# 13 · Lire la collection depuis SQLite

**Modifier** `todo/__init__.py` : remplacer toute la route GET de collection.

```python
    @app.get("/tasks/")
    def list_tasks():
        query = db.select(Task).order_by(Task.id)
        tasks = db.session.scalars(query).all()
        return [task.to_dict() for task in tasks]
```

`select()` décrit la lecture ; `scalars(...).all()` retourne les objets `Task`.

`order_by()` rend l’ordre explicite.

<!--
tasks est maintenant une variable locale à cette fonction, pas le dictionnaire de la factory. Une liste vide produit toujours [].
-->

---

# 13 · Retrouver une task par ID

**Modifier** `todo/__init__.py` : remplacer `find_task()` dans `create_app()`.

```python
    def find_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            abort(404, description="Task not found")
        return task
```

Cette fonction existait déjà. Elle lit désormais la database.

Un ID absent produit toujours une response `404` avec un body JSON.

---

# 13 · Lire une seule task

**Modifier** `todo/__init__.py` : remplacer toute la route GET par ID.

```python
    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        return find_task(task_id).to_dict()
```

La recherche fournit un objet `Task` ; `to_dict()` prépare sa représentation JSON.

L’URL et les champs de la response restent identiques.

---

# 13 · Modifier une task dans SQLite

**Modifier** `todo/__init__.py` : remplacer toute la route PATCH.

```python
    @app.patch("/tasks/<int:task_id>")
    def update_task(task_id):
        task = find_task(task_id)
        fields = read_fields(partial=True)
        for key, value in fields.items():
            setattr(task, key, value)
        db.session.commit()
        return task.to_dict()
```

`setattr(task, "done", True)` équivaut à `task.done = True`.

<!--
Valider tous les champs avant de modifier le modèle. read_fields limite les clés à title et done ; sans cela, setattr permettrait de modifier un attribut non autorisé. Conserver le test qui vérifie la seconde task.
-->

---

# 13 · Supprimer une task dans SQLite

**Modifier** `todo/__init__.py` : remplacer toute la route DELETE.

```python
    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        db.session.delete(find_task(task_id))
        db.session.commit()
        return "", 204
```

Le `commit()` rend la suppression durable.

Garder les routes `/bonjour`, `/api/bonjour`, le handler d’erreurs et **`return app`** à la fin de la factory.

---

# 13 · Préparer une database par test

**Modifier** `tests/conftest.py` : ajouter `from todo.models import db`, puis remplacer la fixture `app` par ce bloc.

```python
@pytest.fixture
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 
            f"sqlite:///{tmp_path / 'test.sqlite'}",
    })
```

<!--
Garder import pytest, from todo import create_app et la fixture client. tmp_path est fourni par pytest et change pour chaque test. Le contexte permet à db de trouver cette app hors d’une request. La slide suivante complète cette même fonction après yield.
-->

---

# 13 · Libérer les connexions après le test

**Modifier** `tests/conftest.py` : ajouter ces lignes **dans `app()`**, juste après `app = create_app(...)`.

```python
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.engine.dispose()
```

Garder `client(app)` inchangée. Après `yield`, pytest nettoie après le test.

Vérifier les comportements existants : **`uv run pytest -q --ignore=tests/test_persistence.py` → 31 passed**.

<!--
remove termine la session ; dispose libère les connexions du moteur. Les tests ne touchent pas instance/flask-todo.sqlite. Le nouveau test de persistance doit encore être adapté pour utiliser son propre fichier temporaire.
-->

---

# 13 · Isoler le test de redémarrage

**Modifier** `tests/test_persistence.py` : remplacer tout son contenu par ce début. Les deux slides suivantes complètent la fonction.

```python
from todo import create_app
from todo.models import db
def test_new_application_reads_committed_data(tmp_path):
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 
            f"sqlite:///{tmp_path / 'restart.sqlite'}",
    }
    first_app = create_app(config)
```

<!--
Le même fichier sera utilisé par deux apps, mais un nouveau tmp_path pour chaque exécution du test. Ne pas exécuter un test contre la database de développement.
-->

---

# 13 · Écrire puis fermer la première app

**Modifier** `tests/test_persistence.py` : continuer **la même fonction**, après `first_app = ...`.

```python
    runner = first_app.test_cli_runner()
    assert runner.invoke(args=["init-db"]).exit_code == 0
    task = first_app.test_client().post(
        "/tasks/", json={"title": "Persistée"}
    ).json
    with first_app.app_context():
        db.session.remove()
        db.engine.dispose()
```

Le test utilise notre commande, crée une task, puis libère les connexions.

---

# 13 · Relire avec une nouvelle app

**Modifier** `tests/test_persistence.py` : continuer **la même fonction**, après le bloc `with`.

```python
    second_app = create_app(config)
    try:
        assert second_app.test_client().get("/tasks/").json == [task]
    finally:
        with second_app.app_context():
            db.session.remove()
            db.engine.dispose()
```

`finally` libère la connexion même si l’assertion échoue.

**`uv run pytest -q` → 32 passed** : la nouvelle app relit la même task.

<!--
La première app a fermé ses connexions. Aucune donnée n’est injectée dans la seconde. Le test mesure bien la persistance dans le fichier, pas seulement le fonctionnement d’un dictionnaire partagé.
-->

---

# flask-13-sqlite · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
uv run flask --app todo:create_app run --debug --port 5001
```

**Résultat attendu : 32 passed.**

Branche `flask-13-sqlite` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/13-sqlite.zip" download>Projet complet (.zip)</a>

Créer une task, arrêter Flask, relancer puis relire : elle est encore là.

<!--
Tous les blocs ont été construits dans les slides. Utiliser le ZIP pour comparer ou reprendre dans un nouveau dossier, sans écraser son travail. Le passage à SQLite garde les huit tests SSR/JSON du début et tous les tests CRUD.
-->

---

# 14 · Deux origins dans le navigateur

React : `http://localhost:5173`

Flask : `http://localhost:5001`

Même machine, **origins différentes** : scheme + host + port.

Le navigateur applique CORS. Un `curl` qui fonctionne ne prouve pas que CORS est correct.

<!--
5 min. Expliquer le preflight OPTIONS provoqué notamment par Content-Type application/json et PATCH. Le backend doit autoriser l’origin, les méthodes et les headers. CORS n’est pas un système de comptes ou de permissions.
-->

---

# 14 · Autoriser notre client

<div class="lesson-step">14-cors</div>

```sh
uv add flask-cors==6.0.1
```

**Modifier** `todo/__init__.py` : dans `create_app()`, après la configuration.

```python
CORS(app, resources={r"/tasks/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
}})
```

Importer `CORS` depuis `flask_cors`. Tester une origin autorisée et une autre.

<!--
5 min. Le fichier complet lit les origins depuis app.config pour pouvoir les adapter. localhost et 127.0.0.1 sont différents. Éviter un wildcard sans explication.
-->

---

# flask-14-cors · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
```

**Résultat attendu : 33 passed.**

Branche `flask-14-cors` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/14-cors.zip" download>Projet complet (.zip)</a>

Connecter votre React ou le client de référence. Vérifier toute une interaction.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# 14 · Même frontend, URL configurable

**Extraire le ZIP `todo-client` dans un nouveau dossier**, puis ouvrir ce dossier dans le terminal :

```sh
npm ci
VITE_API_URL=http://localhost:5001 npm run dev
```

Ouvrir `http://127.0.0.1:5173`.

<a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/todo-client.zip" download>Client React complet (.zip)</a>

Créer deux tasks, en terminer une, supprimer l’autre, recharger.

<!--
8 min. Sous PowerShell : $env:VITE_API_URL="http://localhost:5001" puis npm run dev. Une alternative commune consiste à copier .env.example en .env.local. Redémarrer Vite après modification des variables. Le client historique peut être conservé : adapter seulement son URL et vérifier response.ok.
-->

---

# 14 · Un DELETE échoué ne supprime rien

**Ouvrir le fichier fourni** `todo-client/src/api.js` : observer le contrôle de `response.ok` dans `request()`.

```javascript
const response = await fetch(url, {method: 'DELETE'});
if (!response.ok) throw new Error('Suppression impossible');
// Retirer la task de React seulement après ce succès.
```

`fetch()` ne rejette pas automatiquement une response HTTP `500`.

Arrêter le backend : le client doit expliquer l’erreur et conserver la liste.

<!--
7 min. Faire observer Network, status code et body. Une response 204 est sans JSON à parser. Une erreur réseau après une écriture peut laisser son résultat incertain : recharger avant de retenter aveuglément une création. Le chapitre suivant garde le même client.
-->

---

# Notre backend fonctionne · Quelle suite ?

Tracer : clic → request → route → validation → database → response.

Montrer le test qui attrape la modification du mauvais ID.

Placer `todo/__init__.py` et `tests/__init__.py` sans regarder le corrigé.

Le CRUD fonctionne. Maintenant : **rendre sa validation et son organisation plus faciles à relire.**

<!--
Transition vers Marshmallow et Blueprint, avant le bilan du jour 1. Les mêmes tests serviront de garde-fous pendant les deux refactors.
-->
