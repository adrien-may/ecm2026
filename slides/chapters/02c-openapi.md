# 17 · Relier les schemas aux routes

Chaque route appelle encore `load()` ou `dump()` à la main.

**Flask-smorest relie un schema à une route avec des decorators.**

Cette même description permettra de produire une **specification OpenAPI** : URLs, méthodes, champs et responses de notre API.

Nous gardons nos fonctions, notre database et les tests du CRUD.

<!--
Reprendre les pages 51–53 du support précédent. Pas besoin de MethodView pour comprendre cette étape : le Blueprint Flask-smorest accepte nos fonctions. Le besoin précède les nouveaux decorators. Partir de flask-16-blueprint.
-->

---

# 17 · Tester la documentation attendue

**Créer `tests/test_openapi.py`**, à côté de `test_tasks.py`. Garder le fichier `tests/__init__.py` existant, vide.

```python
def test_openapi_describes_tasks(client):
    response = client.get("/openapi/openapi.json")
    assert response.status_code == 200
    spec = response.get_json()
    post = spec["paths"]["/tasks/"]["post"]
    assert post["requestBody"]["required"] is True
    assert "201" in post["responses"]
    task = spec["components"]["schemas"]["Task"]
    assert task["required"] == ["title"]
```

<!--
Ce test demande une description exploitable par un client : le body est requis, title aussi, et le status de création est documenté. Le endpoint n’existe pas encore ; nous le construisons ensuite.
-->

---

# 17 · Tester aussi l’accès à Swagger UI

**Compléter `tests/test_openapi.py`**, sous le premier test :

```python
def test_swagger_ui_is_available(client):
    response = client.get("/openapi/swagger")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "SwaggerUIBundle" in html
    assert "/openapi/openapi.json" in html
```

**`uv run pytest -q tests/test_openapi.py` → 2 failed : 404.**

Swagger UI sera la page qui affiche la specification et permet d’essayer l’API.

---

# 17 · Installer Flask-smorest maintenant

**Terminal à la racine du backend** :

```bash
uv add flask-smorest==0.47.0
```

**Modifier les imports en haut de `todo/tasks.py`** :

```python
from flask import abort, request
from flask_smorest import Blueprint
```

La ligne `tasks_blueprint = Blueprint(...)` reste en place. Ce Blueprint ajoute les decorators `arguments` et `response`.

---

# 17 · Décrire nos responses d’erreur

Notre API renvoie déjà une clé `error`, parfois des `details`.

**Compléter `todo/schemas.py`**, après `TaskPatchSchema` :

```python
class ErrorSchema(Schema):
    error = fields.String()
    details = fields.Raw()
```

Ce schema décrit ce format dans OpenAPI. Les error handlers continueront à produire nos responses et leurs headers.

<!--
Schema et fields sont déjà importés dans ce fichier. Raw accepte les différentes formes de details. Décrire un format ne déclenche pas une erreur ; ce travail reste celui des handlers existants.
-->

---

# 17 · Nommer notre API

**Dans `todo/__init__.py`**, ajouter aux imports :

```python
from flask_smorest import Api
from .schemas import ErrorSchema
```

**Dans `create_app()`, ajouter dans `app.config.from_mapping(...)`** :

```python
        API_TITLE="ECM Todo API",
        API_VERSION="1.0",
        OPENAPI_VERSION="3.0.3",
```

`API_VERSION` est notre version ; `OPENAPI_VERSION` est celle du format de description.

---

# 17 · Enregistrer l’API et son Blueprint

**Dans `todo/__init__.py`, dans `create_app()`**, après `CORS(...)` et **avant les error handlers**, ajouter :

```python
    api = Api()
    api.ERROR_SCHEMA = ErrorSchema
    api.init_app(app)
```

**À la fin de la factory**, remplacer `app.register_blueprint(...)` par :

```python
    api.register_blueprint(tasks_blueprint)
```

Garder `return app` et les handlers existants. Nos handlers sont enregistrés après ceux de Flask-smorest.

