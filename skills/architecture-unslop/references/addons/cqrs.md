# CQRS

## Picker card
Separate the write side (commands that change state through the domain) from the read side (queries served from models shaped for screens).

## When it fits
Read-heavy screens such as dashboards, reports, search, feeds and lists that join many things, or reads that scale very differently from writes. Apply it per context, not to the whole system.

## Rules (HARD BANS)
- **Commands change state and return nothing or only an id.** Queries never change state.
- **Queries skip the domain model.** They read a view, projection table or search index directly and return DTOs shaped for the screen.
- **Read models are disposable:** they can be rebuilt from the write side or the event stream, and are never the source of truth.
- **Projections are idempotent** (keyed by event id or version) and tolerate events arriving more than once.
- **Say where reads may be stale.** If the read side updates asynchronously, the UI or API documents it (return the new id, then poll or redirect).
- **One handler per command or query.** No `OrderQueries` class with twenty methods.

## Layout additions (per context)
```
application/
├── commands/place-order
└── queries/
    ├── get-order-summary          # handler + DTO
    └── order-summary-projection   # updates the read table from events
adapters/out/postgres/
└── order-summary-view             # read table or SQL view
```

## Overkill warning
When reads are simple lookups of what was written, say once: "A second model and its projections add sync code and stale-read cases with no gain; query the write tables until a screen needs a different shape."
