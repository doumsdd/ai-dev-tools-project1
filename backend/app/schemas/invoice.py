"""Schémas Pydantic pour les factures."""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import Pagination

InvoiceStatus = Literal["brouillon", "envoyee", "payee", "annulee", "en_retard"]
LineCategory = Literal[
    "maconnerie", "plomberie", "electricite", "peinture", "terrassement", "couverture", "autre"
]
LineUnit = Literal["m2", "m3", "heure", "jour", "forfait", "unite"]
ValidVatRate = Literal[5.5, 10.0, 20.0]


class InvoiceLineCreate(BaseModel):
    """Schéma pour créer une ligne de facture."""

    description: str = Field(..., min_length=1, max_length=500)
    category: LineCategory
    quantity: Decimal = Field(..., gt=0, decimal_places=2)
    unit: LineUnit
    unit_price: Decimal = Field(..., gt=0, decimal_places=2)
    vat_rate: Decimal = Field(..., description="Taux de TVA: 5.5, 10, ou 20")
    discount: Decimal = Field(Decimal("0"), ge=0, le=100, decimal_places=2)

    @field_validator("vat_rate")
    @classmethod
    def validate_vat_rate(cls, v: Decimal) -> Decimal:
        allowed = {Decimal("5.5"), Decimal("10"), Decimal("10.0"), Decimal("20"), Decimal("20.0")}
        if v not in allowed:
            raise ValueError("Le taux de TVA doit être 5.5, 10, ou 20")
        return v


class InvoiceLineResponse(BaseModel):
    """Schéma de réponse pour une ligne de facture."""

    id: int
    description: str
    category: str
    quantity: Decimal
    unit: str
    unit_price: Decimal
    vat_rate: Decimal
    discount: Decimal
    total_ht: Decimal

    model_config = {"from_attributes": True}


class InvoiceCreate(BaseModel):
    """Schéma pour créer une facture."""

    client_id: int = Field(..., gt=0, description="ID du client")
    issue_date: date = Field(..., description="Date d'émission")
    due_date: date | None = Field(None, description="Date d'échéance")
    lines: list[InvoiceLineCreate] = Field(..., min_length=1, description="Lignes de facture")
    notes: str | None = None

    @field_validator("lines")
    @classmethod
    def validate_lines_not_empty(cls, v: list[InvoiceLineCreate]) -> list[InvoiceLineCreate]:
        if not v:
            raise ValueError("Au moins une ligne de facture est requise")
        return v


class Invoice(BaseModel):
    """Schéma de réponse complète pour une facture."""

    id: int
    invoice_number: str
    client_id: int
    status: str
    issue_date: date
    due_date: date | None = None
    paid_at: datetime | None = None
    subtotal_ht: Decimal
    total_vat: Decimal
    total_ttc: Decimal
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    lines: list[InvoiceLineResponse] = []

    model_config = {"from_attributes": True}


class InvoiceSummary(BaseModel):
    """Schéma de réponse résumé pour une facture (liste)."""

    id: int
    invoice_number: str
    client_id: int
    client_name: str | None = None
    status: str
    issue_date: date
    due_date: date | None = None
    total_ttc: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class InvoiceListResponse(BaseModel):
    """Schéma de réponse pour la liste des factures."""

    data: list[InvoiceSummary]
    pagination: Pagination


class StatusTransition(BaseModel):
    """Schéma pour la transition de statut."""

    status: InvoiceStatus = Field(..., description="Nouveau statut")
