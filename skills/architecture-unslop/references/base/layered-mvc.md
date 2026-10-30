# Layered / MVC

## Picker card
Controllers → services → models. Fastest to build and easiest to hire for; business rules spread across services as the app grows.

## When it fits
CRUD, admin panels, back offices, content sites, MVPs and prototypes, with few business rules (roughly fewer than five non-trivial ones) and one domain.

## Rules (HARD BANS)
- **Calls go one way:** controller → service → repository/model. A repository never calls a service; a service never touches the request or response objects.
- **No SQL or ORM queries in controllers or views.** Queries live in repositories or model scopes.
- **No business rules in controllers.** A controller parses, validates, calls one service method and maps the result.
- **Services are named after what they do** (`InvoiceIssuer`, `issue_invoice`), not `InvoiceManager` or `InvoiceHelper`.
- **No god service:** split a service when it passes about 300 lines or serves more than one resource.
- **Validation at the boundary** with the stack's schema library before the service is called.

## Layout
```
src/
├── main                       # wiring, server start, timeouts
├── controllers/
│   └── orders-controller      # parse → validate → service → response
├── services/
│   └── order-service          # rules and transactions
├── repositories/
│   └── order-repository       # queries only
├── models/
│   └── order                  # data shape + simple validation
└── migrations/
tests/
└── services/order-service.test
```
With a framework (Laravel, Rails, Django, Spring MVC), use its folder names and keep the same direction of calls.

## Overkill warning
Never overkill. Warn the other way: if the idea has money, approvals, multi-step workflows or several domains, say once that rules will spread across services and Hexagonal would contain them.
