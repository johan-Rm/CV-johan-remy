"""Fabrique CV-Johan-REMY.pdf a partir de index.html.

index.html porte deja la geometrie finale : trois feuilles A4 empilees, colonne
olive sur les deux premieres, fin lisere et pleine largeur sur l'annexe. Le site
et le PDF montrent donc exactement la meme chose, et aucun bloc n'a plus besoin
d'etre deplace ici.

Ce script ne fait que deux choses : figer les fontes en statique, pour que le PDF
ne dependent pas du reseau, et substituer le bloc @media print par celui qui force
une section par feuille. Il ne touche jamais au contenu.

    python3 outils/build-pdf.py

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
SOURCE = RACINE / "index.html"
SORTIE = RACINE / "CV-Johan-REMY.pdf"
TEMPORAIRE = RACINE / ".rendu-pdf.html"

NAVIGATEURS = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")

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

    /* la feuille 2 porte une vraie colonne olive, pas le lisere du site :
       cette regle annule le "padding: 0" prevu pour le lisere, qui sinon
       gagne en specificite et colle le texte au bord de la feuille. */
    .page + .page .sidebar { padding: 12mm 9mm; }
    .main    { zoom: 0.71; padding: 13mm 11mm 11mm 11mm; }

    /* l'annexe n'a pas de colonne olive : elle prend toute la feuille */
    .page.page-annexe, .page + .page.page-annexe {
      grid-template-columns: 10px 1fr;
    }
    .page-annexe .main { zoom: 0.73; padding: 13mm 12mm 11mm 10mm; }

    .sidebar h2 { margin-top: 6mm; }
    .skill-group { margin-bottom: 2.2mm; }
    .lang-list li, .edu-list li { margin-bottom: 2mm; }

    .xp { break-inside: avoid; page-break-inside: avoid; }
  }
"""

DEBUT_CSS = "  /* --- Print --- */"


def remplacer_css_impression(html):
    """Substitue le bloc @media print du site par celui du PDF."""
    if DEBUT_CSS not in html:
        raise SystemExit(f"Bloc CSS introuvable dans index.html : {DEBUT_CSS.strip()}")
    debut = html.index(DEBUT_CSS)
    fin = html.index("</style>", debut)
    return html[:debut] + CSS_IMPRESSION + html[fin:]


def trouver_navigateur():
    for nom in NAVIGATEURS:
        chemin = shutil.which(nom)
        if chemin:
            return chemin
    raise SystemExit(f"Aucun navigateur trouve parmi : {', '.join(NAVIGATEURS)}")


def verifier(pdf):
    """Relit le PDF produit : nombre de feuilles et fins de blocs presentes."""
    if not shutil.which("pdftotext") or not shutil.which("pdfinfo"):
        print("  (poppler-utils absent : verification sautee)")
        return
    infos = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = re.search(r"^Pages:\s+(\d+)", infos, re.M).group(1)
    texte = subprocess.run(["pdftotext", str(pdf), "-"],
                           capture_output=True, text=True).stdout
    manquants = [s for s in ("Lead technique", "structurants", "convaincu",
                             "haute exigence", "plateforme en production")
                 if s not in texte]
    print(f"  {pages} feuilles, {len(texte.split())} mots")
    if pages != "3":
        print(f"  ATTENTION : {pages} feuilles au lieu de 3 — ajuster les zoom")
    if manquants:
        print(f"  ATTENTION : contenu tronque, absent du PDF : {manquants}")


def main():
    html = SOURCE.read_text(encoding="utf-8")
    html = remplacer_css_impression(html)

    print("Fontes figees en statique :", file=sys.stderr)
    html = re.sub(r'\s*<link rel="preconnect"[^>]*>', "", html)
    html = re.sub(r'\s*<link href="https://fonts\.googleapis\.com[^>]*>',
                  "\n<style>" + build_font_css() + "</style>", html)

    # le fichier temporaire reste a la racine : la photo est en chemin relatif
    TEMPORAIRE.write_text(html, encoding="utf-8")
    try:
        subprocess.run([trouver_navigateur(), "--headless=new", "--disable-gpu",
                        "--no-sandbox", "--virtual-time-budget=15000",
                        "--no-pdf-header-footer", f"--print-to-pdf={SORTIE}",
                        TEMPORAIRE.as_uri()],
                       check=True, capture_output=True)
    finally:
        TEMPORAIRE.unlink(missing_ok=True)

    print(f"Ecrit {SORTIE.name}")
    verifier(SORTIE)


if __name__ == "__main__":
    main()
