from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_inventory_shortages_returns_data():
    # Udajemy pojedynczy rekord z SQL Servera
    fake_row = MagicMock()
    fake_row.SKU = "SRUBA-M8"
    fake_row.ProductName = "Śruba M8"
    fake_row.TotalDemand = 700
    fake_row.QuantityOnHand = 500
    fake_row.Shortage = 200

    # Udajemy kursor SQL Servera
    fake_cursor = MagicMock()
    fake_cursor.fetchall.return_value = [fake_row]

    # Udajemy połączenie z bazą
    fake_connection = MagicMock()
    fake_connection.cursor.return_value = fake_cursor
    fake_connection.__enter__.return_value = fake_connection

    # Podmieniamy get_connection w module main
    with patch("main.get_connection", return_value=fake_connection):
        response = client.get("/inventory/shortages")

    assert response.status_code == 200
    assert response.json() == [
        {
            "sku": "SRUBA-M8",
            "product_name": "Śruba M8",
            "total_demand": 700,
            "quantity_on_hand": 500,
            "shortage": 200,
        }
    ]

    fake_cursor.execute.assert_called_once()
    
def test_inventory_database_error():
    with patch(
        "main.get_connection",
        side_effect=Exception("Database unavailable")
    ):
        response = client.get("/inventory/shortages")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Database query failed"
    }