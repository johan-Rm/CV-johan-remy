"""Construit une copie de index.html avec les fontes statiques embarquees en data URI.

Chrome instancie les fontes variables de Google Fonts a la volee et les ecrit en
"Type 3" dans le PDF : un format que certains lecteurs et robots de tri de CV
lisent mal. Ce script fige chaque graisse en fonte statique et l'embarque dans le
HTML, ce qui donne un PDF en CID TrueType, plus leger et lisible partout.

Module utilise par build-pdf.py, qui est le point d'entree.

Dependances : pip install fonttools brotli
"""
import base64
import io
import re
import sys
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/148.0.0.0 Safari/537.36")
CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Rationale&"
           "family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap")
KEEP_SUBSETS = {"latin", "latin-ext"}


def get(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


def parse_faces(css):
    """Extrait (famille, style, graisse, sous-ensemble, url, plage unicode)."""
    faces, subset = [], None
    for chunk in re.split(r"(/\*\s*[a-z-]+\s*\*/)", css):
        header = re.match(r"/\*\s*([a-z-]+)\s*\*/", chunk.strip())
        if header:
            subset = header.group(1)
            continue
        for face in re.findall(r"@font-face\s*\{(.*?)\}", chunk, re.S):
            if subset not in KEEP_SUBSETS:
                continue
            rng = re.search(r"unicode-range:\s*([^;]+);", face)
            faces.append((
                re.search(r"font-family:\s*'([^']+)'", face).group(1),
                re.search(r"font-style:\s*(\S+);", face).group(1),
                int(re.search(r"font-weight:\s*(\d+)", face).group(1)),
                subset,
                re.search(r"url\((https://[^)]+)\)", face).group(1),
                rng.group(1).strip() if rng else None,
            ))
    return faces


def freeze(url, weight):
    """Telecharge une fonte et fige l'axe de graisse si elle est variable."""
    font = TTFont(io.BytesIO(get(url)))
    if "fvar" in font:
        axes = {"wght": weight}
        if any(axis.axisTag == "opsz" for axis in font["fvar"].axes):
            axes["opsz"] = 14
        font = instancer.instantiateVariableFont(font, axes, updateFontNames=False)
    font.flavor = None
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def build_font_css():
    """Renvoie les regles @font-face, fontes embarquees en data URI."""
    rules = []
    for family, style, weight, subset, url, rng in parse_faces(get(CSS_URL).decode()):
        data = freeze(url, weight)
        b64 = base64.b64encode(data).decode("ascii")
        rules.append(
            f"@font-face{{font-family:'{family}';font-style:{style};"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');"
            + (f"unicode-range:{rng};" if rng else "") + "}")
        print(f"  {family} {style} {weight} ({subset}) -> {len(data) // 1024} Ko",
              file=sys.stderr)
    return "".join(rules)
