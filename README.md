# AI Production Copilot

An AI-powered manufacturing assistant that combines Large Language Models (LLMs), real-time production data, and Retrieval-Augmented Generation (RAG) to support manufacturing operations and production planning.

## Project Overview

AI Production Copilot is a portfolio project demonstrating practical AI Engineering, enterprise system integration, and production-oriented software development.

The assistant enables users to ask natural language questions about inventory shortages, production risks, material availability, and internal manufacturing procedures.

Unlike a traditional chatbot, the application uses controlled tool calling and semantic document retrieval to generate answers grounded in enterprise data.

The project follows an incremental development approach, progressing from a local AI solution to a cloud-ready application deployed on Microsoft Azure.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Relational Database | Microsoft SQL Server 2022 |
| Vector Database | Qdrant |
| Local LLM | Qwen3 8B via Ollama |
| Embedding Model | BGE-M3 |
| AI Integration | Tool Calling, RAG, Multi-Step Orchestration |
| Infrastructure | Docker Compose |
| Testing | pytest, unittest.mock |
| AI Evaluation | Hit Rate@K, MRR, Rejection Rate |
| Version Control | Git, GitHub |
| Frontend | Angular — planned |
| Cloud | Microsoft Azure — planned |
| CI/CD | Azure DevOps Pipelines — planned |

## Current Features

### Production Data Integration

- REST API for production, inventory, and order data.
- Microsoft SQL Server integration.
- Inventory shortage detection and severity classification.
- Production context aggregation.
- Delayed order retrieval and pagination.

### AI Engineering

- Local LLM integration through Ollama.
- Separation of AI orchestration and LLM communication.
- Controlled tool calling with server-side validation.
- Multi-tool and multi-step AI orchestration.
- Unified assistant combining production data and internal documentation.
- Conversation context preservation within a single request.
- Bounded tool execution and LLM iterations.

### Retrieval-Augmented Generation

- Qdrant vector database integration.
- Automated document ingestion and text chunking.
- Multilingual semantic embeddings using BGE-M3.
- Configurable retrieval thresholds and top-K results.
- Deterministic document chunk identifiers.
- Document reindexing.
- Source attribution in generated responses.
- Handling questions with insufficient documentation.

### AI Evaluation

- Retrieval development and validation datasets.
- Embedding model comparison.
- Retrieval threshold optimization.
- Automated retrieval evaluation.
- Configurable AI Quality Gate.
- Process exit codes supporting future CI/CD integration.

### Observability

- AI orchestration iteration logging.
- Tool execution logging.
- Tool latency measurement.
- Server-side exception logging.

## Architecture

```text
User / API Client
        |
        v
FastAPI (main.py)
        |
        v
AI Orchestrator (ai_service.py)
        |
        +----> LLM Client (llm_client.py)
        |              |
        |              v
        |        Ollama / Qwen3
        |
        +----> Tool Registry (ai_tools.py)
                       |
                       +----> Production Tool
                       |              |
                       |              v
                       |       Inventory Service
                       |              |
                       |              v
                       |          SQL Server
                       |
                       +----> Knowledge Tool
                                      |
                                      v
                                 RAG Service
                                      |
                                      +----> BGE-M3 Embeddings
                                      |
                                      +----> Qdrant
```

### Document Ingestion Pipeline

```text
Manufacturing Documents
          |
          v
Document Ingestion
          |
          v
Text Chunking
          |
          v
BGE-M3 Embeddings
          |
          v
Qdrant Vector Database
          |
          v
Semantic Retrieval
```

### AI Orchestration Workflow

1. The user submits a natural language question.
2. The LLM determines which tools are required.
3. The backend validates the requested tools and arguments.
4. The tools retrieve production data or relevant documentation.
5. Tool results are added to the conversation context.
6. The LLM may request additional tools within configured limits.
7. The assistant generates a final response based on the available information.

## Example Use Case

**User:**

Which materials are currently missing, and how should shortages be handled according to company procedures?

**AI Production Copilot:**

Current inventory shortages:

- M8 Nut — 650 units (HIGH)
- M8 Bolt — 300 units (MEDIUM)
- Steel Sheet 2 mm — 15 units (LOW)
- Electric Motor 1 kW — 6 units (LOW)

According to the internal warehouse procedure, shortages should be reported to the production planning department. The production planner verifies material availability, delivery dates, and the impact on order fulfillment.

High-priority shortages require urgent analysis and corrective actions.

Source: `warehouse_procedure.txt`

This example is an English illustration of the assistant's workflow. The current assistant is configured to respond in Polish.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| GET | `/inventory/shortages` | Inventory shortages |
| GET | `/inventory/summary` | Inventory shortage summary |
| GET | `/inventory/low-stock` | Products with low stock |
| GET | `/orders/{order_id}` | Order details |
| GET | `/orders/delayed` | Delayed orders |
| GET | `/ai/context` | Aggregated production context |
| POST | `/ai/chat` | Unified AI assistant |
| POST | `/ai/knowledge` | Documentation-based AI assistant |

