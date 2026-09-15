# Les versions du CV

Les trois variantes partagent le même parcours, les mêmes expertises et la même mise en page. `index.html` reprend V2.

| HTML | PDF | Destinataire |
| --- | --- | --- |
| `V0-CV-Johan-REMY.html` | `V0-CV-Johan-REMY.pdf` | Clients freelance ; coordonnées françaises et marocaines |
| `V1-CV-Johan-REMY.html` | `V1-CV-Johan-REMY.pdf` | Employeurs au Maroc ; téléphone marocain et localisation à Essaouira |
| `V2-CV-Johan-REMY.html` | `V2-CV-Johan-REMY.pdf` | Employeurs en France ; téléphone français et localisation à Cannes |

## Différences à conserver

- Le titre HTML : « Développeur Full Stack » pour V0, « Lead Développeur Full Stack » pour V1, V2 et `index.html`.
- Le téléphone et la localisation dans la rubrique Contact.

Les autres changements de contenu ou de présentation sont à reporter dans les quatre HTML. Les noms des PDF et leurs titres ne mentionnent pas le marché visé.

## Organisation des quatre pages

1. Profil et huit blocs d’expertises, dont la méthode de travail avec l’IA ; colonne identité, contact, stack et domaines.
2. Capnour, My Little Kasbah et Smart Global Governance ; colonne langues, formation, savoir-être et méthode.
3. Expériences de Kazen Garden à Altraway CE, en pleine largeur avec un liseré olive.
4. Expériences de Philae à Orsid Provence, avec la même présentation en pleine largeur.

Les missions freelance comportent le secteur, le statut, la localisation, les dates, les réalisations, puis la stack sous forme de tags après la description. Les secteurs ont été déduits des informations disponibles et restent à valider par Johan. La localisation des missions freelance et d’Altraway CE est Essaouira, conformément à sa demande.

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
