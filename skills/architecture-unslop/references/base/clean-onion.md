# Clean / Onion

## Picker card
Concentric rings: entities → use cases → interface adapters → frameworks. Each use case is its own class with an input and output model; dependencies only point inward.

## When it fits
The same situations as Hexagonal, when the team wants explicit use-case classes and request/response models, or already knows Clean Architecture. Common in mobile and in .NET and Java backends.

## Rules (HARD BANS)
- **Inward only:** `frameworks` → `adapters` → `usecases` → `entities`. A ring never names anything in an outer ring.
- **Entities hold enterprise rules** and import nothing but the shared kernel.
- **One use case per class/file** (`PlaceOrder`), with a single public `execute`/`handle`. No `OrderUseCases` grab-bag.
- **Use cases take and return plain models** (`PlaceOrderInput`, `PlaceOrderOutput`), never HTTP requests, ORM rows or framework types.
- **Gateways are interfaces in the use-case ring,** implemented in `adapters`.
- **Presenters/controllers live in `adapters`;** the framework (router, ORM setup, DI container) lives in `frameworks` or `main`.
- **No framework annotations in entities or use cases** (`@Entity`, `@Injectable`, `[Table]`). Put them on adapter classes.

## Layout
```
src/
├── main                                  # frameworks ring: server, DI, config
├── entities/
│   ├── order
│   └── money
├── usecases/
│   └── place-order/
│       ├── place-order                   # interactor
│       ├── place-order-input
│       ├── place-order-output
│       └── order-gateway                 # interface
├── adapters/
│   ├── controllers/place-order-controller
│   ├── presenters/order-presenter
│   └── gateways/postgres-order-gateway
└── frameworks/
    └── db/migrations/
tests/
└── {entities,usecases}/
```
The boundary checker reads `entities` as the domain layer and `usecases` as the application layer.

## Overkill warning
For CRUD, say once: "Each endpoint needs an input model, output model, interactor, gateway and presenter; Layered/MVC covers this with a controller and a service."
