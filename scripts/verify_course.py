"""Install and verify the actual downloadable projects in fresh directories."""
import ast
import json
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = ROOT / "slides/public/checkpoints"
PYTHON_COUNTS = {
    "flask-09-list": 9, "flask-10-create": 20, "flask-11-crud": 31,
    "flask-12-package": 31, "flask-13-sqlite": 32, "flask-14-cors": 33,
    "flask-15-marshmallow": 33, "flask-16-blueprint": 33,
    "flask-17-openapi": 35,
    "fastapi-00-app": 1, "fastapi-01-create": 14, "fastapi-02-crud": 25,
    "fastapi-03-sqlmodel": 25,
}
NODE_COUNTS = {
    "canvas-04-game": 10, "canvas-05-three": 10, "todo-client": 4,
    "nest-00-app": 1, "nest-01-memory": 3, "nest-02-sqlite": 4,
}


def run(folder, *args, expected=0):
    result = subprocess.run(args, cwd=folder, capture_output=True, text=True)
    assert result.returncode == expected, f"{folder}: {args}\n{result.stdout}\n{result.stderr}"
    return result.stdout


def python(folder, count):
    run(folder, "uv", "sync", "--locked")
    out = run(folder, "uv", "run", "--locked", "pytest", "-q")
    assert re.search(rf"\b{count} passed\b", out), out


def node(folder, count=None):
    run(folder, "npm", "ci", "--no-audit", "--no-fund")
    if count is not None:
        out = run(folder, "npm", "test")
        assert re.search(rf"(?:pass|tests) {count}\b", out), out
    run(folder, "npm", "run", "build")


def function_source(path, name):
    source = path.read_text()
    fn = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    return ast.get_source_segment(source, fn)


def main():
    manifest = json.loads((ARCHIVES / "manifest.json").read_text())
    with tempfile.TemporaryDirectory(prefix="ecm-course-qa-") as temp:
        folders = {}
        for item in manifest:
            name = item["branch"]
            if name.startswith("flask-") and int(name.split("-")[1]) < 9:
                continue  # Covered by verify_flask_checkpoints.py.
            with ZipFile(ARCHIVES / item["file"]) as archive:
                assert not any(p.startswith("/") or ".." in Path(p).parts for p in archive.namelist())
                assert not any(part in {"node_modules", ".venv", "__pycache__", "instance"} for p in archive.namelist() for part in Path(p).parts)
                folder = Path(temp) / archive.namelist()[0].split("/")[0]
                archive.extractall(temp)
            folders[name] = folder
            if name in PYTHON_COUNTS:
                python(folder, PYTHON_COUNTS[name])
            elif name.startswith("game-"):
                python(folder / "backend", 1 if name == "game-starter" else 11)
                node(folder / "frontend", 14)
            else:
                node(folder, NODE_COUNTS.get(name))
            print(f"OK {name}: clean install, tests and/or build", flush=True)

        # The FastAPI starter really leaves meaningful work for the exercise.
        folder = folders["fastapi-01-create"]
        out = run(folder, "uv", "run", "pytest", "tests/exercise_contract.py", "-q", expected=1)
        assert "1 failed" in out, out
        print("RED FastAPI starter: individual-resource contract fails", flush=True)

        # New Flask requirements fail before they are implemented.
        for before, after, test in [
            ("flask-09-list", "flask-10-create", "test_create_and_read"),
            ("flask-10-create", "flask-11-crud", "test_partial_update_and_delete_preserve_other_task"),
        ]:
            path = folders[before] / "tests/test_red_transition.py"
            path.write_text("from datetime import datetime, timedelta\n" + function_source(folders[after] / "tests/test_tasks.py", test))
            out = run(folders[before], "uv", "run", "pytest", str(path), "-q", expected=1)
            assert "1 failed" in out, out
            print(f"RED before {after}: {test}", flush=True)

        # Logic is deliberately copied so each project is standalone; prevent drift.
        canonical = (ROOT / "workshops/canvas/src/game.js").read_bytes()
        for path in ["projects/game-starter/frontend/src/game.js", "projects/game-reference/frontend/src/game.js", "workshops/three-demo/src/game.js"]:
            assert (ROOT / path).read_bytes() == canonical, path

        clone = Path(temp) / "bundle-clone"
        run(ROOT, "git", "clone", "-b", "flask-00-ready", str(ARCHIVES / "ecm26-course.bundle"), str(clone))
        branches = run(clone, "git", "branch", "-r")
        assert all(f"origin/{item['branch']}" in branches for item in manifest), branches
        run(clone, "git", "switch", "fastapi-01-create")
        assert (clone / "todo/__init__.py").exists()
        (clone / "student-notes.txt").write_text("Keep my work\n")
        recovery = Path(temp) / "recovery"
        run(clone, "git", "worktree", "add", str(recovery), "origin/flask-13-sqlite")
        assert (clone / "student-notes.txt").read_text() == "Keep my work\n"
        assert (recovery / "todo/models.py").exists()
        print("OK portable bundle: all branches and non-destructive recovery", flush=True)


if __name__ == "__main__":
    main()
