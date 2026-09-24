# Revue des projets pour enrichir le DCI Infotel

Revue du 23 septembre 2026. Lecture statique du code, des configurations, des tests présents et de la documentation. Aucun service lancé, aucune requête vers les bases ou les services externes, aucun projet source modifié. Les tests n’ont pas été exécutés. La revue initiale n’a pas modifié le DCI ; les confirmations et leur intégration ultérieure sont consignées ci-dessous.

Les constats portent sur les copies locales actuelles : ils ne prouvent ni la date de livraison d’une fonctionnalité, ni son activation en production, ni son attribution individuelle dans un projet d’équipe. Les formulations ci-dessous sont des propositions à rattacher à la bonne période.

## Confirmations de Johan et intégration au DCI

Les confirmations ci-dessous, recueillies après la revue, précisent ou remplacent les réserves de la lecture statique présentées plus bas.

- **Kazen Garden** : création en 2022 puis maintenance et évolutions jusqu’à aujourd’hui, dont Nuxt 4. Réservation et paiement Systempay intégral/acompte livrés.
- **MLK** : Blueprint immobilier est bien la version livrée ; API Symfony 8 / API Platform et PostgreSQL confirmés.
- **Immobilière Essaouira** : client direct de 2019 à fin 2025 ; JavaScript, Vuex et Bootstrap confirmés en remplacement de TypeScript/Tailwind.
- **Villa Gonatouki** : JavaScript, Vuex et Vuetify confirmés en remplacement de TypeScript/Tailwind ; demande de ne pas approfondir la période, 2020 conservé.
- **Capnour** : synchronisation asynchrone Jarvi livrée.
- **Notifications push navigateur** : confirmées pour Capnour, MLK, Kazen Garden, OptiValue et la plateforme GRC low-code.
- **OptiValue** : les évolutions back-end, optimisations SQL, migrations, index et commandes CLI sont des propositions de Johan ; la mise en œuvre a été confiée à l’équipe Python. Elles ne doivent pas être présentées comme des développements personnellement réalisés par Johan.
- **Clients directs** : Capnour, MLK, Kazen Garden, Immobilière Essaouira et Villa Gonatouki sont présentés comme des projets clients.
- **Graines Digitales** : aucune expérience distincte ajoutée ; sujet reporté à une discussion ultérieure.

Ces éléments ont été intégrés dans `INFOTEL Monaco - REMY Johan DCI.docx`. Les formulations validées du bloc transversal « Interfaces Nuxt » sont conservées.

## Synthèse

| Projet | Éléments particulièrement utiles au DCI | Point à préciser |
|---|---|---|
| Capnour | Nuxt Layers, relais serveur vers l’API, consentement et visibilité des profils, synchronisation asynchrone, contrats typés et tests | Fonctions réellement livrées à la date retenue |
| MLK / Blueprint immobilier | Gestion de contenu headless, back-office, contrats YAML/TypeScript, chargement progressif des images, SEO structuré | Correspondance entre Blueprint et la version livrée à MLK |
| Kazen Garden | Réservation de séjours, calcul de prix, paiement intégral/acompte, préchargement des images, instrumentation des performances | Évolution après 2022 : le code actuel déclare Nuxt 4 |
| Immobilière Essaouira | Catalogue immobilier, état Vuex, contenus multilingues, sitemap dynamique et caches | Stack historique à rectifier : Bootstrap et JavaScript repérés, pas de preuve de Tailwind/TypeScript dans le front consulté |
| OptiValue | Chargement priorisé, orchestration WebSocket, état partagé, migrations PostgreSQL et index | Ne pas attribuer à cette copie la partie GRC Vue/Golang absente du périmètre |
| Graines Digitales | Socle CMS multi-organisations/multi-projets, droits d’accès, traduction automatique, schémas communs et outils CLI | Période et statut à indiquer si une expérience distincte est ajoutée |
| Villa Gonatouki | Parcours de demande de réservation, gestion des chambres, back-office Symfony/EasyAdmin, traduction automatique | Stack historique : Nuxt 2, JavaScript, Vuex et Vuetify repérés |

## 1. Capnour

Périmètre : `/home/johan/www/cap-nour/webapp` et `api`.

### Confirmé par les sources consultées

