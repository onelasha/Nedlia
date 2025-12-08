# Local Development

This guide covers running Nedlia services locally for development.

## Architecture Overview

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API   │────▶│   Database      │
│   (React)       │     │   (NestJS)      │     │   (PostgreSQL)  │
│   localhost:5173│     │   localhost:3000│     │   localhost:5432│
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

### Frontend (React)

```bash
cd nedlia-front-end/web
pnpm dev
```

Opens at: http://localhost:5173

### Backend API (NestJS)

```bash
cd nedlia-back-end/nestjs
pnpm dev
```

API available at: http://localhost:3000

### Python Workers

```bash
cd nedlia-back-end/python
uv run python -m nedlia_backend_py
```

## Running Everything Together

From the repo root:

```bash
# Terminal 1: Frontend
pnpm --filter @nedlia/web dev

# Terminal 2: Backend
pnpm --filter @nedlia/api dev

# Terminal 3: Workers (if needed)
cd nedlia-back-end/python && uv run python -m nedlia_backend_py
```

Or use a process manager like `concurrently` (to be added).

## Hot Reloading

All services support hot reloading:

- **Frontend**: Vite HMR (instant updates)
- **NestJS**: `--watch` mode (auto-restart on changes)
- **Python**: Use `--reload` flag if using uvicorn/FastAPI

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
```

### Update Dependencies

```bash
# JS
pnpm update

# Python
cd nedlia-back-end/python && uv lock --upgrade
```

## Ports Reference

| Service     | Port | URL                         |
| ----------- | ---- | --------------------------- |
| Frontend    | 5173 | http://localhost:5173       |
| Backend API | 3000 | http://localhost:3000       |
| PostgreSQL  | 5432 | postgresql://localhost:5432 |
| Redis       | 6379 | redis://localhost:6379      |

## Next Steps

- [Testing](testing.md) – Running and writing tests
- [Deployment](deployment.md) – Deploying to environments
