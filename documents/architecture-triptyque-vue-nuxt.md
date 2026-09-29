# Architecture en triptyque : composables, stores, services

Notes de Johan, conservées comme document de contexte pour aligner le CV et le DCI. Elles décrivent l’organisation de la gestion des données côté front-end dans une application Vue.js / Nuxt 4.

La gestion des données repose sur trois couches, pensées pour garder un code prévisible, testable et adapté à Nuxt 4. Chaque couche a un rôle clair, qui ne recouvre pas celui des autres.

## 1. Composables — l’interface entre l’UI et les stores

Les composables (`useXxx()`) font le lien entre l’interface et la logique applicative. Ils exposent aux composants une API réactive locale et orchestrent les échanges avec les stores.

## 2. Stores — l’état global et l’orchestration

Les stores Pinia (`useXxxStore()`) centralisent l’état global. Ils orchestrent :

- la mise en cache ;
- l’appel aux services métier ;
- la mise à jour cohérente de l’interface.

L’interface réagit automatiquement à leurs changements.

## 3. Services — la logique métier et les appels API

Les services contiennent la logique métier : transformation des données, appels REST et WebSocket, gestion des erreurs, lecture des réponses. Ils sont **indépendants de Nuxt, de Pinia et de Vue**, ce qui permet :

- une testabilité maximale ;
- une réutilisation dans d’autres contextes ;
- la garantie qu’aucune logique métier ne remonte dans les composants.

## Flux des données

1. L’utilisateur agit sur l’interface (pages, composants).
2. Les composants appellent les composables (`useXxx()`).
3. Les composables s’appuient sur les stores et/ou les services.
4. Les services échangent avec l’API du back-end.
5. Le store est mis à jour, et l’interface se met à jour automatiquement.

## Règles

- **Un composable n’appelle jamais l’API directement** : il passe par un service.
- **Un store peut appeler un service** ; un composable peut aussi le faire directement quand l’état n’a pas vocation à être global.
- **Un service ne dépend d’aucun framework** : ni Nuxt, ni Pinia, ni Vue. Uniquement du code métier testable.

## Remarque de mise au propre

Les notes d’origine qualifiaient la logique des services de « pure ». Les services font aussi des appels réseau, qui ne sont pas des fonctions pures au sens strict. Le mot est retiré ; l’indépendance vis-à-vis des frameworks, qui est le vrai point, est conservée.
