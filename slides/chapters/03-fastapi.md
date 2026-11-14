# Étape 1 · Le même client, un nouveau backend

Hier : un backend Flask, du SSR, puis une API persistante.

Aujourd’hui : **la même todo API avec FastAPI**.

Le client doit continuer à lister, créer, terminer et supprimer.

Nous retrouvons SQLAlchemy et SQLite : le stockage reste familier.

<!--
5 min. Montrer deux backends avec deux fichiers de données séparés. FastAPI reste du Python. Rappeler la première étape : faire fonctionner le client connu avant de construire le jeu.
-->

---

# 00 · Deux projets voisins, deux backends

**Conserver le dossier Flask du jour 1. Créer un dossier voisin pour FastAPI.**

```text
cours/                       ← dossier parent
├── ecm26-flask-ssr/          ← notre projet Flask du jour 1
│   ├── pyproject.toml
│   ├── todo/__init__.py      ← factory Flask
│   └── todo/tasks.py         ← routes Flask
└── ecm26-fastapi/            ← nouveau dossier à créer
```

Le dossier Flask garde son nom initial, même après l’ajout du CRUD.

**Pas de `ecm26-flask-ssr/ecm26-fastapi/` imbriqué.**

<!--
Si l’étudiant a repris depuis un ZIP, son dossier Flask porte éventuellement le nom du checkpoint. Repérer son pyproject.toml puis aller dans son parent ; ne pas imposer de renommage. Les deux projets ont chacun leur .venv, lockfile et database. Le port Flask reste 5001, FastAPI utilisera 8000.
-->

---

# 00 · Installer quand le besoin arrive

**Dans le terminal, depuis le dossier parent du projet Flask**, créer `ecm26-fastapi/`, puis entrer dedans :

```sh
mkdir ecm26-fastapi
cd ecm26-fastapi
uv init --bare --python 3.12
uv python pin 3.12
uv add fastapi==0.135.1 uvicorn==0.41.0 starlette==0.52.1
uv add --dev pytest==9.2.0 httpx==0.28.1
```

FastAPI décrit l’application ; Uvicorn la sert ; HTTPX équipe le test client.

<!--
5 min. Le checkpoint locke aussi les dépendances transitives. Starlette est la couche utilisée par FastAPI ; le pin stabilise la version du TestClient pour cet atelier, sans ouvrir un cours sur Starlette. On n’installe SQLAlchemy qu’au checkpoint suivant. Montrer la première commande séparément si le groupe tape tout.
-->

---

# 00 · Premier fichier, premier test

<div class="lesson-step">fastapi-00-app</div>

**Créer le fichier** `app.py` à la racine de `ecm26-fastapi/`.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

Le decorator relie encore une URL à une fonction.

**Créer le dossier** `tests/` à la racine, puis le fichier vide **`tests/__init__.py`** dedans.

<!--
5 min. Écrire d’abord le test de health en s’aidant du Flask précédent, observer 404, puis cette route. Le projet racine n’a pas de marker. test_app importe from app import app. Pas de dossier app/ supplémentaire.
-->

---

# 00 · Le test client change légèrement

**Créer le fichier** `tests/test_app.py`, à côté de `tests/__init__.py`.

```python
from fastapi.testclient import TestClient
from app import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Ici **`response.json()` est une méthode**, pas la propriété Flask `.json`.

<!--
5 min. Montrer une panne volontaire de contenu pour conserver le lien avec la qualité des tests. TestClient évite un serveur réseau pendant le test ; ce n’est pas une preuve d’intégration navigateur.
-->

---

# fastapi-00-app · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
uv run uvicorn app:app --reload --port 8000
```

**Résultat attendu : 1 passed.**

Branche `fastapi-00-app` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/fastapi-00-app.zip" download>Projet complet (.zip)</a>

Ouvrir /health puis /docs : retrouver le path et son status code.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# 01 · Une annotation ne valide pas tout

**Exemple à lire dans le Python shell**, aucun nouveau fichier à créer.

```python
def double(value: int):
    return value * 2

double("3")  # "33" : Python n’interdit pas cet appel
```

FastAPI utilise les déclarations à la frontière HTTP avec **Pydantic**.

Une contrainte sur le body doit être observée dans un test de request.

<!--
5 min. Faire prédire avant exécution. Ne pas présenter les type hints comme des contrôles automatiques partout en Python. Pydantic peut convertir des valeurs ; nos champs stricts refusent les conversions trompeuses.
-->

---

# 01 · Ouvrir le starter fourni

**Extraire <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/fastapi-01-create.zip" download>fastapi-01-create (.zip)</a> dans un nouveau dossier**, puis ouvrir ce dossier dans l'éditeur.

