# Frontend guestBTP

Application React + TypeScript pour la gestion de facturation BTP.

## Stack technique

- **React 18** avec TypeScript
- **Vite** pour le bundling et le dev server
- **TanStack Query** pour la gestion des données serveur
- **React Router** pour la navigation
- **Axios** pour les appels HTTP
- **Vitest** pour les tests unitaires

## Installation

```bash
npm install
```

## Développement

```bash
npm run dev
```

L'application sera accessible sur http://localhost:5173

Le proxy Vite redirige automatiquement les appels `/api` vers le backend (http://localhost:8000).

## Tests

```bash
npm test              # Lance les tests en mode watch
npm run test:coverage # Lance les tests avec couverture
```

## Build production

```bash
npm run build
npm run preview       # Prévisualise le build
```

## Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts       # Client API centralisé + hooks TanStack Query
│   ├── components/         # Composants réutilisables
│   ├── pages/              # Pages de l'application
│   ├── hooks/              # Hooks personnalisés
│   ├── types/              # Types TypeScript
│   ├── tests/              # Tests unitaires
│   ├── App.tsx             # Composant racine
│   ├── main.tsx            # Point d'entrée
│   └── index.css           # Styles globaux
├── public/                 # Assets statiques
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## Architecture API

Tous les appels API passent par `src/api/client.ts` :

- **Instance Axios** : `apiClient` configuré avec baseURL et intercepteurs
- **Fonctions API** : `clientsApi`, `invoicesApi`, `analyticsApi`
- **Hooks TanStack Query** : `useClients`, `useInvoices`, etc.
- **Fonctions utilitaires** : `calculateTotal`, `calculateLineTotal`, `calculateLineVat`

## Variables d'environnement

Copier `.env.example` vers `.env` :

```bash
cp .env.example .env
```

- `VITE_API_URL` : URL de l'API backend (optionnel, proxy Vite utilisé par défaut)
