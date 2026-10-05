"""Router pour les analytics."""

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.client import Client
from app.models.invoice import Invoice
from app.schemas.analytics import AnalyticsRevenue, MonthlyRevenue, TopClient

router = APIRouter(prefix="/analytics", tags=["analytics"])

MONTH_NAMES = [
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]


@router.get(
    "/revenue",
    response_model=AnalyticsRevenue,
    status_code=status.HTTP_200_OK,
)
def get_revenue_analytics(
    year: int = Query(None, description="Année à analyser (défaut: année courante)"),
    db: Session = Depends(get_db),
):
    """Agrège le revenu total par mois à partir des factures payées."""
    if year is None:
        year = datetime.now().year

    # Factures payées pour l'année
    paid_invoices = (
        db.query(Invoice)
        .filter(
            Invoice.status == "payee",
            func.extract("year", Invoice.paid_at) == year,
        )
        .all()
    )

    # Totaux globaux
    total_revenue_ht = sum(inv.subtotal_ht for inv in paid_invoices) or Decimal("0")
    total_revenue_ttc = sum(inv.total_ttc for inv in paid_invoices) or Decimal("0")
    total_vat_collected = sum(inv.total_vat for inv in paid_invoices) or Decimal("0")
    paid_count = len(paid_invoices)

    # Factures en attente (brouillon, envoyee, en_retard)
    pending_count = (
        db.query(Invoice)
        .filter(Invoice.status.in_(["brouillon", "envoyee", "en_retard"]))
        .count()
    )

    # Factures annulées
    cancelled_count = (
        db.query(Invoice).filter(Invoice.status == "annulee").count()
    )

    # Moyenne
    average_invoice_amount = (
        (total_revenue_ttc / paid_count).quantize(Decimal("0.01"))
        if paid_count > 0
        else Decimal("0")
    )

    # Ventilation mensuelle
    monthly_map: dict[int, dict] = {m: {"ht": Decimal("0"), "ttc": Decimal("0"), "count": 0} for m in range(1, 13)}
    for inv in paid_invoices:
        month = inv.paid_at.month
        monthly_map[month]["ht"] += inv.subtotal_ht
        monthly_map[month]["ttc"] += inv.total_ttc
        monthly_map[month]["count"] += 1

    monthly_breakdown = [
        MonthlyRevenue(
            month=m,
            month_name=MONTH_NAMES[m - 1],
            revenue_ht=monthly_map[m]["ht"].quantize(Decimal("0.01")),
            revenue_ttc=monthly_map[m]["ttc"].quantize(Decimal("0.01")),
            invoices_count=monthly_map[m]["count"],
        )
        for m in range(1, 13)
    ]

    # Top 5 clients par CA payé
    client_revenue: dict[int, dict] = {}
    for inv in paid_invoices:
        cid = inv.client_id
        if cid not in client_revenue:
            client_revenue[cid] = {"ttc": Decimal("0"), "count": 0}
        client_revenue[cid]["ttc"] += inv.total_ttc
        client_revenue[cid]["count"] += 1

    top_clients_data = sorted(
        client_revenue.items(), key=lambda x: x[1]["ttc"], reverse=True
    )[:5]

    top_clients = []
    for cid, data in top_clients_data:
        client = db.query(Client).filter(Client.id == cid).first()
        top_clients.append(
            TopClient(
                client_id=cid,
                client_name=client.name if client else "Inconnu",
                total_revenue_ttc=data["ttc"].quantize(Decimal("0.01")),
                invoices_count=data["count"],
            )
        )

    return AnalyticsRevenue(
        year=year,
        total_revenue_ht=total_revenue_ht.quantize(Decimal("0.01")),
        total_revenue_ttc=total_revenue_ttc.quantize(Decimal("0.01")),
        total_vat_collected=total_vat_collected.quantize(Decimal("0.01")),
        paid_invoices_count=paid_count,
        pending_invoices_count=pending_count,
        cancelled_invoices_count=cancelled_count,
        average_invoice_amount=average_invoice_amount,
        monthly_breakdown=monthly_breakdown,
        top_clients=top_clients,
    )
