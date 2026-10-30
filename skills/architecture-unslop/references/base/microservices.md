# Microservices

## Picker card
One service per bounded context, each with its own code, database and deploy. Teams ship independently, at the cost of network calls, distributed data and operations work.

## When it fits
Several teams who need to deploy independently, parts with very different scaling or availability needs, or parts that must use different technology. Without one of these, a Modular Monolith gives the same boundaries for less.

## Rules (HARD BANS)
- **Database per service.** No service reads or writes another service's database, not even read-only.
- **No shared domain library.** Share only contracts (OpenAPI, protobuf, event schemas) and generic utilities.
- **Every remote call has a timeout,** a retry policy only for idempotent operations, and a fallback or a clear error.
- **No synchronous call chains longer than two hops** for one user request. Use events or a read-model copy instead.
- **Cross-service workflows use events or a saga,** never a distributed transaction.
- **Events and APIs are versioned;** a consumer tolerates added fields.
- **Each service is internally Hexagonal or Clean** and has its own composition root, migrations, config and health check.
- **Correlation id on every request and message,** propagated through logs.

## Layout
```
services/
├── orders/
│   ├── src/
│   │   ├── main
│   │   ├── domain/
│   │   ├── application/
│   │   └── adapters/
│   │       ├── in/{http,events}/
│   │       └── out/{postgres,billing-client}/
│   ├── migrations/
│   └── tests/
└── billing/
    └── (same shape)
contracts/
├── openapi/orders.yaml
└── events/order-placed.v1.json
```

## Overkill warning
With one team and no deploy or scaling reason, say once: "Every call between domains becomes a network call with retries, timeouts and partial failure, and you run N deploy pipelines; a Modular Monolith keeps the same boundaries and can be split later."
