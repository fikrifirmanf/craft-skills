# Go

**Detect:** `go.mod`.

## Spelling the layout
- `cmd/api/main.go` is the composition root.
- `internal/orders/{domain,application,adapters/http,adapters/postgres}/`. Using `internal/` lets the compiler stop other modules from importing the code.
- A modular monolith uses `internal/modules/<context>/`, and its public entry is a package `internal/modules/<context>/api`.
- Package names are short and lower case (`domain`, `application`, `postgres`). Files are snake_case.
- Define interfaces where they are consumed: the repository port in `domain` (or `application`), not in `postgres`.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | `type OrderID string` with `ParseOrderID(s string) (OrderID, error)` |
| Value object | Struct with unexported fields; `NewMoney(cents int64, currency string) (Money, error)`; methods on value receivers return new values |
| Aggregate | Struct with unexported fields; `NewDraftOrder(...)` and `RestoreOrder(snapshot)`; methods on pointer receivers return `error` |
| Domain error | `type Error struct{ Code string }` implementing `error`, plus sentinel values (`ErrEmptyOrder`) checked with `errors.Is` |
| Port | `type OrderRepository interface { Exists(ctx, id) (bool, error); FindByID(...); Save(ctx, *Order) error }` |
| Use case | Struct holding ports, `func (uc *PlaceOrder) Execute(ctx context.Context, cmd PlaceOrderCommand) (OrderID, error)` |
| Inbound validation | Decode with `DisallowUnknownFields`, then `go-playground/validator` or explicit checks in the HTTP adapter |
| Database | `pgx/v5` pool with `$1` parameters; `unnest` or `CopyFrom` for child rows; `context.WithTimeout` per call |
| Tests | `testing` package; `_test.go` beside the code; table-driven domain tests |

Every function that does I/O takes `ctx context.Context` first. Never discard an error with `_`.

## Install commands to report
```bash
go get github.com/jackc/pgx/v5
go get github.com/go-playground/validator/v10
```
Add `chi`, `gin` or `echo` only if named. Use `net/http` with `http.ServeMux` patterns otherwise.

## Extra boundary tooling
`go-arch-lint`, or a test that lists `go list -deps ./internal/orders/domain` and fails on adapter or driver packages.
