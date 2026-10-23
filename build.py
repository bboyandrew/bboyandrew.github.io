"""Inline images from img/ into pages -> dist/ (single-file HTML).

src/index.html      -> dist/andrey-fediakin.html
variants/<name>.html -> dist/variants/<name>.html
"""
import base64, pathlib, re

root = pathlib.Path(__file__).parent

def inline(m):
    data = (root / "img" / f"{m.group(1)}.jpg").read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()

def build(src, dst):
    out = re.sub(r"\{\{img:([\w-]+)\}\}", inline, src.read_text(encoding="utf-8"))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    print("ok", dst.relative_to(root), len(out) // 1024, "KB")

build(root / "src" / "index.html", root / "dist" / "andrey-fediakin.html")
for v in sorted((root / "variants").glob("*.html")):
    build(v, root / "dist" / "variants" / v.name)
