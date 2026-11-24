from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from exception_handlers import unhandled_exception_handler

from main import app


client = TestClient(app)


def test_cors_allowed_origin():

    response = client.options(
        "/ai/chat",
        headers={
            "Origin": "http://localhost:4200",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )

    assert response.status_code == 200

    assert response.headers[
        "access-control-allow-origin"
    ] == "http://localhost:4200"


def test_cors_disallowed_origin():

    response = client.options(
        "/ai/chat",
        headers={
            "Origin": "https://unknown.example",
            "Access-Control-Request-Method": "POST"
        }
    )

    assert response.status_code == 400

    assert "access-control-allow-origin" not in response.headers
    
def test_cors_on_unhandled_server_error():

    test_app = FastAPI()

    test_app.add_exception_handler(
        Exception,
        unhandled_exception_handler
    )

    @test_app.get("/error")
    def simulate_error():
        raise RuntimeError("Internal failure")

    wrapped_app = CORSMiddleware(
        app=test_app,
        allow_origins=["http://localhost:4200"],
        allow_methods=["GET", "POST"]
    )

    error_client = TestClient(
        wrapped_app,
        raise_server_exceptions=False
    )

    response = error_client.get(
        "/error",
        headers={
            "Origin": "http://localhost:4200"
        }
    )

    assert response.status_code == 500

    assert response.headers[
        "access-control-allow-origin"
    ] == "http://localhost:4200"

    assert response.json() == {
        "detail": "Internal server error"
    }