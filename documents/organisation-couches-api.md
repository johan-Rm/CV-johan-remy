# Organisation en couches d’une API

Notes de Johan, conservées comme document de contexte pour aligner le CV et le DCI. Elles décrivent le rangement du code d’une API par responsabilité : ce qui entre, ce qui sort, ce qui est stocké, et les services qui passent de l’un à l’autre.

## Arborescence

```
dtos/          # représentation des données exposées par l’API
models/        # représentation des données stockées en base
payloads/      # structure et validation des données reçues
validators/    # non documenté dans ces notes
services/
├── event/     # opérations synchrones déclenchées par des événements
├── request/   # traitement des requêtes et format des réponses
└── transform/ # conversions entre models et DTO
```

## Flux d’une requête

1. La requête arrive : `services/request` lit les paramètres (filtres, tri, pagination).
2. Les données reçues sont contrôlées par leur `payload`.
3. `services/transform` convertit les données entre `models` et `dtos`.
4. La réponse repart dans un format commun, construit par `services/request`.
5. Les effets de bord (nettoyage, mises à jour en cascade) passent par `services/event`.

## `dtos/` — Data Transfer Objects

Interface entre l’API et les modèles internes.

1. **Représentation externe des données**
   - Définir la structure des données exposées par l’API.
   - Masquer les détails d’implémentation interne.
   - Assurer la cohérence des réponses de l’API.
2. **Validation des données**
   - Définir les contraintes et règles de validation.
   - Documenter le format attendu de chaque champ.
   - Gérer les conversions de types si nécessaire.
3. **Versionnement de l’API**
   - Faire évoluer les modèles sans casser la compatibilité.
   - Faciliter la migration d’une version d’API à l’autre.
   - Documenter les changements entre versions.

## `models/` — Modèles de données

Représentation des schémas de la base de données et logique métier associée à chaque entité.

1. **Représentation des schémas**
   - Définir la structure des tables et leurs relations.
   - Encapsuler les contraintes d’intégrité des données.
   - Fournir une interface orientée objet pour manipuler les données.
2. **Logique métier**
   - Implémenter les validations propres au domaine.
   - Gérer les règles métier complexes.
   - Assurer la cohérence des données.
3. **Persistance**
   - Gérer les opérations de création, lecture, mise à jour et suppression (CRUD).
   - Encapsuler les requêtes SQL complexes.
   - Optimiser les performances d’accès aux données.

## `payloads/` — Données reçues

Structure et validation des données des requêtes entrantes.

1. **Schéma des requêtes**
   - Spécifier la structure exacte des données attendues.
   - Documenter les champs obligatoires et optionnels.
   - Définir les types et formats acceptés.
2. **Validation des données entrantes**
   - Vérifier la présence des champs requis.
   - Valider les types et les formats.
   - Appliquer les règles de validation métier.
3. **Normalisation**
   - Normaliser les données (casse, format…).
   - Convertir les types si nécessaire.
   - Préparer les données pour les services.

## `services/event/` — Opérations synchrones sur événements

Maintien de la cohérence des données lorsque des événements surviennent dans le système.

1. **Traiter les événements système** : recevoir les données JSON et exécuter les actions synchrones.
2. **Maintenir la cohérence** : nettoyer les données orphelines et mettre à jour les entités liées.
3. **Garantir l’intégrité référentielle** : exécuter les opérations en cascade lors des modifications.

## `services/request/` — Requêtes et réponses

Traitement, validation et mise en forme commune des requêtes HTTP entrantes et des réponses.

1. **Paramètres de requête**
   - Extraire et valider les paramètres (query params).
   - Gérer le filtrage, le tri et la pagination.
   - Convertir les types et valider les formats.
2. **Réponses standardisées**
   - Formater les réponses JSON de façon cohérente.
   - Gérer les métadonnées (pagination, totaux…).
   - Encapsuler les données dans une structure commune.
3. **Erreurs**
   - Produire des réponses d’erreur standardisées.
   - Associer chaque exception au code HTTP approprié.
   - Enrichir les messages d’erreur pour le débogage.

## `services/transform/` — Conversions

Passage entre les modèles internes (représentation en base) et les DTO (représentation de l’API).

1. **Des modèles vers les DTO**
   - Transformer les modèles en DTO exposés par l’API.
   - Masquer les détails d’implémentation interne.
   - Adapter les formats aux clients de l’API.
2. **Des DTO vers les modèles**
   - Transformer les données entrantes en modèles.
   - Valider et normaliser les données.
   - Préparer les données pour la persistance.
3. **Données complexes**
   - Gérer les relations entre entités.
   - Agréger des données de plusieurs sources.
   - Appliquer les règles de transformation propres au domaine.

## Remarques de mise au propre

- Les sections « Requests » et « Payloads » des notes d’origine étaient identiques ; elles sont fusionnées sous `payloads/`, le nom donné dans l’arborescence.
- `validators/` figure dans l’arborescence d’origine sans description.
- La validation apparaît à trois endroits (`dtos`, `payloads`, `models`) ; les notes ne précisent pas quelle couche fait foi.
- Ici, les `models` portent la logique métier et la persistance. La note [architecture-hexagonale-symfony.md](architecture-hexagonale-symfony.md) prend le parti inverse (« pas de logique métier dans les entités ») : ce sont deux organisations différentes.
