"""Tests pour les endpoints clients."""

from decimal import Decimal


def test_create_client(client, sample_client_data):
    """Test de création d'un client."""
    response = client.post("/api/v1/clients", json=sample_client_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Entreprise Durand"
    assert data["email"] == "contact@durand-btp.fr"
    assert data["client_type"] == "entreprise"
    assert data["archived"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_client_invalid_email(client):
    """Test de création avec email invalide."""
    data = {
        "name": "Test",
        "email": "invalid-email",
        "client_type": "particulier",
    }
    response = client.post("/api/v1/clients", json=data)
    assert response.status_code == 422


def test_create_client_name_too_short(client):
    """Test de création avec nom trop court."""
    data = {
        "name": "A",
        "email": "test@example.com",
        "client_type": "particulier",
    }
    response = client.post("/api/v1/clients", json=data)
    assert response.status_code == 422


def test_create_client_invalid_siret(client):
    """Test de création avec SIRET invalide."""
    data = {
        "name": "Test Company",
        "email": "test@example.com",
        "siret": "12345",  # Pas 14 chiffres
        "client_type": "entreprise",
    }
    response = client.post("/api/v1/clients", json=data)
    assert response.status_code == 422


def test_create_client_duplicate_email(client, sample_client_data):
    """Test de création avec email dupliqué."""
    # Crée un premier client
    client.post("/api/v1/clients", json=sample_client_data)

    # Tente de créer avec le même email
    response = client.post("/api/v1/clients", json=sample_client_data)
    assert response.status_code == 400


def test_list_clients(client, sample_client_data):
    """Test de liste des clients."""
    # Crée quelques clients
    client.post("/api/v1/clients", json=sample_client_data)

    data2 = sample_client_data.copy()
    data2["email"] = "autre@example.com"
    data2["name"] = "Autre Entreprise"
    client.post("/api/v1/clients", json=data2)

    # Liste les clients
    response = client.get("/api/v1/clients")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "pagination" in data
    assert len(data["data"]) == 2
    assert data["pagination"]["total"] == 2


def test_list_clients_pagination(client, sample_client_data):
    """Test de pagination des clients."""
    # Crée 5 clients
    for i in range(5):
        data = sample_client_data.copy()
        data["email"] = f"test{i}@example.com"
        data["name"] = f"Client {i}"
        client.post("/api/v1/clients", json=data)

    # Teste la pagination
    response = client.get("/api/v1/clients?page=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["pagination"]["total"] == 5
    assert data["pagination"]["total_pages"] == 3


def test_get_client(client, sample_client_data):
    """Test de récupération d'un client."""
    # Crée un client
    create_response = client.post("/api/v1/clients", json=sample_client_data)
    client_id = create_response.json()["id"]

    # Récupère le client
    response = client.get(f"/api/v1/clients/{client_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == "Entreprise Durand"


def test_get_client_not_found(client):
    """Test de récupération d'un client inexistant."""
    response = client.get("/api/v1/clients/99999")
    assert response.status_code == 404


def test_update_client(client, sample_client_data):
    """Test de mise à jour d'un client."""
    # Crée un client
    create_response = client.post("/api/v1/clients", json=sample_client_data)
    client_id = create_response.json()["id"]

    # Met à jour le client
    update_data = {"name": "Entreprise Durand Modifiée", "phone": "+33 6 12 34 56 78"}
    response = client.patch(f"/api/v1/clients/{client_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Entreprise Durand Modifiée"
    assert data["phone"] == "+33 6 12 34 56 78"


def test_delete_client_soft(client, sample_client_data):
    """Test de suppression (soft delete) d'un client."""
    # Crée un client
    create_response = client.post("/api/v1/clients", json=sample_client_data)
    client_id = create_response.json()["id"]

    # Supprime le client
    response = client.delete(f"/api/v1/clients/{client_id}")
    assert response.status_code == 204

    # Vérifie qu'il n'apparaît plus dans la liste par défaut
    response = client.get("/api/v1/clients")
    assert len(response.json()["data"]) == 0

    # Mais apparaît avec include_archived
    response = client.get("/api/v1/clients?include_archived=true")
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["archived"] is True
