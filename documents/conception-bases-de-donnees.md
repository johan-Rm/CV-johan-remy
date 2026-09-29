# Conception de bases de données

Notes de Johan, conservées comme document de contexte pour aligner le CV et le DCI. Version détaillée de la rubrique « Conception de bases de données » de [domaines-de-competence.md](domaines-de-competence.md).

## Résumé

- Modélisation conforme aux standards **Schema.org**, découpage atomique des tables.
- Conception avancée de bases relationnelles : intégrité, performance, évolutivité.
- Nommage et clés, politique de clés étrangères, plan d’indexation (index simples et composites).
- Stratégie d’identification.
- Gouvernance des métadonnées (énumérations, constantes) : **une source de vérité unique**.
- Pipelines ETL, scripts et traitement de données.
- Normalisation (de la 1NF à la 3NF) et dénormalisation raisonnée.
- Stratégies d’archivage pour préserver la performance des tables principales.
- Tests d’intégrité, fonctionnels (CRUD) et de performance (volumétrie, p95 / p99).
- Évolution du schéma par des migrations versionnées.
- Interopérabilité : Schema.org, typage des DTO et des payloads.
- Scripts d’initialisation et de données de référence (pays, statuts, rôles) reproductibles.
- Outils en ligne de commande pour gérer et automatiser les opérations sur la base.
- Observabilité : métriques (connexions, verrous, entrées-sorties) et alertes (latence, croissance).
- Procédures d’exploitation : montée de version, retour arrière, correction de données en urgence, purge et archivage.

## 1. Modélisation relationnelle et atomique

- **Modélisation fine respectant les formes normales** (viser la 3NF, voire la BCNF, quand c’est pertinent).
  - *Normaliser*, c’est organiser les données en tables pour éviter les doublons et les incohérences.
  - *3NF (troisième forme normale)* : élimine les dépendances transitives ; chaque colonne dépend directement de la clé primaire.
  - *BCNF (forme normale de Boyce-Codd)* : version plus stricte de la 3NF, qui supprime les dépendances « piégeuses ».
  - *Objectif* : éviter les anomalies d’insertion, de mise à jour et de suppression, donc les données redondantes ou corrompues.
  - *Pragmatisme* : la 3NF ou la BCNF comme standard, avec une dénormalisation ponctuelle pour la performance ou le reporting.
- **Cohérence des transactions (propriétés ACID) et invariants entre entités**, pour éviter toute donnée corrompue ou incohérente.
  - *Transactions* : un ensemble d’opérations s’exécute comme une seule unité, tout ou rien, selon les propriétés ACID (atomicité, cohérence, isolation, durabilité). Aucun état ne reste à moitié modifié.
  - *Invariants* : règles métier qui doivent toujours être vraies (par exemple, un projet a au moins un propriétaire).
  - *Ensemble* : les transactions appliquent ou annulent en bloc, les invariants fixent les contraintes métier ; la base reste fiable et cohérente.
- **Vocabulaire métier tracé dans un glossaire, périmètre et flux cadrés par un diagramme de contexte.**
  - Le glossaire évite les confusions : un langage commun.
  - Le diagramme de contexte évite le hors-périmètre : des frontières claires.
  - Les deux posent les bases avant de dessiner le premier schéma relationnel.

## 2. Intégrité

- Clés étrangères avec des règles explicites de suppression et de mise à jour (`ON DELETE` / `ON UPDATE` : restrict, cascade, set null).
- Contraintes de domaine (`CHECK`, bornes, formats) et unicités sur les clés métier.
- Traçabilité : `created_at`, `updated_at`, `created_by` et journaux métier.

## 3. Stratégie d’identification

- **Identifiants auto-incrémentés** comme clés primaires internes, pour la performance et les jointures.
- **UUID** comme identifiants publics, pour l’exposition par l’API, la protection contre l’énumération et la synchronisation.
- Modèle hybride : rapidité en interne, sécurité à l’extérieur.

## 4. Nommage et conventions

- Tables en `snake_case` au singulier (`project`, `user_account`).
- Colonnes explicites, clés étrangères nommées `<entite>_id`, horodatages normalisés.
- Référentiels dans des tables dédiées plutôt que des énumérations codées en dur ; dictionnaire de données versionné.

## 5. Normalisation et dénormalisation maîtrisée

- De la 1NF à la 3NF ou la BCNF, pour éviter les doublons et les anomalies.
- Dénormaliser **seulement** pour un gain mesuré (performance, reporting), avec documentation et tests.

## 6. Interopérabilité et sémantique

- Alignement sur le vocabulaire **Schema.org** quand c’est pertinent, pour un modèle sémantique partageable.
- Vues et DTO sémantisés pour faciliter l’intégration avec des systèmes externes.

## 7. Performance, volumétrie et exploitation

- Prévision de la volumétrie par table : rythme des écritures et des lectures, durée de conservation.
- Plan d’indexation (B-tree par défaut, index composites et partiels) et suivi des plans d’exécution (`EXPLAIN`).
- Partitionnement (par date ou par clé) au-delà de gros volumes.
- Imports et traitements par lots : insertions ou mises à jour combinées (upsert), pagination, fenêtres de maintenance.

## 8. Sécurité, confidentialité et continuité

- Rôles et permissions : moindre privilège, séparation entre lecture et écriture.
- Données sensibles : masquage, chiffrement en transit et au repos, pseudonymisation.
- Sauvegardes et restaurations testées, avec des objectifs de perte de données maximale et de durée d’interruption (RPO / RTO), et des procédures documentées.
- Conformité : traçabilité des accès, purges et durées de conservation légales.

## 9. Gouvernance, versionnement et métadonnées système

- **Migrations versionnées**, atomiques et réversibles : un changement, une migration.
- **Journal des modifications** lisible : quoi, pourquoi, quel impact.
- **Métadonnées système** (rôles, statuts, types) centralisées dans des tables de référence ou des fichiers de configuration versionnés, partagées entre front-end et back-end.
- **Catalogue de données** : responsable, qualité, provenance et niveau de service attendu (SLA).

## 10. Validation et qualité des données

- Tests d’intégrité : pas de clés étrangères orphelines, respect des `CHECK` et des unicités.
- Tests fonctionnels : scénarios métier réalistes de création, lecture, mise à jour et suppression (CRUD).
- Tests de performance sur des jeux de données volumineux, en suivant les temps de réponse des requêtes les plus lentes (95e et 99e centiles, p95 / p99).
- Qualité : doublons, valeurs aberrantes, taux de valeurs vides, règles de nettoyage.

## 11. Industrialisation et exploitation

- Scripts d’initialisation et de données de référence (pays, statuts, rôles) reproductibles.
- Outils en ligne de commande pour gérer et automatiser les opérations sur la base.
- Observabilité : métriques (connexions, verrous, entrées-sorties) et alertes (latence, croissance).
- Procédures d’exploitation : montée de version, retour arrière, correction de données en urgence, purge et archivage.
- Tableaux de bord : requêtes lentes, taille des tables, fragmentation et gonflement des index.