Nous quittons le petit projet `app.py` pour étudier une todo déjà structurée.

Les dossiers **`todo/`** et **`tests/`** sont fournis, avec leurs `__init__.py`.

`todo/schemas.py`, `models.py`, `database.py`, `init_db.py` et `tests/conftest.py` **existent déjà** : ne pas créer de doublons.

Nous lisons d'abord le POST fourni. Ensuite, vous ajouterez les routes manquantes dans ces fichiers.

---

# 01 · Du petit projet au starter FastAPI

**Extraire le ZIP dans le même dossier parent `cours/`**, sous le nom `fastapi-01-create/`.

```text
cours/
├── ecm26-flask-ssr/          ← Flask, conservé
├── ecm26-fastapi/            ← notre première route /health
└── fastapi-01-create/        ← starter fourni, travail ici
    ├── pyproject.toml
    ├── todo/__init__.py      ← factory et routes FastAPI
    └── tests/conftest.py     ← fixtures déjà fournies
```

**Ouvrir `fastapi-01-create/` dans l’éditeur et le terminal.**

Les paths des prochaines slides partent de ce nouveau dossier.

<!--
Ne pas extraire le starter dans todo/ ni recopier ses fichiers dans le projet Flask. Les fichiers FastAPI fournis portent parfois les mêmes noms, mais appartiennent à une autre application. Vérifier le terminal avant chaque uv run.
-->

---

# 01 · Un modèle de body

<div class="lesson-step">fastapi-01-create</div>

**Ouvrir le fichier fourni** `todo/schemas.py` : lire `TaskCreate` et ses imports. Extrait :

```python
Title = Annotated[str, StringConstraints(
    strip_whitespace=True, min_length=1, max_length=255,
    strict=True,
)]

class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: Title
```

Un titre vide ou un champ supplémentaire donne une erreur **422**.

<!--
6 min. Annotated vient de typing ; les autres noms de pydantic. Lire les imports du fichier complet. Le schema valide la request ; le modèle ORM représente la table. Ce sont deux responsabilités même si les champs se ressemblent.
-->

---

# 01 · Où vont les markers ?

**Arbre fourni dans le starter** : repérer ces fichiers dans l’éditeur.

```text
projet/               ← commandes ici ; pas de marker
├── pyproject.toml
├── todo/
│   ├── __init__.py    ← create_app, routes, dependency
│   ├── schemas.py    ← body et response
│   ├── models.py     ← table SQLAlchemy
│   ├── database.py   ← engine SQLite
│   └── init_db.py    ← commande Python
└── tests/
    ├── __init__.py    ← vide, même niveau que conftest.py
    └── conftest.py
```

<!--
4 min. Les fichiers de test sont directement dans tests/. Si un vrai sous-package est créé plus tard, il reçoit son propre marker ; ne pas ajouter des dossiers pour chaque fichier. Tous les imports .models sont relatifs à todo. Le starter fournit cette organisation pour protéger le temps d’exercice.
-->

---

# 01 · Retrouver la connexion SQLite

**Lire les fichiers existants**, sans recopier le code Flask dans FastAPI.

| Repère | Flask : `todo/__init__.py` | FastAPI : `todo/database.py` |
| --- | --- | --- |
| URL | `sqlite:///flask-todo.sqlite` | `sqlite:///.../fastapi-todo.sqlite` |
| Connexion | `db.init_app(app)` | `create_engine(database_url, ...)` |
| Session | `db.session` | `Session(engine)` par request |

Même database SQLite et même ORM ; **chaque projet a son propre fichier de données**.

Flask-SQLAlchemy gérait l’intégration. Avec FastAPI, nous voyons l’engine et la session directement.

---

# 01 · Garder le même ORM

```sh
uv add sqlalchemy==2.1.8
uv run python -m todo.init_db
```

Le fichier devient `instance/fastapi-todo.sqlite`.

Même table `Task`, mêmes `add()`, `commit()`, `select()`.

**Fichiers fournis** : lire `todo/database.py`, `models.py` et `init_db.py`. La commande crée `instance/` et la database.

<!--
5 min. Flask-SQLAlchemy était une intégration à Flask ; ici SQLAlchemy est utilisé directement. python -m todo.init_db part du dossier parent de todo, grâce au marker. Ne pas lancer python todo/init_db.py, car les imports relatifs n’auraient plus le même contexte.
-->

---

# 01 · Une session par request

**Ouvrir** `todo/__init__.py` : lire `get_session()` dans `create_app()`.

```python
def get_session():
    with Session(engine) as session:
        yield session

DatabaseSession = Annotated[Session, Depends(get_session)]
```

