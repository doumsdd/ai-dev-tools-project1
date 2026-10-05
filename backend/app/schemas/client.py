"""Schémas Pydantic pour les clients."""

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.common import Pagination

ClientType = Literal["particulier", "entreprise", "maitre_ouvrage"]


class ClientCreate(BaseModel):
    """Schéma pour créer un client."""

    name: str = Field(..., min_length=2, max_length=255, description="Nom du client")
    email: EmailStr = Field(..., description="Email unique du client")
    phone: str | None = Field(None, max_length=50, description="Téléphone")
    address: str | None = Field(None, max_length=500, description="Adresse")
    siret: str | None = Field(None, description="SIRET (14 chiffres)")
    client_type: ClientType = Field(..., description="Type de client")

    @field_validator("siret")
    @classmethod
    def validate_siret(cls, v: str | None) -> str | None:
        if v is not None and v != "":
            if not re.match(r"^\d{14}$", v):
                raise ValueError("Le SIRET doit contenir exactement 14 chiffres")
        return v if v != "" else None


class ClientUpdate(BaseModel):
    """Schéma pour mettre à jour un client."""

    name: str | None = Field(None, min_length=2, max_length=255)
    phone: str | None = Field(None, max_length=50)
    address: str | None = Field(None, max_length=500)
    siret: str | None = Field(None)
    client_type: ClientType | None = None

    @field_validator("siret")
    @classmethod
    def validate_siret(cls, v: str | None) -> str | None:
        if v is not None and v != "":
            if not re.match(r"^\d{14}$", v):
                raise ValueError("Le SIRET doit contenir exactement 14 chiffres")
        return v if v != "" else None


class Client(BaseModel):
    """Schéma de réponse pour un client."""

    id: int
    name: str
    email: str
    phone: str | None = None
    address: str | None = None
    siret: str | None = None
    client_type: str
    archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ClientListResponse(BaseModel):
    """Schéma de réponse pour la liste des clients."""

    data: list[Client]
    pagination: Pagination
