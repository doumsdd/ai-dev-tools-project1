"""Tests pour les endpoints factures."""

from decimal import Decimal


def _create_client(client, sample_client_data):
    """Helper pour créer un client et retourner son ID."""
    response = client.post("/api/v1/clients", json=sample_client_data)
    assert response.status_code == 201
    return response.json()["id"]


def test_create_invoice(client, sample_client_data, sample_invoice_data):
    """Test de création d'une facture avec calcul automatique des totaux."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    response = client.post("/api/v1/invoices", json=sample_invoice_data)
    assert response.status_code == 201
    data = response.json()

    # Vérifie le numéro de facture
    assert data["invoice_number"].startswith("FA-")

    # Vérifie le statut initial
    assert data["status"] == "brouillon"

    # Vérifie les calculs automatiques
    # Ligne 1: 100 × 45 = 4500 HT
    # Ligne 2: 50 × 120 = 6000 HT
    # Subtotal HT = 10500
    # TVA (20%) = 2100
    # Total TTC = 12600
    assert Decimal(str(data["subtotal_ht"])) == Decimal("10500.00")
    assert Decimal(str(data["total_vat"])) == Decimal("2100.00")
    assert Decimal(str(data["total_ttc"])) == Decimal("12600.00")

    # Vérifie les lignes
    assert len(data["lines"]) == 2
    assert data["lines"][0]["description"] == "Terrassement terrain"
    assert Decimal(str(data["lines"][0]["total_ht"])) == Decimal("4500.00")


def test_create_invoice_with_discount(client, sample_client_data):
    """Test de création avec remise."""
    client_id = _create_client(client, sample_client_data)

    invoice_data = {
        "client_id": client_id,
        "issue_date": "2026-01-15",
        "lines": [
            {
                "description": "Prestation avec remise",
                "category": "maconnerie",
                "quantity": 10,
                "unit": "m2",
                "unit_price": 100.00,
                "vat_rate": 20.0,
                "discount": 10,
            },
        ],
    }

    response = client.post("/api/v1/invoices", json=invoice_data)
    assert response.status_code == 201
    data = response.json()

    # 10 × 100 × (1 - 10/100) = 900 HT
    # TVA 20% = 180
    # TTC = 1080
    assert Decimal(str(data["subtotal_ht"])) == Decimal("900.00")
    assert Decimal(str(data["total_vat"])) == Decimal("180.00")
    assert Decimal(str(data["total_ttc"])) == Decimal("1080.00")


def test_create_invoice_no_lines(client, sample_client_data):
    """Test de création sans lignes (doit échouer)."""
    client_id = _create_client(client, sample_client_data)

    invoice_data = {
        "client_id": client_id,
        "issue_date": "2026-01-15",
        "lines": [],
    }

    response = client.post("/api/v1/invoices", json=invoice_data)
    assert response.status_code == 422


def test_create_invoice_invalid_vat_rate(client, sample_client_data):
    """Test de création avec taux de TVA invalide."""
    client_id = _create_client(client, sample_client_data)

    invoice_data = {
        "client_id": client_id,
        "issue_date": "2026-01-15",
        "lines": [
            {
                "description": "Test",
                "category": "maconnerie",
                "quantity": 10,
                "unit": "m2",
                "unit_price": 100.00,
                "vat_rate": 15.0,
                "discount": 0,
            },
        ],
    }

    response = client.post("/api/v1/invoices", json=invoice_data)
    assert response.status_code == 422


def test_create_invoice_client_not_found(client):
    """Test de création avec client inexistant."""
    invoice_data = {
        "client_id": 99999,
        "issue_date": "2026-01-15",
        "lines": [
            {
                "description": "Test",
                "category": "maconnerie",
                "quantity": 10,
                "unit": "m2",
                "unit_price": 100.00,
                "vat_rate": 20.0,
                "discount": 0,
            },
        ],
    }

    response = client.post("/api/v1/invoices", json=invoice_data)
    assert response.status_code == 404


def test_create_invoice_mixed_vat_rates(client, sample_client_data):
    """Test de création avec différents taux de TVA."""
    client_id = _create_client(client, sample_client_data)

    invoice_data = {
        "client_id": client_id,
        "issue_date": "2026-01-15",
        "lines": [
            {
                "description": "Construction neuve",
                "category": "maconnerie",
                "quantity": 10,
                "unit": "m2",
                "unit_price": 100.00,
                "vat_rate": 20.0,
                "discount": 0,
            },
            {
                "description": "Rénovation simple",
                "category": "plomberie",
                "quantity": 5,
                "unit": "heure",
                "unit_price": 80.00,
                "vat_rate": 10.0,
                "discount": 0,
            },
            {
                "description": "Isolation énergétique",
                "category": "autre",
                "quantity": 20,
                "unit": "m2",
                "unit_price": 50.00,
                "vat_rate": 5.5,
                "discount": 0,
            },
        ],
    }

    response = client.post("/api/v1/invoices", json=invoice_data)
    assert response.status_code == 201
    data = response.json()

    # Ligne 1: 1000 HT, TVA 20% = 200
    # Ligne 2: 400 HT, TVA 10% = 40
    # Ligne 3: 1000 HT, TVA 5.5% = 55
    # Subtotal = 2400, TVA = 295, TTC = 2695
    assert Decimal(str(data["subtotal_ht"])) == Decimal("2400.00")
    assert Decimal(str(data["total_vat"])) == Decimal("295.00")
    assert Decimal(str(data["total_ttc"])) == Decimal("2695.00")


def test_list_invoices(client, sample_client_data, sample_invoice_data):
    """Test de liste des factures."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    # Crée 3 factures
    for i in range(3):
        data = sample_invoice_data.copy()
        data["issue_date"] = f"2026-01-{15 + i}"
        client.post("/api/v1/invoices", json=data)

    # Liste les factures
    response = client.get("/api/v1/invoices")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 3
    assert data["pagination"]["total"] == 3


