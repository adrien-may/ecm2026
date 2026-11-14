"""Rebuild the SQLModel refactor from the slides and preserve existing SQLite data."""
import ast
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / "slides/public/checkpoints"
SLIDES = (ROOT / "slides/chapters/03b-sqlmodel.md").read_text()


def code(title, index=0):
    section = SLIDES.split(f"# {title}\n", 1)[1].split("\n---", 1)[0]
    return re.findall(r"```python\n(.*?)\n```", section, re.S)[index] + "\n"


def run(project, *args):
    result = subprocess.run(args, cwd=project, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def read_checkpoint(name, path):
    with ZipFile(ARCHIVES / f"{name}.zip") as archive:
        return archive.read(f"{name}/{path}").decode()


def normalized(source):
    tree = ast.parse(source)
    imports = sorted(ast.dump(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)))
    tree.body = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
    return imports, ast.dump(tree)


def main():
    with tempfile.TemporaryDirectory(prefix="ecm-sqlmodel-walkthrough-") as temp:
        with ZipFile(ARCHIVES / "fastapi-02-crud.zip") as archive:
            archive.extractall(temp)
        project = Path(temp) / "fastapi-02-crud"
        assert "25 passed" in run(project, "uv", "run", "--locked", "pytest", "-q")
        database_url = f"sqlite:///{Path(temp) / 'existing.sqlite'}"
        run(project, "uv", "run", "--locked", "python", "-c", f'''
from todo import create_app
from todo.models import Base
from fastapi.testclient import TestClient
app = create_app({database_url!r})
Base.metadata.create_all(app.state.engine)
with TestClient(app) as client:
    response = client.post('/tasks/', json={{'title': 'Avant SQLModel'}})
    assert response.status_code == 201
app.state.engine.dispose()
''')
        for path in ("pyproject.toml", "uv.lock"):
            (project / path).write_text(read_checkpoint("fastapi-03-sqlmodel", path))
        schemas = project / "todo/schemas.py"
        s = schemas.read_text().replace("BaseModel, ", "")
        s = "from sqlmodel import SQLModel\n" + s
        start, end = s.index("class TaskCreate("), s.index("class TaskPatch(")
        s = s[:start] + code("03 · Partager la définition du titre") + "\n\n" + s[end:]
        s = s.replace("class TaskPatch(BaseModel):", "class TaskPatch(SQLModel):")
        s = s[:s.index("class TaskRead(")] + code("03 · Garder des schemas HTTP distincts")
        schemas.write_text(s)
        (project / "todo/models.py").write_text(code("03 · Préparer le fichier du modèle") + "\n" + code("03 · Déclarer la table avec SQLModel"))
        p = project / "todo/database.py"
        p.write_text(p.read_text().replace("from sqlalchemy import create_engine", code("03 · Retrouver engine et session").strip()))
        for path in ("todo/init_db.py", "tests/conftest.py", "tests/test_persistence.py"):
            p = project / path
            s = p.read_text().replace("from .models import Base", "from sqlmodel import SQLModel")
            s = s.replace("from todo.models import Base", "from sqlmodel import SQLModel")
            p.write_text(s.replace("Base.metadata", "SQLModel.metadata"))
        p = project / "todo/__init__.py"
        s = p.read_text().replace("from sqlalchemy import select\nfrom sqlalchemy.orm import Session",
                                code("03 · Retrouver engine et session", 1).strip())
        s = s.replace("        return session.scalars(select(Task).order_by(Task.id)).all()\n",
                      code("03 · Lire avec la session SQLModel"))
        s = s.replace("        task = Task(**data.model_dump())\n", code("03 · Créer un nouvel objet"))
        s = s.replace("        for key, value in data.model_dump(exclude_unset=True).items():\n            setattr(task, key, value)\n",
                      code("03 · Dire clairement ce que le PATCH modifie"))
        p.write_text(s)
        assert "25 passed" in run(project, "uv", "run", "--locked", "pytest", "-q")
        for path in ("todo/__init__.py", "todo/schemas.py", "todo/models.py", "todo/database.py", "todo/init_db.py", "tests/conftest.py", "tests/test_persistence.py", "tests/test_tasks.py"):
            assert normalized((project / path).read_text()) == normalized(read_checkpoint("fastapi-03-sqlmodel", path)), path
        print("SQLModel: displayed changes match the checkpoint; 25 tests pass.", flush=True)
        run(project, "uv", "run", "--locked", "python", "-c", f'''
from todo import create_app
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
app = create_app({database_url!r})
SQLModel.metadata.create_all(app.state.engine)
with TestClient(app) as client:
    tasks = client.get('/tasks/').json()
    assert len(tasks) == 1 and tasks[0]['title'] == 'Avant SQLModel'
    task = tasks[0]
    response = client.patch(f"/tasks/{{task['id']}}", json={{'done': True}})
    assert response.status_code == 200
    updated = response.json()
    assert updated == {{**task, 'done': True}}
app.state.engine.dispose()
''')
        print("Existing SQLAlchemy SQLite data is read and updated with SQLModel, without rebuilding the table.", flush=True)


if __name__ == "__main__":
    main()