`Depends` demande une dependency à FastAPI. Ce n’est pas une fixture pytest.

Après utilisation, `with` ferme la session.

<!--
6 min. Relier au yield de la fixture du jour1. Ici le cycle est celui de la request. get_session est lié à l’engine de cette factory ; chaque test injecte un autre fichier SQLite. check_same_thread=False autorise les threads du framework, il ne rend pas une session partagée sûre : on conserve une session par request.
-->

---

# 01 · Le POST reçoit déjà un body validé

**Ouvrir** `todo/__init__.py` : lire la route `create_task()` déjà fournie.

```python
@app.post("/tasks/", response_model=TaskRead, status_code=201)
def create_task(data: TaskCreate, session: DatabaseSession):
    task = Task(**data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

`TaskRead` décrit la response. `from_attributes=True` lit les attributs ORM.

<!--
6 min. Expliquer chaque paramètre : body validé et dependency. Montrer la version Flask à côté dans l’éditeur. Une route sync def convient à ces opérations SQLAlchemy sync ; async ne rendrait pas cette database automatiquement non bloquante.
-->

---

# fastapi-01-create · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run python -m todo.init_db
uv run pytest -q
```

**Résultat attendu : 14 passed.**

Branche `fastapi-01-create` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/fastapi-01-create.zip" download>Projet complet (.zip)</a>

Le starter sait lister et créer. À vous d’implémenter les routes par ID.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

---

# Exercice 1 · Compléter le contrat

<div class="lesson-step">Travail individuel</div>

**Modifier les fichiers existants** `todo/__init__.py`, `todo/schemas.py` et `tests/test_tasks.py` dans le starter.

1. Ajouter GET individuel, PATCH partiel et DELETE.
2. Vérifier ID absent et body invalide sans modifier les données.
3. Connecter le client React sur le port 8000.
4. Expliquer un test qui détecte une vraie régression.

```sh
uv run pytest tests/exercise_contract.py -q
```

Le test fourni est rouge avant votre implémentation.

<!--
30 min de réalisation puis 5 min de retour dans le bloc105. Le brief complet contient le barème, les attentes et les modalités d’usage des assistants. Faire écrire des tests supplémentaires ; la seule réussite du cas fourni n’est pas toute l’évaluation. Solution fastapi-02-crud disponible pour la reprise après l’exercice.
-->

---

# 02 · PATCH : omis n’est pas null

**Modifier** `todo/__init__.py` : dans la route PATCH, après validation et recherche de la task.

```python
fields = data.model_dump(exclude_unset=True)
for key, value in fields.items():
    setattr(task, key, value)
```

`exclude_unset=True` garde seulement les champs envoyés. Cette boucle fonctionne, mais son intention reste générique : l’approfondissement SQLModel propose `sqlmodel_update()`.

`{}` est refusé. `{"done": null}` est refusé.

`{"done": false}` est valide : ne pas tester seulement la vérité de la valeur.

<!--
5 min au débrief. Présenter le TaskPatch du corrigé : StrictBool, Title optionnel comme valeur interne, puis validator qui rejette explicitement null si ce champ a été fourni. Montrer model_fields_set pour distinguer omission et null. Ces choix concrétisent le contrat, ce ne sont pas les valeurs par défaut de tous les projets.
-->

---

# 02 · Un validator a un rôle précis

**Modifier** `todo/schemas.py` : compléter la classe `TaskPatch`. Extrait du corrigé :

```python
@model_validator(mode="after")
def require_nonempty_nonnull_fields(self):
    if not self.model_fields_set:
        raise ValueError("At least one field is required")
    # Le fichier complet refuse aussi les champs fournis à null.
    return self
```

Pydantic appelle ce validator après la validation des champs.

<!--
4 min. Ne pas confondre ce decorator avec route, fixture ou parametrization. Lire les cinq lignes restantes dans schemas.py. L’intérêt d’une validation groupée apparaît maintenant avec le besoin non-vide/non-null, pas au premier exemple FastAPI.
-->

---

# fastapi-02-crud · On se retrouve ici

<div class="lesson-step">Point de synchronisation</div>

```sh
uv run pytest -q
uv run uvicorn todo:create_app --factory --reload --port 8000
```

**Résultat attendu : 25 passed.**

Branche `fastapi-02-crud` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/fastapi-02-crud.zip" download>Projet complet (.zip)</a>

Passer VITE_API_URL de :5001 à :8000 ; redémarrer Vite et refaire les quatre actions.

<!--
Faire exécuter la commande, comparer les fichiers et attendre le groupe. Le ZIP est un état complet. En cas de difficulté, extraire dans un nouveau dossier pour garder son travail.
-->

