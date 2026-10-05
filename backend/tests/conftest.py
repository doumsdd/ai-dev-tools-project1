"""Configuration pytest et fixtures."""

import os

# Force SQLite pour les tests AVANT tout import de l'app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import get_db
from app.main import create_app
from app.models.base import Base


@pytest.fixture(scope="function")
def engine():
    """Crée un engine SQLite en mémoire pour les tests."""
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    yield test_engine
    Base.metadata.drop_all(test_engine)
    test_engine.dispose()


@pytest.fixture(scope="function")
def db(engine):
    """Fournit une session de base de données pour les tests."""
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db):
    """Fournit un client de test FastAPI."""
    app = create_app()

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_client_data():
    """Données de test pour un client."""
    return {
        "name": "Entreprise Durand",
        "email": "contact@durand-btp.fr",
        "phone": "+33 1 23 45 67 89",
        "address": "12 rue du Chantier, 75012 Paris",
        "siret": "12345678901234",
        "client_type": "entreprise",
    }


@pytest.fixture
def sample_invoice_data():
    """Données de test pour une facture."""
    return {
        "client_id": 1,  # Sera mis à jour avec le vrai ID
        "issue_date": "2026-01-15",
        "due_date": "2026-02-15",
        "lines": [
            {
                "description": "Terrassement terrain",
                "category": "terrassement",
                "quantity": 100,
                "unit": "m3",
                "unit_price": 45.00,
                "vat_rate": 20.0,
                "discount": 0,
            },
            {
                "description": "Béton fondation",
                "category": "maconnerie",
                "quantity": 50,
                "unit": "m3",
                "unit_price": 120.00,
                "vat_rate": 20.0,
                "discount": 0,
            },
        ],
    }
