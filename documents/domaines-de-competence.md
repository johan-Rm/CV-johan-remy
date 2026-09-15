# Domaines de compétence

## Conception de bases de données

### Modélisation relationnelle et transactions

- Modélisation fine respectant les bonnes pratiques de normalisation.
- Gestion des transactions atomiques et cohérence entre entités complexes.
- Alignement possible sur des standards ouverts pour favoriser l’interopérabilité.

### Intégrité

- Définition de clés étrangères, contraintes, index et triggers lorsque nécessaire.
- Gestion de l’évolution du schéma via des migrations versionnées.
- Tests de cohérence des données et règles métier encapsulées dans le schéma.

### Performance

- Optimisation par index composites, partitionnement, requêtes préparées et caches.
- Analyse et ajustement des plans d’exécution des requêtes.
- Prévention des problèmes classiques comme les requêtes N+1.

### Sécurité et gouvernance des données

- Gestion fine des accès et rôles au niveau de la base de données.
- Masquage ou chiffrement des données sensibles.
- Stratégies de sauvegarde et restauration éprouvées.

### Évolutivité

- Conception pensée pour la montée en charge : réplication, sharding, hybridation SQL/NoSQL si pertinent.
- Stratégies d’archivage pour préserver la performance des tables principales.

## Conception d’API

### Standards et conception

- Conception REST structurée ou approche GraphQL selon les besoins.
- Structuration claire des points d’accès, gestion des versions et conventions de nommage.
- Séparation entre logique métier et objets de transfert.

### Robustesse et sécurité

- Gestion avancée de l’authentification et de l’autorisation.
- Validation stricte des données entrantes.
- Gestion cohérente et normalisée des erreurs.
- Protection contre les abus (limitation de débit, contrôle des accès).

### Interopérabilité

- Documentation claire et systématique.
- Tests contractuels pour assurer la compatibilité avec les clients.
- Gestion des versions et de la rétrocompatibilité.

### Performance

- Chargement optimisé des données (traitements par lots, mise en cache).
- Gestion des imports et exports volumineux via pagination et traitements asynchrones.
- Suivi de la performance et de la consommation des ressources.

### Évolutivité

- Architecture en couches pour isoler la logique métier.
- Conception pour plusieurs clients et plateformes.
- Montée en charge horizontale avec distribution de la charge.

## Conception d’applications web et de sites modernes

### Expérience utilisateur

- Mise en place d’un système de design cohérent.
- Composants d’interface réutilisables et transitions fluides.
- Respect strict des maquettes et rendu pixel-perfect.

### Architecture frontend

- Organisation claire des composants, stores, services et routes.
- Gestion structurée de l’état, chargement à la demande et découpage du code.
- Rendu côté serveur (SSR) ou génération statique (SSG) pour favoriser le référencement et la rapidité.
- Gestion avancée des flux de données (temps réel, différé, préchargement).

### Montée en charge et maintenance

- Séparation claire des responsabilités.
- Tests automatisés à différents niveaux (unitaires, de bout en bout).
- Intégration continue et déploiement continu.

### Fiabilité et sécurité

- Gestion robuste des erreurs côté client.
- Protection contre les vulnérabilités courantes (XSS, CSRF).
- Suivi de la qualité et de la performance via indicateurs frontend.

### Évolutivité

- Conception modulaire et adaptable (multitenant, interfaces d’administration, SaaS).
- Optimisation pour la montée en charge (cache, CDN, rendu en périphérie de réseau).
- Prise en compte native de l’internationalisation et de l’accessibilité.

## DevOps et intégration

### Conteneurisation et environnements

- Conteneurisation des applications avec Docker.
- Gestion des environnements via Nginx et scripts shell.
- Mise en place d’environnements utilisant plusieurs stacks cohérents.

### Intégration et déploiement continus (CI/CD)

- Pipelines automatisés avec GitLab CI/CD et GitHub Actions.
- Utilisation de Makefiles pour standardiser les processus de travail.
- Déploiement continu et supervision des versions.

### Cloud et hébergement

- Intégration avec Google Cloud Platform.
- Combinaison d’infrastructures cloud et sur site adaptée aux besoins.
- Supervision et observabilité des services.

### Qualité et sécurité

- Analyse continue via SonarQube.
- Sécurisation des pipelines d’intégration.
- Stratégies de tests intégrés avant déploiement.

## Documentation et tests

### Documentation technique

- Spécifications via Swagger/OpenAPI.
- Documentation applicative (Nuxt UI Docs, JSDoc, README).
- Transmission claire des informations aux équipes et aux clients.

### Tests automatisés

- Tests unitaires avec Vitest.
- Tests de bout en bout avec Cypress.
- Tests fonctionnels et d’intégration avec Behat.

### Conventions et qualité

- Application stricte de règles d’analyse statique et de formatage.
- Revue de code systématique et programmation en binôme.
- Validation automatisée dans les processus de travail Git.

## Leadership et collaboration

### Encadrement technique

- Mentorat et accompagnement des développeurs juniors.
- Programmation en binôme pour renforcer la qualité du code.
- Diffusion des bonnes pratiques au sein des équipes.

### Gestion d’équipe

- Structuration et organisation des projets.
- Suivi agile (Scrum, Kanban) avec des outils collaboratifs.
- Coordination entre développeurs, designers et clients.

### Communication et collaboration

- Utilisation d’outils collaboratifs : Figma, ClickUp, Trello, Balsamiq, draw.io.
- Animation de revues de sprint et présentations techniques.
- Gestion de la documentation vivante des projets.

### Refactorisation et legacy

- Identification et réduction de la dette technique.
- Migration progressive des systèmes existants.
- Documentation pour faciliter la reprise de code.

## UI/UX et systèmes de design

### Systèmes de design

- Mise en place et intégration dans plusieurs projets.
- Utilisation de Nuxt UI et Tailwind, et collaboration avec des agences spécialisées.
- Centralisation des composants pour favoriser la réutilisabilité.

### Rendu pixel-perfect

- Respect strict des maquettes fournies.
- Accessibilité (a11y) intégrée dès la conception.
- Internationalisation (i18n) native dans les projets.

### Optimisation

- Optimisation des performances frontend (chargement à la demande, découpage du code).
- Référencement naturel des pages et amélioration des temps de chargement.
- Utilisation du rendu côté serveur (SSR) et de la génération statique (SSG) pour favoriser la rapidité et l’indexation.
