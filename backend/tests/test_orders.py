from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_order_success():
    fake_order = {
        "order_id": 1,
        "status": "Pending",
        "order_date": "2026-11-19",
        "customer_name": "Test Customer",
    }

    with patch(
        "main.get_order_details",
        return_value=fake_order
    ):
        response = client.get("/orders/1")

    assert response.status_code == 200
    assert response.json() == fake_order
    
def test_get_order_not_found():
    with patch(
        "main.get_order_details",
        return_value=None
    ):
        response = client.get("/orders/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}
    
def test_get_delayed_orders_success():
    mock_orders = [
        {
            "order_id": 1,
            "customer_name": "Test Customer",
            "status": "Pending",
            "expected_delivery_date": "2026-11-14"
        }
    ]

    with patch("main.get_delayed_orders_list") as mock_service:
        mock_service.return_value = mock_orders

        response = client.get("/orders/delayed")

    assert response.status_code == 200
    assert response.json() == mock_orders
    
def test_get_delayed_orders_empty():
    with patch("main.get_delayed_orders_list") as mock_service:
        mock_service.return_value = []

        response = client.get("/orders/delayed")

    assert response.status_code == 200
    assert response.json() == []

def test_get_delayed_orders_server_error():
    with patch("main.get_delayed_orders_list") as mock_service:
        mock_service.side_effect = Exception("Database unavailable")

        response = client.get("/orders/delayed")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Failed to retrieve delayed orders"
    }
    
def test_get_delayed_orders_pagination():
    with patch("main.get_delayed_orders_list") as mock_service:
        mock_service.return_value = []

        response = client.get(
            "/orders/delayed?limit=5&offset=10"
        )

    assert response.status_code == 200
    assert response.json() == []

    mock_service.assert_called_once_with(
        limit=5,
        offset=10
    )
    
def test_get_delayed_orders_invalid_limit():
    with patch("main.get_delayed_orders_list") as mock_service:
        response = client.get("/orders/delayed?limit=101")

    assert response.status_code == 422
    mock_service.assert_not_called()