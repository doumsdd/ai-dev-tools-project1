# 📋 guestBTP — Spécifications Produit

> **Version** : 1.0.0  
> **Dernière mise à jour** : 2026-01-15  
> **Statut** : En développement

---

## 1. 🎯 Identité du Produit

| Champ | Valeur |
|-------|--------|
| **Nom** | guestBTP |
| **Tagline** | "La facturation simplifiée pour le BTP" |
| **Type** | Application web SaaS (Single-tenant) |
| **Objectif** | Application portfolio démontrant une architecture moderne avec règles métier réelles |
| **Cible** | Artisans et PME du bâtiment |

### Vision

Permettre aux professionnels du BTP de gérer leur facturation de manière simple, conforme et professionnelle, tout en offrant un tableau de bord clair sur leur activité.

---

## 2. 👥 Personas

### Persona 1 — L'Artisan Indépendant
- **Profil** : Électricien, plombier, maçon en solo
- **Besoin** : Facturer rapidement après intervention, suivre ses impayés
- **Frustration** : Excel / papier, pertes de temps, relances oubliées

### Persona 2 — Le Chef d'Entreprise BTP
- **Profil** : Gère une équipe de 3-10 ouvriers
- **Besoin** : Vue d'ensemble sur la trésorerie, suivi par chantier
- **Frustration** : Pas de visibilité, factures éparpillées

### Persona 3 — Le Comptable
- **Profil** : Expert-comptable de plusieurs artisans
- **Besoin** : Export des données, TVA collectée, bilan
- **Frustration** : Saisie manuelle, erreurs de calcul

---

## 3. ✨ Fonctionnalités

### 3.1 Gestion des Clients (Phase 1)

| Action | Description |
|--------|-------------|
| **Créer** | Formulaire avec nom, email, téléphone, adresse, SIRET, type |
| **Modifier** | Édition de tous les champs sauf email (unique) |
| **Lister** | Tableau paginé avec recherche + filtres |
| **Archiver** | Masquer sans supprimer (soft delete) |
| **Détail** | Fiche client avec historique des factures |

**Champs Client** :
- `name` (obligatoire, min 2 caractères)
- `email` (format RFC 5322, unique)
- `phone` (format libre)
- `address` (texte libre)
- `siret` (14 chiffres, optionnel)
- `client_type` : `particulier` | `entreprise` | `maitre_ouvrage`

### 3.2 Gestion des Factures (Phase 1)

| Action | Description |
|--------|-------------|
| **Créer** | Formulaire multi-étapes (client → lignes → récap) |
| **Consulter** | Détail complet avec lignes, calculs, statut |
| **Lister** | Tableau avec filtres (statut, client, période) |
| **Modifier** | Uniquement en statut `brouillon` |
| **Changer statut** | Transitions contrôlées (voir §4) |

**Numéro de facture** :
- Format : `FA-AAAA-NNNN` (ex: `FA-2026-0001`)
- Auto-généré, séquentiel, non modifiable
- Réinitialisation du compteur chaque année

**Lignes de facture** :
- `description` (obligatoire, max 500 caractères)
- `category` : Maçonnerie | Plomberie | Électricité | Peinture | Terrassement | Couverture | Autre
- `quantity` (nombre décimal, > 0)
- `unit` : m² | m³ | heure | jour | forfait | unité
- `unit_price` (HT, > 0)
- `vat_rate` : 5.5% | 10% | 20%
- `discount` (pourcentage, 0-100, optionnel)
- `total_ht` (calculé automatiquement)

**Taux de TVA BTP** :
| Taux | Cas d'usage |
|------|-------------|
| 5.5% | Rénovation énergétique (isolation, chauffage vert) |
| 10% | Rénovation simple (peinture, plomberie) |
| 20% | Construction neuve, prestations hors éligibilité |

**Calculs automatiques** :
```
total_ht_ligne = quantity × unit_price × (1 - discount/100)
total_vat_ligne = total_ht_ligne × vat_rate / 100
subtotal_ht = Σ total_ht_ligne
total_vat = Σ total_vat_ligne
total_ttc = subtotal_ht + total_vat
```

