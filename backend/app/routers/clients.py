"""Router pour les clients."""

import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.client import Client
from app.schemas.client import Client as ClientResponse
from app.schemas.client import ClientCreate, ClientListResponse, ClientUpdate
from app.schemas.common import Error, Pagination, ValidationError, ValidationDetail

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post(
    "",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ValidationError, "description": "Données invalides"},
    },
)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
):
    """Crée un nouveau client."""
    # Vérifie si l'email existe déjà
    existing = db.query(Client).filter(Client.email == client_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[
                ValidationDetail(
                    field="email",
                    message="Un client avec cet email existe déjà",
                ).model_dump()
            ],
        )

    # Crée le client
    client = Client(**client_data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.get(
    "",
    response_model=ClientListResponse,
    status_code=status.HTTP_200_OK,
)
def list_clients(
    page: int = Query(1, ge=1, description="Numéro de page"),
    limit: int = Query(20, ge=1, le=100, description="Éléments par page"),
    search: str | None = Query(None, description="Recherche par nom ou email"),
    include_archived: bool = Query(False, description="Inclure les clients archivés"),
    db: Session = Depends(get_db),
):
    """Liste les clients avec pagination et filtres."""
    query = db.query(Client)

    # Filtre par statut archivé
    if not include_archived:
        query = query.filter(Client.archived == False)  # noqa: E712

    # Recherche par nom ou email
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Client.name.ilike(search_term)) | (Client.email.ilike(search_term))
        )

    # Compte le total
    total = query.count()
    total_pages = math.ceil(total / limit) if total > 0 else 1

    # Pagination
    offset = (page - 1) * limit
    clients = query.order_by(Client.created_at.desc()).offset(offset).limit(limit).all()

    return ClientListResponse(
        data=[ClientResponse.model_validate(c) for c in clients],
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": Error, "description": "Client non trouvé"},
    },
)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    """Récupère un client par son ID."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Client non trouvé"},
        )
    return client


@router.patch(
    "/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": Error, "description": "Client non trouvé"},
        400: {"model": ValidationError, "description": "Données invalides"},
    },
)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
):
    """Met à jour un client."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Client non trouvé"},
        )

    # Met à jour les champs
    update_data = client_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)

    return client


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": Error, "description": "Client non trouvé"},
    },
)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    """Archive un client (soft delete)."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": "Client non trouvé"},
        )

    client.archived = True
    db.commit()

    return None
