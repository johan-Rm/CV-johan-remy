# Ajouter GitHub au CV et au DCI

**Statut** : ✅ fait le 2026-10-07
Lien GitHub ajouté sous LinkedIn dans les CV et le DCI, exports actualisés.
**Type** : feat
**Tests** : sans objet — ajout de coordonnées et exports documentaires, sans code applicatif.

## Cadrage
Carte rédigée après coup pour tracer l’ajout demandé et validé par Johan.
Ajouter https://github.com/johan-Rm sous LinkedIn. Le DCI ne contenant pas LinkedIn, ajouter les deux liens dans son en-tête.

## Livré
- Trois variantes HTML du CV et index.html : GitHub dans les coordonnées.
- DCI HTML et Word : LinkedIn puis GitHub, liens cliquables.
- Trois PDF du CV et PDF du DCI régénérés avec polices embarquées.

## Vérification
- Lien GitHub présent une fois dans chaque HTML, après LinkedIn.
- index.html identique au CV principal.
- Archive Word intacte, XML du contenu et relations valides ; liens externes présents.
- PDF : lien GitHub cliquable présent ; quatre pages par CV, vingt pages pour le DCI, comme auparavant.
- git diff --check : aucune erreur.

## Documentation
Aucune convention modifiée ; aucune autre documentation impactée.

## Définition de terminé
- [x] Coordonnées ajoutées et validées par Johan.
- [x] Exports actualisés.
- [x] Contrôles effectués.