### 3.3 Dashboard & Analytics (Phase 1)

**Indicateurs clés** :
- 💰 CA total (HT et TTC) — année en cours
- 📊 Factures en attente de paiement (montant + nombre)
- ✅ Factures payées (montant + nombre)
- ❌ Factures annulées (montant + nombre)
- 📈 Graphique mensuel (CA sur 12 mois glissants)
- 🏆 Top 5 clients (CA généré)

**Filtres** :
- Par année
- Par client
- Par statut

### 3.4 Export PDF (Phase 2)

- Génération côté serveur (WeasyPrint) ou client (jsPDF)
- Logo entreprise en en-tête
- Mentions légales obligatoires
- Format A4 professionnel

### 3.5 Gestion des Acomptes (Phase 2)

- Pourcentage d'acompte configurable (ex: 30%)
- Déduction automatique du solde restant
- Lien entre facture d'acompte et facture finale

### 3.6 Gestion des Chantiers (Phase 3)

- Adresse du chantier
- Photos avant/après
- Lien avec factures associées
- Suivi d'avancement


---

## 4. 🔒 Règles Métier

### 4.1 Cycle de Vie d'une Facture

```
┌────────────┐     ┌──────────┐     ┌─────────┐
│ Brouillon  │────▶│ Envoyée  │────▶│ Payée   │
└────────────┘     └──────────┘     └─────────┘
                         │
                         ├──▶ Annulée
                         │
                         └──▶ En retard (auto si due_date < today)
```

### 4.2 Transitions Autorisées

| Depuis → Vers | Brouillon | Envoyée | Payée | Annulée | En retard |
|---------------|-----------|---------|-------|---------|-----------|
| **Brouillon** | — | ✅ | ❌ | ❌ | ❌ |
| **Envoyée** | ❌ | — | ✅ | ✅ | ✅ |
| **Payée** | ❌ | ❌ | — | ❌ | ❌ |
| **Annulée** | ❌ | ❌ | ❌ | — | ❌ |
| **En retard** | ❌ | ❌ | ✅ | ❌ | — |

### 4.3 Contraintes Immuable

- ❌ **Suppression interdite** — aucune facture ne peut être supprimée
- ✅ Une facture `payée` ou `annulée` est en **lecture seule**
- ✅ Une facture `envoyée` ne peut plus être modifiée (lignes, montants)
- ✅ Historique complet des changements de statut (table `status_history`)

### 4.4 Mentions Légales Obligatoires

Chaque facture doit contenir :
- Numéro de facture séquentiel
- Date d'émission
- Identité complète du prestataire et du client
- Détail des prestations (description, quantité, prix unitaire)
- Taux de TVA appliqué
- Mention : *"Pénalité de retard : 3 fois le taux d'intérêt légal"*
- Mention : *"Indemnité forfaitaire pour frais de recouvrement : 40€"*

---

## 5. 🎨 Design & UX

### 5.1 Palette de Couleurs

| Couleur | Code | Usage |
|---------|------|-------|
| Gris anthracite | `#2C3E50` | Primaire, titres, navigation |
| Jaune chantier | `#F39C12` | Accent, boutons CTA, alertes |
| Vert succès | `#27AE60` | Statut payé, confirmations |
| Rouge erreur | `#E74C3C` | Statut annulé, erreurs |
| Bleu info | `#3498DB` | Statut en cours, liens |
| Gris clair | `#ECF0F1` | Fond de page |
| Blanc | `#FFFFFF` | Cards, formulaires |

### 5.2 Typographie

- **Titres** : Roboto Bold (700) — robuste, industriel
- **Corps** : Open Sans Regular (400) — lisible, neutre
- **Monospace** : JetBrains Mono — numéros, codes

### 5.3 Icônes

- Style : outline, stroke 1.5px
- Thème : casque, grue, marteau, clé à molette, plan
- Bibliothèque : Lucide Icons ou Heroicons

### 5.4 Composants UI

