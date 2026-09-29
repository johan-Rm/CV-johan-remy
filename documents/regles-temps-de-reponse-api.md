# Règles de temps de réponse des appels API

Notes de Johan, conservées comme document de contexte pour aligner le CV et le DCI. Elles distinguent les appels qui doivent répondre immédiatement de ceux qui peuvent prendre du temps, et disent quoi faire dans chaque cas.

## ⚡️ 1. Réponses critiques — cible < 200 ms

**Appels concernés**

- Les affichages principaux de l’interface : tableaux de bord, listes paginées, détail d’un élément.
- Les filtres, tris et interactions fréquentes.

**Objectif**

- Temps de réponse **idéalement < 200 ms**.
- Temps maximal toléré **< 500 ms**.

**Actions recommandées**

- Requêtes SQL optimisées : index, pas de requêtes en cascade (N+1).
- Chargement paginé ou différé (lazy loading).
- Réponses allégées : projection stricte par DTO, pas de JSON superflu.
- Préchargement des métadonnées fréquentes (cache ou structure parallèle).

## 🕓 2. Réponses longues — au-delà d’une seconde

**Appels concernés**

- Les exports CSV, JSON ou YAML.
- Les agrégations, statistiques et analyses de gros volumes.
- Les préchargements de données massives.

**Objectif**

- Temps toléré : **jusqu’à 10 à 15 secondes**.
- **30 secondes au maximum** pour un appel synchrone depuis l’interface ; au-delà, passer en traitement asynchrone (file de tâches, WebSocket ou polling).

**Actions recommandées**

- Déporter le traitement vers un système de tâches différées (file de tâches, worker).
- Maîtriser la mémoire (traitement SQL par lots, plafond de RAM).
- Limiter les données en entrée et en sortie (filtres par défaut, formats légers).

## 📊 3. Recommandations transverses

- **Analyser le plan d’exécution** (`EXPLAIN ANALYZE`) de chaque requête SQL critique.
- **Surveiller la mémoire utilisée et la taille des réponses.**
- **Limiter les appels récursifs ou imbriqués dans des boucles** (risque de N+1 ou d’explosion mémoire).
- **Privilégier la robustesse du modèle relationnel** : des jointures sur clé plutôt que des constantes en dur dans le code.

## Remarque de mise au propre

Les notes d’origine annonçaient « > 1 s à 10 s » dans le titre de la section 2, puis « jusqu’à 10-15 secondes » et « 30 secondes max » dans le texte. Le titre est ramené à « au-delà d’une seconde » ; les seuils du texte sont conservés.
