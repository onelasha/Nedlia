# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial monorepo structure with clean architecture
- AWS serverless infrastructure (Terraform + Terragrunt)
- Multi-environment support (dev, testing, staging, production)
- Developer tooling (ESLint, Prettier, Ruff, pre-commit)
- CI/CD pipeline with GitHub Actions
- Documentation (Architecture, Contributing, Security)
- `nedlia-front-end/portal/src/vite-env.d.ts` for Vite client type references (required by TypeScript 6 for side-effect CSS imports)

### Changed

- Bumped all JS dependencies to latest within semver via `pnpm update -r`
- Bumped TypeScript 5.9.3 → 6.0.3 (sdk-js, portal); removed deprecated `baseUrl` from `nedlia-front-end/portal/tsconfig.json`
- Bumped Vite 7.3.0 → 8.0.10 and `@vitejs/plugin-react` 5.1.2 → 6.0.1 (portal)
- Bumped `eslint-plugin-boundaries` 5.3.1 → 6.0.2
- Upgraded all Python lockfiles via `uv sync --upgrade`; notable: starlette 0.50 → 1.0, uvicorn 0.40 → 0.46, ruff 0.14 → 0.15, websockets 15 → 16, pytest 9.0.2 → 9.0.3

### Deprecated

- N/A

### Removed

- N/A

### Fixed

- N/A

### Security

- Added Gitleaks for secret detection
- Added Dependabot for dependency updates

---

## [0.1.0] - YYYY-MM-DD

### Added

- Initial release

[Unreleased]: https://github.com/onelasha/Nedlia/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/onelasha/Nedlia/releases/tag/v0.1.0
