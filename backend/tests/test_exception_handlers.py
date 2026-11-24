from fastapi import FastAPI
from fastapi.testclient import TestClient

from exception_handlers import (
    unhandled_exception_handler
)


def test_unhandled_exception_returns_safe_response():

    test_app = FastAPI()

    test_app.add_exception_handler(
        Exception,
        unhandled_exception_handler
    )

    @test_app.get("/error")
    def simulate_error():
        raise RuntimeError(
            "Sensitive internal information"
        )

    client = TestClient(
        test_app,
        raise_server_exceptions=False
    )

    response = client.get("/error")

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Internal server error"
    }

    assert "Sensitive internal information" not in response.text