- Une base Nuxt commune et quatre espaces sélectionnés à la compilation : public, candidat, entreprise et administration. Cela précise la réutilisation du code et l’isolation des applications derrière la mention « Nuxt Layers ».
- Un relais serveur Nuxt vers l’API Symfony : gestion des JWT, renouvellement des jetons et expiration des sessions. Le navigateur reçoit une session avec cookie HttpOnly ; les jetons de l’API sont traités côté serveur.
- Une politique métier explicite d’exposition des candidats : profil actif, non supprimé, visible et ayant donné son consentement.
- Traitement de la présence au Maroc côté métier, plutôt qu’un simple libellé d’interface.
- Synchronisation de candidatures avec Jarvi par Symfony Messenger et rafraîchissement différé après l’envoi.
- Génération des types de l’API depuis OpenAPI et contrôle des contrats ; tests Vitest côté front et tests fonctionnels PHPUnit côté API, notamment sur la visibilité et les périmètres de recherche.

### Formulations proposées

- Concevoir une architecture Nuxt Layers avec un socle commun et des applications distinctes pour les visiteurs, candidats, entreprises et administrateurs.
- Mettre en œuvre l’authentification et le renouvellement des sessions via un relais serveur vers l’API Symfony.
- Encadrer l’exposition des profils par les règles de visibilité et le consentement des candidats.
- Intégrer la synchronisation asynchrone des candidatures avec un service de recrutement externe.
- Fiabiliser les échanges front-end/back-end par des contrats typés générés depuis OpenAPI et des tests ciblés sur les règles métier.

### Preuves

- [Architecture des espaces](/home/johan/www/cap-nour/webapp/nuxt.config.ts:5).
- [Authentification](/home/johan/www/cap-nour/webapp/base/server/api/auth/login.post.ts:6) et [gestion du relais API](/home/johan/www/cap-nour/webapp/base/server/utils/api.ts:166).
- [Politique de visibilité et consentement](/home/johan/www/cap-nour/api/src/Domain/Candidate/CandidateExposurePolicy.php:10).
- [Présence au Maroc](/home/johan/www/cap-nour/api/src/Domain/Candidate/MoroccoPresence.php).
- [Synchronisation Jarvi](/home/johan/www/cap-nour/api/src/MessageHandler/SubmitCandidateToJarviHandler.php).
- [Scripts de génération et contrôles](/home/johan/www/cap-nour/webapp/package.json), [tests de visibilité](/home/johan/www/cap-nour/api/tests/Functional/VisibilityTest.php).

## 2. MLK / Blueprint immobilier

Périmètre principal demandé : `/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier`. Des répertoires MLK distincts existent aussi ; ne pas supposer que toutes les fonctionnalités du Blueprint ont été livrées au client MLK.

### Confirmé par les sources consultées

- Front Nuxt 4 avec interface d’administration et routes serveur pour les biens, médias, catégories et traductions.
- Contrôle de l’appartenance à un projet pour accéder au dashboard.
- Génération d’artefacts TypeScript depuis des schémas YAML : contrats communs entre données et interface.
- Préchargement des images par lots, adaptation aux formats d’affichage et rendu différé des visuels non critiques selon l’écran actif.
- Navigation structurée par écrans ; préchargement des liens à leur visibilité.
- Données structurées Schema.org / JSON-LD et génération d’URL pour le sitemap.
- Composants avec attributs ARIA et prise en compte de la réduction des animations dans la galerie.
- Tests de mapping et tests du back-office ; scénario Playwright de vérification du chargement de l’accueil.

### Formulations proposées

- Développer une application immobilière headless avec back-office de gestion des biens, médias et contenus multilingues.
- Structurer les échanges de données à partir de schémas partagés et générer les types TypeScript correspondants.
- Concevoir une navigation par écrans avec préchargement ciblé des images et rendu différé des contenus non prioritaires.
- Mettre en place le sitemap dynamique et les données structurées Schema.org pour le référencement des contenus.
- Intégrer des dispositions d’accessibilité dans les composants et tester les transformations de données ainsi que le chargement de l’interface.

### Preuves

- [Routes du dashboard](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/server/api/dashboard).
- [Vérification d’appartenance au projet](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/server/utils/auth/symfonyProjectMember.ts:20).
- [Génération de types](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/services/converter/schema/generateArtifacts.ts).
- [Préchargement des images](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/app/composables/useImageWarmup.ts:37) et [rendu différé](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/app/composables/useDeferredScreenVisuals.ts:27).
- [Données structurées](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/services/seo/schema.ts:163), [sitemap](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/server/api/__sitemap__/urls.get.ts:24).
- [Réduction des animations](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/app/components/gallery/Images.vue:193), [test Playwright](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/tests/e2e/home.smoke.spec.ts:3).

