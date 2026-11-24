# RAG Evaluation and Embedding Model Selection

## Objective

Improve retrieval quality for Polish manufacturing documentation and establish measurable quality requirements for future CI/CD pipelines.

## Experiment Results

| Configuration | Hit Rate@1 | Hit Rate@3 | MRR | Rejection Rate |
|---|---:|---:|---:|---:|
| Nomic with prefixes, threshold 0.65 | 88.89% | 88.89% | 0.8889 | 50.00% |
| BGE-M3, threshold 0.55 | 88.89% | 88.89% | 0.8889 | 83.33% |
| BGE-M3, threshold 0.50 | 100% | 100% | 1.0000 | 83.33% |

Development dataset: 15 questions.

## Selected Configuration

- Embedding model: BGE-M3
- Vector dimensions: 1024
- Vector database: Qdrant
- Collection: manufacturing_knowledge_v2
- Distance metric: Cosine
- Top-K: 3
- Similarity threshold: 0.50
- Chunk size: 500 characters

BGE-M3 was selected because it achieved better retrieval and rejection performance on the development dataset.

## Holdout Validation

The selected configuration was evaluated using 10 previously unused questions.

| Metric | Result | Minimum requirement |
|---|---:|---:|
| Hit Rate@1 | 100% | 80% |
| Hit Rate@3 | 100% | 90% |
| MRR | 1.0000 | 0.8500 |
| Rejection Rate | 75% | 75% |

All predefined retrieval acceptance criteria were met.

## End-to-End Evaluation

Four manually evaluated API requests confirmed correct answer generation, appropriate abstention when information was unavailable, and resistance to one tested prompt injection attempt.

## Automated Quality Gate

The retrieval evaluation is integrated into a standalone quality gate script.

- Exit code 0: All quality requirements are satisfied.
- Exit code 1: At least one quality requirement is not satisfied.

The script is designed for future Azure DevOps CI/CD integration.

## Known Limitations

- Small evaluation datasets limit statistical confidence.
- Semantic similarity does not guarantee answerability.
- Some irrelevant but topically related documents are retrieved.
- The API sources field represents retrieved documents, not validated citations.
- End-to-end generation evaluation is currently manual.
- Production readiness has not yet been established.

## Future Improvements

- Reranking
- Answerability verification
- Structured LLM outputs
- Citation validation
- Automated generation evaluation
- Retrieval latency monitoring
- Azure DevOps pipeline integration

## Rollback Strategy

The previous Nomic embedding collection remains available. The application can switch back to the previous model, collection and threshold through environment configuration.