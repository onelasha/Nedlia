# Event Schema Versioning

Semantic versioning and evolution patterns for Nedlia's event schemas using **[CloudEvents](https://cloudevents.io/)** specification.

## Table of Contents

- [Why Event Schema Versioning?](#why-event-schema-versioning)
- [CloudEvents Specification](#cloudevents-specification)
- [Semantic Versioning for Events](#semantic-versioning-for-events)
- [Event Type Naming Convention](#event-type-naming-convention)
- [Schema Evolution Rules](#schema-evolution-rules)
- [Event Schema Registry](#event-schema-registry)
- [Implementation](#implementation)
- [Consumer Compatibility](#consumer-compatibility)
- [Migration Strategies](#migration-strategies)
- [Related Documentation](#related-documentation)
- [References](#references)

---

## Why Event Schema Versioning?

Events are contracts between producers and consumers. Without versioning:

```
Producer (API)                              Consumer (Worker)
     │                                            │
     │── Event: {placement_id, video_id} ────────►│ ✅ Works
     │                                            │
     │  🔄 Producer adds new required field       │
     │                                            │
     │── Event: {placement_id, video_id, ─────────►│ ❌ Consumer crashes!
     │           product_id (required)}           │    Missing field handler
```

With versioning:

```
Producer (API)                              Consumer (Worker)
     │                                            │
     │── Event v1: {placement_id, video_id} ─────►│ ✅ Works
     │                                            │
     │  🔄 Producer creates v2 with new field     │
     │                                            │
     │── Event v2: {placement_id, video_id, ─────►│ ✅ Consumer handles v1 & v2
     │              product_id}                   │    gracefully
```

---

## CloudEvents Specification

Nedlia events follow the **[CloudEvents 1.0](https://cloudevents.io/)** specification:

```json
{
  "specversion": "1.0",
  "type": "com.nedlia.placement.created.v1",
  "source": "/services/nedlia-api",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "time": "2024-01-15T10:30:00.000Z",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.nedlia.com/events/placement-created/v1.json",
  "subject": "placements/123",
  "data": {
    "placement_id": "123",
    "video_id": "456",
    "product_id": "789",
    "status": "active"
  }
}
```

### Required CloudEvents Attributes

| Attribute     | Type   | Description                                                       |
| ------------- | ------ | ----------------------------------------------------------------- |
| `specversion` | String | CloudEvents version (`"1.0"`)                                     |
| `type`        | String | Event type with version (e.g., `com.nedlia.placement.created.v1`) |
| `source`      | URI    | Producer identifier                                               |
| `id`          | String | Unique event ID (UUID)                                            |

### Optional CloudEvents Attributes

| Attribute         | Type      | Description                                  |
| ----------------- | --------- | -------------------------------------------- |
| `time`            | Timestamp | Event timestamp (RFC 3339)                   |
| `datacontenttype` | String    | Content type of `data` (`application/json`)  |
| `dataschema`      | URI       | Schema URL for `data` payload                |
| `subject`         | String    | Resource identifier (e.g., `placements/123`) |

---

## Semantic Versioning for Events

Event schemas use **semantic versioning** (SemVer):

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Bug fixes (no schema change)
  │     └─ Backward-compatible additions
  └─ Breaking changes
```

### Version in Event Type

Include **major version** in the event type:

```
com.nedlia.placement.created.v1
com.nedlia.placement.created.v2
```

### Version Lifecycle

| Phase          | Duration | Description                        |
| -------------- | -------- | ---------------------------------- |
| **Current**    | Ongoing  | Latest stable version              |
| **Deprecated** | 6 months | Still produced, migration warnings |
| **Sunset**     | 3 months | No longer produced                 |

---

## Event Type Naming Convention

```
com.nedlia.<domain>.<action>.v<major>
```

### Examples

| Event Type                                 | Description           |
| ------------------------------------------ | --------------------- |
| `com.nedlia.placement.created.v1`          | Placement created     |
| `com.nedlia.placement.updated.v1`          | Placement updated     |
| `com.nedlia.placement.deleted.v1`          | Placement deleted     |
| `com.nedlia.video.validation_requested.v1` | Validation requested  |
| `com.nedlia.video.validation_completed.v1` | Validation completed  |
| `com.nedlia.campaign.created.v1`           | Campaign created      |
| `com.nedlia.plugin.sync_requested.v1`      | Plugin sync requested |

### Action Naming

| Action               | When to Use               |
| -------------------- | ------------------------- |
| `created`            | New resource created      |
| `updated`            | Resource modified         |
| `deleted`            | Resource removed          |
| `<action>_requested` | Async operation requested |
| `<action>_completed` | Async operation finished  |
| `<action>_failed`    | Async operation failed    |

---

## Schema Evolution Rules

### Backward-Compatible Changes (Minor Version)

These changes **don't break** existing consumers:

| Change                       | Example                                     | Safe? |
| ---------------------------- | ------------------------------------------- | ----- |
| Add optional field           | `+ "description": string?`                  | ✅    |
| Add new enum value           | `status: "active" \| "archived" \| "draft"` | ✅    |
| Widen numeric range          | `1-100` → `1-1000`                          | ✅    |
| Make required field optional | `video_id: required` → `optional`           | ✅    |

```json
// v1.0.0
{
  "placement_id": "123",
  "video_id": "456"
}

// v1.1.0 - Added optional field (backward compatible)
{
  "placement_id": "123",
  "video_id": "456",
  "description": "Product on table"  // New optional field
}
```

### Breaking Changes (Major Version)

These changes **require a new major version**:

| Change                 | Example                             | Requires v2? |
| ---------------------- | ----------------------------------- | ------------ |
| Remove field           | `- "legacy_id"`                     | ✅           |
| Rename field           | `video_id` → `videoId`              | ✅           |
| Change field type      | `id: string` → `id: number`         | ✅           |
| Add required field     | `+ "product_id": required`          | ✅           |
| Narrow enum values     | Remove `"draft"` from status        | ✅           |
| Change field semantics | `time` from seconds to milliseconds | ✅           |

```json
// v1 - Original schema
{
  "type": "com.nedlia.placement.created.v1",
  "data": {
    "placement_id": "123",
    "video_id": "456"
  }
}

// v2 - Breaking change (new required field)
{
  "type": "com.nedlia.placement.created.v2",
  "data": {
    "placement_id": "123",
    "video_id": "456",
    "product_id": "789"  // New required field
  }
}
```

---

## Event Schema Registry

### Schema Storage

Store schemas in a central location:

```
nedlia-back-end/
  schemas/
    events/
      placement-created/
        v1.json
        v2.json
      placement-updated/
        v1.json
      video-validation-completed/
        v1.json
```

### JSON Schema Definition

```json
// schemas/events/placement-created/v1.json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.nedlia.com/events/placement-created/v1.json",
  "title": "PlacementCreated",
  "description": "Event emitted when a placement is created",
  "type": "object",
  "required": ["placement_id", "video_id", "product_id", "status", "created_at"],
  "properties": {
    "placement_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique placement identifier"
    },
    "video_id": {
      "type": "string",
      "format": "uuid",
      "description": "Associated video identifier"
    },
    "product_id": {
      "type": "string",
      "format": "uuid",
      "description": "Associated product identifier"
    },
    "status": {
      "type": "string",
      "enum": ["active", "archived"],
      "description": "Placement status"
    },
    "time_range": {
      "type": "object",
      "properties": {
        "start_time": { "type": "number", "minimum": 0 },
        "end_time": { "type": "number", "minimum": 0 }
      },
      "required": ["start_time", "end_time"]
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Creation timestamp"
    }
  },
  "additionalProperties": false
}
```

### Schema Validation

```python
# src/infrastructure/events/validation.py
import json
from pathlib import Path

import jsonschema


class EventSchemaValidator:
    """Validate events against registered schemas."""

    def __init__(self, schema_dir: Path):
        self.schema_dir = schema_dir
        self._cache: dict[str, dict] = {}

    def validate(self, event: dict) -> None:
        """Validate event against its schema."""
        event_type = event.get("type", "")

        # Extract schema info from event type
        # com.nedlia.placement.created.v1 -> placement-created/v1
        parts = event_type.split(".")
        if len(parts) < 5:
            raise ValueError(f"Invalid event type: {event_type}")

        domain = parts[2]  # placement
        action = parts[3]  # created
        version = parts[4]  # v1

        schema_path = f"{domain}-{action}/{version}.json"
        schema = self._load_schema(schema_path)

        # Validate data payload
        jsonschema.validate(event.get("data", {}), schema)

    def _load_schema(self, schema_path: str) -> dict:
        if schema_path not in self._cache:
            full_path = self.schema_dir / schema_path
            with open(full_path) as f:
                self._cache[schema_path] = json.load(f)
        return self._cache[schema_path]
```

---

## Implementation

### Event Producer

```python
# src/infrastructure/events/producer.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4

import boto3


@dataclass
class CloudEvent:
    """CloudEvents 1.0 compliant event."""

    type: str  # e.g., "com.nedlia.placement.created.v1"
    source: str
    data: dict[str, Any]
    subject: str | None = None

    def to_dict(self) -> dict:
        return {
            "specversion": "1.0",
            "type": self.type,
            "source": self.source,
            "id": str(uuid4()),
            "time": datetime.utcnow().isoformat() + "Z",
            "datacontenttype": "application/json",
            "subject": self.subject,
            "data": self.data,
        }


class EventProducer:
    """Publish CloudEvents to EventBridge."""

    def __init__(self, event_bus: str, source: str):
        self.client = boto3.client("events")
        self.event_bus = event_bus
        self.source = source

    async def publish(self, event: CloudEvent) -> None:
        """Publish event to EventBridge."""
        cloud_event = event.to_dict()

        self.client.put_events(
            Entries=[{
                "EventBusName": self.event_bus,
                "Source": self.source,
                "DetailType": event.type,
                "Detail": json.dumps(cloud_event),
            }]
        )


# Usage
producer = EventProducer(
    event_bus="nedlia-events",
    source="/services/nedlia-api",
)

await producer.publish(CloudEvent(
    type="com.nedlia.placement.created.v1",
    source="/services/nedlia-api",
    subject=f"placements/{placement.id}",
    data={
        "placement_id": str(placement.id),
        "video_id": str(placement.video_id),
        "product_id": str(placement.product_id),
        "status": placement.status,
        "created_at": placement.created_at.isoformat(),
    },
))
```

### Event Consumer

```python
# src/handlers/file_generator.py
from src.infrastructure.events.validation import EventSchemaValidator

validator = EventSchemaValidator(Path("schemas/events"))


def handler(event: dict, context) -> dict:
    """SQS Lambda handler with schema validation."""
    batch_item_failures = []

    for record in event.get("Records", []):
        message_id = record["messageId"]

        try:
            body = json.loads(record["body"])
            cloud_event = body.get("detail", body)

            # Validate against schema
            validator.validate(cloud_event)

            # Route by event type and version
            event_type = cloud_event["type"]

            if event_type == "com.nedlia.placement.created.v1":
                handle_placement_created_v1(cloud_event["data"])
            elif event_type == "com.nedlia.placement.created.v2":
                handle_placement_created_v2(cloud_event["data"])
            else:
                logger.warning(f"Unknown event type: {event_type}")

        except jsonschema.ValidationError as e:
            logger.error(f"Schema validation failed: {e}")
            batch_item_failures.append({"itemIdentifier": message_id})
        except Exception as e:
            logger.exception(f"Error processing event: {e}")
            batch_item_failures.append({"itemIdentifier": message_id})

    return {"batchItemFailures": batch_item_failures}
```

---

## Consumer Compatibility

### Postel's Law (Robustness Principle)

> "Be conservative in what you send, be liberal in what you accept."

```python
# ✅ Good - Ignore unknown fields
def handle_placement_created(data: dict) -> None:
    placement_id = data["placement_id"]  # Required
    video_id = data["video_id"]  # Required
    description = data.get("description")  # Optional, may not exist
    # Ignore any other fields


# ❌ Bad - Fail on unknown fields
def handle_placement_created(data: dict) -> None:
    if set(data.keys()) != {"placement_id", "video_id"}:
        raise ValueError("Unexpected fields!")
```

### Multi-Version Support

```python
# src/handlers/placement_handler.py

def handle_placement_event(cloud_event: dict) -> None:
    """Handle multiple versions of placement events."""
    event_type = cloud_event["type"]
    data = cloud_event["data"]

    # Extract version from event type
    version = event_type.split(".")[-1]  # "v1" or "v2"

    if version == "v1":
        # v1 doesn't have product_id
        placement_id = data["placement_id"]
        video_id = data["video_id"]
        product_id = None  # Not available in v1

    elif version == "v2":
        # v2 has product_id
        placement_id = data["placement_id"]
        video_id = data["video_id"]
        product_id = data["product_id"]

    else:
        logger.warning(f"Unknown version: {version}")
        return

    process_placement(placement_id, video_id, product_id)
```

---

## Migration Strategies

### Parallel Publishing (Recommended)

Publish both old and new versions during migration:

```python
# During migration period
async def publish_placement_created(placement: Placement) -> None:
    # Publish v1 for old consumers
    await producer.publish(CloudEvent(
        type="com.nedlia.placement.created.v1",
        data={
            "placement_id": str(placement.id),
            "video_id": str(placement.video_id),
        },
    ))

    # Publish v2 for new consumers
    await producer.publish(CloudEvent(
        type="com.nedlia.placement.created.v2",
        data={
            "placement_id": str(placement.id),
            "video_id": str(placement.video_id),
            "product_id": str(placement.product_id),  # New field
        },
    ))
```

### Migration Timeline

```
Week 1-2:  Deploy consumers that handle v1 AND v2
Week 3:    Start publishing v2 alongside v1
Week 4-8:  Monitor; ensure all consumers handle v2
Week 9:    Stop publishing v1
Week 10:   Remove v1 handling code from consumers
```

### EventBridge Rules for Version Routing

```hcl
# Route v1 events to legacy queue
resource "aws_cloudwatch_event_rule" "placement_created_v1" {
  name           = "placement-created-v1"
  event_bus_name = aws_cloudwatch_event_bus.nedlia.name

  event_pattern = jsonencode({
    detail-type = ["com.nedlia.placement.created.v1"]
  })
}

# Route v2 events to new queue
resource "aws_cloudwatch_event_rule" "placement_created_v2" {
  name           = "placement-created-v2"
  event_bus_name = aws_cloudwatch_event_bus.nedlia.name

  event_pattern = jsonencode({
    detail-type = ["com.nedlia.placement.created.v2"]
  })
}
```

---

## Related Documentation

- [ADR-003: Event-Driven Architecture](adr/003-event-driven.md) – Event flow and patterns
- [Error Handling Strategy](error-handling-strategy.md) – Lambda worker error handling
- [Distributed Tracing](distributed-tracing.md) – Trace context in events
- [API Standards](api-standards.md) – Versioning principles

## References

- [CloudEvents Specification](https://cloudevents.io/) – Event format standard
- [JSON Schema](https://json-schema.org/) – Schema definition
- [Semantic Versioning](https://semver.org/) – Version numbering
- [Zalando Event Guidelines](https://opensource.zalando.com/restful-api-guidelines/#events) – Industry reference
