# ADR-001: Clean Architecture

## Status

Accepted

## Context

Nedlia is a polyglot monorepo with multiple services (Python, NestJS, React, Swift). We need a consistent architectural pattern that:

- Works across all languages and frameworks
- Enables testability without external dependencies
- Allows swapping infrastructure without changing business logic
- Provides clear boundaries for team ownership

## Decision

We adopt **Clean Architecture** (also known as Hexagonal/Ports & Adapters) across all projects.

### Layer Structure

```
Domain → Application → Infrastructure → Interface
```

1. **Domain**: Entities, value objects, domain services. No external dependencies.
2. **Application**: Use cases, ports (interfaces), DTOs. Depends only on Domain.
3. **Infrastructure**: Repositories, external clients, ORM. Implements ports.
4. **Interface**: Controllers, CLI, UI. Orchestrates Application layer.

### Dependency Rule

Dependencies point inward. Outer layers depend on inner layers, never the reverse.

### Per-Language Implementation

- **Python**: `domain/`, `application/`, `infrastructure/`, `interface/` packages
- **NestJS**: `core/domain/`, `core/application/`, `infrastructure/`, `interface/` modules
- **React**: `domain/`, `application/`, `infrastructure/`, `ui/` folders
- **Swift**: `Domain/`, `Application/`, `Infrastructure/`, `UI/` groups

## Consequences

### Positive

- Business logic is isolated and testable
- Infrastructure can be swapped (e.g., change database) without touching domain
- Clear boundaries make code ownership easier
- Consistent pattern across all languages

### Negative

- More boilerplate (interfaces, DTOs, mappers)
- Learning curve for developers unfamiliar with the pattern
- Risk of over-engineering simple features

### Mitigations

- Provide clear examples in each language
- Document when to simplify (e.g., simple CRUD doesn't need full layers)
- Code reviews enforce layer boundaries
