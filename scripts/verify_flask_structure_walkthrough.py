"""Apply the displayed SQLite, schema and Blueprint code to the prior checkpoints."""
import ast
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / "slides/public/checkpoints"
SLIDES = "\n".join((ROOT / f"slides/chapters/{name}.md").read_text()
                   for name in ("02-todo", "02b-flask-structure", "02c-openapi"))


def code(title, index=0):
    section = SLIDES.split(f"# {title}\n", 1)[1].split("\n---\n\n# ", 1)[0]
    return re.findall(r"```python\n(.*?)\n```", section, re.S)[index] + "\n"


def replace_function(source, name, replacement):
    node = next(n for n in ast.walk(ast.parse(source))
                if isinstance(n, ast.FunctionDef) and n.name == name)
    start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
    lines = source.splitlines(keepends=True)
    return "".join(lines[:start]) + replacement + "".join(lines[node.end_lineno:])


def read_checkpoint(name, path):
    with ZipFile(ARCHIVES / f"{name}.zip") as archive:
        return archive.read(f"ecm26-flask-{name}/{path}").decode()


def install_metadata(project, name):
    for path in ("pyproject.toml", "uv.lock"):
        (project / path).write_text(read_checkpoint(name, path))


def check(project, count, *paths, failed=False):
    result = subprocess.run(["uv", "run", "--locked", "pytest", "-q", *paths],
                            cwd=project, capture_output=True, text=True)
    assert result.returncode == (1 if failed else 0), result.stdout + result.stderr
    assert count in result.stdout, result.stdout
    print(count, flush=True)


def compare(project, checkpoint, paths):
    class IgnoreDocstrings(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return self.generic_visit(node)

    def normalized(source):
        tree = IgnoreDocstrings().visit(ast.parse(source))
        # Import grouping and blank lines need not match to teach identical code.
        imports = sorted(ast.dump(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)))
        tree.body = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
        return imports, ast.dump(tree)

    for path in paths:
        assert normalized((project / path).read_text()) == normalized(read_checkpoint(checkpoint, path)), path
    print(f"Displayed code matches flask-{checkpoint}: {', '.join(paths)}", flush=True)


