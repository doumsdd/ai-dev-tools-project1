"""Service de calcul des totaux de facture."""

from decimal import Decimal

from app.schemas.invoice import InvoiceLineCreate


def calculate_line_total_ht(line: InvoiceLineCreate) -> Decimal:
    """Calcule le total HT d'une ligne de facture.

    Formule: quantity × unit_price × (1 - discount/100)
    """
    subtotal = line.quantity * line.unit_price
    if line.discount > 0:
        subtotal = subtotal * (1 - line.discount / 100)
    return subtotal.quantize(Decimal("0.01"))


def calculate_line_vat(line: InvoiceLineCreate, line_total_ht: Decimal) -> Decimal:
    """Calcule la TVA d'une ligne de facture."""
    vat = line_total_ht * line.vat_rate / 100
    return vat.quantize(Decimal("0.01"))


def calculate_invoice_totals(
    lines: list[InvoiceLineCreate],
) -> tuple[Decimal, Decimal, Decimal]:
    """Calcule les totaux d'une facture à partir de ses lignes.

    Returns:
        Tuple (subtotal_ht, total_vat, total_ttc)
    """
    subtotal_ht = Decimal("0")
    total_vat = Decimal("0")

    for line in lines:
        line_ht = calculate_line_total_ht(line)
        line_vat = calculate_line_vat(line, line_ht)
        subtotal_ht += line_ht
        total_vat += line_vat

    total_ttc = subtotal_ht + total_vat

    return (
        subtotal_ht.quantize(Decimal("0.01")),
        total_vat.quantize(Decimal("0.01")),
        total_ttc.quantize(Decimal("0.01")),
    )
