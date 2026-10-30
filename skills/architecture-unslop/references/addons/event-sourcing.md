# Event Sourcing

## Picker card
Store every change as an immutable event. Current state is rebuilt by replaying events, so the full history is always available.

## When it fits
History is a requirement: ledgers, wallets, audits, compliance, undo or "what did this look like on date X". Apply it only to the context that needs history.

## Rules (HARD BANS)
- **Events are immutable.** Never update or delete a stored event. Fix mistakes with a compensating event.
- **Append with an expected version** (optimistic concurrency). A version conflict is retried or rejected, never overwritten.
- **Events are versioned.** A schema change gets a new version and an upcaster. Old events must still load.
- **Aggregates rebuild only from their own events:** `apply(event)` changes state and has no side effects or I/O.
- **Decisions happen before events.** Command methods check rules, then record events; `apply` never rejects.
- **Reads come from projections (CQRS),** not from replaying aggregates on every query.
- **Snapshots are an optimization only,** added when replay is measured to be slow, and always rebuildable.
- **Personal data in events** goes in a separate store referenced by id, or is encrypted with a per-subject key, so erasure requests can be honored.

## Layout additions (per context)
```
domain/
└── order                       # decide → record events; apply(event)
adapters/out/
├── event-store/                # append(streamId, expectedVersion, events), load(streamId)
└── projections/
```

## Overkill warning
Without a history or audit need, say once: "Every state change needs an event, an apply method, versioning and projections, and simple fixes become compensating events; store current state and add an audit table instead."
