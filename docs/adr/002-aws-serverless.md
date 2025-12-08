# ADR-002: AWS Serverless Stack

## Status

Accepted

## Context

Nedlia needs a cloud infrastructure that:

- Scales automatically with demand
- Minimizes operational overhead
- Provides cost efficiency (pay-per-use)
- Integrates well with our event-driven architecture

## Decision

We adopt an **AWS-native serverless stack**:

| Component     | AWS Service                       |
| ------------- | --------------------------------- |
| Compute       | Lambda                            |
| API           | API Gateway                       |
| Database      | Aurora Serverless v2 (PostgreSQL) |
| Messaging     | EventBridge + SQS                 |
| Cache         | ElastiCache (Redis)               |
| Auth          | Cognito                           |
| Storage       | S3                                |
| Secrets       | Secrets Manager, SSM              |
| Observability | CloudWatch, X-Ray                 |

### Why AWS-Native?

- Single vendor simplifies operations
- Deep integration between services
- Mature tooling and documentation
- Team familiarity

### Why Serverless?

- No server management
- Automatic scaling
- Pay only for what we use
- Built-in high availability

## Consequences

### Positive

- Zero server maintenance
- Automatic scaling from 0 to millions of requests
- Cost-effective for variable workloads
- Built-in redundancy and fault tolerance

### Negative

- Cold starts can affect latency
- Vendor lock-in to AWS
- 15-minute Lambda timeout limits long-running tasks
- Local development requires emulation

### Mitigations

- Use provisioned concurrency for latency-sensitive functions
- Abstract AWS-specific code behind interfaces (clean architecture helps)
- Use Step Functions for long-running workflows
- Use LocalStack or SAM Local for development
