# Example slice

One feature, built end to end through every layer, so the user sees the pattern working rather than empty folders. Build it around the core concept of the user's idea. `Order` with "place order" is the fallback.

## Pick the slice

Choose the one command that best shows a business rule: `PlaceOrder`, `TransferFunds`, `BookAppointment`, `SubmitClaim`, `ApproveLeave`. Prefer a command with at least two invariants and a state change. Avoid a pure read or a plain create with no rules.

## Files per layer (Hexagonal / Clean / Modular Monolith)

| Layer | File | Must contain |
|---|---|---|
| Shared kernel | `domain-error` | One error type carrying a stable code (`EMPTY_ORDER`), with no HTTP status inside |
| Domain | value object (`Money`, `Email`, `TimeSlot`) | Private constructor or validated factory, immutable, equality by value, operations that return new instances |
| Domain | aggregate (`Order`) | Factory for new (`draft`) and for rehydration (`restore`), at least two invariants enforced in methods, a state change, no public setters, pending domain events, and a snapshot for persistence |
| Domain | events | Past-tense event (`OrderPlaced`) with id, the facts, and `occurredAt` passed in (never read from the system clock inside the domain) |
| Domain | repository port | Interface for whole aggregates only: `exists`, `findById`, `save` |
| Application | use case (`PlaceOrder`) | Takes a command, loads or creates the aggregate, calls domain methods, saves; clock and other outside data come in through ports or constructor arguments; idempotent on a client-supplied id |
| Application | one more port if the idea needs outside data | e.g. `ProductCatalog.pricesFor(ids)`: batched, never one call per item |
| Inbound adapter | HTTP handler or controller | Strict input schema, identity from auth (never from the body), one use case call, domain error code → 4xx, unknown errors rethrown to the framework's error handler |
| Outbound adapter | repository implementation | Explicit columns, bound parameters, bulk insert for child rows, one transaction per aggregate, row ↔ aggregate mapping in the adapter |
| Outbound adapter | migration | Tables for the aggregate, plus an `outbox` table only when Event-Driven or Event Sourcing was picked |
| Composition root | `main` | Builds adapters, injects them into use cases, sets database and HTTP timeouts. The only place that knows every concrete class |
| Tests | domain test | At least: the happy path computes the right result; each invariant rejects bad input with its code; the state change records exactly one event; a forbidden transition is rejected |
| Tests | use case test | In-memory fakes for every port; a retry with the same id does not create a second aggregate |

## Variations by choice

| Choice | Change to the slice |
|---|---|
| Layered / MVC + Simple models | `controllers/` → `services/` → `models/` + `repositories/`. Validation in the controller; rules in the service; still no SQL in controllers. Domain and use case tests become service tests with a fake repository. |
| Vertical Slice | All files for the feature in `features/<feature>/` (handler, command, validator, data access, test). Only true shared code (`Money`, `DomainError`) in `shared/`. |
| Clean / Onion | `entities/` instead of `domain/`, `usecases/` instead of `application/`, one input and output port per use case. |
| Modular Monolith | The slice lives in `modules/<context>/`. Add the module's public `index`/`api` entry exporting only the use case and its command type. |
| Microservices | The slice is one service: its own `main`, migration and config. Other services are reached through an HTTP or message client adapter, never shared code. |
| Full DDD | Add a `context-map.md` beside the modules listing each context, what it owns, and how it talks to others. |
| Tactical DDD / Simple models | No context map. |
| CQRS | Add one query (`GetOrderSummary`) with its own read model and a query handler that reads from a view or projection table; the command side returns only the id. |
| Event Sourcing | The repository appends events with an expected version and rebuilds the aggregate by replaying them; no `status` column update. Add a projection for the read side. |
| Event-Driven | Save events to the `outbox` in the same transaction; add a relay that publishes them and one consumer in another context that handles `OrderPlaced` idempotently. |

## Shape reference (TypeScript, Hexagonal)

The aggregate's public surface, which the other stacks mirror in their own idiom:

```ts
export class Order {
  static draft(id: OrderId, customerId: string, currency: string): Order;
  static restore(snapshot: OrderSnapshot): Order;
  addLine(productId: string, quantity: number, unitPrice: Money): void; // throws DomainError
  place(at: Date): void;                                                 // records OrderPlaced
  total(): Money;
  pendingEvents(): readonly OrderPlaced[];
  clearEvents(): void;                                                   // after the transaction commits
  toSnapshot(): OrderSnapshot;
}
```

## Report after scaffolding

List the files created, the files skipped because they existed, the install commands the user must run, and how to run the domain tests and the boundary check.
