# 🏗️ guestBTP — Smart Invoicing for Construction Businesses

> **Streamline billing workflows for construction companies with AI-assisted development**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg)](https://www.typescriptlang.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-green.svg)](https://swagger.io/specification/)
[![Tests](https://img.shields.io/badge/Tests-28%20pytest-brightgreen.svg)](https://docs.pytest.org/)

---

## 🎯 The Problem

Construction businesses face unique billing challenges that generic invoicing tools don't address:

- **Complex VAT rules**: Reduced rates (5.5%, 10%) for energy renovation, standard rates (20%) for new builds
- **Strict compliance requirements**: Invoices cannot be deleted once issued (legal traceability)
- **Status tracking**: Need to track invoice lifecycle (draft → sent → paid → overdue)
- **Industry-specific workflows**: Progress billing, retainage, milestone-based payments
- **Manual processes**: Spreadsheets and paper-based systems lead to errors and lost revenue

**Result**: Construction companies waste hours on administrative tasks, make calculation errors, and struggle with compliance.

---

## 💡 The Solution

**guestBTP** is a modern, full-stack invoicing application designed specifically for construction businesses. It automates complex calculations, enforces business rules, and provides real-time analytics—all through an intuitive interface.

### Key Benefits

✅ **Automated VAT calculations** — No more manual rate lookups  
✅ **Compliance by design** — Invoices are immutable, status changes are tracked  
✅ **Real-time analytics** — Track revenue, outstanding invoices, and cash flow  
✅ **Professional invoicing** — Auto-numbering (FA-2026-0001), branded templates  
✅ **AI-assisted development** — Built with modern AI tools for rapid iteration

## 🏛️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│              React 18 + TypeScript + Vite                    │
│         TanStack Query • React Router • Tailwind CSS        │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API (JSON)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                         BACKEND                              │
│                    FastAPI + Pydantic v2                     │
│        SQLAlchemy 2.0 • JWT Auth • Business Logic          │
└──────────────────────────┬──────────────────────────────────┘
                           │ ORM
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                               │
│              PostgreSQL 15 (Production)                      │
│              SQLite (Development / Testing)                  │
└─────────────────────────────────────────────────────────────┘
```

### Development Pipeline

The project follows a three-stage AI-assisted pipeline, where each tool specializes in a specific layer:

```
┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│    LOVABLE     │  →   │     CLINE      │  →   │   GITHUB CI    │
│   (UI / UX)    │      │  (Full-Stack)  │      │   (Validate)   │
└────────────────┘      └────────────────┘      └────────────────┘
   Design prompts         API + Business          Tests + Security
   Mock data              Database models         Docker builds
   React components       Docker setup            Audit reports
```

### Data Flow: Creating an Invoice

```
User fills form (React)
        │
        ▼
POST /api/v1/invoices  ──►  Pydantic validation
        │                           │
        ▼                           ▼
Invoice service computes      Business rules enforced
totals + VAT (5.5/10/20%)     (status machine, numbering)
        │
        ▼
SQLAlchemy INSERT  ──►  PostgreSQL
        │
        ▼
Response → React Query cache → UI update
```

> **Key design choice**: The backend is the single source of truth. All calculations (totals, VAT, numbering) happen server-side to guarantee data integrity. The frontend is a thin, reactive layer.

---

## 🤖 AI Workflow

This project was built end-to-end using a **multi-agent AI pipeline**, demonstrating how modern AI tools can collaborate to ship production-ready software.

### Phase 1 — Design & Prototyping (Lovable)

**Tool**: [Lovable](https://lovable.dev) — AI-powered UI generator

| Step | Input | Output |
|------|-------|--------|
| 1. Design system | Brand guidelines | `design-tokens.md` (colors, typography, spacing) |
| 2. Mock data | Business requirements | `mock-data.json` (realistic clients & invoices) |
| 3. Invoice form | `01-invoice-detail.md` | React form with line items, VAT, totals |
| 4. Invoice list | `02-invoice-list.md` | Filterable table with status badges |
| 5. Dashboard | `03-dashboard.md` | Analytics cards + Recharts visualizations |
| 6. Polish | `04-polish.md` | Final UI refinements, responsive design |

**Result**: Production-ready React components with Tailwind CSS styling, ready to be wired to a backend.

### Phase 2 — Backend Development (Cline AI)

**Tool**: Cline AI — Full-stack coding assistant

| Step | Task | Output |
|------|------|--------|
| 1. API design | OpenAPI spec | `openapi.yaml` (all endpoints documented) |
| 2. Database | SQLAlchemy models | `Client`, `Invoice`, `InvoiceLine` with relationships |
| 3. Business logic | Domain services | Invoice calculator, status machine, auto-numbering |
| 4. Validation | Pydantic schemas | Request/response validation for all endpoints |
| 5. Testing | pytest suite | 28 tests covering all business rules |
| 6. Containerization | Docker setup | Multi-stage Dockerfile + docker-compose |

**Result**: Fully tested FastAPI backend with PostgreSQL integration and CI/CD pipeline.

### Phase 3 — Security & CI/CD (GitHub Actions)

**Tool**: GitHub Actions — Automated validation

```yaml
Pipeline:
  ├── Lint (ruff) ──────────────────► Code quality
  ├── Test (pytest) ────────────────► 28 tests passing
  ├── Security (bandit + pip-audit) ► No vulnerabilities
  ├── Build (Docker) ──────────────► Image builds successfully
  └── Frontend (npm build) ────────► TypeScript compiles
```

### AI Agent Capabilities

The project includes a dedicated `agent-capabilities/` folder with tools that AI agents can use to validate the application:

- **`validate_invoice_math.py`** — Standalone script that verifies invoice calculations against business rules
- Agents can run this script to independently verify the backend's correctness

### Why This Matters

This workflow demonstrates that AI-assisted development is not just about generating code — it's about **orchestrating specialized AI tools** where each one excels at its specific task:

| Concern | Tool | Why |
|---------|------|-----|
| UI/UX design | Lovable | Specialized in React + Tailwind generation |
| Backend logic | Cline | Full-stack reasoning, test generation |
| Validation | GitHub Actions | Deterministic, repeatable checks |
| Verification | Custom scripts | Domain-specific business rule validation |

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend Framework** | FastAPI | 0.100+ |
| **Language** | Python | 3.11+ |
| **ORM** | SQLAlchemy | 2.0 |
| **Validation** | Pydantic | v2 |
| **Database** | PostgreSQL / SQLite | 15 / 3.40 |
| **Frontend Framework** | React | 18 |
| **Language** | TypeScript | 5 |
| **Build Tool** | Vite | 5 |
| **State Management** | TanStack Query | 5 |
| **Routing** | React Router | v6 |
| **Styling** | Tailwind CSS | 3 |
| **Charts** | Recharts | 2 |
| **Testing (Backend)** | pytest | 7.4 |
| **Testing (Frontend)** | Vitest | 1 |
| **Containerization** | Docker | 24 |

---

## ✨ Features

### ✅ Phase 1 — MVP (Implemented)

- **Client Management**
  - Create, update, and list clients (individuals, companies, project owners)
  - Track contact information and billing addresses
  
- **Invoice Management**
  - Create invoices with multiple line items
  - Automatic VAT calculations (5.5%, 10%, 20%)
  - Discounts (percentage or fixed amount)
  - Auto-numbering (FA-2026-0001)
  
- **Status Tracking**
  - Draft → Sent → Paid | Overdue | Cancelled
  - Immutable invoices (no deletion)
  - Full audit trail
  
- **Analytics Dashboard**
  - Total revenue (paid invoices)
  - Outstanding receivables
  - Invoice count by status
  - Monthly revenue trends

### 🚧 Phase 2 — Enhanced (Planned)

- 📥 PDF export for invoices
- 💰 Deposit/advance payment tracking
- 🔍 Advanced search and filtering
- 📧 Email delivery integration

### 🔮 Phase 3 — Advanced (Future)

- 📸 Construction site management
- 🔔 Automated notifications
- 📱 Mobile app (React Native)

---

## 📁 Project Structure

```
ai-dev-tools-project1/
├── README.md                      # This file
├── AGENTS.md                      # AI agent instructions
├── product-spec.md                # Product specifications
├── openapi.yaml                   # OpenAPI 3.0 specification
│
├── backend/                       # FastAPI Backend
│   ├── app/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── config.py             # Pydantic Settings
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── client.py
│   │   │   ├── invoice.py
│   │   │   └── invoice_line.py
│   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── client.py
│   │   │   ├── invoice.py
│   │   │   └── analytics.py
│   │   ├── routers/              # API endpoints
│   │   │   ├── clients.py
│   │   │   ├── invoices.py
│   │   │   └── analytics.py
│   │   ├── services/             # Business logic
│   │   │   ├── invoice_calculator.py
│   │   │   ├── invoice_number.py
│   │   │   └── status_machine.py
│   │   └── database/             # DB session
│   ├── tests/                    # pytest tests (28 tests)
│   ├── docker/                   # PostgreSQL init scripts
│   ├── Dockerfile                # Multi-stage build
│   ├── docker-compose.yml        # Local dev environment
│   ├── requirements.txt          # Production dependencies
│   └── requirements-dev.txt      # Dev dependencies
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── api/                  # API client
│   │   ├── pages/                # Page components
│   │   ├── components/           # Reusable components
│   │   ├── types/                # TypeScript types
│   │   └── tests/                # Vitest tests
│   ├── public/                   # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── lovable/                      # Lovable AI prompts
│   ├── prompts/                  # 4 iterative prompts
│   ├── mock-data.json            # Sample data
│   └── design-tokens.md          # Design system
│
├── agent-capabilities/           # AI agent tools
│   ├── README.md
│   └── validate_invoice_math.py  # Invoice validation script
│
├── security/                     # Security audits
│   ├── README.md
│   ├── audit-report.md
│   ├── bandit-output.txt
│   └── pip-audit-output.txt
│
├── docs/                         # Documentation
│   └── agent-extension-pack.md
│
└── .github/workflows/            # CI/CD
    └── ci.yml                    # GitHub Actions
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (recommended)
- PostgreSQL 15 (if running without Docker)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/doumsdd/ai-dev-tools-project1.git
cd ai-dev-tools-project1

# Start backend with Docker
cd backend
docker-compose up --build
```

The API will be available at `http://localhost:8000`  
Swagger documentation: `http://localhost:8000/docs`

```bash
# In a new terminal, start frontend
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Option 2: Local Development

**Backend**:

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements-dev.txt

# Run the server
uvicorn app.main:app --reload
```

**Frontend**:

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

**Coverage**: 28 tests covering:
- Client CRUD operations
- Invoice creation and validation
- Status transitions (state machine)
- Automatic calculations (totals, VAT)
- Invoice numbering
- Analytics endpoints

### Frontend Tests

```bash
cd frontend
npm test
```

---

## 📡 API Documentation

Full API specification available in [`openapi.yaml`](./openapi.yaml).

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/clients` | Create a new client |
| `GET` | `/api/v1/clients` | List all clients |
| `GET` | `/api/v1/clients/{id}` | Get client details |
| `POST` | `/api/v1/invoices` | Create a new invoice |
| `GET` | `/api/v1/invoices` | List all invoices |
| `GET` | `/api/v1/invoices/{id}` | Get invoice details |
| `PATCH` | `/api/v1/invoices/{id}/status` | Update invoice status |
| `GET` | `/api/v1/analytics/revenue` | Get revenue analytics |

**Interactive documentation**: `http://localhost:8000/docs` (Swagger UI)

---

## 📋 Business Rules

guestBTP enforces strict business rules to ensure compliance:

### Invoice Immutability

❌ **Invoices can never be deleted** once created  
✅ Status changes are tracked in audit log  
✅ Paid and cancelled invoices are read-only

### Status Workflow

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Draft   │ →  │   Sent   │ →  │   Paid   │
└──────────┘    └──────────┘    └──────────┘
                       │
                       ├──────→ ┌──────────┐
                       │        │ Overdue  │
                       │        └──────────┘
                       │
                       └──────→ ┌──────────┐
                                │ Cancelled│
                                └──────────┘
```

### VAT Rates (Construction Industry)

- **5.5%** — Energy renovation (insulation, heat pumps, etc.)
- **10%** — Residential renovation
- **20%** — New construction, commercial work

---

## 🎨 Design System

### Color Palette

- **Primary**: Anthracite Gray `#2C3E50` — Professional, industrial
- **Accent**: Construction Yellow `#F39C12` — High visibility, energetic
- **Success**: Green `#27AE60` — Paid invoices, positive actions
- **Danger**: Red `#E74C3C` — Overdue invoices, errors

### Typography

- **Headings**: Roboto — Clean, modern, technical
- **Body**: Open Sans — Readable, professional

### Style

Industrial, robust, professional — reflecting the construction industry's values of reliability and precision.

---

## 🔒 Security

### Implemented Measures

✅ **Input validation** — Pydantic schemas for all endpoints  
✅ **SQL injection protection** — SQLAlchemy ORM with parameterized queries  
✅ **XSS prevention** — React's built-in escaping  
✅ **CORS configuration** — Restricted origins  
✅ **Secrets management** — Environment variables, `.env` files in `.gitignore`  
✅ **Security audits** — bandit (Python), npm audit (Node.js)  

### Audit Reports

- [Security audit report](./security/audit-report.md)
- [bandit output](./security/bandit-output.txt)
- [pip-audit output](./security/pip-audit-output.txt)

---

## 📄 Documentation

- [Product specifications](./product-spec.md) — Complete requirements
- [API specification](./openapi.yaml) — OpenAPI 3.0
- [Agent extension pack](./docs/agent-extension-pack.md) — AI tools guide
- [Agent capabilities](./agent-capabilities/README.md) — Validation scripts

---

## 🚧 Deployment

### Production Ready

The application is containerized and ready for deployment:

**Backend**:
- Docker multi-stage build (optimized image size)
- PostgreSQL for production database
- Gunicorn + Uvicorn workers (planned)

**Frontend**:
- Static build optimized for CDN
- Ready for Vercel, Netlify, or Cloudflare Pages

### Recommended Stack

- **Frontend**: Vercel (free tier, global CDN)
- **Backend**: Railway or Render (managed hosting)
- **Database**: Railway PostgreSQL or Supabase (managed DB)

**Estimated cost**: $5-20/month

---

## 🤝 Contributing

This is a portfolio project demonstrating AI-assisted development. Contributions, issues, and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT © 2026

---

## 🙏 Acknowledgments

- **FastAPI** — Modern, fast web framework for Python
- **React** — UI component library
- **Lovable** — AI-powered frontend generation
- **Cline AI** — Full-stack development assistant
- **Tailwind CSS** — Utility-first CSS framework

---

<p align="center">
  <strong>Built with 🏗️ for the construction industry</strong><br>
  <em>Demonstrating the power of AI-assisted development</em>
</p>
