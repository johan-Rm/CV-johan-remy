# Vision du code moderne

Notes anciennes de Johan, conservées comme document de contexte pour aligner le CV et le DCI. Elles datent d’avant le workflow AIOD : la relecture humaine de chaque ligne y est encore implicite.

## ✅ Lisible

> *« Le code est plus souvent lu qu’écrit. »* – donc on structure, on nomme bien, on commente peu mais bien, et on évite le code astucieux qui épate mais sème le désordre.

## ✅ Testable

> On peut casser, refactoriser ou faire évoluer sans sueurs froides. C’est modulaire, découplé, et soutenu par des **tests unitaires** et/ou d’intégration.

## ✅ Composable et réutilisable

> Le code moderne aime la **composition** : on crée des briques simples et spécialisées (services, hooks, composables…) que l’on assemble. Moins de classes monolithiques, plus de petites fonctions pures.

## ✅ Typé

> Dans la mesure du possible : TypeScript, Python (type hints), PHP 8+ avec ses types stricts… Le typage, c’est de la documentation et de la sécurité à l’exécution.

## ✅ Fondé sur des conventions

> On suit les standards de la communauté ou de l’équipe. En Symfony ou en Nuxt, on colle à la manière de faire du framework. Le code moderne, c’est aussi **éviter la guerre des styles**.

## ✅ Orienté expérience développeur (DX)

> On pense à celui qui passera après soi (ou à soi-même dans six mois) : on écrit des **scripts en ligne de commande**, des **docs Markdown**, on met des **checklists dans les PR**, on crée des **composants d’interface réutilisables** et on soigne les **messages d’erreur**.

## ✅ Intégré à la chaîne DevOps, CI et qualité

> Formatage automatique (Prettier, Black, PHP-CS-Fixer), linting, tests dans la CI, couverture, sécurité, performances… Le code moderne, c’est aussi du **code qui s’intègre bien dans une chaîne de production logicielle**.

## ✅ Orienté règles métier

> Le code n’est pas là pour faire joli : il sert un produit, un besoin, une échéance. Le code moderne **sait faire des compromis intelligents** ; il est **pragmatique**, pas dogmatique.
