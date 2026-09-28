# Les versions du CV

Les trois variantes partagent le même parcours, les mêmes expertises et la même mise en page. `index.html` conserve une ancienne version et ne fait pas partie de cette actualisation.

| HTML | PDF | Destinataire |
| --- | --- | --- |
| `V0-CV-Johan-REMY.html` | `V0-CV-Johan-REMY.pdf` | France et Maroc ; coordonnées françaises et marocaines |
| `V1-CV-Johan-REMY.html` | `V1-CV-Johan-REMY.pdf` | Employeurs au Maroc ; téléphone marocain et localisation à Essaouira |
| `Johan-REMY-CV.html` (V2) | `Johan-REMY-CV.pdf` | Employeurs en France ; téléphone français et localisation à Cannes |

## Différences à conserver

- Titre HTML commun : « Senior Développeur Full Stack ».
- V0 : deux téléphones, Essaouira et Cannes ; mobilité en France limitée aux Alpes-Maritimes (06).
- V1 : téléphone marocain et Essaouira ; aucune mention de mobilité française.
- V2 : téléphone français, Cannes, nationalité française et mobilité Alpes-Maritimes (06).
- Disponibilité « Dès que possible » dans les trois variantes.
- L’intention de rejoindre une équipe en CDI en première page est réservée à V2.
- « A PROPOS DE MOI » s’ouvre sur « Originaire de Marseille, je suis récemment revenu en France » dans V0 et V2 seulement : V1 affiche Essaouira. Les durées (six ans en France, neuf ans et demi au Maroc, dont huit en freelance) sont communes aux trois.
- Les missions freelance et Altraway CE indiquent « À distance » dans V2 et « Essaouira » dans V0/V1. Le nom « Immobilière Essaouira » reste intact.

Les modifications communes concernent les trois variantes numérotées. Les PDF sont générés depuis leurs HTML respectifs ; leurs noms ne mentionnent pas le marché visé.

## Organisation des quatre pages

1. Accroche et expériences Capnour, My Little Kasbah et Smart Global Governance ; colonne identité, contact, formation et stack. Espacements aérés entre les expériences.
2. Expériences de Kazen Garden à Altraway CE, en pleine largeur avec un liseré olive.
3. Expériences de Philae à Orsid Provence, avec la même présentation en pleine largeur.
4. « A PROPOS DE MOI » et expertises clés ; colonne langues, savoir-être, méthode et domaines.

La photo, le texte justifié, les répétitions et les listes de technologies sont conservés à la demande de Johan. Le site obsolète est retiré des coordonnées. Philae indique CDI. Le titre AFPA mentionne le niveau 6 (bac+3/4), confirmé par Johan.

## Mise en page et contrôle

Chaque `.page` est une boîte A4 de hauteur fixe, avec `overflow: hidden` : un débordement peut couper du texte sans créer de page supplémentaire.

La géométrie, les espacements, les densités (`zoom`) et les règles d’impression vivent dans les HTML. Le script PDF conserve ces règles ; il embarque des polices statiques pour rendre le PDF indépendant du réseau.

Après une modification, vérifier dans le navigateur la limite basse du contenu de chaque colonne, en attendant le chargement des polices. Conserver la marge basse et contrôler les quatre pages. Un simple comptage des pages ne suffit pas à détecter une coupure.

## Générer les PDF

```sh
python3 outils/build-pdf.py
python3 outils/build-pdf.py V0-CV-Johan-REMY.html
```

Le script nécessite Chrome ou Chromium (y compris Chrome Windows sous WSL) et un accès réseau pour récupérer les polices. `fontTools` et `brotli` sont facultatifs : sans eux, il utilise les polices statiques servies par l’API Google Fonts.

Il vérifie le nombre de pages. Si `pdfinfo` et `pdftotext` sont installés, il contrôle aussi quelques repères textuels. Ces contrôles complètent la vérification du rendu.