<!--
L’ordre est volontaire : notre handler HTTPException conserve notamment le header Allow d’une response 405. ERROR_SCHEMA doit être fixé avant init_app pour que la specification décrive bien nos erreurs.
-->

---

# 17 · Décrire la response de collection

**Dans `todo/tasks.py`, remplacer `list_tasks()` et ses decorators** :

```python
@tasks_blueprint.get("/")
@tasks_blueprint.response(200, TaskSchema(many=True))
def list_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query).all()
    return tasks
```

`@response` appelle le `dump()` du schema et documente le status `200`.

La fonction peut renvoyer les objets `Task` directement.

---

# 17 · Charger les arguments de création

**Dans `todo/tasks.py`, remplacer `create_task()` et ses decorators** :

```python
@tasks_blueprint.post("/")
@tasks_blueprint.arguments(TaskSchema, error_status_code=400)
@tasks_blueprint.response(201, TaskSchema)
def create_task(data):
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return task
```

`@arguments` appelle `load()` sur le body JSON et fournit **`data` à la fonction**. Une validation refusée renvoie `400`, comme avant.

<!--
Lire de l’extérieur vers l’intérieur : la route enregistre la fonction, arguments prépare son entrée, response traite sa sortie. Ne plus appeler TaskSchema().load dans la fonction : cela ferait deux validations. Sans error_status_code, la valeur par défaut serait 422.
-->

---

# 17 · Garder l’ordre de nos contrôles HTTP

**Dans `todo/tasks.py`, ajouter après `find_task()`** :

```python
@tasks_blueprint.before_request
def check_write_request():
    if request.method == "PATCH":
        find_task(request.view_args["task_id"])
    if request.method in {"POST", "PATCH"}:
        request.get_json()
```

`@before_request` exécute ce contrôle avant la route : un ID absent reste `404` ; un mauvais Content-Type reste `415`.

<!--
Flask-smorest valide les arguments avant d’entrer dans notre fonction. Ce hook conserve l’ordre du contrat testé précédemment : rechercher l’ID du PATCH, puis parser le JSON, puis valider les champs. view_args contient les valeurs extraites du path. get_json réutilise ensuite son résultat en cache. Les tests existants couvrent ces cas : le refactor ne doit pas les changer.
-->

---

# 17 · Décrire la lecture d’une task

**Dans `todo/tasks.py`, remplacer `get_task()` et ses decorators** :

```python
@tasks_blueprint.get("/<int:task_id>")
@tasks_blueprint.response(200, TaskSchema)
def get_task(task_id):
    return find_task(task_id)
```

Même règle que pour la collection, avec **un seul objet**.

`find_task()` conserve le comportement `404` si cet ID n’existe pas.

---

# 17 · Décrire l’entrée du PATCH

**Dans `todo/tasks.py`, remplacer les decorators et la signature de `update_task()`** par :

```python
@tasks_blueprint.patch("/<int:task_id>")
@tasks_blueprint.arguments(
    TaskPatchSchema(partial=True), error_status_code=400
)
@tasks_blueprint.response(200, TaskSchema)
def update_task(fields, task_id):
```

Le decorator fournit les **`fields` validés** en premier. Flask fournit aussi le `task_id` extrait du path.

La slide suivante donne le nouveau body de la fonction.

---

# 17 · Appliquer les champs du PATCH

**Dans `todo/tasks.py`, remplacer le body de `update_task()`**, juste sous la signature précédente :

```python
    task = find_task(task_id)
    for key, value in fields.items():
        setattr(task, key, value)
    db.session.commit()
    return task
```

Plus de `load()` ni de `dump()` dans cette fonction : les deux decorators s’en chargent.

La mutation et le `commit()` restent notre responsabilité.

---

# 17 · Décrire une response sans body

**Dans `todo/tasks.py`, remplacer `delete_task()` et ses decorators** :

```python
@tasks_blueprint.delete("/<int:task_id>")
@tasks_blueprint.response(204)
def delete_task(task_id):
    db.session.delete(find_task(task_id))
    db.session.commit()
    return None
```

Le status `204` n’a pas de body : aucun schema de sortie à fournir.

