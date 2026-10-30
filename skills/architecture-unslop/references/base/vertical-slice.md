# Vertical Slice

## Picker card
One folder per feature holds everything that feature needs, from request to database. Features change independently; shared code stays minimal.

## When it fits
Many endpoints or commands with little shared logic, feature teams, or a codebase where layered folders made every change touch five places. Often paired with CQRS-style command and query handlers.

## Rules (HARD BANS)
- **One folder per feature** (`features/place-order/`), holding handler, request/command, validator, data access and tests.
- **No imports between feature folders.** Shared needs go to `shared/` (domain types, `DomainError`) only when two or more features need them.
- **A feature may talk to the database directly** through the project's data access, but rules that several features must agree on live in a domain type in `shared/domain`, not copied.
- **No generic `services/` or `repositories/` folder** collecting code from every feature.
- **Each feature validates its own input** at its entry point.

## Layout
```
src/
├── main                                 # registers every feature's route/handler
├── shared/
│   ├── domain/{order,money}             # rules more than one feature relies on
│   └── kernel/domain-error
└── features/
    ├── place-order/
    │   ├── place-order-handler
    │   ├── place-order-command          # + schema
    │   ├── place-order-data             # queries for this feature only
    │   └── place-order.test
    └── get-order-summary/
        ├── get-order-summary-handler
        └── get-order-summary-query
```
The boundary checker treats each folder under `features/` as its own context, so imports between features are flagged.

## Overkill warning
With a handful of endpoints sharing most rules, say once: "Shared rules will either be copied between slices or pulled back into shared folders; Hexagonal keeps them in one domain."
