# 03 · Rapprocher schemas et modèles

Nous avons retrouvé **SQLAlchemy** avant de changer notre manière de décrire les données.

**SQLModel s’appuie sur SQLAlchemy et Pydantic.** Il rapproche leur syntaxe et propose des opérations de création et de mise à jour.

Nous allons partager le champ `title`, puis rendre le PATCH plus lisible.

Le contrat HTTP, SQLite et les **25 tests** restent notre point de comparaison.

<!--
SQLModel n’est pas obligatoire avec FastAPI. C’est un choix adapté ici pour rapprocher les annotations Pydantic et le modèle de table. Les repères engine, session, transaction, select, commit et refresh restent utiles. Ne pas présenter un schema HTTP et une table comme la même responsabilité.
-->

---

# 03 · Installer SQLModel au moment du refactor

**Dans le dossier FastAPI complet `fastapi-02-crud/`**, lancer :

```bash
uv run pytest -q
uv remove sqlalchemy
uv add sqlmodel==0.0.50
```

Avant modification : **25 passed**. SQLModel installe SQLAlchemy comme dependency ; notre lockfile conserve ici la version `2.1.8`.

**Continuer dans ce projet.** Les slides suivantes modifient ses fichiers existants, sans créer un second `todo/`.

---

# 03 · Partager la définition du titre

**Dans `todo/schemas.py`**, retirer `BaseModel` des imports Pydantic et ajouter `from sqlmodel import SQLModel`.

**Remplacer `TaskCreate` par ces deux classes**. Garder `Title` et ses contraintes au-dessus.

```python
class TaskBase(SQLModel):
    model_config = ConfigDict(extra="forbid")
    title: Title

class TaskCreate(TaskBase):
    pass
```

`TaskBase` partage le titre ; `TaskCreate` reste le schema de création.

---

# 03 · Garder des schemas HTTP distincts

**Dans `todo/schemas.py`**, remplacer seulement `class TaskPatch(BaseModel):` par `class TaskPatch(SQLModel):`. Garder ses champs et son validator.

**Remplacer la classe `TaskRead` entière** par :

```python
class TaskRead(TaskBase):
    id: int
    done: bool
    creation_date: str
```

`title` est hérité de `TaskBase`. SQLModel sait lire les attributs ; l’ancien `ConfigDict(from_attributes=True)` devient inutile ici.

---

# 03 · Préparer le fichier du modèle

**Remplacer le contenu de `todo/models.py` par ces imports**. La slide suivante ajoute la nouvelle classe `Task`.

```python
from datetime import UTC, datetime
from sqlmodel import Field
from .schemas import TaskBase
```

`TaskBase` apporte le titre et ses contraintes. `Field` décrit les valeurs attribuées par le backend ; `UTC` indique le timezone utilisé pour la date.

La classe SQLAlchemy `Base` disparaît. **Ne pas créer un nouveau fichier.**

---

# 03 · Déclarer la table avec SQLModel

**Dans `todo/models.py`**, ajouter sous les imports :

```python
class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    done: bool = False
    creation_date: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
```

`table=True` crée un modèle de table. Avant insertion, `id` vaut `None` ; SQLite lui attribue ensuite sa valeur.

<!--
Le nom de table reste task et les mêmes colonnes sont conservées. creation_date reste une string ISO UTC pour préserver exactement le contrat. default_factory produit une date pour chaque nouvelle task ; ce n’est pas une date calculée une seule fois à l’import.
-->

---

# 03 · Retrouver engine et session

**Dans `todo/database.py`**, remplacer l’import de `create_engine` :

```python
from sqlmodel import create_engine
```

**Dans `todo/__init__.py`**, remplacer les deux imports SQLAlchemy par :

```python
from sqlmodel import Session, select
```

Garder l’URL SQLite, `check_same_thread=False`, `get_session()` et `Depends` : **une session par request**, fermée à la fin.

---

# 03 · Mettre à jour la création des tables

**Modifier ces trois fichiers existants** :

- `todo/init_db.py`
- `tests/conftest.py`
- `tests/test_persistence.py`

Dans chacun, remplacer l’import de `Base` par **`from sqlmodel import SQLModel`**, puis `Base.metadata` par **`SQLModel.metadata`**.

