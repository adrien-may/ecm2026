"""Verify the downloadable teaching states and their deliberate regressions."""

import ast
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS = ROOT / "slides/public/checkpoints"
EXPECTED = {
    "00-ready": 0,
    "01-flask": 0,
    "02-pytest": 1,
    "03-route": 2,
    "04-template": 2,
    "05-name": 5,
    "06-fixtures": 5,
    "07-test-quality": 7,
    "08-json": 8,
}


def run(folder, *args, expected=0):
    result = subprocess.run(args, cwd=folder, capture_output=True, text=True)
    assert result.returncode == expected, result.stdout + result.stderr
    return result.stdout


def function_source(folder, name):
    source = (folder / "tests/test_app.py").read_text()
    node = next(node for node in ast.parse(source).body
                if isinstance(node, ast.FunctionDef) and node.name == name)
    return ast.get_source_segment(source, node)


def main():
    with tempfile.TemporaryDirectory(prefix="ecm26-checkpoints-") as temp:
        folders = {}
        for name, count in EXPECTED.items():
            with ZipFile(CHECKPOINTS / f"{name}.zip") as archive:
                archive.extractall(temp)
            folder = Path(temp) / f"ecm26-flask-{name}"
            folders[name] = folder
            run(folder, "uv", "sync", "--locked")
            if count:
                output = run(folder, "uv", "run", "--locked", "python", "-m", "pytest", "-q")
                assert re.search(rf"\b{count} passed\b", output), output
                print(f"{name}: {count} passed", flush=True)
            elif name == "01-flask":
                run(folder, "uv", "run", "--locked", "python", "-c",
                    "from app import app; assert app.test_client().get('/bonjour').status_code == 404")
                print("01-flask: /bonjour returns 404 as announced", flush=True)
            else:
                run(folder, "uv", "run", "--locked", "python", "-c",
                    "import importlib.util; assert importlib.util.find_spec('flask') is None")
                print("00-ready: no Flask installed", flush=True)

        # Each new behavioural requirement must fail against the preceding implementation.
        for before, after, test in [
            ("02-pytest", "03-route", "test_default_page"),
            ("04-template", "05-name", "test_page_displays_samira"),
            ("07-test-quality", "08-json", "test_api_returns_json"),
        ]:
            folder = folders[before]
            tests = folder / "tests/test_app.py"
            original = tests.read_text()
            tests.write_text(original + "\n\n" + function_source(folders[after], test) + "\n")
            output = run(folder, "uv", "run", "--locked", "python", "-m", "pytest", "-q", "-k", test, expected=1)
            assert "1 failed" in output, output
            tests.write_text(original)
            print(f"RED before {after}: {test} fails as announced", flush=True)

        folder = folders["07-test-quality"]
        slides = (ROOT / "slides/chapters/01-flask.md").read_text()

        def displayed(title):
            section = slides.split(f"# {title}\n", 1)[1].split("\n---", 1)[0]
            return re.search(r"```python\n(.*?)\n```", section, re.S)[1] + "\n"

        fixture_code = displayed("07 · Préparer la fixture de capture") + displayed("07 · Écouter pendant le test seulement")
        fixture_node = next(node for node in ast.parse((folder / "tests/conftest.py").read_text()).body
                            if isinstance(node, ast.FunctionDef) and node.name == "captured_templates")
        assert ast.dump(ast.parse(fixture_code).body[0]) == ast.dump(fixture_node)
        assert ast.dump(ast.parse(displayed("07 · Vérifier le template réellement utilisé"))) == ast.dump(
            ast.parse((folder / "tests/test_template_signal.py").read_text()))
        print("Template signal fixture and test match the displayed code.", flush=True)
        template = folder / "templates/hello.html"
        original = template.read_text()
        assert "<h1>Bonjour {{ name }}</h1>" in original
        template.write_text(original.replace("<h1>Bonjour {{ name }}</h1>", "<h1>Bonjour</h1>"))
        for selection, expected, summary in [
            ("matches_its_template", 0, "1 passed"),
            ("uses_expected_template", 0, "1 passed"),
            ("displays_requested_name", 1, "2 failed"),
        ]:
            output = run(folder, "uv", "run", "--locked", "python", "-m", "pytest", "-q", "-k", selection, expected=expected)
            assert summary in output, output
            print(f"REGRESSION {selection}: {summary}", flush=True)

        # The instructor's runnable solution and the final download must be the same code.
        for path in ["app.py", "templates/hello.html", "tests/__init__.py", "tests/test_app.py", "tests/test_template_signal.py", "tests/conftest.py", "pyproject.toml", "uv.lock"]:
            assert (ROOT / "lessons/01-flask-ssr" / path).read_bytes() == (folders["08-json"] / path).read_bytes(), path
        print("Final download matches the instructor lesson.", flush=True)


if __name__ == "__main__":
    main()
