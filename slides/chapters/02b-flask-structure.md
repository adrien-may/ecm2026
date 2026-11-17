# 15 · Une serialization vraiment à la main

Le CRUD fonctionne. **Comment convertir une task en JSON ?**

**Expérience dans `uv run python`**, à la racine du backend. Aucun fichier à créer.

```python
from todo.models import Task
task = Task(title='Dire "bonjour"', done=False)
text = '{"title": "' + task.title + '", "done": '
text += str(task.done) + '}'
print(text)
```

Résultat : `{"title": "Dire "bonjour"", "done": False}`.

**Ce n’est pas du JSON valide** : guillemets non échappés et `False`.

<!--
Reprendre le besoin de la page 47 du cours précédent : sortir des objets ORM devient pénible si chaque route invente sa conversion. Cette construction est volontairement mauvaise, à tester dans le shell seulement. Ne pas remplacer une route par cet exemple.
-->

---

# 15 · JSON règle une partie du problème

**Dans le même Python shell**, remplacer la concaténation par :

```python
import json
data = {"title": task.title, "done": task.done}
print(json.dumps(data))
```

Le JSON est valide : les guillemets sont échappés, `False` devient `false`.

Mais il faut encore **choisir les attributs, les nommer et maintenir cette liste**.

Quitter avec `exit()`. Dans l’app, `Task.to_dict()` fait déjà ce choix à la main.

<!--
Ne pas attribuer à Marshmallow le travail de json.dumps. Flask utilise déjà un encodeur JSON lorsqu’une route renvoie un dictionnaire. Marshmallow va remplacer la description manuelle des champs et regrouper les règles de validation.
-->

---

# 15 · Une règle, un endroit pour la lire

Notre app contient deux descriptions d’une task :

- `read_fields()` vérifie les champs du body.
- `Task.to_dict()` choisit les champs de la response.

Nous allons décrire ces champs dans des **schemas Marshmallow**.

**Objectif du refactor : les mêmes requests et responses, les mêmes 33 tests.**

<!--
Extension du jour 1, inspirée des pages 49–54 du support précédent. Partir du checkpoint flask-14-cors fonctionnel, pas d’un projet vide. Montrer les répétitions dans le code avant d’installer le package. Un schema HTTP et un modèle de database ont des responsabilités différentes.
-->

---

# 15 · Le schema entre données et modèle

<img src="/diagrams/serialization-flow.svg" alt="Le dictionnaire d’entrée passe par schema.load, puis les champs validés construisent un modèle Task. schema.dump transforme le modèle en dictionnaire de sortie." style="width: 100%; height: 260px; object-fit: contain" />

`load()` fournit les champs validés. **Notre code construit `Task`**.

`dump()` lit ses attributs et fournit un dictionnaire. **Flask encode le JSON**.

<!--
Le schema standard du cours ne construit pas automatiquement un objet ORM. Le trajet de lecture part d’une Task chargée par SQLAlchemy, le trajet de création aboutit à Task(**data) puis au commit. Le dessin distingue les objets des dictionnaires et les deux directions load/dump.
-->

---

# 15 · De JavaScript à Python, étape par étape

| JavaScript | Body JSON | Python après le parse |
| --- | --- | --- |
| `true` / `false` | `true` / `false` | `True` / `False` |
| `null` | `null` | `None` |
| Un objet | `{...}` | `dict` |
| Un tableau | `[...]` | `list` |

`JSON.stringify()` produit le body ; **`request.get_json()` le parse**.

Ensuite seulement, **Marshmallow applique notre schema et nos règles**.

<!--
Le protocole échange du JSON, pas un objet JavaScript en mémoire. La conversion true/True est faite par le parse/encode JSON, même sans Marshmallow. Des fields Marshmallow peuvent aussi convertir des valeurs ; plus loin nous refuserons volontairement "false" et 0 pour un boolean strict.
-->

---

# 15 · Parse, validate, serialize

| Étape | Exemple | Responsable |
| --- | --- | --- |
| Parse JSON | Body JSON → dictionnaire Python | `request.get_json()` |
| Deserialize et validate | Dictionnaire → champs acceptés | `schema.load()` |
| Écrire en database | Champs acceptés → objet `Task` | SQLAlchemy |
| Serialize | Objet `Task` → dictionnaire de sortie | `schema.dump()` |
| Produire le JSON | Dictionnaire → body JSON | Flask |

**`load()` valide l’entrée. `dump()` ne valide pas la sortie.**

