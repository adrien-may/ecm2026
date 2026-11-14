"""Check both course PDFs and point checkpoint downloads to the public repository."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = Path(__file__).resolve().parents[1]
DECKS = [("slides", "ecm26-three-days"), ("options", "ecm26-options")]
DOWNLOAD_BASE = "https://github.com/adrien-may/ecm2026/raw/refs/heads/main/slides/public/checkpoints/"
writers = []
linked_files = set()
for deck, filename in DECKS:
    entry = ROOT / "slides" / f"{deck}.md"
    sources = [entry] + [
        entry.parent / src
        for src in re.findall(r"^src: (.+)$", entry.read_text(), re.MULTILINE)
    ]
    content = "\n".join(source.read_text() for source in sources)
    expected = set(re.findall(r'href="[^"]*/checkpoints/([^"]+)"', content))
    path = ROOT / "output" / f"{filename}.pdf"
    writer = PdfWriter(clone_from=str(path))
    page_count = len(re.findall(r"^# ", content, re.MULTILINE))
    if len(writer.pages) != page_count:
        raise ValueError(f"{filename}: expected {page_count} pages, got {len(writer.pages)}")
    if any(not (page.extract_text() or "").strip() or "Loading slide..." in page.extract_text()
           for page in writer.pages):
        raise ValueError(f"{filename}: blank or still-loading page")
    links = set()
    count = 0
    for page in writer.pages:
        for reference in page.get("/Annots", []):
            action = reference.get_object().get("/A")
            if not action or "/URI" not in action:
                continue
            uri = str(action["/URI"])
            url = urlsplit(uri)
            local = url.hostname in {"localhost", "127.0.0.1"} and url.path.startswith("/checkpoints/")
            if local or uri.startswith(DOWNLOAD_BASE):
                filename = Path(url.path).name
                if not (ROOT / "slides/public/checkpoints" / filename).is_file():
                    raise ValueError(f"Unknown checkpoint download: {filename}")
                action[NameObject("/URI")] = TextStringObject(DOWNLOAD_BASE + filename)
                count += 1
                links.add(filename)
    if expected - links:
        raise ValueError(f"{filename}: missing download links: {sorted(expected - links)}")
    linked_files |= links
    writers.append((path, writer, count))

manifest = json.loads((ROOT / "slides/public/checkpoints/manifest.json").read_text())
missing = {item["file"] for item in manifest} - linked_files
if missing:
    raise ValueError(f"Course PDFs are missing checkpoint links: {sorted(missing)}")

# Validate the whole set before replacing either output.
for path, writer, count in writers:
    temporary = path.with_suffix(".tmp.pdf")
    writer.write(temporary)
    assert len(PdfReader(temporary).pages) == len(writer.pages)
    temporary.replace(path)
    print(f"{path.name}: {len(writer.pages)} pages, {count} download links to GitHub")