def main():
    with tempfile.TemporaryDirectory(prefix="ecm-structure-walkthrough-") as temporary:
        root = Path(temporary)
        with ZipFile(ARCHIVES / "12-package.zip") as archive:
            archive.extractall(root)
        project = root / "ecm26-flask-12-package"
        persistence = project / "tests/test_persistence.py"
        persistence.write_text(code("13 · Constater la perte des données"))
        check(project, "1 failed", "tests/test_persistence.py", failed=True)

        install_metadata(project, "13-sqlite")
        model = project / "todo/models.py"
        model.write_text(code("13 · Préparer SQLAlchemy") + "\n" +
                         code("13 · Décrire la table Task") + "\n" +
                         code("13 · Convertir une task en dictionnaire"))
        app = project / "todo/__init__.py"
        source = app.read_text()
        helper = source[source.index("def read_fields("):source.index("def create_app(")]
        factory = code("13 · Configurer avant de connecter") + code("13 · Créer le dossier et connecter l’ORM")
        factory += "\n" + code("13 · Ajouter notre commande init-db") + "\n"
        source = code("13 · Préparer les imports de la factory") + "\n" + helper + factory + source[source.index("    @app."):]
        for function, title in [
            ("create_task", "Écrire une task dans SQLite"),
            ("list_tasks", "Lire la collection depuis SQLite"),
            ("find_task", "Retrouver une task par ID"),
            ("get_task", "Lire une seule task"),
            ("update_task", "Modifier une task dans SQLite"),
            ("delete_task", "Supprimer une task dans SQLite"),
        ]:
            source = replace_function(source, function, code(f"13 · {title}"))
        app.write_text(source)
        fixture = project / "tests/conftest.py"
        fixture.write_text("from todo.models import db\n" + replace_function(
            fixture.read_text(), "app", code("13 · Préparer une database par test") +
            code("13 · Libérer les connexions après le test")))
        check(project, "31 passed", "--ignore=tests/test_persistence.py")
        persistence.write_text(code("13 · Isoler le test de redémarrage") +
                               code("13 · Écrire puis fermer la première app") +
                               code("13 · Relire avec une nouvelle app"))
        check(project, "32 passed")
        compare(project, "13-sqlite", ["todo/__init__.py", "todo/models.py", "tests/conftest.py", "tests/test_persistence.py"])

        # The already documented CORS step precedes the new schema lesson.
        for path in ("todo/__init__.py", "tests/test_persistence.py"):
            (project / path).write_text(read_checkpoint("14-cors", path))
        install_metadata(project, "15-marshmallow")
        schemas = code("15 · Installer Marshmallow maintenant") + "\n".join(code(f"15 · {title}") for title in (
            "Décrire les champs du schema", "Préparer le titre avant validation",
            "Décrire les champs du PATCH", "Garder un boolean strict", "Refuser une modification vide"))
        (project / "todo/schemas.py").write_text(schemas)
        source = code("15 · Préparer les erreurs Marshmallow") + app.read_text()
        source = source.replace("    @app.errorhandler(HTTPException)",
                                code("15 · Préparer les erreurs Marshmallow", 1) + "\n    @app.errorhandler(HTTPException)")
        for function, title in [
            ("create_task", "Valider puis créer avec load"),
            ("list_tasks", "Serialize la collection avec dump"),
            ("get_task", "Serialize une seule task"),
            ("update_task", "Charger un PATCH partiel"),
        ]:
            source = replace_function(source, function, code(f"15 · {title}"))
        source = replace_function(source, "read_fields", "")
        app.write_text(source)
        model.write_text(replace_function(model.read_text(), "to_dict", ""))
        check(project, "33 passed")
        compare(project, "15-marshmallow", ["todo/__init__.py", "todo/models.py", "todo/schemas.py"])

        routes = code("16 · Déclarer le Blueprint") + "\n"
        for name, title in [
            ("list_tasks", "Déplacer la route de collection"),
            ("create_task", "Déplacer la route de création"),
            ("find_task", "Déplacer la recherche par ID"),
            ("get_task", "Déplacer la lecture par ID"),
            ("update_task", "Déplacer la modification"),
            ("delete_task", "Déplacer la suppression"),
        ]:
            routes += code(f"16 · {title}") + "\n"
            source = replace_function(source, name, "")
        (project / "todo/tasks.py").write_text(routes)
        source = code("16 · Importer le groupe dans la factory") + "\n" + source[source.index("def create_app("):]
        source = source.replace("    return app\n", code("16 · Enregistrer le CRUD dans l’app"))
        app.write_text(source)
        check(project, "33 passed")
        compare(project, "16-blueprint", ["todo/__init__.py", "todo/tasks.py", "todo/models.py", "todo/schemas.py"])

        documentation = project / "tests/test_openapi.py"
        documentation.write_text(code("17 · Tester la documentation attendue") + "\n" +
                                 code("17 · Tester aussi l’accès à Swagger UI"))
        check(project, "2 failed", "tests/test_openapi.py", failed=True)
        install_metadata(project, "17-openapi")
        schemas_file = project / "todo/schemas.py"
        schemas_file.write_text(schemas_file.read_text() + "\n" + code("17 · Décrire nos responses d’erreur"))
        source = code("17 · Nommer notre API") + app.read_text()
        source = source.replace("    app.config.from_mapping(\n", "    app.config.from_mapping(\n" +
                                code("17 · Nommer notre API", 1))
        source = source.replace("    @app.cli.command", code("17 · Enregistrer l’API et son Blueprint") +
                                "\n    @app.cli.command")
        source = source.replace("    app.register_blueprint(tasks_blueprint)\n",
                                code("17 · Enregistrer l’API et son Blueprint", 1))
        app.write_text(source)
        routes_file = project / "todo/tasks.py"
        routes = routes_file.read_text().replace("from flask import Blueprint, abort, request",
                                                code("17 · Installer Flask-smorest maintenant").strip())
        for function, title in [
            ("list_tasks", "Décrire la response de collection"),
            ("create_task", "Charger les arguments de création"),
            ("get_task", "Décrire la lecture d’une task"),
            ("delete_task", "Décrire une response sans body"),
        ]:
            routes = replace_function(routes, function, code(f"17 · {title}"))
        routes = replace_function(routes, "update_task", code("17 · Décrire l’entrée du PATCH") +
                                  code("17 · Appliquer les champs du PATCH"))
        # Insert the hook immediately after find_task, as instructed.
        node = next(n for n in ast.parse(routes).body if isinstance(n, ast.FunctionDef) and n.name == "find_task")
        lines = routes.splitlines(keepends=True)
        lines.insert(node.end_lineno, "\n" + code("17 · Garder l’ordre de nos contrôles HTTP") + "\n")
        routes_file.write_text("".join(lines))
        check(project, "33 passed", "--ignore=tests/test_openapi.py")
        source = source.replace('        OPENAPI_VERSION="3.0.3",\n', '        OPENAPI_VERSION="3.0.3",\n' +
                                code("17 · Activer Swagger UI"))
        app.write_text(source)
        check(project, "35 passed")
        compare(project, "17-openapi", ["todo/__init__.py", "todo/tasks.py", "todo/schemas.py", "tests/test_openapi.py"])


if __name__ == "__main__":
    main()