<!--
load ne crée pas automatiquement un modèle et dump ne produit pas directement une string JSON. Le contrat de sortie reste vérifié par les tests. L’ancien cours utilisait SQLAlchemyAutoSchema ; les champs sont explicites ici pour rendre leur rôle visible.
-->

---

# 15 · Installer Marshmallow maintenant

**Terminal à la racine du backend** :

```sh
uv add marshmallow==4.4.0
```

**Créer le fichier** `todo/schemas.py`, à côté de `todo/models.py` et `todo/__init__.py`.

Le dossier `todo/` existe. **Aucun nouveau `__init__.py`.**

**Modifier** `todo/schemas.py` : commencer par ces imports.

```python
from marshmallow import Schema, ValidationError, fields
from marshmallow import pre_load, validate, validates_schema
```

---

# 15 · Décrire les champs du schema

**Modifier** `todo/schemas.py`, ajouter cette classe après les imports. Nous la nommons `TaskSchema`.

```python
class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(
        required=True, validate=validate.Length(min=1, max=255)
    )
    done = fields.Boolean(dump_only=True)
    creation_date = fields.String(dump_only=True)
```

<!--
fields décrit les champs HTTP. required impose title à la création ; Length impose la longueur. dump_only expose un champ en sortie sans l’accepter en entrée. Les clés inconnues sont rejetées par défaut, y compris id, done et creation_date pendant load.
-->

---

# 15 · Qui choisit les valeurs ?

| Champ | POST reçu du client | Response renvoyée |
| --- | --- | --- |
| `title` | Obligatoire, string de 1 à 255 caractères | Oui |
| `id` | Interdit : `dump_only=True` | Oui |
| `done` | Interdit à la création | Oui |
| `creation_date` | Interdit : `dump_only=True` | Oui |

La database et le backend attribuent les autres valeurs.

Le PATCH aura son propre schema pour autoriser `done`.

---

# 15 · Préparer le titre avant validation

**Modifier** `todo/schemas.py` : ajouter cette méthode **dans `TaskSchema`**, sous les champs.

```python
    @pre_load
    def strip_title(self, data, **kwargs):
        if not isinstance(data, dict):
            return data
        if isinstance(data.get("title"), str):
            return {**data, "title": data["title"].strip()}
        return data
```

**`@pre_load`** appelle la méthode avant la validation.

`"   "` devient `""`, puis échoue à `Length(min=1)`.

<!--
strip_title est un nom choisi pour notre méthode ; pre_load est fourni par Marshmallow. **kwargs reçoit les options du hook, comme many et partial. La copie évite de modifier le dictionnaire reçu. Une mauvaise structure sera rejetée par le schema.
-->

---

# 15 · Essayer load avant la route

**Terminal à la racine** : lancer `uv run python`, puis saisir :

```python
from todo.schemas import TaskSchema
schema = TaskSchema()
schema.load({"title": "  Lire  "})
schema.load({"title": "   "})
```

Premier résultat : **`{"title": "Lire"}`**.

Deuxième appel : **`ValidationError`**. Aucun accès à la database.

Quitter Python avec `exit()`.

<!--
Faire essayer aussi {} et {"title": "Lire", "id": 7}. Le premier manque de title ; le second tente d’envoyer un champ réservé à la sortie. Ne pas copier ces expressions dans schemas.py.
-->

---

# 15 · Décrire les champs du PATCH

**Modifier** `todo/schemas.py` : ajouter cette classe **après `TaskSchema`**, sans indentation devant `class`.

```python
class TaskPatchSchema(TaskSchema):
    done = fields.Boolean()
```

L’héritage reprend les champs et le nettoyage du titre.

Ici, `done` devient modifiable.

Nous utiliserons **`partial=True`** pour autoriser l’absence de `title`.

<!--
Les champs id et creation_date restent dump_only. partial ignore les champs requis absents ; il n’autorise ni null, ni les champs inconnus, ni un titre vide. Les slides suivantes complètent cette même classe avant son utilisation.
-->

---

# 15 · Garder un boolean strict

**Modifier** `todo/schemas.py` : ajouter cette méthode **dans `TaskPatchSchema`**, sous `done`.

```python
    @pre_load
    def strict_done(self, data, **kwargs):
        if isinstance(data, dict) and "done" in data:
            if type(data["done"]) is not bool:
                raise ValidationError({"done": ["Expected bool"]})
        return data
```

Marshmallow peut convertir `0` ou `"false"`. Notre contrat les refuse.

Le test de PATCH invalide doit continuer à détecter cette différence.

