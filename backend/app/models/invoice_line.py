"""Modèle InvoiceLine."""

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class InvoiceLine(Base):
    """Modèle représentant une ligne de facture."""

    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False
    )

    description: Mapped[str] = mapped_column(String(500), nullable=False)

    # Enum stocké comme string
    category: Mapped[str] = mapped_column(String(20), nullable=False)

    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0"), nullable=False)

    # Total calculé
    total_ht: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relations
    invoice = relationship("Invoice", back_populates="lines")

    def __repr__(self) -> str:
        return f"<InvoiceLine(id={self.id}, description='{self.description[:30]}')>"
