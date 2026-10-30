# Event-Driven

## Picker card
Parts of the system publish events when something happens, and other parts react, instead of calling each other directly.

## When it fits
Reactions that cross contexts or systems ("when an order is placed, reserve stock and email the customer"), integration with other systems, notifications, and workflows that may take a long time.

## Rules (HARD BANS)
- **Transactional outbox:** events are written to an `outbox` table in the same transaction as the state change, then published by a relay. Never publish to a broker before the database commits.
- **Consumers are idempotent:** they record processed event ids, or their effect is naturally repeatable.
- **Events are facts in past tense** (`OrderPlaced`) with a stable schema, an id, `occurredAt` and a version. Commands to another context ("ReserveStock") are messages to one owner, not broadcast events.
- **Events carry what consumers need** or an id plus a way to fetch it. Never a serialized ORM entity.
- **Failed messages go to a dead-letter queue** with the error, after bounded retries with backoff.
- **No event bus for in-process calls** inside one context. A function call is clearer there.
- **Long workflows are explicit:** a process manager or saga with its own state, not a chain of handlers nobody can see as a whole.

## Layout additions
```
<context>/adapters/
├── out/outbox/                # outbox writer used by the repository
├── out/relay/                 # reads outbox, publishes to broker
└── in/events/on-<event>       # consumer, idempotent
contracts/events/<event>.v1    # schema shared with consumers
```

## Overkill warning
In a single module with no outside consumers, say once: "Events between parts of one module add a broker, retries and eventual consistency where a function call would do."
