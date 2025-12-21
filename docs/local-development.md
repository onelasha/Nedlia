# Local Development

This guide covers running Nedlia services locally for development.

## Architecture Overview

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API   │────▶│   Database      │
│   (React)       │     │   (FastAPI)     │     │   (PostgreSQL)  │
│   localhost:5173│     │   localhost:8000│     │   localhost:5432│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  Python Workers │
                        │  (Background)   │
                        └─────────────────┘
```

## Prerequisites

Complete the [Getting Started](getting-started.md) guide first.

## Database Setup

### Option 1: Docker (Recommended)

```bash
# Start PostgreSQL
docker run -d \
  --name nedlia-postgres \
  -e POSTGRES_USER=nedlia \
  -e POSTGRES_PASSWORD=nedlia \
  -e POSTGRES_DB=nedlia_dev \
  -p 5432:5432 \
  postgres:15

# Verify connection
psql postgresql://nedlia:nedlia@localhost:5432/nedlia_dev
```

### Option 2: Local PostgreSQL

```bash
# macOS with Homebrew
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb nedlia_dev
```

Update your `.env`:

```bash
DATABASE_URL=postgresql://nedlia:nedlia@localhost:5432/nedlia_dev
```

## Running Services

All services are run via **Nx**:

### Frontend Portal (React/Vite)

```bash
nx run portal:serve
```

Opens at: http://localhost:5173

### Backend API (FastAPI)

```bash
nx run api:serve
```

API available at: http://localhost:8000

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Placement Service (FastAPI)

```bash
nx run placement-service:serve
```

API available at: http://localhost:8001

- Swagger UI: http://localhost:8001/docs

## Available Nx Targets

| Project               | Targets                                                                   |
| --------------------- | ------------------------------------------------------------------------- |
| **portal**            | `serve`, `build`, `preview`, `lint`, `format`, `test`, `typecheck`        |
| **api**               | `install`, `serve`, `lint`, `format`, `test`, `typecheck`                 |
| **placement-service** | `install`, `serve`, `lint`, `format`, `test`, `typecheck`, `docker-build` |
| **workers**           | `install`, `lint`, `format`, `test`, `typecheck`                          |
| **sdk-js**            | `build`, `lint`, `test`                                                   |

Examples:

```bash
# Build portal for production
nx run portal:build

# Run all tests
nx run-many -t test

# Lint only affected projects
nx affected -t lint

# Type check everything
nx run-many -t typecheck
```

## Running Everything Together

From the repo root, use multiple terminals:

```bash
# Terminal 1: Backend API
nx run api:serve

# Terminal 2: Placement Service
nx run placement-service:serve

# Terminal 3: Frontend
nx run portal:serve
```

Or run all affected services:

```bash
nx run-many -t serve
```

## Hot Reloading

All services support hot reloading:

- **Frontend**: Vite HMR (instant updates)
- **FastAPI**: `--reload` flag (enabled by default in `nx run api:serve`)

## Environment Variables

### Required for Local Dev

```bash
# .env
NODE_ENV=development
LOG_LEVEL=debug

# Database
DATABASE_URL=postgresql://nedlia:nedlia@localhost:5432/nedlia_dev

# Frontend
VITE_API_URL=http://localhost:3000

# Auth (use test values locally)
JWT_SECRET=local-dev-secret-change-in-prod
```

### Optional

```bash
# AWS (only if testing AWS integrations)
AWS_PROFILE=nedlia-dev
AWS_REGION=us-east-1

# Redis (if using caching)
REDIS_URL=redis://localhost:6379
```

## Debugging

### VS Code

Launch configurations are in `.vscode/launch.json`. Use:

- **Debug Frontend**: Launches Chrome with debugger attached
- **Debug NestJS**: Attaches to Node.js process
- **Debug Python**: Attaches to Python process

### Browser DevTools

- React DevTools: Install browser extension
- Network tab: Inspect API calls
- Console: Check for errors

### Logging

```bash
# Increase log verbosity
LOG_LEVEL=debug pnpm dev
```

## Common Tasks

### Reset Database

```bash
# Drop and recreate
docker exec -it nedlia-postgres psql -U nedlia -c "DROP DATABASE nedlia_dev;"
docker exec -it nedlia-postgres psql -U nedlia -c "CREATE DATABASE nedlia_dev;"

# Run migrations (when available)
pnpm --filter @nedlia/api migrate
```

### Clear All Caches

```bash
# Node modules
rm -rf node_modules
rm -rf nedlia-*/node_modules
pnpm install

# Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".venv" -exec rm -rf {} +

# Nx cache
nx reset
```

### Update Dependencies

```bash
# JS
pnpm update

# Python (per-project)
cd nedlia-back-end/api && uv lock --upgrade && uv sync
```

## Ports Reference

| Service           | Port | URL                         |
| ----------------- | ---- | --------------------------- |
| Frontend (Portal) | 5173 | http://localhost:5173       |
| Backend API       | 8000 | http://localhost:8000       |
| Placement Service | 8001 | http://localhost:8001       |
| PostgreSQL        | 5432 | postgresql://localhost:5432 |
| Redis             | 6379 | redis://localhost:6379      |

## Next Steps

- [Testing](testing.md) – Running and writing tests
- [Deployment](deployment.md) – Deploying to environments
