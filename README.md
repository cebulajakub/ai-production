# AI Production Copilot

An AI-powered manufacturing assistant that combines a local Large Language Model (LLM) with real production data stored in SQL Server.

## Project Overview

AI Production Copilot is a portfolio project demonstrating how generative AI can interact with enterprise systems through controlled tool calling.

Users can ask questions in natural language about production risks, inventory shortages, and material availability. The assistant retrieves real data from SQL Server and uses an LLM to generate understandable answers.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** Microsoft SQL Server 2022
- **LLM:** Qwen3 8B via Ollama
- **AI Integration:** Tool calling
- **Infrastructure:** Docker Compose
- **Testing:** pytest

## Current Features

- REST API for production and inventory data
- SQL Server integration
- Inventory shortage detection and severity classification
- Local LLM integration through Ollama
- Tool calling for retrieving production context
- Tool allowlisting and argument validation
- Basic AI error handling and logging
- Separation of AI orchestration and LLM communication

## Architecture

```text
User / API Client
       |
       v
FastAPI (main.py)
       |
       v
AI Service (ai_service.py)
       |
       +----> LLM Client (llm_client.py)
       |             |
       |             v
       |        Ollama / Qwen3
       |
       +----> AI Tools (ai_tools.py)
                     |
                     v
              Inventory Service
                     |
                     v
                 SQL Server
```

## Example

**User:** Which products have the largest inventory shortages?

**AI Production Copilot:**

- M8 Nut — shortage of 650 units (HIGH)
- M8 Bolt — shortage of 300 units (MEDIUM)
- Steel Sheet 2 mm — shortage of 15 units (LOW)
- Electric Motor 1 kW — shortage of 6 units (LOW)

The assistant retrieves these values from the database using a controlled tool call.

## API Example

**Endpoint:** `POST /ai/chat`

Request:

```json
{
  "message": "What are the biggest inventory shortages?"
}
```

Response:

```json
{
  "answer": "The largest inventory shortage concerns M8 nuts..."
}
```

## Security

The project includes basic safeguards:

- Explicit allowlist of executable AI tools
- Tool argument validation
- Maximum number of tool calls per request
- Generic API error responses
- Server-side exception logging

These safeguards are educational and do not constitute a complete production security solution.

## Roadmap

### Phase 1 — Backend & AI Foundations
- [x] Docker Compose development environment
- [x] FastAPI and SQL Server integration
- [x] Manufacturing inventory REST API
- [x] Local LLM integration with Ollama (Qwen3)
- [x] AI tool calling with production data
- [x] Basic AI security and tool allowlisting
- [x] Separation of AI orchestration and LLM client

### Phase 2 — RAG & Enterprise Data Integration
- [ ] Qdrant vector database
- [ ] Document ingestion, chunking and embeddings
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] Mock Microsoft Dynamics 365 OData API
- [ ] AI tools for ERP data retrieval
- [ ] Angular frontend

### Phase 3 — Azure Cloud Integration
- [ ] Azure OpenAI integration with configurable LLM providers
- [ ] Azure Blob Storage for manufacturing documents
- [ ] Azure Key Vault for secrets management
- [ ] Azure Managed Identity for secure service authentication
- [ ] Cloud-ready application configuration
- [ ] Azure hosting and deployment

### Phase 4 — DevOps, Security & Observability
- [ ] Azure DevOps Repos integration
- [ ] Azure Pipelines for CI/CD
- [ ] Automated tests and code quality checks
- [ ] Secure deployment with environment-specific configuration
- [ ] Application Insights and Azure Monitor
- [ ] Authentication, authorization and API rate limiting
- [ ] LLM evaluation and RAG quality metrics

### Phase 5 — Portfolio & Documentation
- [ ] Architecture diagrams
- [ ] API documentation and usage examples
- [ ] Local and Azure deployment guides
- [ ] Security and cost considerations
- [ ] Final portfolio demonstration

## Project Status

**In active development.**

The project is being developed incrementally to demonstrate practical AI Engineering skills and enterprise integration patterns.