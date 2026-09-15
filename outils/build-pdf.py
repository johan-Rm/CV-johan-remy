"""Fabrique les trois PDF du CV avec les fontes statiques embarquées.

La géométrie et les règles d’impression sont définies dans chaque HTML :
profil et expertises, puis expériences sur trois pages ; colonnes latérales
sur les deux premières pages. Le script conserve ces règles à l’identique.

    python3 outils/build-pdf.py
    python3 outils/build-pdf.py V0-CV-Johan-REMY.html
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

# Une section = une feuille : profil et expertises, puis trois pages d’expérience.
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
    # Repères communs aux trois variantes, répartis sur les quatre pages.
    manquants = [s for s in ("Expertises clés", "Smart Global Governance",
                             "Concepteur D\u00e9veloppeur", "Altraway",
                             "IA & méthode de travail", "Orsid Provence")
                 if s not in texte]
    print(f"  {pages} feuilles, {len(texte.split())} mots")
    if pages != str(FEUILLES_ATTENDUES):
        print(f"  ATTENTION : {pages} feuilles au lieu de {FEUILLES_ATTENDUES}"
              " — ajuster les zoom")
    if manquants:
        print(f"  ATTENTION : contenu tronque, absent du PDF : {manquants}")


def fabriquer(source, sortie, css_fontes, navigateur, chemin_pour):
    """Rend une variante HTML en PDF, puis relit le resultat."""
    html = source.read_text(encoding="utf-8")
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