<!--
Ne pas supposer que fields.Boolean applique exactement notre contrat. Les valeurs booléennes JSON true/false deviennent True/False en Python. Les hooks de nettoyage du titre et du boolean sont indépendants ; leur ordre ne change pas le résultat.
-->

---

# 15 · Refuser une modification vide

**Modifier** `todo/schemas.py` : ajouter cette méthode **dans `TaskPatchSchema`**, après `strict_done()`.

```python
    @validates_schema
    def require_change(self, data, **kwargs):
        if not data:
            raise ValidationError("Provide title or done")
```

**Nouveau decorator : `@validates_schema`** vérifie une règle sur l’ensemble des champs chargés.

`partial=True` autorise l’absence de `title`, mais nous refusons `{}`.

<!--
Contraster validate.Length, appliqué à un champ, et validates_schema, appliqué à l’ensemble. Un schema invalide lève ValidationError avant toute mutation.
-->

---

# 15 · Préparer les erreurs Marshmallow

**Modifier** `todo/__init__.py` : ajouter ces imports en haut du fichier.

```python
from marshmallow import ValidationError
from .schemas import TaskPatchSchema, TaskSchema
```

Puis ajouter le bloc suivant **dans `create_app()`**, avant le handler `HTTPException` :

```python
    @app.errorhandler(ValidationError)
    def validation_error(error):
        body = {"error": "Invalid task fields"}
        body["details"] = error.messages
        return body, 400
```

<!--
Réutiliser le decorator errorhandler déjà rencontré. ValidationError n’est pas une HTTPException. Garder le handler HTTP existant : JSON malformé, mauvais Content-Type, 404 et 405 doivent toujours être traités. Les détails du body d’erreur peuvent changer ; le contrat impose une response JSON en 400.
-->

---

# 15 · Valider puis créer avec load

**Modifier** `todo/__init__.py` : remplacer toute la route POST dans `create_app()`.

```python
    @app.post("/tasks/")
    def create_task():
        data = TaskSchema().load(request.get_json())
        task = Task(**data)
        db.session.add(task)
        db.session.commit()
        return TaskSchema().dump(task), 201
```

`load()` doit réussir avant `Task(**data)`. `dump()` remplace `to_dict()`.

<!--
La route relie les responsabilités dans l’ordre : parse, load, modèle, commit, dump, response. Ne pas supprimer read_fields ni to_dict tout de suite : PATCH et GET les utilisent encore.
-->

---

# 15 · Serialize la collection avec dump

**Modifier** `todo/__init__.py` : remplacer toute la route GET de collection.

```python
    @app.get("/tasks/")
    def list_tasks():
        query = db.select(Task).order_by(Task.id)
        tasks = db.session.scalars(query).all()
        return TaskSchema(many=True).dump(tasks)
```

**`many=True`** applique le même schema à chaque objet de la liste.

La response reste une liste JSON, y compris quand elle est vide.

---

# 15 · Serialize une seule task

**Modifier** `todo/__init__.py` : remplacer toute la route GET par ID.

```python
    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        return TaskSchema().dump(find_task(task_id))
```

Sans `many=True`, le schema traite un seul objet.

`find_task()` conserve son rôle : retrouver la task ou produire `404`.

---

# 15 · Charger un PATCH partiel

**Modifier** `todo/__init__.py` : remplacer toute la route PATCH.

```python
    @app.patch("/tasks/<int:task_id>")
    def update_task(task_id):
        task = find_task(task_id)
        schema = TaskPatchSchema(partial=True)
        fields = schema.load(request.get_json())
        for key, value in fields.items():
            setattr(task, key, value)
        db.session.commit()
        return TaskSchema().dump(task)
```

La validation complète précède toute modification du modèle.

---

# 15 · Retirer le code remplacé

**Modifier** `todo/__init__.py` : supprimer toute la fonction `read_fields()` située avant `create_app()`.

**Modifier** `todo/models.py` : supprimer uniquement la méthode `Task.to_dict()`. Garder tous les champs du modèle.

Garder la route DELETE, les fixtures et **tous les tests existants**.

**`uv run pytest -q` → 33 passed**.

Un refactor réussi change l’organisation sans changer les comportements promis.

<!--
Chercher read_fields et to_dict dans le projet : plus aucun appel. Les données restent dans le même fichier, sans migration ni réinitialisation. Demander quel test aurait détecté la conversion indésirable de "false".
-->

---

