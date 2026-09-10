# Les trois versions du CV

Le CV existe en trois fichiers HTML autonomes. Ils portent le **même parcours,
les mêmes missions et la même mise en page** : seuls sept blocs changent, pour
adresser trois situations différentes.

| Fichier | PDF produit | À qui il s'adresse |
| --- | --- | --- |
| `V0-CV-Johan-REMY.html` | `V0-CV-Johan-REMY.pdf` | Clients, pour des missions en **freelance** — les deux pays à égalité |
| `V1-CV-Johan-REMY.html` | `V1-CV-Johan-REMY.pdf` | Employeurs **au Maroc**, pour un poste en CDI — présence sur place |
| `V2-CV-Johan-REMY.html` | `V2-CV-Johan-REMY.pdf` | Employeurs **en France**, pour un poste en CDI — travail à distance |

Aucun nom de fichier ne cite un pays ni un marché : ces PDF partent chez des
recruteurs, et leur nom ne doit pas révéler qu'il existe une version taillée
pour quelqu'un d'autre. Les deux versions « en poste » sont donc simplement
numérotées, et c'est ce tableau — qui reste chez toi — qui dit laquelle vise
quoi. **V1 pour le Maroc, V2 pour la France.**

## Les six blocs qui diffèrent

Une modification du parcours, d'une mission ou de la mise en page doit être
reportée **dans les trois fichiers**. Ces six blocs-là, au contraire, sont
propres à chaque version et ne se recopient pas.

| # | Où | Quoi |
| --- | --- | --- |
| 1 | `<title>`, en tête de fichier | Ne doit **jamais** nommer un pays : Chrome le recopie dans les propriétés du PDF, où le destinataire peut le lire |
| 2 | Page 1, colonne olive, « Contact » | Le téléphone : **un seul numéro**, celui du pays visé. Seule la V0 affiche les deux |
| 3 | Page 1, colonne olive, « Contact » | La ligne « Localisation » : **un seul pays**, et la mobilité annoncée |
| 4 | Page 1, « Profil », **4ᵉ** paragraphe | Sa fin : ce qui est recherché, et « en prestation » pour la seule V0 |
| 5 | Page 2, colonne olive, bas | « Ce que je cherche » ou « Poste recherché », puis « Disponibilité » |
| 6 | Page 3, chapeau de l'annexe | La phrase qui rattache les missions au marché visé |

Le CV tient sur **quatre feuilles** : profil et expérience freelance, suite de
l'expérience salariée, puis deux feuilles d'annexe qui détaillent les dix
missions freelance.

Le bloc de titre en haut à droite — « Senior Développeur Full Stack » puis
« Orchestration Multi Agents » — et la ligne de mots-clés sous lui sont au
contraire **identiques dans les trois versions** : c'est la signature commune.

## La contrainte à connaître avant d'écrire une ligne

**Le texte en trop ne passe pas à la page suivante : il disparaît.** Chaque
feuille est une boîte fermée. Une phrase ajoutée en page 1 pousse le bas de page
hors du A4 sans le moindre signal — le PDF affiche toujours trois feuilles, et
seul un coup d'œil au rendu révèle la coupure.

État des marges, à la dernière mesure :

| Feuille | Marge disponible |
| --- | --- |
| 1 — profil et expérience | ~22 lignes (colonne de droite) · ~1,5 ligne (colonne olive) |
| 2 — expérience salariée | ~2 lignes |
| 3 — annexe, missions récentes | ~10 lignes |
| 4 — annexe, missions plus anciennes | ~35 lignes |

La colonne olive de la page 1 est le point le plus fragile : elle est saturée.
La page 2 l'est presque autant. Les deux feuilles d'annexe, elles, ont de la
réserve.

Chaque mission résumée en page 1 doit tenir sur **une seule ligne** : au-delà
d'environ 103 caractères, elle passe sur deux et laisse un mot orphelin.

Les deux seuls réglages de densité sont les `zoom` des colonnes, dans
`outils/build-pdf.py`. Les baisser laisse du blanc en bas de page ; les monter
tronque le contenu.

## Vérifier avant d'envoyer

    python3 outils/build-pdf.py                        # les trois PDF
    python3 outils/build-pdf.py V2-CV-Johan-REMY.html  # un seul

Le script annonce le nombre de feuilles de chaque PDF : **il en faut exactement
quatre**. Un feuillet de plus, ou du texte manquant en bas de page, signale un
débordement — relire la contrainte ci-dessus.

Avec `poppler-utils` installé (`pdftotext`, `pdfinfo`), le script relit aussi le
texte du PDF et signale tout contenu tronqué. Sans lui, il compte seulement les
feuilles : le débordement en bas de page passe alors inaperçu, et la seule
vérification fiable est de **regarder le PDF**.

## Deux pièges qui ne se voient pas à l'écran

### Le texte doit rester du texte

Si Chrome embarque les polices lui-même, il les écrit en « Type 3 » : le texte
n'est plus du texte mais un dessin, et les robots de tri de CV n'en extraient
plus rien. C'est le seul rôle de `outils/inline_fonts.py`, qui fige les polices
avant le rendu — par instanciation si `fontTools` est installé, sinon en
récupérant les polices déjà statiques de l'ancienne API de Google Fonts.

Contrôle, sur un PDF produit : il ne doit contenir **aucun** `/Subtype /Type3`,
et une poignée de `/Subtype /Type0`. Un PDF correct pèse environ 220 Ko ; s'il
approche 700 Ko, les polices sont en Type 3.

### Les blocs « Expérience » doivent rester frères

`.xp` porte une bordure gauche. Un `.xp` oublié ouvert englobe tous les suivants,
qui affichent alors **deux** bordures parallèles, décalées de la valeur du
`padding-left`. Le défaut a existé : le bloc « Philae » n'était pas fermé, et un
`</div>` en trop en page 1 rééquilibrait le compte, ce qui le rendait invisible
à toute vérification globale.

Contrôle : dans chaque feuille, autant de `<div` que de `</div>`, et tous les
`.xp` à la même profondeur d'imbrication.
