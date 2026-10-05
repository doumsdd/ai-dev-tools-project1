"""Service de génération de numéro de facture."""

from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.invoice import Invoice


def generate_invoice_number(db: Session, issue_date: date) -> str:
    """Génère un numéro de facture unique au format FA-AAAA-NNNN.

    Le compteur est réinitialisé chaque année.

    Args:
        db: Session de base de données
        issue_date: Date d'émission de la facture

    Returns:
        Numéro de facture unique (ex: "FA-2026-0001")
    """
    year = issue_date.year

    # Compte les factures existantes pour cette année
    count = (
        db.query(func.count(Invoice.id))
        .filter(func.extract("year", Invoice.issue_date) == year)
        .scalar()
    )

    # Incrémente le compteur
    next_number = count + 1

    # Formate le numéro
    return f"FA-{year}-{next_number:04d}"