# flask-15-marshmallow · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
```

**Résultat attendu : 33 passed, sans modifier les tests.**

Branche `flask-15-marshmallow` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/15-marshmallow.zip" download>Projet complet (.zip)</a>

Expliquer le trajet de `{"title": "  Lire  "}` jusqu’à la response `201`.

Prochaine étape : donner une place aux routes CRUD.

<!--
Pause de synchronisation réelle. Faire relire un cas invalide et la preuve que la database n’a pas changé. En cas de reprise, extraire le ZIP dans un nouveau dossier puis uv sync --locked.
-->

---

# 16 · Regrouper les routes d’une ressource

`todo/__init__.py` configure l’app **et** contient toutes les routes.

Quand une deuxième ressource arrive, ce fichier devient difficile à parcourir.

Un **Blueprint** regroupe des routes que l’on **enregistre** dans l’app.

Nous allons déplacer le CRUD des tasks dans `todo/tasks.py`.

**Aucun nouveau package à installer : Blueprint fait partie de Flask.**

<!--
Le Blueprint n’est ni un serveur ni une seconde application. L’ancien support utilisait le Blueprint de Flask-smorest ; nous commençons avec le mécanisme natif pour distinguer regroupement, registration et automatisation des schemas.
-->

---

# 16 · Créer le module des routes

**Créer le fichier** `todo/tasks.py` dans le dossier `todo/` existant.

```text
todo/
├── __init__.py        ← factory et configuration, déjà présent
├── models.py          ← modèles SQLAlchemy, déjà présent
├── schemas.py         ← schemas Marshmallow, déjà présent
├── tasks.py           ← nouveau fichier, routes CRUD
└── templates/         ← dossier HTML existant
```

**`tasks.py` est un fichier**, pas un nouveau dossier.

Un seul `todo/__init__.py` ; aucun `tasks/__init__.py` à créer.

---

# 16 · Déclarer le Blueprint

**Modifier** `todo/tasks.py`, encore vide : écrire ce bloc.

```python
from flask import Blueprint, abort, request
from .models import Task, db
from .schemas import TaskPatchSchema, TaskSchema

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")
```

`"tasks"` est le nom du Blueprint ; `url_prefix` précède ses routes.

Il est déclaré, **mais pas encore enregistré dans notre app**.

<!--
Les imports viennent des modules voisins, pas de create_app. Cela évite un import circulaire : la factory importera tasks, qui importe models et schemas. Le nom Python tasks_blueprint et le nom du Blueprint sont choisis par nous.
-->

---

# 16 · Déplacer la route de collection

**Déplacer** `list_tasks()` de `todo/__init__.py` vers `todo/tasks.py`, après la déclaration du Blueprint. Utiliser ce bloc :

```python
@tasks_blueprint.get("/")
def list_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query).all()
    return TaskSchema(many=True).dump(tasks)
```

`@tasks_blueprint.get("/")` + prefix `/tasks` → **GET `/tasks/`**.

Supprimer l’ancienne route de la factory ; `def` n’est plus indenté.

<!--
db.session trouve la bonne app dans le contexte de la request. tasks dans la fonction contient les résultats de la lecture ; tasks_blueprint désigne le groupe de routes.
-->

---

# 16 · Déplacer la route de création

**Déplacer** `create_task()` de `todo/__init__.py` vers `todo/tasks.py`, après `list_tasks()`. Utiliser ce bloc :

```python
@tasks_blueprint.post("/")
def create_task():
    data = TaskSchema().load(request.get_json())
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return TaskSchema().dump(task), 201
```

Seuls le decorator, le path et l’indentation changent.

---

# 16 · Déplacer la recherche par ID

**Déplacer** `find_task()` de `todo/__init__.py` vers `todo/tasks.py`, après `create_task()`. Utiliser ce bloc :

```python
def find_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404, description="Task not found")
    return task
```

Cette fonction appartient au CRUD des tasks. Elle reste un helper Python, sans decorator.

---

# 16 · Déplacer la lecture par ID

**Déplacer** `get_task()` de `todo/__init__.py` vers `todo/tasks.py`, après `find_task()`. Utiliser ce bloc :

```python
@tasks_blueprint.get("/<int:task_id>")
def get_task(task_id):
    return TaskSchema().dump(find_task(task_id))
```

Prefix `/tasks` + path `/<int:task_id>` → **GET `/tasks/42`**.

Ne pas écrire `/tasks/<int:task_id>` dans le Blueprint : cela doublerait le prefix.

---

# 16 · Déplacer la modification

**Déplacer** `update_task()` de `todo/__init__.py` vers `todo/tasks.py`, après `get_task()`. Utiliser ce bloc :

```python
@tasks_blueprint.patch("/<int:task_id>")
def update_task(task_id):
    task = find_task(task_id)
    schema = TaskPatchSchema(partial=True)
    fields = schema.load(request.get_json())
    for key, value in fields.items():
        setattr(task, key, value)
    db.session.commit()
    return TaskSchema().dump(task)
