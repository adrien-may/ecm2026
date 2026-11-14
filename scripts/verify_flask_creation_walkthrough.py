"""Run the POST lesson by applying the displayed code to the previous checkpoint."""
from pathlib import Path
import ast
import re
import subprocess
import tempfile
import textwrap
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SLIDES = (ROOT / "slides/chapters/02-todo.md").read_text()


def code(title):
    section = SLIDES.split(f"# {title}\n", 1)[1].split("\n---\n\n# ", 1)[0]
    return re.search(r"```python\n(.*?)\n```", section, re.S)[1] + "\n"


def check(project, expected, failing=False):
    result = subprocess.run(
        ["uv", "run", "--frozen", "python", "-m", "pytest", "-q"],
        cwd=project, text=True, capture_output=True,
    )
    assert result.returncode == (1 if failing else 0), result.stdout + result.stderr
    assert expected in result.stdout, result.stdout
    print(expected)


def main():
    with tempfile.TemporaryDirectory(prefix="ecm-post-walkthrough-") as temporary:
        folder = Path(temporary)
        with ZipFile(ROOT / "slides/public/checkpoints/09-list.zip") as archive:
            archive.extractall(folder)
        project = folder / "ecm26-flask-09-list"
        app = project / "app.py"
        tests = project / "tests/test_tasks.py"
        baseline = app.read_text()
        assert "read_fields" not in baseline and "HTTPException" not in baseline
        check(project, "9 passed")

        tests.write_text(tests.read_text() + "\n" + code("10 · Créer puis relire"))
        check(project, "1 failed, 9 passed", failing=True)

        helper = code("10 · Écrire read_fields(), première partie")
        helper = helper.replace("    return data\n", code("10 · Compléter la validation du titre") + "    return data\n")
        body = baseline[baseline.index("def create_app()") :]
        body = body.replace("    tasks = {}\n", "    tasks = {}\n    next_id = 1\n")
        handler = textwrap.indent(code("10 · Préparer des erreurs JSON"), "    ")
        route = textwrap.indent(code("10 · Écrire la route POST complète"), "    ")
        position = body.rindex("    return app")
        body = body[:position] + handler + "\n" + route + "\n" + body[position:]
        app.write_text(code("10 · Préparer la validation du body") + "\n\n" + helper + "\n\n" + body)
        ast.parse(app.read_text())
        check(project, "10 passed")

        tests.write_text("import pytest\n" + tests.read_text() + "\n" + code("10 · Vérifier aussi les body invalides"))
        check(project, "18 passed")

        with ZipFile(ROOT / "slides/public/checkpoints/10-create.zip") as archive:
            reference_tests = archive.read("ecm26-flask-10-create/tests/test_tasks.py").decode()
            reference_app = ast.parse(archive.read("ecm26-flask-10-create/app.py").decode())
        tests.write_text(reference_tests)
        check(project, "20 passed")
        built_functions = {node.name: node for node in ast.walk(ast.parse(app.read_text())) if isinstance(node, ast.FunctionDef)}
        reference_functions = {node.name: node for node in ast.walk(reference_app) if isinstance(node, ast.FunctionDef)}
        for name in ("read_fields", "http_error", "create_task"):
            assert ast.dump(built_functions[name]) == ast.dump(reference_functions[name]), name
        print("Displayed helpers and POST match the distributed checkpoint; all 20 tests pass.")


if __name__ == "__main__":
    main()
