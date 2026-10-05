"""Schémas communs (erreurs, pagination)."""

from pydantic import BaseModel


class Error(BaseModel):
    """Schéma d'erreur standard."""

    error: str
    message: str


class ValidationDetail(BaseModel):
    """Détail d'une erreur de validation."""

    field: str
    message: str


class ValidationError(BaseModel):
    """Schéma d'erreur de validation."""

    error: str = "validation_error"
    message: str
    details: list[ValidationDetail]


class Pagination(BaseModel):
    """Schéma de pagination."""

    page: int
    limit: int
    total: int
    total_pages: int
