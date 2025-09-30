#!/usr/bin/env python3
"""
build.py — scan ./images and ./collections to maintain gallery.json + collections.json

Rules:
- /images: all images become thumbnail items
- /collections/<slug>/: if contains index.html (or any .html), it becomes a FEATURED collection
  - title: from <title> tag or slug
  - summary: from collections/<slug>/meta.json["summary"] or descriptions/<slug>.{md,txt}
  - cover: prefer collections/<slug>/cover.* else first image in that folder else images/sample
  - pages: count *.html in the collection folder
  - images: count image files inside the collection folder
  - tags: from meta.json["tags"] or []

Optional sidecars:
- /descriptions/<base>.md|.txt for any image or collection slug

Usage: python build.py
"""
import os, json, time, pathlib, re, html

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "images"
COL = ROOT / "collections"
DESC = ROOT / "descriptions"
OUT_G = ROOT / "gallery.json"
OUT_C = ROOT / "collections.json"

IMG_EXT = {".png",".jpg",".jpeg",".gif",".webp",".avif",".svg"}
HTML_EXT = {".html",".htm"}

def slugify(s): return re.sub(r"(^-+|-+$)", "", re.sub(r"[^a-z0-9]+","-", s.lower()))

def read_sidecar(base):
    for ext in (".md",".txt"):
        p = (DESC / f"{base}{ext}")
        if p.exists():
            try:
                return p.read_text(encoding="utf-8").strip()
            except Exception:
                pass
    return ""

def parse_title_from_html(path: pathlib.Path):
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"<title>(.*?)</title>", txt, flags=re.IGNORECASE|re.DOTALL)
        if m: return html.unescape(m.group(1).strip())
    except Exception:
        pass
    return ""

def choose_cover(folder: pathlib.Path):
    for name in ("cover.jpg","cover.png","cover.webp","cover.jpeg","thumb.jpg","thumb.png"):
        p = folder / name
        if p.exists(): return f"collections/{folder.name}/{name}"
    # else first image in folder
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() in IMG_EXT:
            return f"collections/{folder.name}/{p.name}"
    return ""

def count_images(folder: pathlib.Path):
    n=0
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_EXT: n+=1
    return n

def build_gallery():
    items = []
    IMG.mkdir(exist_ok=True, parents=True)
    for p in sorted(IMG.iterdir()):
        if p.is_file() and p.suffix.lower() in IMG_EXT:
            item = {
                "id": slugify(p.stem),
                "file": p.name,
                "src": f"images/{p.name}",
                "thumb": f"images/{p.name}",
                "title": p.stem.replace('_',' ').title(),
                "caption": read_sidecar(p.stem),
                "tags": [],
                "created": time.strftime("%Y-%m-%d", time.localtime(p.stat().st_mtime)),
            }
            items.append(item)
    OUT_G.write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_G} with {len(items)} items.")

def build_collections():
    entries = []
    if not COL.exists(): 
        OUT_C.write_text("[]", encoding="utf-8"); 
        print("No collections/ folder found."); 
        return
    for folder in sorted([d for d in COL.iterdir() if d.is_dir()]):
        # qualifies if it has any html file
        htmls = [p for p in folder.iterdir() if p.suffix.lower() in HTML_EXT]
        if not htmls: 
            continue
        # pick index.html if present
        index = next((p for p in htmls if p.name.lower()=='index.html'), htmls[0])
        title = parse_title_from_html(index) or folder.name.replace('-',' ').title()
        meta_path = folder / "meta.json"
        meta = {}
        if meta_path.exists():
            try: meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception: meta = {}
        summary = meta.get("summary") or read_sidecar(folder.name)
        cover = meta.get("cover") or choose_cover(folder)
        tags = meta.get("tags") or []
        pages = len([p for p in folder.iterdir() if p.suffix.lower() in HTML_EXT])
        images = count_images(folder)
        entries.append({
            "slug": folder.name,
            "title": title,
            "summary": summary,
            "href": f"collections/{folder.name}/{index.name}",
            "cover": cover,
            "pages": pages,
            "images": images,
            "tags": tags
        })
    OUT_C.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_C} with {len(entries)} collections.")

if __name__ == "__main__":
    build_gallery()
    build_collections()
    print("Done.")
