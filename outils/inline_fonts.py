"""Construit une copie d'une variante du CV, fontes statiques embarquees en data URI.

Chrome instancie les fontes variables de Google Fonts a la volee et les ecrit en
"Type 3" dans le PDF : un format que certains lecteurs et robots de tri de CV
lisent mal. Ce script fige chaque graisse en fonte statique et l'embarque dans le
HTML, ce qui donne un PDF en CID TrueType, plus leger et lisible partout.

Deux chemins, le second sans aucune dependance :

  - avec fontTools : chaque graisse est instanciee depuis la fonte variable et
    limitee aux sous-ensembles latins. C'est le plus leger.
  - sans fontTools : l'API v1 de Google Fonts sert une fonte DEJA statique, une
    par graisse, en TrueType — donc rien a instancier ni a decompresser. Plus
    lourd a telecharger, mais le PDF reste en CID TrueType, jamais en Type 3.

Module utilise par build-pdf.py, qui est le point d'entree.

Dependances facultatives : pip install fonttools brotli
"""
import base64
import io
import re
import sys
import urllib.request

try:
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
except ModuleNotFoundError:            # le repli statique prend le relais
    TTFont = instancer = None

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/148.0.0.0 Safari/537.36")
CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Rationale&"
           "family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap")
KEEP_SUBSETS = {"latin", "latin-ext"}

# Un navigateur d'avant WOFF2 : l'API v1 lui sert du TrueType statique.
UA_STATIQUE = ("Mozilla/5.0 (Linux; U; Android 4.0.3; en-us) AppleWebKit/534.30 "
               "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30")
# Les graisses reellement utilisees par le CV.
FACES_STATIQUES = (
    ("Inter", "normal", 300), ("Inter", "normal", 400), ("Inter", "normal", 500),
    ("Inter", "normal", 600), ("Inter", "normal", 700), ("Inter", "italic", 400),
    ("Rationale", "normal", 400),
)
SIGNATURES_TTF = (b"\x00\x01\x00\x00", b"true")


def get(url, ua=UA):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": ua}), timeout=30).read()


def regle_font_face(family, style, weight, data, rng=None):
    """Une regle @font-face portant la fonte en data URI."""
    b64 = base64.b64encode(data).decode("ascii")
    return (f"@font-face{{font-family:'{family}';font-style:{style};"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');"
            + (f"unicode-range:{rng};" if rng else "") + "}")


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


def build_font_css_instanciees():
    """Chemin nominal : fontes variables figees graisse par graisse."""
    rules = []
    for family, style, weight, subset, url, rng in parse_faces(get(CSS_URL).decode()):
        data = freeze(url, weight)
        rules.append(regle_font_face(family, style, weight, data, rng))
        print(f"  {family} {style} {weight} ({subset}) -> {len(data) // 1024} Ko",
              file=sys.stderr)
    return "".join(rules)


def build_font_css_statiques():
    """Repli sans dependance : fontes deja statiques servies par l'API v1."""
    rules = []
    for family, style, weight in FACES_STATIQUES:
        spec = f"{family}:{weight}{'italic' if style == 'italic' else ''}"
        css = get(f"https://fonts.googleapis.com/css?family={spec}", UA_STATIQUE)
        url = re.search(r"url\((https://[^)]+)\)", css.decode())
        if not url:
            raise SystemExit(f"Aucune fonte servie pour {spec}")
        data = get(url.group(1), UA_STATIQUE)
        if data[:4] not in SIGNATURES_TTF:
            raise SystemExit(f"{spec} : reponse non TrueType, PDF en Type 3 evite")
        rules.append(regle_font_face(family, style, weight, data))
        print(f"  {family} {style} {weight} (statique) -> {len(data) // 1024} Ko",
              file=sys.stderr)
    return "".join(rules)


def build_font_css():
    """Renvoie les regles @font-face, fontes embarquees en data URI.

    Le repli est large a dessein : fontTools sans brotli, ou une fonte variable
    illisible, doit basculer sur les statiques plutot que produire un PDF en
    Type 3 — que les robots de tri de CV lisent mal.
    """
    if TTFont is not None:
        try:
            return build_font_css_instanciees()
        except Exception as erreur:
            print(f"  (instanciation impossible : {erreur} — repli statique)",
                  file=sys.stderr)
    else:
        print("  (fontTools absent : fontes statiques de l'API v1)", file=sys.stderr)
    return build_font_css_statiques()
