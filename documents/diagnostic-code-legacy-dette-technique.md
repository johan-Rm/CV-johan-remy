# Diagnostic de code legacy et de dette technique

Un diagnostic de code legacy et de dette technique examine à la fois l’état technique de l’application et l’organisation qui permet de la faire évoluer. Il sert à identifier les risques, à comprendre les difficultés rencontrées et à définir un plan d’amélioration adapté aux priorités métier.

## 1. Comprendre le contexte

- Recueillir les objectifs métier, les contraintes et les priorités.
- Identifier les principales difficultés : bugs récurrents, lenteur des livraisons, départs de développeurs, coûts de maintenance, etc.
- Retracer l’historique du projet : migrations, choix techniques et contraintes organisationnelles ayant influencé ces choix.

## 2. Cartographier l’existant technique

- **Architecture :** composants, couplage, dépendances, schémas de base de données et flux d’API.
- **Stack technique :** technologies et versions utilisées, composants obsolètes ou non maintenus, dépendances présentant des vulnérabilités connues.
- **Tests :** présence et pertinence des tests unitaires, d’intégration et de bout en bout ; couverture des parcours critiques et fiabilité des tests.
- **Qualité du code :** lisibilité, duplication, complexité cyclomatique et cohérence des conventions.
- **Sécurité et conformité :** gestion des secrets et des accès, vulnérabilités identifiées et exigences applicables au contexte, notamment en matière de protection des données.

## 3. Analyser les processus et les pratiques

- **Intégration et déploiement continus (CI/CD) :** automatisation, contrôles qualité, durée et fiabilité des déploiements.
- **Méthodes de travail :** fonctionnement réel des pratiques Scrum, Kanban ou hybrides, et adéquation aux besoins de l’équipe.
- **Communication :** alignement entre direction technique, développeurs, produit et direction générale.
- **Gestion des tickets :** organisation du backlog, critères de priorisation et répartition entre bugs, évolutions et maintenance.

## 4. Évaluer la dette technique

- Distinguer la dette acceptable à court terme de celle qui bloque les évolutions ou expose l’application à un risque important.
- Repérer les zones critiques : modules sensibles, code fortement enchevêtré, dépendances fragiles ou absence de tests sur des parcours essentiels.
- Relier les constats à leurs conséquences métier : ralentissement des évolutions, incidents, risques de sécurité et coût de maintenance.
- Utiliser une échelle de lecture simple, par exemple rouge, orange et vert, avec des critères explicites. Signaler séparément les points non évalués.
- Documenter les constats et les éléments qui les étayent afin de justifier les priorités.

## 5. Formuler les recommandations et le plan de redressement

- Identifier les améliorations rapides : actions ciblées, à faible effort et à bénéfice identifiable.
- Préparer une amélioration progressive du code pour rétablir la stabilité et faciliter les évolutions.
- Clarifier les priorités : sécurité, fiabilité, performance, maintenabilité, évolutivité ou expérience utilisateur, selon les besoins.
- Construire une feuille de route réaliste, alignée sur les objectifs métier et la capacité de l’équipe.
- Préciser, pour chaque action, le bénéfice attendu, l’effort estimé, les dépendances et les critères de réussite.

## Outils et pratiques utiles

Les outils sont à sélectionner selon les technologies du projet et le périmètre du diagnostic.

| Domaine | Exemples d’outils ou de pratiques |
| --- | --- |
| Analyse du code et des dépendances | SonarQube, PHPStan, ESLint, Pylint, Bandit, Snyk |
| Analyse des performances | Profilage SQL, suivi des temps de réponse des API, outils de suivi des performances applicatives tels que Datadog ou New Relic |
| Échanges avec l’équipe | Entretiens ou ateliers avec les développeurs et la direction technique pour identifier les difficultés récurrentes |
| Revue documentaire | Comparaison de la documentation avec le code et le fonctionnement réel de l’application |

Les résultats automatiques doivent être interprétés et confrontés au contexte. Le taux de couverture des tests, à lui seul, ne suffit pas à évaluer leur pertinence.

## Livrable attendu

Un document synthétique, par exemple une dizaine de pages ou 15 à 20 diapositives, comprenant :

- Le périmètre du diagnostic et ses limites.
- Une cartographie de l’existant technique et organisationnel.
- Une évaluation de la dette technique, de l’architecture et des pratiques de travail, fondée sur des constats documentés.
- Les risques principaux, les priorités et les améliorations rapides proposées.
- Une feuille de route de redressement, éventuellement à 3, 6 et 12 mois, à adapter au contexte et aux moyens disponibles.

## Finalité du diagnostic

Donner à la direction et à l’équipe les éléments nécessaires pour décider où stabiliser l’existant, améliorer progressivement le code ou envisager une réécriture ciblée, en tenant compte des bénéfices, des coûts et des risques.
