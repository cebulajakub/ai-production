from unittest.mock import patch
import pytest

from inventory_service import get_shortages
from inventory_service import get_shortages_summary
from inventory_service import get_production_context

@pytest.mark.parametrize(
    "shortage, expected_severity",
    [
        (1, "LOW"),
        (99, "LOW"),
        (100, "MEDIUM"),
        (499, "MEDIUM"),
        (500, "HIGH"),
        (501, "HIGH"),
    ]
)
def test_shortage_severity(shortage, expected_severity):
    fake_data = [
        {
            "sku": "TEST-001",
            "shortage": shortage,
        }
    ]

    with patch(
        "inventory_service.get_inventory_shortages",
        return_value=fake_data
    ):
        result = get_shortages()

    assert result[0]["severity"] == expected_severity
    
def test_shortages_sorted_descending():
    fake_data = [
        {"sku": "A", "shortage": 50},
        {"sku": "B", "shortage": 700},
        {"sku": "C", "shortage": 200},
    ]

    with patch(
        "inventory_service.get_inventory_shortages",
        return_value=fake_data
    ):
        result = get_shortages()

    assert [item["sku"] for item in result] == ["B", "C", "A"]
    
def test_shortages_summary():
    fake_shortages = [
        {"sku": "A", "severity": "HIGH"},
        {"sku": "B", "severity": "HIGH"},
        {"sku": "C", "severity": "MEDIUM"},
        {"sku": "D", "severity": "LOW"},
    ]

    with patch(
        "inventory_service.get_shortages",
        return_value=fake_shortages
    ):
        result = get_shortages_summary()

    assert result == {
        "total_products_with_shortages": 4,
        "high_priority": 2,
        "medium_priority": 1,
        "low_priority": 1,
    }
    
def test_shortages_summary_empty():
    with patch(
        "inventory_service.get_shortages",
        return_value=[]
    ):
        result = get_shortages_summary()

    assert result == {
        "total_products_with_shortages": 0,
        "high_priority": 0,
        "medium_priority": 0,
        "low_priority": 0,
    }
    
def test_production_context():
    fake_shortages = [
        {"sku": "SRUBA-M8", "shortage": 200, "severity": "MEDIUM"},
        {"sku": "SILNIK-1KW", "shortage": 600, "severity": "HIGH"},
    ]

    with patch(
        "inventory_service.get_shortages",
        return_value=fake_shortages
    ) as mock_get_shortages:
        result = get_production_context()

    assert result["summary"] == {
        "total_products_with_shortages": 2,
        "high_priority": 1,
        "medium_priority": 1,
        "low_priority": 0,
    }

    assert result["shortages"] == fake_shortages

    mock_get_shortages.assert_called_once()