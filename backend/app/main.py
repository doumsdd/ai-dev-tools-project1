"""Application principale FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.session import engine
from app.models import Base
from app.routers import analytics, clients, invoices


def create_tables():
    """Crée les tables si nécessaire (en production, utiliser Alembic)."""
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    """Factory pour créer l'application FastAPI."""
    app = FastAPI(
        title="guestBTP API",
        description="API de facturation pour entreprises du BTP",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inclusion des routers
    api_prefix = settings.API_V1_PREFIX
    app.include_router(clients.router, prefix=api_prefix)
    app.include_router(invoices.router, prefix=api_prefix)
    app.include_router(analytics.router, prefix=api_prefix)

    # Health check
    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()

# Crée les tables au démarrage (hors tests)
import os
if os.environ.get("DATABASE_URL") != "sqlite:///:memory:":
    create_tables()