Attention : la [carte d’accessibilité](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/dev-book/tasks/017-accessibilite-site-public.md) reste marquée « À faire ». La [carte d’audit Lighthouse nocturne](/home/johan/www/graines-digitales/modern-web-apps/blueprint-immobilier/dev-book/tasks/040-audit-lighthouse-production-nocturne.md) est aussi à faire. Des scripts d’audit existent, mais cette revue ne démontre ni une conformité WCAG/RGAA achevée ni des Core Web Vitals au vert en production.

## 3. Kazen Garden

Périmètre : `/home/johan/www/kazen-garden`, front et back-office Symfony/Sylius.

### Confirmé par les sources consultées

- Parcours de réservation de séjours avec quantités, calcul du montant et choix entre acompte et paiement intégral.
- Confirmation de paiement contrôlant les données reçues ; code d’intégration Systempay. Une dépendance PayPal seule ne prouve pas son utilisation réelle.
- Traduction automatique de contenus côté back-end.
- Préchargement d’images par lots avec taille adaptée au viewport, mémorisation des images préchargées et interruption des lots devenus inutiles après navigation.
- Instrumentation LCP, INP et CLS avec `web-vitals`, activable en développement. Ce n’est pas un relevé de performance de production.
- Notifications dans l’interface, sans preuve suffisante ici d’un service de push navigateur.

### Formulations proposées

- Développer un parcours de réservation de séjours avec calcul des prix et paiement intégral ou par acompte.
- Intégrer le traitement et la confirmation des paiements Systempay.
- Optimiser l’affichage des images par un préchargement adaptatif aux dimensions de l’écran et aux changements de page.
- Instrumenter les indicateurs de performance du navigateur pour accompagner les optimisations.

### Preuves

- [Calcul du prix et acompte](/home/johan/www/kazen-garden/digital-management-system/src/Payment/BookingPrice.php:20), [confirmation du paiement](/home/johan/www/kazen-garden/digital-management-system/src/Payment/BookingConfirmation.php:22), [intégration Systempay](/home/johan/www/kazen-garden/digital-management-system/src/Payment/Payment.php:148).
- [Préchargement des images](/home/johan/www/kazen-garden/nuxt-modern-website/app/composables/useImageWarmup.ts:38).
- [Instrumentation des performances](/home/johan/www/kazen-garden/nuxt-modern-website/app/plugins/web-vitals.client.ts:1).
- [Notifications d’interface](/home/johan/www/kazen-garden/nuxt-modern-website/app/composables/useNotification.ts).
- [Stack actuelle](/home/johan/www/kazen-garden/nuxt-modern-website/package.json).

Le front actuel déclare Nuxt 4.5.1. Le DCI associe Nuxt 3 à 2022 : conserver la distinction entre création et évolutions ultérieures, et dater les nouvelles réalisations avant de les affecter à 2022.

## 4. Immobilière Essaouira

### Confirmé par les sources consultées

- Catalogue immobilier avec informations détaillées, prix, surfaces, localisation, galeries, documents PDF, vidéos et biens associés.
- État applicatif structuré en modules Vuex, dont recherche, biens, localisations et catégories.
- Traduction automatique via Google Cloud Translate côté Symfony.
- Sitemap construit pour plusieurs familles de contenus ; configuration de caches de composants et de pages SSR.
- Front Nuxt 2 / JavaScript avec Bootstrap. Les manifestes et fichiers lus ne corroborent pas le TypeScript et Tailwind actuellement mentionnés dans le DCI pour cette mission.

### Formulations proposées

- Développer un catalogue immobilier multilingue avec fiches détaillées, médias et critères de recherche.
- Centraliser l’état des recherches et des contenus dans des modules Vuex.
- Automatiser la traduction des contenus et la génération des sitemaps ; configurer des caches pour les pages et composants.

### Preuves

- [Modèle front des biens](/home/johan/www/immobiliere-essaouira/nuxt-modern-website/store/accommodations.js:4), [recherche](/home/johan/www/immobiliere-essaouira/nuxt-modern-website/store/search.js).
- [Traduction automatique](/home/johan/www/immobiliere-essaouira/digital-management-system/src/Service/Translation/Translator.php:322).
- [Bootstrap](/home/johan/www/immobiliere-essaouira/nuxt-modern-website/nuxt.config.js:119), [caches](/home/johan/www/immobiliere-essaouira/nuxt-modern-website/nuxt.config.js:167), [sitemap](/home/johan/www/immobiliere-essaouira/nuxt-modern-website/nuxt.config.js:482).

## 5. OptiValue

Périmètre : `/home/johan/www/lab/answer-project`. Cette copie concerne OptiValue, pas la plateforme GRC Vue/Golang.

