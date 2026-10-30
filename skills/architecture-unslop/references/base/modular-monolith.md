# Modular Monolith

## Picker card
One deployable, one database server, but one module per business domain with hard boundaries. Modules can be split into services later without a rewrite.

## When it fits
Two or more distinct domains (orders and billing, HR and payroll) with one team or a few teams, or any case where Microservices were considered without a deploy or team reason.

## Rules (HARD BANS)
- **One module per bounded context** under `modules/` (or `contexts/`). Each module is internally Hexagonal or Clean.
- **A module's public entry is its only door:** an `index`/`api` file or package exporting use cases, command/query types and event types. Other modules never import its `domain`, `application` or `adapters`.
- **No shared tables.** Each module owns its tables (a schema or table prefix per module). Another module's data is read through its public API or a copy kept up to date by events, never by JOIN across modules.
- **No shared domain objects.** Only the shared kernel (ids, `Money`, `DomainError`) is shared, and it stays small.
- **Cross-module writes do not share a transaction.** Use events (outbox) or a process manager for multi-module workflows.
- **No circular module dependencies.** If A calls B and B calls A, one direction becomes an event.

## Layout
```
src/
├── main                                 # composition root: wires every module
├── shared/kernel/                       # ids, Money, DomainError only
└── modules/
    ├── orders/
    │   ├── index                        # public API: PlaceOrder, OrderPlaced
    │   ├── domain/
    │   ├── application/
    │   └── adapters/{in,out}/
    └── billing/
        ├── index
        ├── domain/
        ├── application/
        └── adapters/
            └── in/events/on-order-placed     # reacts to orders, never imports its internals
tests/
└── modules/{orders,billing}/
```

## Overkill warning
With a single domain, say once: "There is only one module to separate; start with Hexagonal in one folder and add `modules/` when a second domain appears."
