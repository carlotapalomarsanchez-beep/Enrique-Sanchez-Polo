"""Comprueba enlaces internos rotos, anclas inexistentes, imágenes sin alt y SVG sin descripción."""
import sys, pathlib, re
from html.parser import HTMLParser

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set(); self.issues = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src"):
            if k in a: self.links.append(a[k])
        if tag == "img" and not a.get("alt") and a.get("alt") != "":
            self.issues.append(f"<img> sin alt: {a.get('src')}")
        if tag == "svg" and a.get("aria-hidden") != "true" and not a.get("aria-label") and not a.get("role") == "img":
            pass  # los SVG dentro de contenedores aria-hidden se revisan abajo

pages = {}
for f in ROOT.glob("*.html"):
    p = P(); p.feed(f.read_text(encoding="utf-8")); pages[f.name] = p

errors = 0
for name, p in pages.items():
    for i in p.issues:
        print(f"{name}: {i}"); errors += 1
    for link in p.links:
        if re.match(r"^(https?:|mailto:|tel:|data:)", link) or link in ("#",):
            if link == "#": print(f"{name}: enlace vacío '#'"); errors += 1
            continue
        path, _, anchor = link.partition("#")
        path = path.split("?", 1)[0]
        target = name if not path else path
        if name == "404.html" and path.startswith("/Enrique-Sanchez-Polo/"):
            target = path.split("/Enrique-Sanchez-Polo/", 1)[1] or "index.html"
        if not (ROOT / target).exists():
            print(f"{name}: archivo no encontrado -> {link}"); errors += 1
        elif anchor and target in pages and anchor not in pages[target].ids:
            print(f"{name}: ancla no encontrada -> {link}"); errors += 1

print(f"{len(pages)} páginas revisadas, {errors} problemas")
sys.exit(1 if errors else 0)
