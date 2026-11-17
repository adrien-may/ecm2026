"""Export the course checkpoint refs without checking out or staging files."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides/public/checkpoints"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = [
        "flask-00-ready", "flask-01-flask", "flask-02-pytest", "flask-03-route",
        "flask-04-template", "flask-05-name", "flask-06-fixtures", "flask-07-test-quality",
        "flask-08-json", "flask-09-list", "flask-10-create", "flask-11-crud",
        "flask-12-package", "flask-13-sqlite", "flask-14-cors",
        "flask-15-marshmallow", "flask-16-blueprint", "flask-17-openapi",
        "fastapi-00-app", "fastapi-01-create", "fastapi-02-crud", "fastapi-03-sqlmodel",
        "canvas-01-draw", "canvas-02-animation", "canvas-03-input", "canvas-04-game",
        "nest-00-app", "nest-01-memory", "nest-02-sqlite",
        "todo-client", "game-starter", "game-reference", "canvas-05-three",
    ]
    manifest = []
    for name in names:
        filename = name.removeprefix("flask-") if name.startswith("flask-") else name
        if name == "canvas-05-three":
            filename = "three-demo"
        path = OUT / f"{filename}.zip"
        prefix = f"ecm26-{name}" if name.startswith("flask-") else name
        git("archive", "--format=zip", f"--prefix={prefix}/", f"--output={path}", name)
        manifest.append({"branch": name, "commit": git("rev-parse", name).decode().strip(), "file": path.name})
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Exported {len(names)} checkpoint ZIPs and their Git branch manifest")


if __name__ == "__main__":
    main()
