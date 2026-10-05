# guestBTP Backend

API FastAPI pour l'application de facturation BTP.

## 🚀 Démarrage rapide

### Avec Docker (recommandé)

```bash
cd backend
docker-compose up --build
```

L'API sera accessible sur http://localhost:8000
- Documentation Swagger : http://localhost:8000/docs
- Documentation ReDoc : http://localhost:8000/redoc

### En local (development)

1. Crée un environnement virtuel :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installe les dépendances :
```bash
pip install -r requirements-dev.txt
```

3. Configure les variables d'environnement :
```bash
cp .env.example .env
# Édite .env avec tes valeurs
```

4. Lance l'API :
```bash
uvicorn app.main:app --reload
```

## 🧪 Tests

```bash
# Lance tous les tests
pytest

# Avec couverture
pytest --cov=app --cov-report=html

# Tests verbeux
pytest -v
```

## 📁 Structure du projet

```
backend/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration
│   ├── database/
│   │   └── session.py       # Session SQLAlchemy
│   ├── models/              # Modèles SQLAlchemy
│   │   ├── client.py
│   │   ├── invoice.py
│   │   └── invoice_line.py
│   ├── schemas/             # Schémas Pydantic
│   │   ├── client.py
│   │   ├── invoice.py
│   │   └── analytics.py
│   ├── routers/             # Endpoints API
│   │   ├── clients.py
│   │   ├── invoices.py
│   │   └── analytics.py
│   └── services/            # Logique métier
│       ├── invoice_calculator.py
│       ├── invoice_number.py
│       └── status_machine.py
├── tests/                   # Tests pytest
│   ├── test_clients.py
│   ├── test_invoices.py
│   └── test_analytics.py
├── docker/
│   └── init.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements-dev.txt
```

## 🔌 Endpoints API

### Clients
- `POST /api/v1/clients` - Créer un client
- `GET /api/v1/clients` - Lister les clients (paginé)
- `GET /api/v1/clients/{id}` - Récupérer un client
- `PATCH /api/v1/clients/{id}` - Modifier un client
- `DELETE /api/v1/clients/{id}` - Archiver un client

### Factures
- `POST /api/v1/invoices` - Créer une facture (calculs auto)
- `GET /api/v1/invoices` - Lister les factures (paginé, filtrable)
- `GET /api/v1/invoices/{id}` - Récupérer une facture
- `PATCH /api/v1/invoices/{id}/status` - Changer le statut

### Analytics
- `GET /api/v1/analytics/revenue` - Revenu par mois (factures payées)

## 📊 Règles métier

### Calculs automatiques
```
total_ht_ligne = quantity × unit_price × (1 - discount/100)
total_vat_ligne = total_ht_ligne × vat_rate / 100
subtotal_ht = Σ total_ht_ligne
total_vat = Σ total_vat_ligne
total_ttc = subtotal_ht + total_vat
```

### Transitions de statut
- `brouillon` → `envoyee`, `annulee`
- `envoyee` → `payee`, `en_retard`
- `en_retard` → `payee`
- `payee`, `annulee` → lecture seule

### Numérotation
- Format : `FA-AAAA-NNNN` (ex: `FA-2026-0001`)
- Auto-généré, séquentiel par année

## 🐛 Débogage

```bash
# Voir les logs
docker-compose logs -f api

# Accéder à la base de données
docker-compose exec db psql -U guestbtp -d guestbtp

# Redémarrer les services
docker-compose restart
```

## 📝 Licence

MIT
