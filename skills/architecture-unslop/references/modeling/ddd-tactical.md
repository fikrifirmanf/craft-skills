# Tactical DDD

## Picker card
Aggregates, entities, value objects, repositories and domain events inside one domain, so rules live with the data they protect.

## When it fits
One domain with real invariants: totals that must add up, state machines, limits, approvals, money.

## Rules (HARD BANS)
- **No anemic models.** Behavior lives on the aggregate (`order.place()`), not in a service that sets fields (`order.status = 'placed'`). No public setters.
- **Invariants are enforced inside the aggregate root.** Child entities are changed only through the root.
- **One aggregate per transaction.** Other aggregates are updated afterwards through domain events.
- **Reference other aggregates by id,** never by object.
- **Keep aggregates small:** only what must be consistent together. A list that can grow without limit is a separate aggregate.
- **Value objects are immutable and self-validating** (`Money`, `Email`, `Quantity`, `DateRange`). No raw strings or numbers for domain concepts that carry rules.
- **Repositories exist per aggregate root only** and load or save whole aggregates. No `OrderLineRepository`, and no generic `BaseRepository<T>` exposing `update(field)`.
- **Domain events are past tense** (`OrderPlaced`), carry facts, and are recorded by the aggregate, then published by the application or outbox after commit.
- **Domain services only** for rules that span aggregates and belong to none of them. They are stateless and named in domain language.
- **Factories** (`Order.draft`, `Order.restore`) separate creating a new aggregate from rehydrating a stored one.
- **No time or randomness inside the domain:** pass `now` and ids in.

## Overkill warning
For data entry with no invariants, say once: "Aggregates and value objects add mapping code with no rule to protect; Simple models are enough until rules appear."
