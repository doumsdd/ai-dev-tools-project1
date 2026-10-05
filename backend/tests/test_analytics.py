"""Tests pour les endpoints analytics."""

from datetime import datetime, timedelta
from decimal import Decimal


def _create_client_and_invoice(client, sample_client_data, issue_date, status="brouillon"):
    """Helper pour créer un client et une facture."""
    # Crée le client
    response = client.post("/api/v1/clients", json=sample_client_data)
    client_id = response.json()["id"]

    # Crée la facture
    invoice_data = {
        "client_id": client_id,
        "issue_date": issue_date,
        "lines": [
            {
                "description": "Prestation test",
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
    invoice_id = response.json()["id"]

    # Transitionne vers le statut désiré
    if status == "envoyee":
        client.patch(
            f"/api/v1/invoices/{invoice_id}/status",
            json={"status": "envoyee"},
        )
    elif status == "payee":
        client.patch(
            f"/api/v1/invoices/{invoice_id}/status",
            json={"status": "envoyee"},
        )
        client.patch(
            f"/api/v1/invoices/{invoice_id}/status",
            json={"status": "payee"},
        )
    elif status == "annulee":
        client.patch(
            f"/api/v1/invoices/{invoice_id}/status",
            json={"status": "annulee"},
        )

    return invoice_id


def test_analytics_revenue_empty(client):
    """Test analytics avec aucune facture."""
    response = client.get("/api/v1/analytics/revenue?year=2026")
    assert response.status_code == 200
    data = response.json()

    assert data["year"] == 2026
    assert data["total_revenue_ht"] == "0.00"
    assert data["total_revenue_ttc"] == "0.00"
    assert data["paid_invoices_count"] == 0
    assert len(data["monthly_breakdown"]) == 12
    assert len(data["top_clients"]) == 0


def test_analytics_revenue_with_paid_invoices(client, sample_client_data):
    """Test analytics avec factures payées."""
    # Crée 3 factures payées
    for i in range(3):
        data = sample_client_data.copy()
        data["email"] = f"client{i}@example.com"
        _create_client_and_invoice(client, data, "2026-01-15", status="payee")

    response = client.get("/api/v1/analytics/revenue?year=2026")
    assert response.status_code == 200
    data = response.json()

    # 3 factures × 1000 HT = 3000 HT
    # TVA = 600
    # TTC = 3600
    assert Decimal(data["total_revenue_ht"]) == Decimal("3000.00")
    assert Decimal(data["total_revenue_ttc"]) == Decimal("3600.00")
    assert data["paid_invoices_count"] == 3

    # Les factures sont payées aujourd'hui (mois courant), pas en janvier
    # Donc on vérifie que le total est correct, pas la ventilation mensuelle
    total_from_monthly = sum(Decimal(m["revenue_ttc"]) for m in data["monthly_breakdown"])
    assert total_from_monthly == Decimal("3600.00")

    # Au moins un mois a des factures
    months_with_invoices = [m for m in data["monthly_breakdown"] if m["invoices_count"] > 0]
    assert len(months_with_invoices) > 0


def test_analytics_revenue_only_paid_invoices(client, sample_client_data):
    """Test que seules les factures payées sont comptées."""
    # Crée des factures avec différents statuts
    data1 = sample_client_data.copy()
    data1["email"] = "client1@example.com"
    _create_client_and_invoice(client, data1, "2026-01-15", status="payee")

    data2 = sample_client_data.copy()
    data2["email"] = "client2@example.com"
    _create_client_and_invoice(client, data2, "2026-01-15", status="envoyee")

    data3 = sample_client_data.copy()
    data3["email"] = "client3@example.com"
    _create_client_and_invoice(client, data3, "2026-01-15", status="brouillon")

    data4 = sample_client_data.copy()
    data4["email"] = "client4@example.com"
    _create_client_and_invoice(client, data4, "2026-01-15", status="annulee")

    response = client.get("/api/v1/analytics/revenue?year=2026")
    assert response.status_code == 200
    data = response.json()

    # Seule 1 facture payée
    assert data["paid_invoices_count"] == 1
    assert Decimal(data["total_revenue_ttc"]) == Decimal("1200.00")

    # Les autres statuts sont comptés séparément
    assert data["pending_invoices_count"] == 2  # brouillon + envoyee
    assert data["cancelled_invoices_count"] == 1


def test_analytics_revenue_top_clients(client, sample_client_data):
    """Test du top clients."""
    # Crée plusieurs factures pour différents clients
    for i in range(5):
        data = sample_client_data.copy()
        data["email"] = f"client{i}@example.com"
        data["name"] = f"Client {i}"
        _create_client_and_invoice(client, data, "2026-01-15", status="payee")

    response = client.get("/api/v1/analytics/revenue?year=2026")
    assert response.status_code == 200
    data = response.json()

    # Vérifie le top clients
    assert len(data["top_clients"]) == 5
    # Tous ont le même CA (1200 TTC)
    for tc in data["top_clients"]:
        assert Decimal(tc["total_revenue_ttc"]) == Decimal("1200.00")
        assert tc["invoices_count"] == 1


def test_analytics_revenue_average(client, sample_client_data):
    """Test du calcul de la moyenne."""
    # Crée 4 factures payées
    for i in range(4):
        data = sample_client_data.copy()
        data["email"] = f"client{i}@example.com"
        _create_client_and_invoice(client, data, "2026-01-15", status="payee")

    response = client.get("/api/v1/analytics/revenue?year=2026")
    assert response.status_code == 200
    data = response.json()

    # 4 factures × 1200 TTC = 4800 TTC
    # Moyenne = 4800 / 4 = 1200
    assert Decimal(data["average_invoice_amount"]) == Decimal("1200.00")
