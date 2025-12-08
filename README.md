# Nedlia Monorepo

Nedlia is a polyglot monorepo that contains all core services, frontends, SDKs, plugins, and infrastructure for the Nedlia platform.

## Structure

```text
nedlia-back-end/      Python and NestJS backend services
nedlia-front-end/     React web frontend
nedlia-IaC/           Infrastructure as Code (Terraform/CDK/Pulumi)
nedlia-plugin/        Native plugins (SwiftUI, etc.)
nedlia-sdk/           Public SDKs (Python, JS, Swift, ...)
```

### Back-end

```text
nedlia-back-end/
  python/             Python backend components
  nestjs/             NestJS backend services (API, workers, etc.)
```

### Front-end

```text
nedlia-front-end/
  web/                React web application
```

### SDKs

```text
nedlia-sdk/
  python/             Python SDK for Nedlia APIs
  js/                 JavaScript/TypeScript SDK
  swift/              Swift SDK (optional, future)
```

### Plugins

```text
nedlia-plugin/
  ios/                iOS / SwiftUI plugin(s)
```

### Infrastructure

```text
nedlia-IaC/
  terraform/          Terraform modules (optional)
  cdk/ or pulumi/     Alternative IaC stacks (optional)
```

## Tooling

- Package manager (JS): pnpm with workspaces
- Monorepo orchestration (JS): Nx
- Python: uv or compatible tooling via `pyproject.toml` per project
- CI/CD: GitHub Actions (planned)

Root `package.json` defines a workspace that includes:

- `nedlia-back-end/nestjs`
- `nedlia-front-end/web`
- `nedlia-sdk/js`

## Getting Started

### Prerequisites

- Node.js (LTS)
- pnpm (`corepack enable` recommended)
- Python 3.11+

### Install JS dependencies

From the repository root:

```bash
pnpm install
```

Once Nx projects are fully wired, you will be able to run:

```bash
pnpm lint
pnpm test
pnpm build
```

### Python projects

Each Python project has its own `pyproject.toml`:

- `nedlia-back-end/python/pyproject.toml`
- `nedlia-sdk/python/pyproject.toml`

Tooling is configured via `[tool.uv]` sections and can be extended per project.

## Conventions

- One repo for all core components (backends, frontends, SDKs, plugins, IaC).
- Per-language best practices inside each subfolder.
- Shared configuration at the root:
  - `.editorconfig` for formatting basics
  - `.gitignore` covering Node, Python, IDE, and OS artifacts

## Roadmap

- Add Nx configuration and initial NestJS + React + JS SDK projects.
- Flesh out Python backend and SDK package layout and tests.
- Add GitHub Actions workflows for linting, testing, and building all projects.
- Introduce SwiftUI plugin project(s) and iOS build pipeline.
- Define infrastructure layout and provisioning workflows in `nedlia-IaC/`.
