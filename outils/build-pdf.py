"""Fabrique CV-Johan-REMY.pdf a partir de index.html.

index.html porte le design du site : trois pages hautes cote a cote, colonne
olive complete sur la premiere, fin lisere sur les suivantes. Le PDF, lui, doit
tenir sur trois feuilles A4 dont les deux premieres portent la colonne olive,
ce qui suppose d'en repartir le contenu sur ces deux sections. Aucune regle CSS
ne sait deplacer un bloc d'un endroit a un autre du document : la transformation
se fait donc ici, sur une copie.

La feuille 3 est l'annexe des missions freelance : elle garde le lisere fin et
prend toute la largeur, ses deux colonnes de texte ayant besoin de la place.

index.html reste la source unique du contenu. Ce script n'en modifie jamais
le contenu, il ne fait que le reorganiser pour l'impression.

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
    .page + .page.page-annexe .sidebar { padding: 0; }
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

DEBUT_QUEUE = "    <h2>Langues</h2>"
FIN_ASIDE = "  </aside>"
ASIDE_VIDE = '<aside class="sidebar"></aside>'
DEBUT_CSS = "  /* --- Print --- */"


def repartir_colonne(html):
    """Deplace la queue de la colonne olive (Langues -> Disponibilite) en feuille 2.

    La feuille 3 (annexe) garde sa colonne vide : elle n'est qu'un lisere, ce qui
    lui laisse toute la largeur de la feuille pour ses deux colonnes de texte.
    """
    if DEBUT_QUEUE not in html:
        raise SystemExit(f"Bloc introuvable dans index.html : {DEBUT_QUEUE.strip()}")
    debut = html.index(DEBUT_QUEUE)
    fin = html.index(FIN_ASIDE, debut)
    queue = html[debut:fin].rstrip() + "\n"
    html = html[:debut] + html[fin:]

    if ASIDE_VIDE not in html:
        raise SystemExit(f"Colonne de la feuille 2 introuvable : {ASIDE_VIDE}")
    return html.replace(
        ASIDE_VIDE, '<aside class="sidebar">\n\n' + queue + "\n  </aside>", 1)


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
    html = repartir_colonne(html)
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
