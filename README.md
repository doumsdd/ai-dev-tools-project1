# 🏗️ guestBTP — Application de Facturation BTP

> **La facturation simplifiée pour les entreprises du BTP**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](https://swagger.io/specification/)

## 📖 Présentation

**guestBTP** est une application web moderne de gestion de facturation conçue spécialement pour les artisans et entreprises du secteur du bâtiment (BTP). Elle permet de gérer clients, factures, et suivre le chiffre d'affaires en respectant les règles métier spécifiques au secteur.

### 🎯 Objectif

Ce projet a été conçu comme un **projet portfolio** démontrant :
- Une architecture full-stack moderne (FastAPI + React)
- L'implémentation de règles métier réelles (non-suppression des factures, traçabilité)
- La gestion de spécificités BTP (TVA réduite, catégories de travaux)
- Un design soigné avec thème industriel

## ✨ Fonctionnalités

### Phase 1 — MVP
- 👥 **Gestion des clients** (particuliers, entreprises, maîtres d'ouvrage)
- 📄 **Création de factures** avec lignes, TVA BTP (5.5%, 10%, 20%), remises
- 📊 **Dashboard** avec analytics (CA, factures en attente/payées)
- 🔒 **Règles métier strictes** : pas de suppression, statuts traçables
- 🔢 **Numérotation automatique** des factures (FA-2026-0001)

### Phase 2 — Enrichissement (à venir)
- 📥 Export PDF des factures
- 💰 Gestion des acomptes
- 🔍 Recherche avancée + filtres
- 📧 Envoi par email

### Phase 3 — Avancé (à venir)
- 📸 Gestion des chantiers
- 🔔 Notifications
- 📱 App mobile

## 🛠️ Stack Technique

| Couche | Technologie |
|--------|-------------|
| **Backend** | Python 3.11+ / FastAPI |
| **ORM** | SQLAlchemy 2.0 |
| **Base de données** | SQLite (dev) / PostgreSQL (prod) |
| **Validation** | Pydantic v2 |
| **Auth** | JWT (jose) |
| **Frontend** | React 18 + TypeScript |
| **Build** | Vite |
| **State** | TanStack Query |
| **Routing** | React Router v6 |
| **UI** | Tailwind CSS + shadcn/ui |
| **Charts** | Recharts |
| **Tests** | pytest (backend) / Vitest (frontend) |

## 📁 Structure du Projet

```
ai-dev-tools-project1/
├── README.md
├── .gitignore
├── product-spec.md          # Spécifications produit
├── openapi.yaml             # Spécification API OpenAPI 3.0
│
├── backend/                 # ✅ API REST (FastAPI) — IMPLÉMENTÉ
│   ├── app/
│   │   ├── main.py          # Point d'entrée FastAPI
│   │   ├── config.py        # Configuration (Pydantic Settings)
│   │   ├── models/          # SQLAlchemy (Client, Invoice, InvoiceLine)
│   │   ├── schemas/         # Pydantic v2 (validation + sérialisation)
│   │   ├── routers/         # Endpoints (clients, invoices, analytics)
│   │   ├── services/        # Logique métier (calculs, numérotation, statuts)
│   │   └── database/        # Session SQLAlchemy
│   ├── tests/               # ✅ 28 tests pytest (SQLite in-memory)
│   ├── docker/              # Scripts d'initialisation PostgreSQL
│   ├── Dockerfile           # Multi-stage build optimisé
│   ├── docker-compose.yml   # API + PostgreSQL
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── frontend/                # Interface utilisateur (React)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── theme/
│   ├── public/
│   ├── package.json
│   └── .env.example
│
└── lovable/                 # Prompts frontend Lovable
    ├── prompts/             # 4 prompts itératifs
    ├── mock-data.json
    └── design-tokens.md
```

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11+
- Node.js 18+
- npm ou yarn
- Docker & Docker Compose (optionnel)

### Backend (avec Docker — recommandé)

```bash
cd backend
docker-compose up --build
```

L'API sera disponible sur `http://localhost:8000`
Documentation Swagger : `http://localhost:8000/docs`

### Backend (en local)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`
Documentation Swagger : `http://localhost:8000/docs`

### Tests

```bash
cd backend
pytest tests/ -v
```

**28 tests** couvrant les clients, factures, analytics, transitions de statut, calculs automatiques, et numérotation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

L'application sera disponible sur `http://localhost:5173`

## 📡 API

La spécification complète de l'API est disponible dans [`openapi.yaml`](./openapi.yaml).

### Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/v1/clients` | Créer un client |
| `GET` | `/api/v1/clients` | Lister les clients |
| `POST` | `/api/v1/invoices` | Créer une facture |
| `GET` | `/api/v1/invoices` | Lister les factures |
| `GET` | `/api/v1/analytics/revenue` | Statistiques de revenus |

## 📋 Règles Métier

- ❌ **Une facture ne peut jamais être supprimée**
- ✅ Statuts : `brouillon` → `envoyée` → `payée` | `annulée` | `en_retard`
- ✅ Une facture payée ou annulée est en **lecture seule**
- ✅ Historique complet des changements de statut
- ✅ TVA BTP : 5.5% (rénovation énergétique), 10% (rénovation), 20% (neuf)

## 🎨 Thème BTP

- **Palette** : gris anthracite (#2C3E50), jaune chantier (#F39C12)
- **Typographie** : Roboto (titres), Open Sans (corps)
- **Style** : industriel, robuste, professionnel

## 📄 Documentation

- [Spécifications produit](./product-spec.md) — Cahier des charges complet
- [Spécification API](./openapi.yaml) — OpenAPI 3.0

## 📝 License

MIT © 2026

---

<p align="center">
  Fait avec 🏗️ pour le secteur du BTP
</p>
