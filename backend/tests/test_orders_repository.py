from unittest.mock import MagicMock, patch
from datetime import datetime
from types import SimpleNamespace

from orders_repository import get_order_by_id


def test_get_order_by_id_with_items():
    fake_order = SimpleNamespace(
        OrderId=1,
        Status="Pending",
        OrderDate=datetime(2026, 11, 19),
        CustomerName="Test Customer",
    )

    fake_items = [
        SimpleNamespace(
            SKU="SRUBA-M8",
            ProductName="Śruba M8",
            Quantity=100,
        ),
        SimpleNamespace(
            SKU="NAKRETKA-M8",
            ProductName="Nakrętka M8",
            Quantity=200,
        ),
    ]
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = fake_order
    mock_cursor.fetchall.side_effect = [fake_items, []]

    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connection.__enter__.return_value = mock_connection

    with patch(
        "orders_repository.get_connection",
        return_value=mock_connection,
    ):
        result = get_order_by_id(1)
    
    assert result["order_id"] == 1
    assert len(result["items"]) == 2
    assert result["items"][0]["sku"] == "SRUBA-M8"
    assert result["items"][1]["quantity"] == 200

    assert mock_cursor.fetchall.call_count == 1
    
def test_get_order_by_id_not_found():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None

    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connection.__enter__.return_value = mock_connection

    with patch(
        "orders_repository.get_connection",
        return_value=mock_connection
    ):
        result = get_order_by_id(99999)

    assert result is None
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.fetchall.assert_not_called()
    
def test_get_delayed_orders_pagination_parameters():
    with patch("orders_repository.get_connection") as mock_connection:
        mock_cursor = MagicMock()

        mock_connection.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        from orders_repository import get_delayed_orders

        result = get_delayed_orders(limit=5, offset=10)

    assert result == []

    query, offset, limit = mock_cursor.execute.call_args.args

    assert "OFFSET ? ROWS" in query
    assert "FETCH NEXT ? ROWS ONLY" in query
    assert offset == 10
    assert limit == 5