def test_get_invoice(client, sample_client_data, sample_invoice_data):
    """Test de récupération d'une facture."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    # Crée une facture
    create_response = client.post("/api/v1/invoices", json=sample_invoice_data)
    invoice_id = create_response.json()["id"]

    # Récupère la facture
    response = client.get(f"/api/v1/invoices/{invoice_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == invoice_id
    assert len(data["lines"]) == 2


def test_invoice_status_transitions(client, sample_client_data, sample_invoice_data):
    """Test des transitions de statut."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    # Crée une facture (brouillon)
    create_response = client.post("/api/v1/invoices", json=sample_invoice_data)
    invoice_id = create_response.json()["id"]
    assert create_response.json()["status"] == "brouillon"

    # brouillon → envoyee
    response = client.patch(
        f"/api/v1/invoices/{invoice_id}/status",
        json={"status": "envoyee"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "envoyee"

    # envoyee → payee
    response = client.patch(
        f"/api/v1/invoices/{invoice_id}/status",
        json={"status": "payee"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "payee"
    assert response.json()["paid_at"] is not None


def test_invoice_invalid_transition(client, sample_client_data, sample_invoice_data):
    """Test de transition invalide."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    # Crée une facture
    create_response = client.post("/api/v1/invoices", json=sample_invoice_data)
    invoice_id = create_response.json()["id"]

    # Tente brouillon → payee (invalide, doit passer par envoyee)
    response = client.patch(
        f"/api/v1/invoices/{invoice_id}/status",
        json={"status": "payee"},
    )
    assert response.status_code == 400


def test_invoice_paid_is_readonly(client, sample_client_data, sample_invoice_data):
    """Test qu'une facture payée ne peut plus changer de statut."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    # Crée et paie une facture
    create_response = client.post("/api/v1/invoices", json=sample_invoice_data)
    invoice_id = create_response.json()["id"]

    client.patch(
        f"/api/v1/invoices/{invoice_id}/status",
        json={"status": "envoyee"},
    )
    client.patch(
        f"/api/v1/invoices/{invoice_id}/status",
        json={"status": "payee"},
    )

    # Tente de changer le statut (doit échouer)
    response = client.patch(
        f"/api/v1/invoices/{invoice_id}/status",
        json={"status": "brouillon"},
    )
    assert response.status_code == 400


def test_invoice_numbering_sequence(client, sample_client_data, sample_invoice_data):
    """Test de la numérotation séquentielle des factures."""
    client_id = _create_client(client, sample_client_data)
    sample_invoice_data["client_id"] = client_id

    # Crée 3 factures
    numbers = []
    for i in range(3):
        data = sample_invoice_data.copy()
        data["issue_date"] = f"2026-01-{15 + i}"
        response = client.post("/api/v1/invoices", json=data)
        numbers.append(response.json()["invoice_number"])

    # Vérifie la séquence
    assert numbers[0] == "FA-2026-0001"
    assert numbers[1] == "FA-2026-0002"
    assert numbers[2] == "FA-2026-0003"

