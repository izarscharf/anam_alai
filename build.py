#!/usr/bin/env python3
"""Scan the content folders and write manifest.json for the site.

Run locally before previewing:  python3 build.py
On GitHub this runs automatically (see .github/workflows/pages.yml).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def read_text(path):
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def is_image(p):
    return p.is_file() and p.suffix.lower() in IMAGE_EXT


def title_from_folder(name):
    # "01-night-walks" -> "Night Walks" (leading number only sets the order)
    # "1995-plateau"   -> "Plateau - 1995" (a leading year is moved to the end)
    year = re.match(r"^(\d{4})[-_ ]+", name)
    name = re.sub(r"^\d+[-_ ]+", "", name)
    title = " ".join(w.capitalize() for w in re.split(r"[-_ ]+", name) if w)
    return f"{title} - {year.group(1)}" if year else title


def image_entry(img):
    return {
        "src": img.relative_to(ROOT).as_posix(),
        "caption": read_text(img.with_suffix(".txt")),
    }


def build_projects():
    projects = []
    for folder in sorted(p for p in (ROOT / "projects").iterdir() if p.is_dir()):
        images = [image_entry(i) for i in sorted(folder.iterdir()) if is_image(i)]
        if not images:
            continue
        projects.append({
            "slug": folder.name,
            "title": title_from_folder(folder.name),
            "description": read_text(folder / "description.txt"),
            "images": images,
        })
    return projects


def build_overview(projects):
    by_src = {img["src"]: (p["slug"], img) for p in projects for img in p["images"]}
    overview = []
    for line in read_text(ROOT / "overview.txt").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        src = "projects/" + line.removeprefix("projects/")
        if src not in by_src:
            print(f"warning: overview.txt entry not found: {line}", file=sys.stderr)
            continue
        slug, img = by_src[src]
        overview.append({**img, "project": slug})
    return overview


def build_about():
    about = ROOT / "about"
    portrait = next((i for i in sorted(about.glob("portrait.*")) if is_image(i)), None)
    return {
        "bio": read_text(about / "bio.txt"),
        "portrait": portrait.relative_to(ROOT).as_posix() if portrait else "",
    }


def build_cv():
    # "# Heading" starts a section; entries are "year<TAB or 2+ spaces>text".
    sections = []
    for line in read_text(ROOT / "cv.txt").splitlines():
        line = line.strip()
        if line.startswith("#"):
            sections.append({"title": line.lstrip("# "), "entries": []})
        elif line and sections:
            parts = re.split(r"\t+|\s{2,}", line, maxsplit=1)
            year, text = parts if len(parts) == 2 else ("", line)
            sections[-1]["entries"].append({"year": year, "text": text})
    return [s for s in sections if s["entries"]]


def build_news():
    # news/<name>.txt: "key: value" lines (date, title, source, link), a blank line, then the text.
    # An image with the same name is the thumbnail. Newest first = filenames sorted descending.
    folder = ROOT / "news"
    if not folder.is_dir():
        return []
    news = []
    for txt in sorted(folder.glob("*.txt"), reverse=True):
        header, _, text = read_text(txt).partition("\n\n")
        item = {"date": "", "title": "", "source": "", "link": "", "text": text.strip(), "image": ""}
        for line in header.splitlines():
            key, sep, value = line.partition(":")
            if sep and key.strip().lower() in item:
                item[key.strip().lower()] = value.strip()
        image = next((i for i in sorted(folder.glob(txt.stem + ".*")) if is_image(i)), None)
        if image:
            item["image"] = image.relative_to(ROOT).as_posix()
        news.append(item)
    return news


def main():
    projects = build_projects()
    manifest = {
        "site": json.loads(read_text(ROOT / "site.json") or "{}"),
        "about": build_about(),
        "cv": build_cv(),
        "news": build_news(),
        "overview": build_overview(projects),
        "projects": projects,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    n = sum(len(p["images"]) for p in projects)
    print(f"manifest.json: {len(projects)} projects, {n} images, {len(manifest['overview'])} in overview")


if __name__ == "__main__":
    main()
