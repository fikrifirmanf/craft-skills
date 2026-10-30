# Hexagonal (Ports & Adapters)

## Picker card
The domain sits in the center. Database, HTTP, queues and third parties plug in through ports (interfaces) and adapters (implementations), so each can be swapped or faked in tests.

## When it fits
Real business rules, money, external systems (payment gateways, legacy APIs), or a need to test rules without infrastructure. The default once an idea has more than CRUD.

## Rules (HARD BANS)
- **Domain imports nothing outside itself** and the shared kernel: no ORM, driver, HTTP, queue, framework, logger, environment or system clock.
- **Application imports domain and its own ports only.** Never an adapter.
- **Driven ports** (repository, gateway, clock, id generator, event publisher) are interfaces in the domain or `application/ports`. **Driving ports** are the use cases themselves.
- **Adapters are split by direction:** `adapters/in` (HTTP, CLI, consumers) call use cases; `adapters/out` (database, HTTP clients, queues) implement driven ports.
- **No ORM entities as domain objects.** The out-adapter maps rows ↔ aggregates.
- **One composition root** creates adapters and injects them. No service locator, and no `new PostgresRepo()` inside a use case.
- **Third-party models stop at the adapter.** A Stripe or SAP type never appears in a port signature. Map it to a domain type (anti-corruption layer).

## Layout
```
src/
├── main                                # composition root
├── shared/kernel/domain-error
└── orders/                             # or modules/orders when a second domain appears
    ├── domain/
    │   ├── order                       # aggregate root
    │   ├── money                       # value object
    │   ├── order-events
    │   └── order-repository            # driven port
    ├── application/
    │   ├── place-order                 # use case = driving port
    │   └── ports/product-catalog       # driven port for outside data
    └── adapters/
        ├── in/http/place-order-handler
        └── out/
            ├── postgres/postgres-order-repository
            └── catalog/http-product-catalog
tests/
└── orders/{domain,application}/
```

## Overkill warning
For CRUD with no rules (an admin panel, a blog), say once: "Every table gets a port, an adapter and mapping code with no rule to protect; Layered/MVC does this with a third of the files."
