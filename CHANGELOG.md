# Changelog

All notable changes to AI Production Copilot will be documented in this file.

This project follows Semantic Versioning.

## [0.1.0] - 2026-11-25

### Added

- FastAPI backend with SQL Server integration.
- Production inventory and order management endpoints.
- Local LLM integration using Ollama and Qwen3 8B.
- Function calling with validated and allowlisted tools.
- Retrieval-Augmented Generation using Qdrant and BGE-M3.
- Document ingestion, chunking and vector indexing.
- Retrieval evaluation and automated AI quality gate.
- Unified AI orchestration combining production data and company knowledge.
- Angular frontend with standalone components and lazy-loaded routes.
- Interactive AI Chat with Markdown rendering and retry functionality.
- Production Dashboard with dynamic KPIs, charts and operational alerts.
- Multi-stage frontend Docker build.
- Nginx static file hosting and reverse proxy.
- Angular development and production configurations.
- Full Stack Docker Compose deployment.

### Validation

- Successful Angular production build.
- Successful frontend Docker image build.
- All four Docker Compose services running.
- Frontend and backend health endpoints verified.
- Eight manual Full Stack Smoke Test scenarios passed.
- End-to-end AI interaction combining SQL Server and RAG verified.

### Known Limitations

- Ollama runs outside Docker Compose.
- Authentication and authorization are not implemented.
- HTTPS is not configured.
- Chat history is not persisted.
- Retrieved document citations are not independently validated.
- Container health checks and automated deployment pipelines remain planned.
- Base container images are not fully pinned.
- Database and vector index initialization still require manual setup.

### Planned

- Azure DevOps Boards and Pipelines.
- Automated CI/CD and release quality gates.
- Azure Blob Storage integration.
- Azure OpenAI integration.
- Azure Key Vault and Managed Identity.
- Cloud deployment and observability.