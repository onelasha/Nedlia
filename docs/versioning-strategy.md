# Versioning Strategy

Comprehensive versioning strategy for Nedlia's microservices, APIs, SDKs, and deployment artifacts.

## Table of Contents

- [Overview](#overview)
- [What Gets Versioned](#what-gets-versioned)
- [Version Formats](#version-formats)
- [API Versioning](#api-versioning)
- [Deployment Artifact Versioning](#deployment-artifact-versioning)
- [SDK Versioning](#sdk-versioning)
- [Event Schema Versioning](#event-schema-versioning)
- [Database Schema Versioning](#database-schema-versioning)
- [When to Bump Versions](#when-to-bump-versions)
- [CI/CD Tagging Strategy](#cicd-tagging-strategy)
- [Changelog Generation](#changelog-generation)
- [Version Compatibility Matrix](#version-compatibility-matrix)
- [Related Documentation](#related-documentation)
- [References](#references)

---

## Overview

Nedlia uses a **hybrid versioning strategy** that applies different versioning schemes based on what is being versioned:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Nedlia Versioning Strategy                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Component              │ Version Format        │ Example                    │
│  ───────────────────────┼───────────────────────┼──────────────────────────  │
│  API Contract           │ URL SemVer (major)    │ /v1/placements             │
│  Deployment Artifact    │ Git SHA + Timestamp   │ main-abc123f-20241218      │
│  SDKs (public)          │ Full SemVer           │ 1.2.3                      │
│  Event Schemas          │ SemVer in type        │ placement.created.v1       │
│  Database Migrations    │ Sequential + Date     │ 20241218_001_add_column    │
│  Product Release        │ CalVer (optional)     │ 2024.12.1                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Principle

```
Version ≠ Build ID

Version:  Semantic meaning (breaking changes, features, compatibility)
Build ID: Unique identifier for a specific deployable artifact
```

---

## What Gets Versioned

### Must Have Versions

| Component               | Why                              | Who Cares              |
| ----------------------- | -------------------------------- | ---------------------- |
| **API Contract**        | Breaking changes affect clients  | SDK users, integrators |
| **SDKs**                | Clients pin to specific versions | Developers using SDKs  |
| **Event Schemas**       | Consumers depend on structure    | Internal workers       |
| **Database Migrations** | Order matters, rollback needs    | DevOps, DB admins      |

### Should Have Build IDs (Not Versions)

| Component          | Why                      | Format                  |
| ------------------ | ------------------------ | ----------------------- |
| **API Service**    | Traceability, rollback   | `main-abc123f-20241218` |
| **Lambda Workers** | Immutable deployments    | `main-abc123f-20241218` |
| **Infrastructure** | Terraform state tracking | Git SHA                 |

### Optional Versions

| Component           | When Useful               | Format             |
| ------------------- | ------------------------- | ------------------ |
| **Product Release** | Marketing, customer comms | CalVer `2024.12.1` |
| **Documentation**   | Major doc overhauls       | SemVer or date     |

---

## Version Formats

### Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Bug fixes (backward compatible)
  │     └─ New features (backward compatible)
  └─ Breaking changes
```

**Used for:** SDKs, Event Schemas, Libraries

**Example:** `1.2.3` → `1.2.4` (patch) → `1.3.0` (feature) → `2.0.0` (breaking)

### Calendar Versioning (CalVer)

```
YYYY.MM.RELEASE
  │    │    │
  │    │    └─ Release number within month
  │    └─ Month
  └─ Year
```

**Used for:** Product releases, changelogs

**Example:** `2024.12.1` → `2024.12.2` → `2025.01.1`

### Git SHA + Timestamp

```
BRANCH-SHA-DATE
   │    │    │
   │    │    └─ Build date (YYYYMMDD)
   │    └─ Short Git SHA (7 chars)
   └─ Branch name
```

**Used for:** Docker images, Lambda deployments

**Example:** `main-abc123f-20241218`

---

## API Versioning

### Strategy: URL-Based Major Version

```
https://api.nedlia.com/v1/placements
https://api.nedlia.com/v2/placements
```

### When to Increment API Version

| Change Type        | Example                          | Version Impact |
| ------------------ | -------------------------------- | -------------- |
| Remove endpoint    | DELETE `/v1/legacy`              | **v2**         |
| Remove field       | Remove `legacy_id` from response | **v2**         |
| Change field type  | `id: string` → `id: number`      | **v2**         |
| Rename field       | `video_id` → `videoId`           | **v2**         |
| Add required field | New required `product_id`        | **v2**         |
| Add optional field | New optional `description`       | Same version   |
| Add new endpoint   | New `/v1/analytics`              | Same version   |
| Bug fix            | Fix validation logic             | Same version   |

### API Version Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    API Version Lifecycle                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  v1 ──────────────────────────────────────────────────────────► │
│      │                                                           │
│      │  v2 released                                              │
│      │  │                                                        │
│      │  ▼                                                        │
│      │  v1 DEPRECATED ─────────────────────────────────────────► │
│      │  (6 months)     │                                         │
│      │                 │  v1 SUNSET                              │
│      │                 │  │                                      │
│      │                 │  ▼                                      │
│      │                 │  v1 REMOVED                             │
│      │                 │                                         │
│      ▼                 ▼                                         │
│  v2 ──────────────────────────────────────────────────────────► │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Deprecation Headers

```http
HTTP/1.1 200 OK
Deprecation: Sun, 01 Jun 2025 00:00:00 GMT
Sunset: Sun, 01 Sep 2025 00:00:00 GMT
Link: </v2/placements>; rel="successor-version"
```

---

## Deployment Artifact Versioning

### Strategy: Git SHA + Timestamp (No Manual Versioning)

Every commit to `main` produces a deployable artifact. No manual version bumps needed.

### Docker Image Tags

```bash
# Format: BRANCH-SHA-DATE
nedlia-api:main-abc123f-20241218
nedlia-api:main-def456g-20241219

# Also tag as latest for convenience
nedlia-api:latest
```

### Lambda Function Versions

```bash
# Use Git SHA in description
aws lambda publish-version \
  --function-name nedlia-file-generator \
  --description "main-abc123f-20241218"
```

### Benefits

| Benefit                  | Explanation              |
| ------------------------ | ------------------------ |
| **No version conflicts** | Every build is unique    |
| **Easy rollback**        | Deploy previous SHA      |
| **Full traceability**    | SHA links to exact code  |
| **No manual steps**      | CI/CD handles everything |

### When Services Don't Change

**Question:** Should unchanged services get new versions?

**Answer:** No. Only rebuild and redeploy services that changed.

```yaml
# CI/CD with change detection
jobs:
  detect-changes:
    outputs:
      api: ${{ steps.filter.outputs.api }}
      workers: ${{ steps.filter.outputs.workers }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'services/api/**'
              - 'libs/shared/**'
            workers:
              - 'services/workers/**'
              - 'libs/shared/**'

  build-api:
    needs: detect-changes
    if: needs.detect-changes.outputs.api == 'true'
    steps:
      - run: docker build -t nedlia-api:${{ github.sha }} .
```

---

## SDK Versioning

### Strategy: Full Semantic Versioning

SDKs are **public packages** that developers pin to specific versions. They need proper SemVer.

### Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE]

1.0.0        # Initial release
1.1.0        # New feature (backward compatible)
1.1.1        # Bug fix
2.0.0        # Breaking change
2.0.0-beta.1 # Pre-release
```

### SDK Version Matrix

| SDK        | Package Name  | Current Version |
| ---------- | ------------- | --------------- |
| JavaScript | `@nedlia/sdk` | `1.x.x`         |
| Python     | `nedlia-sdk`  | `1.x.x`         |
| Swift      | `NedliaSDK`   | `1.x.x`         |

### SDK vs API Version Independence

```
SDK Version    API Version    Notes
───────────────────────────────────────────────────
SDK 1.0.0      API v1         Initial release
SDK 1.1.0      API v1         New SDK features, same API
SDK 1.2.0      API v1         More SDK features
SDK 2.0.0      API v1 + v2    SDK supports both API versions
SDK 2.1.0      API v2         Deprecate v1 support in SDK
```

### Automated Version Bumping

Use [Conventional Commits](https://www.conventionalcommits.org/) + [semantic-release](https://semantic-release.gitbook.io/):

```bash
# Commit messages determine version bump
feat: add batch placement API     → MINOR bump (1.1.0 → 1.2.0)
fix: handle timeout errors        → PATCH bump (1.2.0 → 1.2.1)
feat!: change auth flow           → MAJOR bump (1.2.1 → 2.0.0)
BREAKING CHANGE: remove legacy    → MAJOR bump
```

---

## Event Schema Versioning

### Strategy: Version in Event Type

```json
{
  "type": "com.nedlia.placement.created.v1",
  "data": { ... }
}
```

See [Event Schema Versioning](event-schema-versioning.md) for full details.

### Quick Reference

| Change             | Version Impact        |
| ------------------ | --------------------- |
| Add optional field | Same version          |
| Add required field | **New major version** |
| Remove field       | **New major version** |
| Change field type  | **New major version** |

---

## Database Schema Versioning

### Strategy: Sequential Migrations with Date Prefix

```
migrations/
  20241201_001_create_placements_table.sql
  20241205_001_add_status_column.sql
  20241218_001_add_product_id_column.sql
  20241218_002_create_analytics_table.sql
```

### Format

```
YYYYMMDD_NNN_description.sql
   │      │      │
   │      │      └─ Human-readable description
   │      └─ Sequence number within day
   └─ Date created
```

### Migration Best Practices

| Practice                             | Reason                        |
| ------------------------------------ | ----------------------------- |
| Never edit existing migrations       | Already applied to production |
| Always add, never remove columns     | Backward compatibility        |
| Use feature flags for schema changes | Gradual rollout               |
| Test rollback scripts                | Recovery capability           |

---

## When to Bump Versions

### Decision Tree

```
                    ┌─────────────────────┐
                    │  What changed?      │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ API Contract │   │ Internal     │   │ SDK Code     │
    │              │   │ Service Code │   │              │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                   │
           ▼                  ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ Breaking?    │   │ Just rebuild │   │ Use SemVer   │
    │ Yes → v2     │   │ with new     │   │ based on     │
    │ No  → same   │   │ Git SHA      │   │ change type  │
    └──────────────┘   └──────────────┘   └──────────────┘
```

### Quick Reference Table

| What Changed        | API Version | Build ID | SDK Version           |
| ------------------- | ----------- | -------- | --------------------- |
| Bug fix in API      | Same        | New SHA  | Patch if SDK affected |
| New API endpoint    | Same        | New SHA  | Minor                 |
| Remove API field    | **Bump**    | New SHA  | Major                 |
| Refactor internals  | Same        | New SHA  | No change             |
| New SDK feature     | Same        | Same     | Minor                 |
| SDK breaking change | Depends     | Depends  | Major                 |

---

## CI/CD Tagging Strategy

### Git Tags

```bash
# SDK releases (manual or automated)
git tag -a sdk-js-v1.2.0 -m "JavaScript SDK v1.2.0"
git tag -a sdk-py-v1.2.0 -m "Python SDK v1.2.0"

# API version milestones (rare)
git tag -a api-v2-release -m "API v2 initial release"

# Product releases (optional)
git tag -a release-2024.12.1 -m "December 2024 Release 1"
```

### Docker Image Tags

```yaml
# .github/workflows/build.yml
- name: Build and tag Docker image
  run: |
    SHORT_SHA=$(git rev-parse --short HEAD)
    DATE=$(date +%Y%m%d)
    BRANCH=${GITHUB_REF_NAME}

    # Primary tag: branch-sha-date
    docker tag nedlia-api:build nedlia-api:${BRANCH}-${SHORT_SHA}-${DATE}

    # Convenience tags
    docker tag nedlia-api:build nedlia-api:${BRANCH}-latest

    # Production tag (on main only)
    if [ "$BRANCH" = "main" ]; then
      docker tag nedlia-api:build nedlia-api:latest
    fi
```

### Lambda Deployment Tags

```yaml
- name: Deploy Lambda
  run: |
    aws lambda update-function-code \
      --function-name nedlia-file-generator \
      --zip-file fileb://function.zip

    # Publish version with description
    aws lambda publish-version \
      --function-name nedlia-file-generator \
      --description "${{ github.ref_name }}-${{ github.sha }}-$(date +%Y%m%d)"
```

---

## Changelog Generation

### Conventional Commits

Use standardized commit messages:

```bash
# Format: type(scope): description

feat(api): add batch placement endpoint
fix(sdk): handle network timeout errors
docs(readme): update installation guide
refactor(workers): simplify event processing
perf(api): optimize placement queries
test(sdk): add integration tests for auth

# Breaking changes
feat(api)!: change authentication flow
BREAKING CHANGE: OAuth2 now required
```

### Automated Changelog

```yaml
# .github/workflows/release.yml
- name: Generate Changelog
  uses: conventional-changelog/standard-version@v9
  with:
    preset: conventionalcommits
```

### Changelog Format

```markdown
# Changelog

## [1.3.0] - 2024-12-18

### Added

- Batch placement API endpoint (#123)
- Support for custom metadata fields (#125)

### Fixed

- Network timeout handling in SDK (#124)

### Changed

- Improved error messages for validation failures

## [1.2.1] - 2024-12-10

### Fixed

- Race condition in concurrent updates (#120)
```

---

## Version Compatibility Matrix

### Maintaining Compatibility

```
┌─────────────────────────────────────────────────────────────────┐
│                  Version Compatibility Matrix                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SDK Version   │ API v1  │ API v2  │ Event Schema v1 │ v2      │
│  ──────────────┼─────────┼─────────┼─────────────────┼──────── │
│  1.0.x         │ ✅      │ ❌      │ ✅              │ ❌      │
│  1.1.x         │ ✅      │ ❌      │ ✅              │ ❌      │
│  2.0.x         │ ✅      │ ✅      │ ✅              │ ✅      │
│  2.1.x         │ ⚠️ dep  │ ✅      │ ⚠️ dep          │ ✅      │
│  3.0.x         │ ❌      │ ✅      │ ❌              │ ✅      │
│                                                                  │
│  ✅ = Supported  ⚠️ dep = Deprecated  ❌ = Not supported        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Documenting Compatibility

Include in SDK documentation:

```markdown
## Compatibility

| SDK Version | Minimum API Version | Maximum API Version |
| ----------- | ------------------- | ------------------- |
| 2.x         | v1 (deprecated)     | v2                  |
| 1.x         | v1                  | v1                  |

### Deprecation Notice

SDK 2.x still supports API v1, but it will be removed in SDK 3.0.
Please migrate to API v2 before upgrading to SDK 3.x.
```

---

## Related Documentation

- [API Standards](api-standards.md) – URL versioning, deprecation headers
- [Event Schema Versioning](event-schema-versioning.md) – CloudEvents versioning
- [Deployment](deployment.md) – CI/CD pipelines
- [Release Management](release-management.md) – Release process

## References

- [Semantic Versioning](https://semver.org/) – SemVer specification
- [Calendar Versioning](https://calver.org/) – CalVer specification
- [Conventional Commits](https://www.conventionalcommits.org/) – Commit message standard
- [Keep a Changelog](https://keepachangelog.com/) – Changelog format
