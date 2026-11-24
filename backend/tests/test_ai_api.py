from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


@patch("main.get_ai_response")
def test_chat_success(mock_ai):
    mock_ai.return_value = "Brakuje nakrętek M8."

    response = client.post(
        "/ai/chat",
        json={"message": "Jakie mamy niedobory?"}
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "Brakuje nakrętek M8."
    }

    mock_ai.assert_called_once_with(
        "Jakie mamy niedobory?"
    )


@pytest.mark.parametrize("payload", [
    {"message": ""},
    {"message": "a" * 2001},
    {},
    {"message": None}
])
@patch("main.get_ai_response")
def test_chat_invalid_input(mock_ai, payload):

    response = client.post(
        "/ai/chat",
        json=payload
    )

    assert response.status_code == 422

    mock_ai.assert_not_called()


@patch("main.get_ai_response")
def test_chat_service_unavailable(mock_ai):

    mock_ai.side_effect = RuntimeError(
        "Sensitive infrastructure information"
    )

    response = client.post(
        "/ai/chat",
        json={"message": "Sprawdź produkcję"}
    )

    assert response.status_code == 503
    assert isinstance(response.json()["detail"], str)

    assert "Sensitive infrastructure information" not in response.text
    
@patch("main.answer_from_knowledge")
def test_knowledge_response_contract(mock_knowledge):

    mock_knowledge.return_value = {
        "answer": "Niedobór należy zgłosić do planisty.",
        "sources": ["warehouse_procedure.txt"]
    }

    response = client.post(
        "/ai/knowledge",
        json={"message": "Komu zgłosić niedobór?"}
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "Niedobór należy zgłosić do planisty.",
        "sources": ["warehouse_procedure.txt"]
    }

    mock_knowledge.assert_called_once_with(
        "Komu zgłosić niedobór?"
    )