### API Example

**Endpoint:** `POST /ai/chat`

Request:

```json
{
  "message": "Jakich materiałów aktualnie brakuje i jak należy postępować w przypadku niedoborów?"
}
```

Example response:

```json
{
  "answer": "Największy niedobór dotyczy nakrętek M8. Zgodnie z procedurą magazynową problem należy zgłosić do działu planowania produkcji."
}
```

Interactive API documentation is available locally at:

`http://localhost:8000/docs`

## AI Security and Reliability

The project implements several application-level safeguards:

- Explicit allowlist of executable AI tools.
- Server-side tool argument validation.
- Rejection of unknown tools and unexpected arguments.
- Input length validation.
- Maximum of 5 LLM iterations per request.
- Maximum of 6 tool calls per request.
- System prompt instructions against fabricated production data.
- System prompt instructions treating retrieved documents as untrusted data.
- Generic API error responses.
- Server-side exception logging.
- Environment-based CORS configuration.
- Typed API request and response contracts using Pydantic.
- Centralized exception handling.
- Safe HTTP error responses.
- CORS headers on unhandled server error responses.

These safeguards reduce operational risks but do not constitute a complete production security solution.

## Testing and Quality Assurance

### Backend Tests

The backend includes automated tests covering:

- API endpoints.
- Inventory business logic.
- Shortage severity classification.
- Database repository operations.
- Error handling.
- AI orchestration.
- Multi-tool execution.
- Sequential tool calling.
- Conversation context preservation.
- Tool execution and iteration limits.

LLM responses are mocked in orchestration unit tests to provide fast and deterministic execution without requiring a running language model.

Latest regression results:

| Test Category | Result |
|---|---:|
| Existing backend tests | 23/23 passed |
| AI orchestration tests | 5/5 passed |
| Total | 28/28 passed |

### RAG Evaluation

Current retrieval configuration:

| Parameter | Value |
|---|---|
| Embedding model | BGE-M3 |
| Vector dimensions | 1024 |
| Similarity metric | Cosine |
| Top-K | 3 |
| Score threshold | 0.50 |
| Collection | manufacturing_knowledge_v2 |

Validation results:

| Metric | Result | Required |
|---|---:|---:|
| Hit Rate@1 | 100% | 80% |
| Hit Rate@3 | 100% | 90% |
| Mean Reciprocal Rank | 1.00 | 0.85 |
| Rejection Rate | 75% | 75% |

**RAG Quality Gate: PASSED**

The validation dataset contains 10 questions, including 6 answerable questions and 4 questions without sufficient supporting documentation.

These results are based on a small validation dataset and do not guarantee production-level accuracy.

Detailed evaluation results are available in [docs/rag-evaluation.md](docs/rag-evaluation.md).

## Local Development

### Prerequisites

- Python 3.12
- Docker and Docker Compose
- Ollama
- Git

Download the required local AI models:

```bash
ollama pull qwen3:8b
ollama pull bge-m3
```

Configure the required environment variables, including the SQL Server password, in a local `.env` file.

Never commit credentials or secrets to version control.

Start the application:

```bash
docker compose up -d --build
```

The backend is available at:

`http://localhost:8000`

The local environment also requires an initialized production database, the configured Qdrant collection, and indexed manufacturing documents.

### Document Indexing

After creating the configured Qdrant collection, index the manufacturing documents:

```bash
docker compose exec backend python qdrant_indexer.py
```

### Running Backend Tests

From the backend directory, using the configured Python virtual environment:

```bash
python -m pytest -v
```

### Running AI Evaluation

From the project root:

```bash
docker compose exec backend python evaluate_retrieval.py
```

### Running the AI Quality Gate

```bash
docker compose exec backend python quality_gate.py
```

The quality gate returns exit code `0` when all configured requirements are satisfied and exit code `1` when a quality requirement fails.

## Development Workflow

The project follows a feature-based development workflow:

- Feature branches.
- Incremental commits.
- Pull requests and code review.
- Automated regression testing.
- AI quality evaluation.
- Squash merging.
- Short-lived feature branches.

GitHub is used for source code management. Azure DevOps Boards and Pipelines will be introduced for work item management and automated CI/CD.

## Known Limitations and Technical Debt

- Local LLM inference latency requires optimization.
- Semantic retrieval may return related documents that do not contain the requested information.
- Generated source references are not independently validated.
- Retrieval evaluation uses a limited validation dataset.
- Invalid tool calls currently terminate the request instead of triggering a recovery workflow.
- Document reindexing is not atomic.
- Authentication and authorization are not yet implemented.
- API rate limiting is not yet implemented.
- A test dependency deprecation warning requires future maintenance.

