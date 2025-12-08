# ADR-003: Event-Driven Architecture

## Status

Accepted

## Context

Nedlia's code review platform needs to:

- Process PRs asynchronously (analysis takes time)
- Notify multiple systems when events occur
- Scale different components independently
- Handle failures gracefully

## Decision

We adopt an **event-driven architecture** with **eventual consistency**.

### Event Flow

```
Command → Handler → Persist → Publish Event → Subscribers
```

1. API receives command (e.g., "create review")
2. Lambda handler validates and persists to Aurora
3. Handler publishes event to EventBridge (e.g., `review.created`)
4. SQS queues receive event and trigger downstream Lambdas
5. Consumers process event (send notifications, update read models, etc.)

### Key Patterns

- **CQRS**: Separate command (write) and query (read) paths
- **Eventual Consistency**: Reads may lag writes; design for it
- **Idempotency**: All handlers must handle duplicate events
- **Dead Letter Queues**: Failed events go to DLQ for inspection

### Event Format

We use [CloudEvents](https://cloudevents.io/) specification:

```json
{
  "specversion": "1.0",
  "type": "com.nedlia.review.created",
  "source": "/reviews",
  "id": "uuid",
  "time": "2024-01-01T00:00:00Z",
  "data": {
    "reviewId": "123",
    "prUrl": "https://..."
  }
}
```

## Consequences

### Positive

- Services are decoupled; can evolve independently
- Natural fit for async processing (code analysis)
- Easy to add new consumers without changing producers
- Built-in retry and failure handling via SQS

### Negative

- Eventual consistency requires careful UI design
- Debugging distributed flows is harder
- Event schema evolution needs governance
- More infrastructure to manage

### Mitigations

- Use X-Ray for distributed tracing
- Implement correlation IDs across all events
- Document event schemas in a registry
- Design UI to handle "processing" states gracefully
