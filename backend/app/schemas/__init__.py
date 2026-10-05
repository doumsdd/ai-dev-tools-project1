"""Schémas Pydantic."""

from app.schemas.analytics import (
    AnalyticsRevenue,
    MonthlyRevenue,
    TopClient,
)
from app.schemas.client import (
    Client,
    ClientCreate,
    ClientListResponse,
    ClientUpdate,
)
from app.schemas.common import (
    Error,
    Pagination,
    ValidationDetail,
    ValidationError,
)
from app.schemas.invoice import (
    Invoice,
    InvoiceCreate,
    InvoiceLineCreate,
    InvoiceLineResponse,
    InvoiceListResponse,
    InvoiceSummary,
    StatusTransition,
)

__all__ = [
    "Client",
    "ClientCreate",
    "ClientUpdate",
    "ClientListResponse",
    "Invoice",
    "InvoiceCreate",
    "InvoiceLineCreate",
    "InvoiceLineResponse",
    "InvoiceSummary",
    "InvoiceListResponse",
    "StatusTransition",
    "AnalyticsRevenue",
    "MonthlyRevenue",
    "TopClient",
    "Error",
    "ValidationError",
    "ValidationDetail",
    "Pagination",
]