- **Cards** : ombre légère (`shadow-sm`), coins arrondis (`rounded-lg`)
- **Tableaux** : tri par colonne, pagination, export CSV
- **Formulaires** : validation en temps réel, messages d'erreur inline
- **Toasts** : notifications non-bloquantes en bas à droite
- **Modales** : confirmation pour actions critiques

---

## 6. 🚀 Phases de Développement

### Phase 1 — MVP (Semaines 1-4)
- [x] Setup projet (dossier, README, specs)
- [ ] API REST complète (clients, factures, analytics)
- [ ] Frontend : pages Dashboard, Clients, Factures
- [ ] Règles métier (statuts, non-suppression)
- [ ] Tests unitaires + intégration
- [ ] Seed data (données de démo)

### Phase 2 — Enrichissement (Semaines 5-8)
- [ ] Export PDF des factures
- [ ] Gestion des acomptes
- [ ] Recherche avancée + filtres
- [ ] Rapport annuel (CA, TVA collectée)
- [ ] Envoi de factures par email

### Phase 3 — Fonctionnalités Avancées (Semaines 9-12)
- [ ] Gestion des chantiers (adresse, photos)
- [ ] Notifications (factures en retard)
- [ ] Version mobile responsive
- [ ] Authentification multi-utilisateurs

### Phase 4 — Bonus Portfolio (Optionnel)
- [ ] Prévisions de trésorerie
- [ ] Suggestions d'articles (basé sur historique)
- [ ] Application mobile (React Native)
- [ ] Internationalisation (FR/EN)


---

## 7. 🛠️ Architecture Technique

### Backend (FastAPI)

```
backend/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration (env vars)
│   ├── database.py          # Connexion SQLAlchemy
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── client.py
│   │   ├── invoice.py
│   │   └── invoice_line.py
│   ├── schemas/             # Schémas Pydantic
│   │   ├── client.py
│   │   ├── invoice.py
│   │   └── analytics.py
│   ├── routes/              # Endpoints API
│   │   ├── clients.py
│   │   ├── invoices.py
│   │   └── analytics.py
│   ├── services/            # Logique métier
│   │   ├── client_service.py
│   │   ├── invoice_service.py
│   │   └── analytics_service.py
│   └── utils/               # Helpers
│       ├── invoice_number.py
│       └── validators.py
├── tests/
│   ├── test_clients.py
│   ├── test_invoices.py
│   └── test_analytics.py
├── requirements.txt
└── .env.example
```

### Frontend (React + Vite)

```
frontend/
├── src/
│   ├── main.tsx             # Point d'entrée React
│   ├── App.tsx              # Router principal
│   ├── components/          # Composants réutilisables
│   │   ├── ui/              # Boutons, inputs, cards
│   │   ├── layout/          # Header, Sidebar, Footer
│   │   └── invoice/         # Composants spécifiques facture
│   ├── pages/               # Pages de l'application
│   │   ├── Dashboard.tsx
│   │   ├── Clients.tsx
│   │   ├── ClientDetail.tsx
│   │   ├── Invoices.tsx
│   │   ├── InvoiceCreate.tsx
│   │   └── InvoiceDetail.tsx
│   ├── services/            # Appels API
│   │   ├── api.ts           # Axios instance
│   │   ├── clients.ts
│   │   ├── invoices.ts
│   │   └── analytics.ts
│   ├── hooks/               # Hooks personnalisés
│   │   ├── useClients.ts
│   │   └── useInvoices.ts
│   ├── theme/               # Configuration Tailwind
│   │   └── theme.ts
│   └── types/               # Types TypeScript
│       ├── client.ts
│       └── invoice.ts
├── public/
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── .env.example
```


---

## 8. 📊 Modèle de Données

### Table `clients`

| Colonne | Type | Contrainte |
|---------|------|------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT |
| `name` | VARCHAR(255) | NOT NULL |
| `email` | VARCHAR(255) | UNIQUE |
| `phone` | VARCHAR(50) | — |
| `address` | TEXT | — |
| `siret` | VARCHAR(50) | — |
| `client_type` | ENUM | NOT NULL ('particulier', 'entreprise', 'maitre_ouvrage') |
| `archived` | BOOLEAN | DEFAULT FALSE |
| `created_at` | TIMESTAMP | DEFAULT NOW() |
| `updated_at` | TIMESTAMP | DEFAULT NOW() |

