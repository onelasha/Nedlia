# Testing

This guide covers the testing strategy, tools, and practices for Nedlia.

## Testing Philosophy

We follow the **testing pyramid**:

```text
        ┌───────────┐
        │    E2E    │  Few, slow, high confidence
        ├───────────┤
        │Integration│  Some, medium speed
        ├───────────┤
        │   Unit    │  Many, fast, focused
        └───────────┘
```

## Test Organization by Layer

Following clean architecture, tests are organized by layer:

| Layer          | Test Type   | Location                  | Tools                        |
| -------------- | ----------- | ------------------------- | ---------------------------- |
| Domain         | Unit        | `tests/unit/domain/`      | pytest, Jest                 |
| Application    | Unit        | `tests/unit/application/` | pytest, Jest                 |
| Infrastructure | Integration | `tests/integration/`      | pytest, Jest, Testcontainers |
| Interface      | E2E         | `tests/e2e/`              | Playwright, Supertest        |

## Running Tests

### All Tests

```bash
# Using Makefile
make test

# Or individually
pnpm test              # JS/TS tests
cd nedlia-back-end/python && uv run pytest  # Python tests
```

### By Project

```bash
# Frontend
pnpm --filter @nedlia/web test

# Backend API
pnpm --filter @nedlia/api test

# Python backend
cd nedlia-back-end/python && uv run pytest

# Python SDK
cd nedlia-sdk/python && uv run pytest
```

### Watch Mode

```bash
# JS/TS (re-runs on file changes)
pnpm test --watch

# Python
uv run pytest-watch
```

### With Coverage

```bash
# JS/TS
pnpm test --coverage

# Python
uv run pytest --cov --cov-report=html
```

## Writing Tests

### Unit Tests (Domain & Application)

Unit tests should be:

- **Fast**: No I/O, no network, no database
- **Isolated**: No dependencies on other tests
- **Focused**: Test one thing

#### Python Example

```python
# tests/unit/domain/test_review.py
from nedlia_backend_py.domain.review import Review

def test_review_can_be_created():
    review = Review(
        id="123",
        pr_url="https://github.com/org/repo/pull/1",
        status="pending"
    )
    assert review.id == "123"
    assert review.is_pending()

def test_review_can_be_completed():
    review = Review(id="123", pr_url="...", status="pending")
    review.complete(findings=["Issue 1", "Issue 2"])
    assert review.is_completed()
    assert len(review.findings) == 2
```

#### TypeScript Example

```typescript
// tests/unit/domain/review.spec.ts
import { Review } from '@/core/domain/review';

describe('Review', () => {
  it('can be created', () => {
    const review = new Review({
      id: '123',
      prUrl: 'https://github.com/org/repo/pull/1',
      status: 'pending',
    });
    expect(review.id).toBe('123');
    expect(review.isPending()).toBe(true);
  });

  it('can be completed', () => {
    const review = new Review({ id: '123', prUrl: '...', status: 'pending' });
    review.complete(['Issue 1', 'Issue 2']);
    expect(review.isCompleted()).toBe(true);
    expect(review.findings).toHaveLength(2);
  });
});
```

### Integration Tests (Infrastructure)

Integration tests verify that adapters work correctly with real services.

```python
# tests/integration/test_review_repository.py
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres():
    with PostgresContainer("postgres:15") as pg:
        yield pg

def test_can_save_and_retrieve_review(postgres):
    repo = PostgresReviewRepository(postgres.get_connection_url())
    review = Review(id="123", pr_url="...", status="pending")

    repo.save(review)
    retrieved = repo.find_by_id("123")

    assert retrieved.id == review.id
```

### E2E Tests (Interface)

E2E tests verify complete user flows.

```typescript
// tests/e2e/review-flow.spec.ts
import { test, expect } from '@playwright/test';

test('user can submit a PR for review', async ({ page }) => {
  await page.goto('/');
  await page.click('text=New Review');
  await page.fill('input[name="prUrl"]', 'https://github.com/org/repo/pull/1');
  await page.click('text=Submit');

  await expect(page.locator('.review-status')).toHaveText('Pending');
});
```

## Test Fixtures

### Python

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_review():
    return Review(id="test-123", pr_url="https://...", status="pending")

@pytest.fixture
def mock_repository():
    return Mock(spec=ReviewRepository)
```

### TypeScript

```typescript
// tests/fixtures.ts
export const sampleReview = {
  id: 'test-123',
  prUrl: 'https://...',
  status: 'pending',
};

export const createMockRepository = () => ({
  save: jest.fn(),
  findById: jest.fn(),
});
```

## Coverage Requirements

| Layer          | Minimum Coverage |
| -------------- | ---------------- |
| Domain         | 90%              |
| Application    | 80%              |
| Infrastructure | 70%              |
| Interface      | 60%              |

CI will fail if coverage drops below these thresholds (once configured).

## Test Naming Conventions

Use descriptive names that explain the scenario:

```python
# Good
def test_review_status_changes_to_completed_when_all_checks_pass():
    ...

# Bad
def test_review():
    ...
```

```typescript
// Good
it('should return 404 when review is not found', () => { ... });

// Bad
it('works', () => { ... });
```

## Mocking Guidelines

1. **Mock at boundaries**: Only mock infrastructure (DB, HTTP, etc.)
2. **Don't mock domain**: Domain logic should be tested with real objects
3. **Use fakes over mocks**: When possible, use in-memory implementations

```python
# Good: Fake repository
class InMemoryReviewRepository(ReviewRepository):
    def __init__(self):
        self._reviews = {}

    def save(self, review):
        self._reviews[review.id] = review

    def find_by_id(self, id):
        return self._reviews.get(id)

# Use in tests
def test_create_review_use_case():
    repo = InMemoryReviewRepository()
    use_case = CreateReviewUseCase(repo)
    ...
```

## CI Integration

Tests run automatically on every PR:

1. **Lint** → **Unit Tests** → **Integration Tests** → **Build**
2. All must pass before merge
3. Coverage reports uploaded to PR comments (planned)

## Debugging Failed Tests

```bash
# Run single test with verbose output
pytest tests/unit/test_review.py::test_review_can_be_created -v

# Run with debugger
pytest --pdb

# JS/TS
pnpm test -- --testNamePattern="review can be created"
```

## Next Steps

- [Local Development](local-development.md) – Running services locally
- [Deployment](deployment.md) – CI/CD pipeline