### Confirmé par les sources consultées

- Initialisation progressive : chargement des autorisations, chargements parallèles des données prioritaires, puis chargement différé des données complémentaires.
- Smart Prefetch explicite dans le store des projets.
- Connexion WebSocket authentifiée et distribution centralisée des événements vers les stores des documents et projets : mécanisme cohérent avec la description du pattern Mediator.
- API Python avec Azure Functions et PostgreSQL ; migrations de contraintes et d’index, dont index composites, partiels et GIN.
- Outillage des migrations via Make et documentation d’utilisation.

### Formulations proposées

- Orchestrer le chargement progressif du dashboard en séparant les données d’autorisation, les données prioritaires et les chargements différés.
- Centraliser la distribution des événements WebSocket pour synchroniser les documents, projets et indicateurs de l’interface.
- Structurer les migrations PostgreSQL et les index adaptés aux accès applicatifs.

### Preuves

- [Initialisation progressive](/home/johan/www/lab/answer-project/front/app/composables/useNuxtServerInit.ts:39), [Smart Prefetch](/home/johan/www/lab/answer-project/front/app/stores/project.ts:831).
- [Connexion WebSocket](/home/johan/www/lab/answer-project/front/app/stores/socket.ts:19), [distribution des événements](/home/johan/www/lab/answer-project/front/app/stores/app.ts:57).
- [Dépendances back-end](/home/johan/www/lab/answer-project/back/requirements.txt).
- [Index PostgreSQL](/home/johan/www/lab/answer-project/migrations/back/20250507010025_add_indexes_if_not_exists.up.sql), [migrations et commandes](/home/johan/www/lab/answer-project/migrations/README.md).

Les compléments fournis par Johan sur EXPLAIN/ANALYZE, la prévention des N+1, les réponses HTTP unifiées et les constantes partagées restent des éléments déclarés. Cette passe ne constitue pas une preuve indépendante de chacun de ces points. Les dépendances Azure ne permettent pas non plus d’attribuer automatiquement tous les services Azure à son périmètre personnel.

## 6. Graines Digitales

Périmètre : socle de coordination, API Symfony 8 et outils transverses. C’est un apport distinct de l’intégration d’un site client.

### Confirmé par les sources consultées

- Modélisation des organisations, projets, membres et rôles ; contrôle des droits de lecture/écriture au niveau des projets.
- Gestion de contenu multilingue : ressources, traductions, locale source et langues activées par projet.
- Traduction automatique des champs marqués par attribut PHP, en remplissant les champs manquants sans écraser les traductions déjà présentes.
- Contrats partagés YAML et génération d’artefacts TypeScript dans le front associé.
- CLI Python pour les bases, schémas et génération de structures documentaires réutilisables ; présence de tests dédiés.
- Configuration Docker et scripts Make pour les environnements et les contrôles qualité.

### Formulations proposées

- Concevoir un socle de gestion de contenu headless multi-organisations et multi-projets sous Symfony et API Platform.
- Mettre en place des droits d’accès par projet et des contrats de données partagés avec les frontends.
- Automatiser la traduction des contenus en préservant les traductions déjà renseignées.
- Développer des outils CLI Python pour la gestion des schémas, des bases et de la documentation réutilisable.

### Preuves

- [Périmètre du socle](/home/johan/www/graines-digitales/README.md).
- [Contrôle d’accès projet](/home/johan/www/graines-digitales/api/symfony-8-api-platform/src/Security/ProjectAccessGuard.php:15).
- [Traduction automatique sélective](/home/johan/www/graines-digitales/api/symfony-8-api-platform/src/Translation/ResourceAutoTranslator.php:15).
- [CLI bases et validation de schémas](/home/johan/www/graines-digitales/scripts/cli/db/commands.py), [génération de structures](/home/johan/www/graines-digitales/scripts/cli/blueprints/scaffold.py).
- [Tests des générateurs](/home/johan/www/graines-digitales/scripts/tests/test_blueprints_scaffold.py).
- [Configuration PostgreSQL actuelle](/home/johan/www/graines-digitales/api/symfony-8-api-platform/docker-compose.prod.yml:119).

Le socle actuel utilise PostgreSQL. Cela ne suffit pas à remplacer MySQL dans l’expérience MLK : il faut identifier la version de l’API réellement utilisée lors de la mission. Pour ajouter une expérience Graines Digitales au DCI, préciser les dates et son statut : activité propre, R&D ou socle mutualisé pour clients.

## 7. Villa Gonatouki