### Table `invoices`

| Colonne | Type | Contrainte |
|---------|------|------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT |
| `invoice_number` | VARCHAR(20) | UNIQUE, NOT NULL |
| `client_id` | INTEGER | FOREIGN KEY → clients(id) |
| `status` | ENUM | NOT NULL ('brouillon', 'envoyee', 'payee', 'annulee', 'en_retard') |
| `issue_date` | DATE | NOT NULL |
| `due_date` | DATE | — |
| `subtotal_ht` | DECIMAL(10,2) | NOT NULL |
| `total_vat` | DECIMAL(10,2) | NOT NULL |
| `total_ttc` | DECIMAL(10,2) | NOT NULL |
| `notes` | TEXT | — |
| `created_at` | TIMESTAMP | DEFAULT NOW() |
| `updated_at` | TIMESTAMP | DEFAULT NOW() |

### Table `invoice_lines`

| Colonne | Type | Contrainte |
|---------|------|------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT |
| `invoice_id` | INTEGER | FOREIGN KEY → invoices(id) |
| `description` | VARCHAR(500) | NOT NULL |
| `category` | ENUM | NOT NULL ('maconnerie', 'plomberie', 'electricite', 'peinture', 'terrassement', 'couverture', 'autre') |
| `quantity` | DECIMAL(10,2) | NOT NULL, > 0 |
| `unit` | VARCHAR(50) | NOT NULL |
| `unit_price` | DECIMAL(10,2) | NOT NULL, > 0 |
| `vat_rate` | DECIMAL(4,2) | NOT NULL (5.5, 10, 20) |
| `discount` | DECIMAL(5,2) | DEFAULT 0 |
| `total_ht` | DECIMAL(10,2) | NOT NULL |

### Table `status_history`

| Colonne | Type | Contrainte |
|---------|------|------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT |
| `invoice_id` | INTEGER | FOREIGN KEY → invoices(id) |
| `old_status` | VARCHAR(50) | — |
| `new_status` | VARCHAR(50) | NOT NULL |
| `changed_at` | TIMESTAMP | DEFAULT NOW() |
| `changed_by` | VARCHAR(255) | — |

---

## 9. 🔒 Règles de Validation

### Clients

| Règle | Détail |
|-------|--------|
| Nom obligatoire | Min 2 caractères |
| Email valide | Format RFC 5322 |
| Email unique | Pas de doublon |
| SIRET | 14 chiffres (optionnel) |
| Type client | Valeur de l'enum obligatoire |

### Factures

| Règle | Détail |
|-------|--------|
| Client existant | `client_id` doit référencer un client valide |
| Au moins 1 ligne | Impossible de créer une facture vide |
| Quantité > 0 | Nombre décimal strictement positif |
| Prix unitaire > 0 | Nombre décimal strictement positif |
| TVA valide | 5.5, 10, ou 20 uniquement |
| Date émission | ≤ date du jour |
| Date échéance | ≥ date d'émission |
| Numéro unique | Auto-généré, non modifiable |

### Transitions de statut

- Respecter la matrice du §4.2
- Journaliser chaque changement dans `status_history`
- Empêcher modification d'une facture `envoyée`, `payée`, `annulée`


---

## 10. 📈 Métriques de Succès (Portfolio)

| Critère | Objectif |
|---------|----------|
| Code propre | Linting (Ruff, ESLint), formatage (Black, Prettier) |
| Tests | Couverture > 80% |
| Documentation | README complet, OpenAPI, commentaires |
| API RESTful | Respect des standards HTTP, codes de statut |
| UX | Responsive, intuitive, accessible |
| Règles métier | Toutes implémentées et testées |
| Git | Commits atomiques, messages conventionnels |

---

## 11. 📚 Ressources

- [OpenAPI Specification](./openapi.yaml)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Réglementation facturation BTP](https://www.economie.gouv.fr/entreprises/facture-obligations)

---

<p align="center">
  <strong>guestBTP</strong> — La facturation simplifiée pour le BTP 🏗️
</p>

