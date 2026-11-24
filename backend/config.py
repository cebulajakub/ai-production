import os


APP_NAME = "AI Production Copilot"

APP_ENV = os.getenv("APP_ENV", "development")

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:4200"
    ).split(",")
    if origin.strip()
]