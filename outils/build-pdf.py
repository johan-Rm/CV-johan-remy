"""Fabrique les PDF du CV a partir de ses trois variantes HTML.

Chaque variante porte deja la geometrie finale : quatre feuilles A4 empilees,
colonne olive sur les deux premieres, fin lisere et pleine largeur sur les deux
feuilles d'annexe.
Le site et le PDF montrent donc exactement la meme chose, et aucun bloc n'a plus
besoin d'etre deplace ici.

Ce script ne fait que deux choses : figer les fontes en statique, pour que le PDF
ne dependent pas du reseau, et substituer le bloc @media print par celui qui force
une section par feuille. Il ne touche jamais au contenu.

    python3 outils/build-pdf.py                        # les trois variantes
    python3 outils/build-pdf.py V1-CV-Johan-REMY.html  # une seule

Les trois variantes se distinguent par sept blocs seulement, listes dans
outils/variantes.md. Le reste du contenu est identique.

Dependances : fonttools, brotli, et Chrome (ou Chromium) installe.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from inline_fonts import build_font_css  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
TEMPORAIRE = RACINE / ".rendu-pdf.html"

# Une section = une feuille : profil, experience, et deux feuilles d'annexe.
FEUILLES_ATTENDUES = 4

# Une variante HTML = un PDF. L'ordre est celui de la generation par defaut.
# Aucun nom de fichier ne nomme un pays ni un marche : le PDF part chez un
# recruteur, et son nom ne doit pas trahir qu'il existe une version taillee pour
# quelqu'un d'autre. Les deux variantes en poste sont donc numerotees, et
# outils/variantes.md dit laquelle vise quoi.
VARIANTES = {
    "V0-CV-Johan-REMY.html": "V0-CV-Johan-REMY.pdf",
    "V1-CV-Johan-REMY.html": "V1-CV-Johan-REMY.pdf",
    "V2-CV-Johan-REMY.html": "V2-CV-Johan-REMY.pdf",
}

NAVIGATEURS = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")

# Sous WSL, Chrome n'est souvent installe que cote Windows. Il rend alors tres
# bien les fichiers du dépôt, a condition de lui passer des chemins Windows.
CHROME_WINDOWS = (
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
    "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
)

# Regles d'impression du PDF : une section = exactement une feuille A4.
# Les deux valeurs de zoom sont les seuls reglages de densite ; les augmenter
# tronque le contenu, les baisser laisse du blanc en bas de page.
CSS_IMPRESSION = """  /* --- Print (genere par outils/build-pdf.py) --- */
  @media print {
    html, body {
      display: block;
      padding: 0;
      background: #FFFFFF;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* une section = exactement une feuille A4 : aucune coupure à gérer */
    .page, .page + .page {
      width: 210mm;
      height: 297mm;
      min-height: 0;
      margin: 0;
      overflow: hidden;
      box-shadow: none;
      grid-template-columns: 72mm 1fr;
      break-after: page;
      page-break-after: always;
    }
    .page:last-child { break-after: auto; page-break-after: auto; }

    /* densité : un seul réglage par colonne */
    .sidebar { zoom: 0.84; padding: 12mm 9mm; }
    .main    { zoom: 0.71; padding: 13mm 11mm 11mm 11mm; }

    /* l'annexe n'a pas de colonne olive : elle prend toute la feuille */
    .page.page-annexe, .page + .page.page-annexe {
      grid-template-columns: 10px 1fr;
    }
    /* le lisere reste un trait : sans ce rappel, un padding herite de
       .sidebar gonfle sa boite et la fait deborder sur le texte */
    .page-annexe .sidebar { padding: 0; }
    .page-annexe .main { zoom: 0.73; padding: 13mm 12mm 11mm 10mm; }

    .sidebar h2 { margin-top: 6mm; }
    .skill-group { margin-bottom: 2.2mm; }
    .lang-list li, .edu-list li { margin-bottom: 2mm; }

    .xp { break-inside: avoid; page-break-inside: avoid; }
  }
"""

DEBUT_CSS = "  /* --- Print --- */"


def remplacer_css_impression(html, source="la variante"):
    """Substitue le bloc @media print du site par celui du PDF."""
    if DEBUT_CSS not in html:
        raise SystemExit(f"Bloc CSS introuvable dans {source} : {DEBUT_CSS.strip()}")
    debut = html.index(DEBUT_CSS)
    fin = html.index("</style>", debut)
    return html[:debut] + CSS_IMPRESSION + html[fin:]


def trouver_navigateur():
    """Renvoie (executable, convertisseur de chemin) du premier Chrome trouve."""
    for nom in NAVIGATEURS:
        chemin = shutil.which(nom)
        if chemin:
            return chemin, str

    for chemin in CHROME_WINDOWS:
        if Path(chemin).exists():
            print("  (Chrome absent de Linux : rendu par le Chrome de Windows)")
            return chemin, vers_chemin_windows

    raise SystemExit("Aucun navigateur trouve parmi : "
                     f"{', '.join(NAVIGATEURS)} ni cote Windows")


def vers_chemin_windows(chemin):
    """Traduit un chemin WSL en chemin UNC comprehensible par un binaire Windows."""
    return subprocess.run(["wslpath", "-w", str(chemin)],
                          capture_output=True, text=True, check=True).stdout.strip()


def compter_feuilles(pdf):
    """Compte les feuilles sans poppler, en lisant les objets /Type /Page."""
    return str(len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes())))


def verifier(pdf):
    """Relit le PDF produit : nombre de feuilles et fins de blocs presentes."""
    if not shutil.which("pdftotext") or not shutil.which("pdfinfo"):
        feuilles = compter_feuilles(pdf)
        note = ("" if feuilles == str(FEUILLES_ATTENDUES)
                else f"  ATTENTION : attendu {FEUILLES_ATTENDUES} — ajuster les zoom")
        print(f"  {feuilles} feuilles (poppler-utils absent : contenu non relu){note}")
        return
    infos = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = re.search(r"^Pages:\s+(\d+)", infos, re.M).group(1)
    texte = subprocess.run(["pdftotext", str(pdf), "-"],
                           capture_output=True, text=True).stdout
    # une sentinelle par zone du document, toutes communes aux trois variantes :
    # sidebar p1, corps p1, sidebar p2, corps p2 (debut et fin), annexe p3
    manquants = [s for s in ("Lead technique", "Smart Global Governance",
                             "Concepteur D\u00e9veloppeur", "convaincu",
                             "haute exigence", "plateforme en production")
                 if s not in texte]
    print(f"  {pages} feuilles, {len(texte.split())} mots")
    if pages != str(FEUILLES_ATTENDUES):
        print(f"  ATTENTION : {pages} feuilles au lieu de {FEUILLES_ATTENDUES}"
              " — ajuster les zoom")
    if manquants:
        print(f"  ATTENTION : contenu tronque, absent du PDF : {manquants}")


def fabriquer(source, sortie, css_fontes, navigateur, chemin_pour):
    """Rend une variante HTML en PDF, puis relit le resultat."""
    html = remplacer_css_impression(source.read_text(encoding="utf-8"), source.name)
    html = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", html)
    html = re.sub(r'\s*<link href="https://fonts\.googleapis\.com[^>]*>',
                  "\n<style>" + css_fontes + "</style>", html)

    # le fichier temporaire reste a la racine : la photo est en chemin relatif
    TEMPORAIRE.write_text(html, encoding="utf-8")
    try:
        subprocess.run([navigateur, "--headless=new", "--disable-gpu",
                        "--no-sandbox", "--virtual-time-budget=15000",
                        "--no-pdf-header-footer",
                        f"--print-to-pdf={chemin_pour(sortie)}",
                        chemin_pour(TEMPORAIRE)],
                       check=True, capture_output=True)
    finally:
        TEMPORAIRE.unlink(missing_ok=True)

    print(f"Ecrit {sortie.name}")
    verifier(sortie)


def main(argv):
    demandees = argv or list(VARIANTES)
    inconnues = [n for n in demandees if n not in VARIANTES]
    if inconnues:
        raise SystemExit(f"Variante inconnue : {inconnues} — attendu : {list(VARIANTES)}")

    print("Fontes figees en statique :", file=sys.stderr)
    css_fontes = build_font_css()

    navigateur, chemin_pour = trouver_navigateur()

    for nom in demandees:
        source = RACINE / nom
        if not source.exists():
            raise SystemExit(f"Variante absente du depot : {source}")
        fabriquer(source, RACINE / VARIANTES[nom], css_fontes, navigateur, chemin_pour)


if __name__ == "__main__":
    main(sys.argv[1:])
