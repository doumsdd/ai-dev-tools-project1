"""Schémas Pydantic pour les analytics."""

from decimal import Decimal

from pydantic import BaseModel, Field


class MonthlyRevenue(BaseModel):
    """Revenu mensuel."""

    month: int = Field(..., ge=1, le=12)
    month_name: str
    revenue_ht: Decimal
    revenue_ttc: Decimal
    invoices_count: int


class TopClient(BaseModel):
    """Top client par revenu."""

    client_id: int
    client_name: str
    total_revenue_ttc: Decimal
    invoices_count: int


class AnalyticsRevenue(BaseModel):
    """Réponse complète pour l'endpoint analytics/revenue."""

    year: int
    total_revenue_ht: Decimal
    total_revenue_ttc: Decimal
    total_vat_collected: Decimal
    paid_invoices_count: int
    pending_invoices_count: int
    cancelled_invoices_count: int
    average_invoice_amount: Decimal
    monthly_breakdown: list[MonthlyRevenue]
    top_clients: list[TopClient]