```

<!--
Le code conserve l’ordre recherche, validation, mutation, commit, serialization. Le Blueprint organise les routes ; il ne remplace ni les schemas ni les transactions.
-->

---

# 16 · Déplacer la suppression

**Déplacer** `delete_task()` de `todo/__init__.py` vers `todo/tasks.py`, après `update_task()`. Utiliser ce bloc :

```python
@tasks_blueprint.delete("/<int:task_id>")
def delete_task(task_id):
    db.session.delete(find_task(task_id))
    db.session.commit()
    return "", 204
```

Les cinq routes CRUD et leur helper sont maintenant dans **`todo/tasks.py`**.

Elles doivent avoir disparu de `create_app()`.

---

# 16 · Importer le groupe dans la factory

**Modifier** `todo/__init__.py` : remplacer son bloc d’imports par celui-ci.

```python
from pathlib import Path
from flask import Flask, render_template, request
from flask_cors import CORS
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
from .models import db
from .tasks import tasks_blueprint
```

La factory configure l’app et importe le Blueprint.

Elle garde les deux routes de salutation, les handlers d’erreurs et `init_db()`.

---

# 16 · Enregistrer le CRUD dans l’app

**Modifier** `todo/__init__.py` : ajouter cette ligne **dans `create_app()`**, juste avant son `return app` existant.

```python
    app.register_blueprint(tasks_blueprint)
    return app
```

**Registration** : Flask ajoute les routes déclarées par le Blueprint.

Sans cette ligne, `/tasks/` renvoie `404`.

**`uv run pytest -q` → 33 passed**, avec les mêmes tests HTTP.

<!--
Ne pas ajouter un second return app. Les routes sont toutes définies au moment de l’import puis enregistrées une fois par app. Deux apps peuvent utiliser le même Blueprint. Les tests de factory et de persistance vérifient aussi ce scénario.
-->

---

# 16 · Retrouver le bon fichier

| Besoin | Fichier à ouvrir |
| --- | --- |
| Configurer SQLite ou enregistrer un Blueprint | `todo/__init__.py` |
| Décrire une colonne de la database | `todo/models.py` |
| Accepter ou refuser un champ HTTP | `todo/schemas.py` |
| Ajouter ou modifier une opération CRUD | `todo/tasks.py` |
| Prouver un comportement HTTP | `tests/test_tasks.py` |

La structure donne des repères. **Les tests prouvent le comportement.**

<!--
Faire chercher le fichier concerné par trois demandes : changer la longueur autorisée, ajouter une ressource, modifier une colonne. Ajouter une colonne nécessiterait aussi une migration ; le schema HTTP n’est pas le schéma SQLite.
-->

---

# 16 · Situer les outils du cours précédent

| Outil / pattern | Ce qu’il apporte |
| --- | --- |
| `Schema` / serialization | Décrire les champs, utiliser `load()` et `dump()` |
| `SQLAlchemyAutoSchema` | Déduire certains champs depuis un modèle ORM |
| `Blueprint` / registration | Regrouper des routes et les ajouter à une app |
| Flask-smorest | Ajouter `@arguments`, `@response` et une description OpenAPI |

Le cours précédent combinait ces outils. Nous avons maintenant écrit les opérations qu’ils peuvent automatiser.

<!--
Source : pages 49–54 du Google Slides précédent. Avec Flask-smorest, @arguments appelle le chargement/validation et injecte les données ; @response effectue la serialization de sortie et décrit son status code. OpenAPI décrit l’interface, mais ne prouve pas la logique CRUD. La prochaine étape installe Flask-smorest et montre ses decorators. SQLAlchemyAutoSchema reste une piste de recherche.
-->

---

# flask-16-blueprint · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
uv run flask --app todo:create_app run --debug --port 5001
```

**Résultat attendu : 33 passed.** Même React, mêmes données, mêmes URLs.

Branche `flask-16-blueprint` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/16-blueprint.zip" download>Projet complet (.zip)</a>

Montrer où une task est validée, enregistrée puis transformée pour la response.

<!--
Pause : comparer les fichiers, exécuter les tests et une interaction React. Les checkpoints 15 et 16 gardent le même fichier SQLite que 14 ; aucune suppression des données n’est nécessaire. Les archives restent des projets autonomes.
-->