**`uv run pytest -q --ignore=tests/test_openapi.py` → 33 passed.**

---

# 17 · Activer Swagger UI

**Dans `todo/__init__.py`, compléter `app.config.from_mapping(...)`**, après `OPENAPI_VERSION` :

```python
        OPENAPI_URL_PREFIX="/openapi",
        OPENAPI_SWAGGER_UI_PATH="/swagger",
        OPENAPI_SWAGGER_UI_URL=(
            "https://cdn.jsdelivr.net/npm/"
            "swagger-ui-dist@5.32.0/"
        ),
```

Flask sert la specification. Le navigateur télécharge les fichiers de Swagger UI depuis ce CDN : **premier chargement avec Internet**.

**`uv run pytest -q` → 35 passed.**

---

# 17 · Lancer et ouvrir la documentation

**Terminal à la racine du backend**, après avoir arrêté l’ancien serveur avec `Ctrl+C` :

```bash
uv run flask --app todo init-db
uv run flask --app todo run --port 5001 --debug
```

Ouvrir [localhost:5001/openapi/swagger](http://localhost:5001/openapi/swagger).

Le document brut est sur [localhost:5001/openapi/openapi.json](http://localhost:5001/openapi/openapi.json).

**OpenAPI = le document. Swagger UI = son interface de lecture et d’essai.**

---

# 17 · Lire la carte de notre API

<img src="/screenshots/openapi-overview.png" alt="Swagger UI affiche ECM Todo API et les opérations GET, POST, PATCH, DELETE du groupe tasks." style="width: 100%; height: 280px; object-fit: contain; object-position: left" />

Chaque ligne décrit une opération : **méthode, path, body attendu et responses**.

Cette carte aide le frontend à utiliser l’API et peut servir à générer un client.

<!--
Capture de l’API de ce checkpoint, pas d’une API générique. Déplier POST puis Schemas en live. Les routes /bonjour et /api/bonjour restent de simples routes Flask hors du Blueprint documenté ici.
-->

---

# 17 · Essayer une request depuis Swagger UI

1. Déplier **POST `/tasks/`**, cliquer **Try it out**.
2. Saisir `{"title": "Lire la documentation"}`, puis **Execute**.
3. Lire le status `201` et la task reçue, avec son `id`.
4. Essayer **GET `/tasks/`** : la task apparaît dans la liste.

**Execute appelle notre vraie API et écrit dans notre SQLite de développement.**

La specification décrit l’interface. Les tests vérifient aussi les règles, les erreurs et la persistence : ils restent nécessaires.

---

# flask-17-openapi · On se retrouve ici

**Depuis la racine du backend** :

```bash
uv run pytest -q
```

**Résultat attendu : 35 passed.** Le CRUD fonctionne et sa documentation s’ouvre.

Checkpoint : `flask-17-openapi` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/17-openapi.zip" download>Télécharger le projet complet</a>.

Avant de continuer : retrouver le schema d’entrée, le decorator qui l’utilise et la route correspondante dans Swagger UI.

<!--
En cas de reprise, uv sync --locked puis init-db et run. Le checkpoint comporte aussi le test template_rendered ; sa finalité reste différente de celle des assertions sur le HTML. Demander aux étudiants d’expliquer arguments, response, Blueprint et OpenAPI avec leurs propres mots.
-->

---

# Fin du jour 1 · Expliquer son backend

Tracer : clic → request → Blueprint → schema → database → response.

Expliquer pourquoi un body invalide ne modifie aucune task.

Montrer le test qui détecte la modification du mauvais ID.

Placer `models.py`, `schemas.py`, `tasks.py` et `__init__.py` sans corrigé.

Demain : **FastAPI remplace l’implémentation ; le contrat reste stable.**

<!--
5 min de bilan. Demander aussi quelle différence existe entre load et dump, puis entre déclarer et enregistrer un Blueprint. Le test SSR reste au programme : le template partagé peut reproduire la même erreur dans l’app et dans un test faible. Aucun travail FastAPI le soir n’est nécessaire.
-->
