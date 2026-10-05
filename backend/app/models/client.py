"""Modèle Client."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Client(Base):
    """Modèle représentant un client."""

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    siret: Mapped[str | None] = mapped_column(String(14), nullable=True)

    # Enum stocké comme string avec contrainte CHECK
    client_type: Mapped[str] = mapped_column(String(20), nullable=False, default="particulier")

    archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relations
    invoices = relationship("Invoice", back_populates="client", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, name='{self.name}', email='{self.email}')>"