The current application uses demonstration manufacturing data and fictional internal procedures. It is not intended to control real manufacturing equipment or replace approved operational safety procedures.

## Roadmap

### Phase 1 — Backend & AI Foundations

- [x] Docker Compose development environment
- [x] FastAPI and SQL Server integration
- [x] Manufacturing inventory REST API
- [x] Order management API
- [x] Local LLM integration with Ollama
- [x] AI tool calling with production data
- [x] Basic AI security and tool allowlisting
- [x] Separation of AI orchestration and LLM client
- [x] Automated backend tests

### Phase 2 — RAG & Unified AI Assistant

- [x] Qdrant vector database
- [x] Document ingestion and chunking
- [x] Multilingual embeddings
- [x] Retrieval-Augmented Generation
- [x] Embedding model comparison
- [x] Retrieval threshold optimization
- [x] Automated retrieval evaluation
- [x] AI Quality Gate
- [x] Unified SQL and RAG assistant
- [x] Multi-step AI orchestration
- [x] Tool execution limits
- [x] AI logging and latency measurement
- [x] Automated AI orchestration tests
- [ ] Mock Microsoft Dynamics 365 OData API
- [ ] AI tools for ERP data retrieval

### Phase 3 — Angular Frontend & Full Stack Integration

- [x] Frontend-ready API contracts
- [x] CORS configuration
- [ ] Angular application architecture
- [ ] AI chat interface
- [ ] Production dashboard
- [ ] Inventory and shortage management views
- [ ] Order management views
- [ ] Document management interface
- [ ] Frontend error and loading states
- [ ] Frontend automated tests
- [ ] Full stack Docker Compose environment

### Phase 4 — Azure DevOps & CI/CD

- [ ] Azure DevOps Boards
- [ ] User stories and work item management
- [ ] GitHub integration with Azure Pipelines
- [ ] Automated build and regression tests
- [ ] Automated AI Quality Gate
- [ ] Container image build and publishing
- [ ] Environment-specific configuration
- [ ] Continuous deployment pipelines
- [ ] Release approvals and rollback strategy

### Phase 5 — Azure Cloud Integration

- [ ] Azure OpenAI integration
- [ ] Configurable LLM providers
- [ ] Azurite local storage integration
- [ ] Azure Blob Storage for manufacturing documents
- [ ] Azure Key Vault for secrets management
- [ ] Azure Managed Identity
- [ ] Microsoft Entra ID authentication
- [ ] Azure container hosting and deployment

### Phase 6 — Production Readiness

- [ ] Authentication and authorization
- [ ] API rate limiting
- [ ] Application Insights and Azure Monitor
- [ ] Structured logging and distributed tracing
- [ ] LLM response quality evaluation
- [ ] Citation validation
- [ ] Prompt injection testing
- [ ] Performance and cost optimization
- [ ] Production release and rollback procedures

### Phase 7 — Portfolio & Documentation

- [x] Initial architecture documentation
- [x] API documentation and usage examples
- [x] RAG evaluation report
- [ ] Complete local deployment guide
- [ ] Azure deployment guide
- [ ] Architecture decision records
- [ ] Security and cost considerations
- [ ] Final portfolio demonstration

## Project Status

**In active development.**

The local backend, RAG pipeline, and unified AI orchestration are implemented and tested.

The next development milestone is frontend readiness and Angular integration, followed by Azure DevOps automation and Microsoft Azure deployment.

The project demonstrates practical AI Engineering skills, enterprise integration patterns, automated quality evaluation, and production-oriented application development.

## Containerized Full Stack Deployment

AI Production Copilot supports a local containerized deployment using Docker Compose.

### Prerequisites

- Docker Desktop
- Ollama running on the host machine
- Qwen3 8B model
- BGE-M3 embedding model
- Configured environment variables
- Initialized SQL Server database
- Initialized Qdrant collection and indexed documents

### Build and Start

```powershell
docker compose up -d --build
```

### Application Endpoints

| Service | URL |
|---|---|
| Web Application | http://localhost:8080 |
| Frontend Health | http://localhost:8080/health |
| Backend Health via Proxy | http://localhost:8080/api/health |
| Backend Swagger | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |

### Deployment Architecture

The Angular application is built using a multi-stage Docker build and served by Nginx.

Nginx forwards API requests to the FastAPI backend through the internal Docker network.

SQL Server and Qdrant use persistent Docker volumes. Ollama runs on the host machine and provides local LLM inference and embeddings.

The current release is intended for local development and demonstration purposes. Public production deployment requires additional security and infrastructure configuration.

### Current Release

**v0.1.0 — Local Full Stack MVP**