"""Router pour les factures."""

import math
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.client import Client
from app.models.invoice import Invoice
from app.models.invoice_line import InvoiceLine
from app.schemas.common import Error, Pagination
from app.schemas.invoice import (
    Invoice as InvoiceResponse,
)
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceListResponse,
    InvoiceSummary,
    StatusTransition,
)
from app.services.invoice_calculator import (
    calculate_invoice_totals,
    calculate_line_total_ht,
)
from app.services.invoice_number import generate_invoice_number
from app.services.status_machine import get_allowed_transitions, validate_transition

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post(
    "",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": Error, "description": "Données invalides"},
        404: {"model": Error, "description": "Client non trouvé"},
    },
)
def create_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
):
    """Crée une nouvelle facture avec calcul automatique des totaux."""
    # Vérifie que le client existe
    client = db.query(Client).filter(Client.id == invoice_data.client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Client non trouvé"},
        )

    # Vérifie que issue_date <= today
    today = datetime.now().date()
    if invoice_data.issue_date > today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "validation_error",
                "message": "La date d'émission ne peut pas être dans le futur",
            },
        )

    # Vérifie que due_date >= issue_date
    if invoice_data.due_date and invoice_data.due_date < invoice_data.issue_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "validation_error",
                "message": "La date d'échéance doit être >= à la date d'émission",
            },
        )

    # Génère le numéro de facture
    invoice_number = generate_invoice_number(db, invoice_data.issue_date)

    # Calcule les totaux
    subtotal_ht, total_vat, total_ttc = calculate_invoice_totals(invoice_data.lines)

    # Crée la facture
    invoice = Invoice(
        invoice_number=invoice_number,
        client_id=invoice_data.client_id,
        status="brouillon",
        issue_date=invoice_data.issue_date,
        due_date=invoice_data.due_date,
        subtotal_ht=subtotal_ht,
        total_vat=total_vat,
        total_ttc=total_ttc,
        notes=invoice_data.notes,
    )
    db.add(invoice)
    db.flush()  # Pour obtenir l'ID de la facture

    # Crée les lignes de facture
    for line_data in invoice_data.lines:
        line_total_ht = calculate_line_total_ht(line_data)
        line = InvoiceLine(
            invoice_id=invoice.id,
            description=line_data.description,
            category=line_data.category,
            quantity=line_data.quantity,
            unit=line_data.unit,
            unit_price=line_data.unit_price,
            vat_rate=line_data.vat_rate,
            discount=line_data.discount,
            total_ht=line_total_ht,
        )
        db.add(line)

    db.commit()
    db.refresh(invoice)

    return invoice


@router.get(
    "",
    response_model=InvoiceListResponse,
    status_code=status.HTTP_200_OK,
)
def list_invoices(
    page: int = Query(1, ge=1, description="Numéro de page"),
    limit: int = Query(20, ge=1, le=100, description="Éléments par page"),
    status_filter: str | None = Query(None, alias="status", description="Filtrer par statut"),
    client_id: int | None = Query(None, description="Filtrer par client"),
    db: Session = Depends(get_db),
):
    """Liste les factures avec pagination et filtres."""
    query = db.query(Invoice)

    # Filtres
    if status_filter:
        query = query.filter(Invoice.status == status_filter)
    if client_id:
        query = query.filter(Invoice.client_id == client_id)

    # Compte le total
    total = query.count()
    total_pages = math.ceil(total / limit) if total > 0 else 1

    # Pagination
    offset = (page - 1) * limit
    invoices = query.order_by(Invoice.created_at.desc()).offset(offset).limit(limit).all()

    # Construit la réponse avec le nom du client
    data = []
    for inv in invoices:
        summary = InvoiceSummary(
            id=inv.id,
            invoice_number=inv.invoice_number,
            client_id=inv.client_id,
            client_name=inv.client.name if inv.client else None,
            status=inv.status,
            issue_date=inv.issue_date,
            due_date=inv.due_date,
            total_ttc=inv.total_ttc,
            created_at=inv.created_at,
        )
        data.append(summary)

    return InvoiceListResponse(
        data=data,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": Error, "description": "Facture non trouvée"},
    },
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
):
    """Récupère une facture par son ID."""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Facture non trouvée"},
        )
    return invoice


@router.patch(
    "/{invoice_id}/status",
    response_model=InvoiceResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": Error, "description": "Transition invalide"},
        404: {"model": Error, "description": "Facture non trouvée"},
    },
)
def transition_invoice_status(
    invoice_id: int,
    transition: StatusTransition,
    db: Session = Depends(get_db),
):
    """Change le statut d'une facture selon les règles de transition."""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Facture non trouvée"},
        )

    # Valide la transition
    if not validate_transition(invoice.status, transition.status):
        allowed = get_allowed_transitions(invoice.status)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_transition",
                "message": (
                    f"Transition de '{invoice.status}' vers '{transition.status}' "
                    f"non autorisée. Transitions permises: "
                    f"{', '.join(allowed) if allowed else 'aucune'}"
                ),
            },
        )

    # Applique la transition
    invoice.status = transition.status

    # Si payée, enregistre la date de paiement
    if transition.status == "payee":
        invoice.paid_at = datetime.now()

    db.commit()
    db.refresh(invoice)

    return invoice