Les appels `create_all(...)` gardent leur engine. Les assertions des tests restent identiques.

**Aucun nouveau fichier ni nouveau `__init__.py`**. Notre table existante reste compatible.

---

# 03 · Lire avec la session SQLModel

**Dans `todo/__init__.py`**, remplacer uniquement le body de `list_tasks()` :

```python
        query = select(Task).order_by(Task.id)
        return session.exec(query).all()
```

`exec()` adapte le résultat à ce `select(Task)` : nous obtenons directement les objets `Task`.

La version SQLAlchemy faisait explicitement ce travail avec `scalars()`.

---

# 03 · Créer un nouvel objet

**Dans `todo/__init__.py`, dans `create_task()`**, remplacer `Task(**data.model_dump())` par :

```python
        task = Task.model_validate(data)
```

`data` a déjà été validé comme `TaskCreate` par FastAPI. `model_validate()` construit et valide le modèle `Task` à partir de ces données.

Garder `session.add(task)`, `commit()`, `refresh(task)` et `return task`.

**Créer une task produit un nouvel objet. Modifier une task doit garder son ID.**

---

# 03 · Dire clairement ce que le PATCH modifie

**Dans `todo/__init__.py`, dans `update_task()`**, remplacer la boucle `for ... setattr(...)` par :

```python
        changes = data.model_dump(exclude_unset=True)
        task.sqlmodel_update(changes)
```

`TaskPatch` limite et valide les champs autorisés. `exclude_unset=True` garde seulement ceux envoyés ; `sqlmodel_update()` les applique à **l’objet existant**.

Cette méthode ne remplace pas la validation. Le `commit()` reste à faire.

<!--
Un Task(**changes) créerait une autre task : ce n’est pas un PATCH. sqlmodel_update exprime l’intention et évite une boucle générique dans la route. Ne jamais lui transmettre directement un body non validé. done=False doit bien être appliqué, les champs absents préservés.
-->

---

# 03 · Relire le PATCH complet

**Vérifier le body de `update_task()` dans `todo/__init__.py`**, sous son decorator et sa signature existants :

```python
        task = find_task(session, task_id)
        changes = data.model_dump(exclude_unset=True)
        task.sqlmodel_update(changes)
        session.commit()
        session.refresh(task)
        return task
```

La session suit déjà `task`, chargée par `find_task()`. `commit()` enregistre les changements ; `refresh()` relit les valeurs sauvegardées.

---

# fastapi-03-sqlmodel · On se retrouve ici

**Terminal dans le projet FastAPI** :

```bash
uv run python -m todo.init_db
uv run pytest -q
uv run uvicorn todo:create_app --factory --reload --port 8000
```

**25 passed**, avec les mêmes assertions HTTP et de persistence.

Branche `fastapi-03-sqlmodel` · <a href="https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/fastapi-03-sqlmodel.zip" download>Projet complet (.zip)</a>

Ouvrir `/docs` et reconnecter React. L’interface et les données restent les mêmes.

<!--
Le checkpoint SQLAlchemy 02 reste disponible pour comparer avec 03. Les imports metadata ont changé dans deux fichiers de tests, aucune assertion n’a été assouplie. Les tests protègent aussi la conservation des autres champs, les valeurs false, les erreurs et la persistence après redémarrage.
-->

---

# Ce qui change, ce qui reste stable

| Sujet | Flask | FastAPI |
| --- | --- | --- |
| Langage | Python | Python |
| Contrat du client | `/tasks/`, JSON | Identique |
| Validation | Schemas Marshmallow | Modèles SQLModel / Pydantic |
| Documentation API | Flask-smorest + Swagger UI | `/docs` généré |
| Stockage choisi | SQLite + SQLAlchemy | SQLite + SQLModel |

Changer de framework ne garantit pas à lui seul de meilleures performances.

<!--
5 min. WSGI/ASGI sont les interfaces backend/serveur, après le modèle HTTP acquis. Les deux frameworks savent construire des APIs. La documentation générée n’est pas une preuve que le comportement répond au besoin. Les données sont séparées pour pouvoir comparer sans interférence.
-->