### Confirmé par les sources consultées

- Parcours de demande de réservation avec chambres, dates de séjour, nombre d’adultes/enfants, coordonnées et message au gestionnaire.
- État du parcours dans Vuex ; interface thématique avec composants plein écran et galeries.
- Back-office Symfony / EasyAdmin avec modèle de chambres, services et activités de l’établissement.
- Traduction automatique via Google Cloud Translate et outillage Symfony associé.
- Front Nuxt 2, JavaScript, Vuetify, Swiper et modules de gestion des dates.

### Formulations proposées

- Développer un site hôtelier multilingue avec parcours de demande de réservation : choix de chambre, dates de séjour, occupants et coordonnées.
- Centraliser les données du parcours dans Vuex et concevoir des interfaces de présentation plein écran.
- Structurer l’administration des chambres, services et activités avec Symfony/EasyAdmin et automatiser la traduction des contenus.

### Preuves

- [État des réservations](/home/johan/www/villa-gonatouki/nuxt-modern-website/store/hotels.js:19).
- [Soumission de demande](/home/johan/www/villa-gonatouki/nuxt-modern-website/components/theme-full-screen/components/BookingFormCompletFullScreen.vue:167).
- [Modèle des chambres](/home/johan/www/villa-gonatouki/digital-management-system/src/Entity/HotelRoom.php).
- [Traduction du back-office](/home/johan/www/villa-gonatouki/digital-management-system/src/Translation/EasyAdminTranslator.php:307).
- [Dépendances front](/home/johan/www/villa-gonatouki/nuxt-modern-website/package.json), [configuration Vuetify](/home/johan/www/villa-gonatouki/nuxt-modern-website/nuxt.config.js:203), [dépendances back](/home/johan/www/villa-gonatouki/digital-management-system/composer.json).

Ne pas transformer ce parcours en moteur de réservation avec disponibilités garanties et paiement intégré sans preuve supplémentaire. Le code front consulté ne confirme pas les mentions TypeScript/Tailwind du DCI ; il montre JavaScript/Vuetify.

## Vérification du bloc transversal « Interfaces Nuxt »

| Affirmation | Appui trouvé | Limite à conserver |
|---|---|---|
| Temps réel | WebSocket et distribution des événements dans OptiValue | Ne pas généraliser aux cinq sites clients |
| Notifications push | Notifications d’interface et événements serveur repérés | Aucun flux complet de push navigateur confirmé dans les fichiers examinés |
| Traduction automatique | Implémentations Symfony dans Graines Digitales, Kazen Garden, Immobilière Essaouira et Villa Gonatouki | Distinguer traduction de contenu et simple internationalisation de l’interface |
| Préférences utilisateur / color mode | Modules et composants de thème dans les projets modernes | Vérifier le comportement livré avant d’affirmer une priorité uniforme sur tous les projets |
| Navigation et état réactif | Stores Pinia/Vuex, navigation par écrans, chargements progressifs | « Sans rupture visuelle » reste un résultat à observer en exécution |
| Stratégies de chargement | OptiValue, Blueprint et préchargement des images Kazen Garden | Choisir les mécanismes propres à chaque projet |
| Affichage instantané des images | Préchargement et caches présents | Effet recherché, pas une garantie sur toute connexion et première visite |
| Performance et SEO | JSON-LD, sitemap, caches, scripts Lighthouse, instrumentation web-vitals | Aucun score de production ni validation générale des Core Web Vitals établi ici |
| Accessibilité, données personnelles, sécurité | ARIA, réduction des animations, consentement, contrôle d’accès et sessions | La présence de mécanismes ne constitue pas une attestation de conformité globale |

## Questions avant intégration historique au DCI

1. Les années des missions correspondent-elles à leur création, ou à l’ensemble de leur maintenance et évolution ? En particulier Kazen Garden et les deux anciens sites Nuxt 2.
2. Blueprint immobilier est-il la version livrée pour MLK ou un produit/socle dérivé ? Quelle API et quel SGBD utilisait la version livrée ?
3. Quels projets ont réellement reçu des notifications push, au sens navigateur/service worker, et lesquels ont des notifications dans l’application ?
4. Quelles dates et quel intitulé utiliser pour Graines Digitales si le socle est présenté comme une expérience propre ?

Pour la mission Infotel, les apports les plus directement pertinents sont la modélisation de contenus, le multilingue, les droits d’accès, les échanges API, la documentation, les tests et l’évolution de plateformes Symfony. Aucun de ces constats ne démontre une expérience Ibexa/eZ Platform.
