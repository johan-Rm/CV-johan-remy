# Les trois versions du CV

Le CV existe en trois fichiers HTML autonomes. Ils portent le **même parcours,
les mêmes missions et la même mise en page** : seuls sept blocs changent, pour
adresser trois situations différentes.

| Fichier | PDF produit | À qui il s'adresse |
| --- | --- | --- |
| `index.html` | `CV-Johan-REMY.pdf` | Clients, pour des missions en freelance — les deux pays à égalité |
| `V1-CV-Johan-REMY.html` | `V1-CV-Johan-REMY.pdf` | Employeurs **au Maroc**, pour un poste en CDI — présence sur place |
| `V2-CV-Johan-REMY.html` | `V2-CV-Johan-REMY.pdf` | Employeurs **en France**, pour un poste en CDI — travail à distance |

Aucun nom de fichier ne cite un pays ni un marché : ces PDF partent chez des
recruteurs, et leur nom ne doit pas révéler qu'il existe une version taillée
pour quelqu'un d'autre. Les deux versions « en poste » sont donc simplement
numérotées, et c'est ce tableau — qui reste chez toi — qui dit laquelle vise
quoi. **V1 pour le Maroc, V2 pour la France.**

## Les sept blocs qui diffèrent

Une modification du parcours, d'une mission ou de la mise en page doit être
reportée **dans les trois fichiers**. Ces sept blocs-là, au contraire, sont
propres à chaque version et ne se recopient pas.

| # | Où | Quoi |
| --- | --- | --- |
| 1 | `<title>`, en tête de fichier | Le titre affiché dans l'onglet du navigateur |
| 2 | Page 1, colonne olive, « Contact » | L'ordre des deux téléphones : le pays visé passe en premier |
| 3 | Page 1, colonne olive, « Contact » | La ligne « Localisation » et la mobilité annoncée |
| 4 | Page 1, en haut à droite | La ligne de titre : « Senior » seul, ou « Senior / Lead » |
| 5 | Page 1, « Profil », 3ᵉ paragraphe | La phrase qui dit ce qui est recherché |
| 6 | Page 2, colonne olive, bas | « Ce que je cherche » ou « Poste recherché », puis « Disponibilité » |
| 7 | Page 3, chapeau de l'annexe | La phrase qui rattache les missions au marché visé |

## La contrainte à connaître avant d'écrire une ligne

**La page 1 est pleine au caractère près.** Dans sa version d'origine, elle se
termine pile sur « standardisation des réponses HTTP. », sans une ligne de
marge. Toute phrase ajoutée en page 1 — et le bloc n° 5 est le seul endroit
tentant — pousse le bas de page hors de la feuille A4, silencieusement : le
texte n'est pas reporté sur la page suivante, il disparaît.

C'est pourquoi le bloc n° 5 tient en une phrase courte, et pourquoi la substance
du positionnement est écrite dans le bloc n° 6, en page 2, où il reste de la
place.

Les deux seuls réglages de densité sont les `zoom` des colonnes, dans
`outils/build-pdf.py`. Les baisser laisse du blanc en bas de page ; les monter
tronque le contenu.

## Vérifier avant d'envoyer

    python3 outils/build-pdf.py                        # les trois PDF
    python3 outils/build-pdf.py V2-CV-Johan-REMY.html  # un seul

Le script annonce le nombre de feuilles de chaque PDF : **il en faut exactement
trois**. Un quatrième feuillet, ou du texte manquant en bas de page, signale un
débordement — relire la contrainte ci-dessus.

Avec `poppler-utils` installé (`pdftotext`, `pdfinfo`), le script relit aussi le
texte du PDF et signale tout contenu tronqué. Sans lui, il compte seulement les
feuilles : le débordement en bas de page passe alors inaperçu, et la seule
vérification fiable est de **regarder le PDF**.
