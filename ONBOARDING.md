# Onboarding

Welcome to Nedlia. This page is the **single path** from a fresh laptop to your first merged pull request. Follow it top to bottom — links go to deeper docs only when you need them.

> **Time budget**: ~60–90 minutes if your machine is fresh. ~30 minutes if you already have Node, pnpm, and Python set up.

---

## Table of Contents

1. [What you're going to do](#1-what-youre-going-to-do)
2. [Install prerequisites](#2-install-prerequisites)
3. [Clone and install](#3-clone-and-install)
4. [Verify the environment](#4-verify-the-environment)
5. [Run a project](#5-run-a-project)
6. [Make your first change](#6-make-your-first-change)
7. [Open your first PR](#7-open-your-first-pr)
8. [What to read next](#8-what-to-read-next)

---

## 1. What you're going to do

By the end of this page you will have:

- ✅ All required tools installed (Node 20, pnpm 10, Python 3.13, uv)
- ✅ The repo cloned and dependencies installed
- ✅ Git hooks active (this is mandatory — see [§4](#4-verify-the-environment))
- ✅ At least one project running locally
- ✅ Your first PR open against `main`

If something blocks you, jump to [docs/getting-started.md](docs/getting-started.md) for the deeper version of any step.

---

## 2. Install prerequisites

| Tool    | Version | macOS install                                                |
| ------- | ------- | ------------------------------------------------------------ |
| Node.js | 20.x+   | `nvm install 20 && nvm use 20`                               |
| pnpm    | 10.x    | `corepack enable && corepack prepare pnpm@latest --activate` |
| Python  | 3.13.5  | `pyenv install 3.13.5 && pyenv local 3.13.5`                 |
| uv      | latest  | `curl -LsSf https://astral.sh/uv/install.sh \| sh`           |
| Git     | 2.x+    | `brew install git` (or already installed)                    |

Verify:

```bash
node -v && pnpm -v && python -V && uv --version && git --version
```

If any of these fail, open [docs/getting-started.md](docs/getting-started.md) for full per-OS instructions.

---

## 3. Clone and install

```bash
git clone https://github.com/onelasha/Nedlia.git
cd Nedlia
pnpm install
```

`pnpm install` will:

- Install all JS workspace dependencies (root, portal, sdk-js)
- Run a `postinstall` check that warns if git hooks aren't installed
- Run `husky install` to set up git hooks

For Python projects, dependencies install on demand when you run an Nx task that needs them. To pre-install dev tools (ruff, pytest, mypy) for a specific project:

```bash
cd nedlia-back-end/api && uv sync --extra dev
```

---

## 4. Verify the environment

This is **mandatory**. Run:

```bash
pnpm verify-hooks
```

Expected output: `✅ Git hooks installed`

> **Why this matters.** Hooks enforce **Shift-Left Parity** — `pre-commit` runs the same lint/format/test checks as CI, so a green commit equals a green build. Skipping hooks (`--no-verify`) is not allowed.

Run a baseline build to confirm everything compiles:

```bash
pnpm nx run-many -t lint,build,test
```

If lint or test fails on `main`, that's a bug — file an issue. Otherwise, you're ready.

---

## 5. Run a project

Pick one based on what you'll be working on.

### Frontend (React portal)

```bash
nx run portal:serve         # http://localhost:5173
```

### Backend API

```bash
nx run api:serve            # http://localhost:8000
```

You can also serve workers and the placement service:

```bash
nx run workers:serve
nx run placement-service:serve   # http://localhost:8001
```

For the full local stack (database, etc.) see [docs/local-development.md](docs/local-development.md).

---

## 6. Make your first change

Branch off `main`:

```bash
git checkout -b chore/<your-name>-onboarding
```

Make a tiny visible change — for example, add yourself to a `CONTRIBUTORS` file, fix a typo you spot in a doc, or add a comment to a file you're curious about.

> **Branch & commit conventions** are in [docs/branching-strategy.md](docs/branching-strategy.md).

Stage and commit using **Conventional Commits** format:

```bash
git add <file>
git commit -m "docs: fix typo in <file>"
```

Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, `perf`, `style`. Subject must be lower-case.

> **Cross-project rule.** The pre-commit hook blocks commits that touch more than one of: `nedlia-back-end/`, `nedlia-front-end/`, `nedlia-sdk/`, `nedlia-plugin/`, `nedlia-IaC/`. Split into separate commits per project.

---

## 7. Open your first PR

```bash
git push -u origin chore/<your-name>-onboarding
gh pr create --fill
```

Your PR will trigger:

1. **CI** — same checks as the local pre-commit hook, plus full test matrix
2. **Dependabot** — already running, doesn't affect your PR
3. **CodeRabbit / SonarCloud** — automated review (if configured for the repo)

Address feedback by pushing more commits to the same branch (don't force-push unless asked).

> Read [docs/pull-request-guidelines.md](docs/pull-request-guidelines.md) for what reviewers look for.

---

## 8. What to read next

Pick the section that matches your role. **You don't need to read everything** — these are starting points.

### If you're working on the **backend** (api, workers, services)

1. [ARCHITECTURE.md](ARCHITECTURE.md) — clean architecture, AWS event-driven design
2. [docs/python-style-guide.md](docs/python-style-guide.md)
3. [docs/api-standards.md](docs/api-standards.md)
4. [docs/error-handling.md](docs/error-handling.md)
5. [docs/idempotency.md](docs/idempotency.md) — non-optional for handlers

### If you're working on the **frontend** (portal)

1. [docs/frontend-architecture.md](docs/frontend-architecture.md)
2. [docs/typescript-style-guide.md](docs/typescript-style-guide.md)
3. [docs/accessibility.md](docs/accessibility.md)
4. [nedlia-front-end/portal/README.md](nedlia-front-end/portal/README.md)

### If you're working on **infrastructure** (IaC)

1. [nedlia-IaC/README.md](nedlia-IaC/README.md)
2. [nedlia-IaC/docs/ORGANIZATION.md](nedlia-IaC/docs/ORGANIZATION.md)
3. [nedlia-IaC/docs/NAMING_CONVENTIONS.md](nedlia-IaC/docs/NAMING_CONVENTIONS.md)
4. [docs/deployment.md](docs/deployment.md)

### If you're working on **SDKs or plugins**

1. [nedlia-sdk/README.md](nedlia-sdk/README.md)
2. [nedlia-plugin/README.md](nedlia-plugin/README.md)
3. [docs/versioning-strategy.md](docs/versioning-strategy.md)

### If you want the **full reference index**

See the [Documentation section in README.md](README.md#-documentation), which lists every doc grouped by purpose.

---

## Stuck?

- **Hooks not installing?** `pnpm exec husky install`
- **`pnpm verify-hooks` fails?** Re-clone or check `.husky/` exists at the repo root.
- **`nx` command not found?** Use `pnpm nx ...` instead — Nx is a workspace dependency, not a global.
- **Python venv issues?** Each Python project has its own `.venv`. Run `uv sync --extra dev` inside that project's directory.
- **Anything else?** File an issue or ask in the team channel.

Welcome aboard. 🎬
