FROM python:3.12-slim-bookworm

WORKDIR /app

# Narzędzia potrzebne do instalacji sterownika ODBC
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates \
    unixodbc \
    && rm -rf /var/lib/apt/lists/*

# Repozytorium Microsoft dla Debiana 12
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list \
    -o /etc/apt/sources.list.d/microsoft-prod.list

# Sterownik Microsoft ODBC Driver 18
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py database.py inventory_repository.py inventory_service.py orders_repository.py orders_service.py llm_client.py ai_tools.py ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]