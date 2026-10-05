# Instructions pour les Agents IA

Ce document contient les règles et conventions à suivre pour toute modification de ce projet guestBTP.

## Architecture du projet

```
.
├── backend/              # API FastAPI (Python 3.11+)
│   ├── app/
│   │   ├── models/      # Modèles SQLAlchemy
│   │   ├── schemas/     # Schémas Pydantic
│   │   ├── routers/     # Endpoints API
│   │   └── services/    # Logique métier
│   └── tests/           # Tests pytest
├── frontend/            # Application React + TypeScript
│   ├── src/
│   │   ├── api/         # Client API centralisé
│   │   ├── components/  # Composants React
│   │   ├── pages/       # Pages de l'application
│   │   └── types/       # Types TypeScript
│   └── tests/           # Tests Vitest
├── openapi.yaml         # Spécification OpenAPI (source de vérité)
└── .github/workflows/   # CI/CD GitHub Actions
```

## Règles obligatoires

### Règle 1 — API First

**Toute modification de l'API doit d'abord mettre à jour `openapi.yaml`.**

- `openapi.yaml` est la source de vérité pour l'API
- Endpoints REST : `/api/v1/{resource}`
- Verbes HTTP : GET (lire), POST (créer), PATCH (modifier), DELETE (supprimer)

### Règle 2 — Tests obligatoires

**Tout nouveau code backend doit être accompagné d'un test pytest.**

- Couverture minimale : 80%
- Exécuter : `cd backend && pytest --cov=app`

**Tout nouveau code frontend doit être accompagné d'un test Vitest.**

- Exécuter : `cd frontend && npm test`

### Règle 3 — Client API centralisé

**Utilise toujours `frontend/src/api/client.ts` pour les appels frontend.**

- Ne jamais utiliser `fetch()` ou `axios` directement dans les composants
- Utiliser les hooks TanStack Query : `useClients()`, `useInvoices()`, etc.
- Fonctions utilitaires de calcul : `calculateTotal()`, `calculateLineTotal()`

### Règle 4 — Règles métier strictes

#### Calculs de factures

- **Ligne HT** : `quantity × unit_price × (1 - discount/100)`
- **TVA ligne** : `line_ht × vat_rate / 100`
- **Total HT** : somme des lignes HT
- **Total TVA** : somme des TVA par ligne
- **Total TTC** : Total HT + Total TVA
- **Arrondi** : 2 décimales avec `Decimal` (Python)

#### Taux de TVA autorisés

Uniquement : `5.5`, `10`, `20` (pourcent)

#### Numérotation des factures

Format : `FA-YYYY-NNNN` (ex: `FA-2026-0001`) — compteur réinitialisé chaque année.


### Règle 5 — Qualité du code

#### Backend (Python)

- **Linting** : `ruff` (config dans `pyproject.toml`)
- **Formatage** : ligne max 100 caractères
- **Types** : utiliser les type hints partout
- **Docstrings** : obligatoires pour les fonctions publiques

#### Frontend (TypeScript)

- **Strict mode** : TypeScript strict activé
- **Composants** : fonctionnels uniquement (pas de classes)
- **Props** : typer explicitement avec `interface` ou `type`

### Règle 6 — Sécurité

**Avant chaque commit, exécuter les audits de sécurité :**

```bash
cd backend && bandit -r app/
cd backend && pip-audit -r requirements.txt
```

- Ne jamais committer de secrets ou credentials
- Utiliser les variables d'environnement (`.env`)
- Valider toutes les entrées utilisateur avec Pydantic

### Règle 7 — Validation mathématique

**Avant de créer une facture, valider les calculs avec l'outil dédié :**

```bash
python agent-capabilities/validate_invoice_math.py < invoice.json
```

Cet outil vérifie que les calculs HT/VAT/TTC sont exacts et protège contre les erreurs de calcul.

## Conventions de nommage

### Backend

- **Fichiers** : `snake_case` (ex: `invoice_calculator.py`)
- **Classes** : `PascalCase` (ex: `InvoiceCreate`)
- **Fonctions** : `snake_case` (ex: `calculate_total`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `VALID_TRANSITIONS`)

### Frontend

- **Fichiers** : `PascalCase` pour composants, `camelCase` pour utilitaires
- **Composants** : `PascalCase` (ex: `InvoiceList`)
- **Fonctions** : `camelCase` (ex: `calculateTotal`)
- **Types** : `PascalCase` (ex: `Invoice`, `ClientCreate`)

### API

- **Endpoints** : `/api/v1/{resource}`
- **Champs JSON** : `snake_case` (ex: `client_id`, `issue_date`)

## Workflow de développement

1. **Créer une branche** : `git checkout -b feature/ma-feature`
2. **Modifier `openapi.yaml`** si l'API change
3. **Implémenter le backend** avec tests
4. **Implémenter le frontend** avec tests
5. **Exécuter les audits** : `ruff`, `pytest`, `bandit`, `pip-audit`
6. **Valider les calculs** avec `validate_invoice_math.py`
7. **Committer** : message clair et descriptif
8. **Créer une PR** vers `develop`

## CI/CD

GitHub Actions exécute automatiquement :
- Linting avec `ruff`
- Tests avec `pytest` (couverture)
- Tests avec `vitest`
- Audit de sécurité avec `bandit` et `pip-audit`

Voir `.github/workflows/ci.yml` pour les détails.

## Erreurs courantes à éviter

1. ❌ Modifier un endpoint sans mettre à jour `openapi.yaml`
2. ❌ Oublier les tests pour du nouveau code
3. ❌ Utiliser `fetch()` directement dans les composants frontend
4. ❌ Calculer les totaux manuellement (utiliser les fonctions dédiées)
5. ❌ Utiliser des taux de TVA autres que 5.5, 10, 20
6. ❌ Transition de statut invalide (respecter la machine à états)
7. ❌ Committer des secrets ou credentials
8. ❌ Ignorer les avertissements de `bandit` ou `pip-audit`

---

**Note** : Ce document est lu par les agents IA (Cline, etc.) pour comprendre les conventions du projet. Toute modification doit respecter ces règles.

#### Machine à états des statuts

```
brouillon → envoyee → payee
                  ↘ en_retard → payee
         ↘ annulee
```

Transitions valides :
- `brouillon` → `envoyee`, `annulee`
- `envoyee` → `payee`, `en_retard`
- `en_retard` → `payee`
- `payee` → (lecture seule)
- `annulee` → (lecture seule)
