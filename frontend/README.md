# AI Production Copilot — Frontend

Angular web application for AI Production Copilot, designed to provide production planners with a unified interface for production data, AI-assisted analysis, and company knowledge.

## Technology Stack

- Angular 22
- TypeScript
- Node.js 24 LTS
- npm
- SCSS
- Standalone Components
- Angular Router
- Angular Signals
- RxJS
- HttpClient
- Vitest

## Architecture

The frontend follows a feature-based architecture with separation of concerns between business features, application layout, shared API configuration, and services.

```text
src/
├── app/
│   ├── core/
│   │   ├── config/
│   │   │   └── api.config.ts
│   │   └── services/
│   │       ├── health.ts
│   │       └── health.spec.ts
│   ├── features/
│   │   ├── dashboard/
│   │   ├── ai-chat/
│   │   ├── inventory/
│   │   ├── orders/
│   │   ├── knowledge/
│   │   └── evaluation/
│   ├── layout/
│   │   └── main-layout/
│   ├── app.config.ts
│   ├── app.routes.ts
│   ├── app.ts
│   ├── app.html
│   └── app.scss
└── styles.scss
```

## Implemented Features

- Responsive application layout
- Sidebar navigation
- Standalone Angular components
- Feature-based architecture
- Lazy-loaded feature routes
- Centralized API configuration
- FastAPI integration
- Reactive API availability status using Angular Signals
- HTTP timeout and error handling
- Manual API connection refresh
- Automated frontend tests
- Optimized production build

## Application Routes

| Route | Feature | Status |
|---|---|---|
| `/dashboard` | Production Dashboard | Planned |
| `/ai-chat` | AI Production Assistant | Planned |
| `/inventory` | Inventory Management | Planned |
| `/orders` | Production Orders | Planned |
| `/knowledge` | Company Knowledge Base | Planned |
| `/evaluation` | AI Evaluation | Planned |

All feature routes are implemented with lazy loading. Business feature pages currently contain placeholder components.

## Prerequisites

- Node.js 24 LTS
- npm
- Docker Desktop
- Running AI Production Copilot backend for API integration

## Getting Started

### 1. Start the Backend

From the repository root:

```bash
docker compose up -d
```

The backend must be configured according to the main project README.

### 2. Install Frontend Dependencies

```bash
cd frontend
npm ci
```

### 3. Start the Development Server

```bash
npm start
```

Open http://localhost:4200 in your browser.

The development server automatically reloads the application when source files change.

## Local Services

| Service | URL |
|---|---|
| Angular Frontend | http://localhost:4200 |
| FastAPI Backend | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| OpenAPI Specification | http://localhost:8000/openapi.json |

## API Configuration

The backend base URL is centralized in:

```text
src/app/core/config/api.config.ts
```

Current development configuration:

```typescript
export const API_BASE_URL = 'http://localhost:8000';
```

Environment-specific API configuration will be introduced during containerization and cloud deployment.

## Backend Integration

The frontend communicates with the FastAPI backend using Angular HttpClient.

The Health Service currently integrates with:

```http
GET /health
```

API availability is represented by three reactive states:

| State | Description |
|---|---|
| Checking | Health request is in progress |
| Online | Health endpoint responded successfully |
| Offline | Request failed or exceeded the timeout |

The application checks API availability during layout initialization. Users can manually refresh the connection status by clicking the API status indicator.

Health requests have a five-second timeout.

The health indicator represents API endpoint availability and does not guarantee the availability of SQL Server, Qdrant, Ollama, or other backend dependencies.

## Testing

The frontend uses Vitest and Angular TestBed for automated testing.

### Development Tests

```bash
npm test
```

### CI/CD Tests

```bash
npm run test:ci
```

The CI command executes all tests once without enabling watch mode.

### Test Coverage Areas

- Root application component
- Router outlet rendering
- Application layout
- Health Service
- HTTP request validation
- API availability states
- API failure handling
- API recovery
- Feature component initialization

### Current Test Results

| Test Category | Result |
|---|---:|
| Test files | 9/9 passed |
| Automated tests | 14/14 passed |
| Non-watch test execution | Passed |
| Production build | Passed |

HTTP service tests use HttpTestingController to simulate backend responses without requiring running backend services.

## Production Build

Generate an optimized production build:

```bash
npm run build
```

Build output:

```text
dist/frontend/browser/
```

The production build includes:

- TypeScript compilation
- Template compilation
- JavaScript bundling
- Tree shaking
- Minification
- Lazy-loaded feature chunks
- Optimized static assets

### Initial Build Baseline

| Metric | Result |
|---|---:|
| Main JavaScript bundle | 258.05 kB |
| Estimated main bundle transfer size | 69.65 kB |
| Lazy-loaded feature chunks | 6 |
| Build duration | 2.582 seconds |

These measurements represent the initial application foundation and will change as business features are implemented.

## Available npm Commands

| Command | Description |
|---|---|
| `npm ci` | Install dependencies using the lock file |
| `npm start` | Start the development server |
| `npm run build` | Generate a production build |
| `npm run watch` | Build in development watch mode |
| `npm test` | Run development tests |
| `npm run test:ci` | Run automated tests without watch mode |

## Development Principles

- Feature-based architecture
- Separation of concerns
- Strict TypeScript configuration
- Reusable services and components
- Reactive state management
- Lazy loading
- Centralized API communication
- Explicit loading and error states
- Automated testing
- Reproducible dependency installation
- CI/CD readiness

## Security Considerations

- No backend credentials or API secrets should be stored in frontend source code.
- API communication is restricted by backend CORS configuration in the local development environment.
- CORS is not a replacement for authentication or authorization.
- Business logic and sensitive operations remain on the backend.
- Authentication and authorization will be introduced during later development milestones.

## Current Limitations

- Business feature pages are placeholders.
- API configuration currently targets the local development environment.
- API health checks are performed on initialization and manual refresh.
- Authentication and authorization are not yet implemented.
- Frontend containerization is not yet implemented.
- Cloud deployment and automated pipelines are planned for future milestones.

## Roadmap

### Phase 1 — Angular Foundation

- [x] Angular project initialization
- [x] Feature-based architecture
- [x] Application layout
- [x] Routing and lazy loading
- [x] HttpClient configuration
- [x] Angular Signals integration
- [x] Backend health integration
- [x] Automated frontend tests
- [x] Production build
- [x] CI test command

### Phase 2 — Business Features

- [ ] AI Chat interface
- [ ] AI orchestration endpoint integration
- [ ] Chat message history
- [ ] Loading and error states
- [ ] Production dashboard
- [ ] Inventory management views
- [ ] Production order views
- [ ] Knowledge base interface
- [ ] AI evaluation interface

### Phase 3 — Production Readiness

- [ ] Frontend Dockerfile
- [ ] Nginx configuration
- [ ] Full-stack Docker Compose integration
- [ ] Environment-specific API configuration
- [ ] Azure DevOps CI/CD pipelines
- [ ] Microsoft Entra ID authentication
- [ ] Azure cloud deployment
- [ ] Application monitoring
- [ ] Production release and rollback strategy

## Project

This frontend is part of the AI Production Copilot portfolio project, demonstrating practical AI engineering, full-stack development, cloud integration, and production-oriented software delivery.

For backend architecture, AI orchestration, RAG implementation, database configuration, and project-wide documentation, see the [main project README](../README.md).
