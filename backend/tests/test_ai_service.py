from unittest.mock import patch
import json
from copy import deepcopy
import ai_service

from ai_service import get_ai_response


@patch("ai_service.chat_completion")
def test_response_without_tools(mock_chat):

    mock_chat.return_value = {
        "role": "assistant",
        "content": "Cześć! Jak mogę pomóc?"
    }

    result = get_ai_response("Cześć")

    assert result == "Cześć! Jak mogę pomóc?"
    assert mock_chat.call_count == 1
    
@patch("ai_service.execute_tool")
@patch("ai_service.chat_completion")
def test_multiple_tool_calls(mock_chat, mock_execute):

    mock_chat.side_effect = [
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "function": {
                        "name": "get_production_context",
                        "arguments": {}
                    }
                },
                {
                    "function": {
                        "name": "search_company_knowledge",
                        "arguments": {
                            "query": "Procedura niedoborów"
                        }
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Połączona odpowiedź SQL i RAG."
        }
    ]

    mock_execute.side_effect = [
        {
            "shortages": [
                {
                    "product": "Nakrętka M8",
                    "quantity": 650
                }
            ]
        },
        {
            "found": True,
            "documents": [
                {
                    "source": "warehouse_procedure.txt",
                    "text": "Zgłoś niedobór do planisty."
                }
            ]
        }
    ]

    result = get_ai_response(
        "Jakie mamy niedobory i co z nimi zrobić?"
    )

    assert result == "Połączona odpowiedź SQL i RAG."
    assert mock_chat.call_count == 2
    assert mock_execute.call_count == 2

    mock_execute.assert_any_call(
        "get_production_context",
        {}
    )

    mock_execute.assert_any_call(
        "search_company_knowledge",
        {"query": "Procedura niedoborów"}
    )
    
@patch("ai_service.execute_tool")
@patch("ai_service.chat_completion")
def test_sequential_tool_calls(mock_chat, mock_execute):

    responses = iter([
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "function": {
                        "name": "get_production_context",
                        "arguments": {}
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "function": {
                        "name": "search_company_knowledge",
                        "arguments": {
                            "query": "Procedura niedoborów"
                        }
                    }
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Odpowiedź końcowa."
        }
    ])

    captured_messages = []

    def fake_chat(messages, tools=None):
        captured_messages.append(deepcopy(messages))
        return next(responses)

    mock_chat.side_effect = fake_chat

    mock_execute.side_effect = [
        {"shortages": [{"product": "Nakrętka M8"}]},
        {"found": True, "documents": []}
    ]

    result = get_ai_response("Przeanalizuj niedobory")

    assert result == "Odpowiedź końcowa."
    assert mock_chat.call_count == 3
    assert mock_execute.call_count == 2

    tool_messages = [
        message
        for message in captured_messages[2]
        if message["role"] == "tool"
    ]

    assert len(tool_messages) == 2

    assert tool_messages[0]["tool_name"] == (
        "get_production_context"
    )

    assert tool_messages[1]["tool_name"] == (
        "search_company_knowledge"
    )

    assert json.loads(tool_messages[0]["content"]) == {
        "shortages": [{"product": "Nakrętka M8"}]
    }

    assert json.loads(tool_messages[1]["content"]) == {
        "found": True,
        "documents": []
    }
    
@patch("ai_service.execute_tool")
@patch("ai_service.chat_completion")
def test_iteration_limit(mock_chat, mock_execute):

    mock_chat.return_value = {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "function": {
                    "name": "get_production_context",
                    "arguments": {}
                }
            }
        ]
    }

    mock_execute.return_value = {
        "shortages": []
    }

    result = get_ai_response("Sprawdź produkcję")

    assert mock_chat.call_count == ai_service.MAX_ITERATIONS
    assert mock_execute.call_count == ai_service.MAX_ITERATIONS
    assert "limicie operacji" in result
    
@patch("ai_service.execute_tool")
@patch("ai_service.chat_completion")
def test_tool_call_limit(mock_chat, mock_execute):

    mock_chat.return_value = {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "function": {
                    "name": "get_production_context",
                    "arguments": {}
                }
            }
            for _ in range(ai_service.MAX_TOOL_CALLS + 1)
        ]
    }

    result = get_ai_response("Sprawdź produkcję")

    mock_execute.assert_not_called()

    assert mock_chat.call_count == 1
    assert "limicie operacji" in result