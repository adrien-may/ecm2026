"""Build a portable source-and-PDF kit, excluding local runtime data."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/ecm26-course-kit.zip"
SKIP = {"node_modules", ".venv", "__pycache__", ".pytest_cache", "dist", "dist-options", "instance", ".git", ".DS_Store"}
DIRECTORIES = ["slides", "lessons", "projects", "workshops", "contracts", "assessments", "docs", "scripts"]
FILES = ["README.md", "COURSE_PLAN.md", "CHECKPOINTS.md", "HANDOFF.md", "package.json", "package-lock.json", ".gitignore", "output/ecm26-three-days.pdf", "output/ecm26-options.pdf"]


def main():
    OUT.parent.mkdir(exist_ok=True)
    sources = [ROOT / path for path in FILES]
    for directory in DIRECTORIES:
        for path in (ROOT / directory).rglob("*"):
            if not path.is_file() or any(part in SKIP for part in path.relative_to(ROOT).parts):
                continue
            if path.name in {".env", ".env.local", "ecm26-flask-checkpoints.bundle"}:
                continue
            sources.append(path)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as archive:
        for path in sorted(sources):
            assert path.is_file(), path
            archive.write(path, "ecm26/" + str(path.relative_to(ROOT)))
    with ZipFile(OUT) as archive:
        assert archive.testzip() is None
        assert not any(part in SKIP or part == "_reference" for name in archive.namelist() for part in Path(name).parts)
        print(f"Course kit: {len(archive.namelist())} files, {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
