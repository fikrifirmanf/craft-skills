# Simple models

## Picker card
Plain data classes or records with validation. Logic lives in services. Quick to write and easy to read for CRUD.

## When it fits
Data entry, listings, admin tools, content, and prototypes, where most operations are create, read, update and delete with field validation.

## Rules (HARD BANS)
- **Validate on the way in** with a schema at the boundary, and again in the model for invariants that must always hold (non-negative price, required fields).
- **One service method per business operation** (`publishPost`, `archiveProduct`), not a generic `update(entity)` used for everything.
- **Status changes go through a named method** that checks the allowed transitions, even in a service. No raw `status = x` from controllers.
- **Money is never a float.** Use integer minor units or a decimal type.
- **Promote to Tactical DDD** when a model gains several invariants or a state machine. Record that in a new ADR.

## Overkill warning
Never overkill. Warn the other way: if the idea has money flows, approvals or multi-step states, say once that rules will scatter across services and Tactical DDD keeps them in one place.
