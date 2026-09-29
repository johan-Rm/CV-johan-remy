# Architecture hexagonale et bonnes pratiques Symfony 7

Notes de Johan, conservées comme document de contexte pour aligner le CV et le DCI.

## 🏗️ Architecture recommandée

### 📂 Structure standard (hexagonale/modulaire adaptée)

```
src/
├── Domain/            # Entités métier, interfaces, logique pure
├── Application/       # Cas d’usage (services applicatifs)
├── Infrastructure/    # Adaptateurs techniques (ORM, API, Mailer…)
├── UI/Http/           # Contrôleurs et DTO pour l’interface HTTP
├── UI/Cli/            # Commandes Symfony
```

### 🧩 Avantages

* Séparation claire des responsabilités (Clean Architecture)
* Testabilité facilitée (les cas d’usage n'ont pas de dépendances techniques)
* Adapté aux projets **multi-clients / multi-interfaces**

---

## ⚙️ Bonnes pratiques Symfony 7

### 1. **Utilisation des attributs**

✅ Préférer les attributs PHP (`#[Route]`, `#[AsCommand]`) aux annotations Doctrine ou Symfony obsolètes.

### 2. **Dependency Injection explicite**

✅ Privilégier l’**autowiring par constructeur**, éviter le container service locator.
❌ Ne pas injecter le conteneur dans les services (`ContainerInterface`).

### 3. **DTO & Validation**

✅ Utiliser des **DTO distincts** des entités Doctrine.
✅ Utiliser `#[Assert]` sur les propriétés des DTO pour validation.

### 4. **Tests & architecture**

✅ Tester les cas d’usage sans dépendance à Symfony (tests unitaires purs).
✅ Utiliser des **tests fonctionnels** uniquement sur les contrôleurs ou intégrations complexes.

### 5. **Eviter les pièges Doctrine**

✅ Charger les relations explicitement (`JOIN FETCH`, `EntityGraph`)
✅ Eviter les "N+1" query.
✅ Pas de logique métier dans les entités (pas de `sendInvoice()` ou `register()` dans une `User` entity).

### 6. **Commandes Symfony**

✅ Créer des commandes pour les ETL, les imports/exports de données.
✅ Les découpler de l'infrastructure pour pouvoir réutiliser les cas d’usage ailleurs.
