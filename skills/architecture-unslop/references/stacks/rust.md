# Rust

**Detect:** `Cargo.toml`.

## Spelling the layout
- Single crate: `src/orders/{domain,application,adapters}/` with `mod.rs` (or `orders/domain.rs` files), `src/main.rs` as the composition root.
- Strongest option: a Cargo workspace with one crate per layer, so the compiler enforces the dependency rule:
  ```
  crates/orders/domain/        # package orders-domain: no sqlx, no axum in Cargo.toml
  crates/orders/application/   # depends on orders-domain only
  crates/orders/adapters/      # depends on both, plus sqlx/axum
  crates/app/                  # binary: composition root
  ```
  Keep the folder names `domain`, `application`, `adapters` so the boundary checker recognises them.
- A module's public entry is its `lib.rs` or `mod.rs` with `pub use` of the use cases and types it exposes; everything else stays `pub(crate)`.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | Newtype `pub struct OrderId(Uuid)` with `TryFrom<&str>` |
| Value object | Newtype or struct with private fields, `Money::new(cents: i64, currency: Currency) -> Result<Self, DomainError>`; `#[derive(Clone, PartialEq, Eq)]` |
| Aggregate | Struct with private fields; `Order::draft(...)`, `Order::restore(snapshot)`; `&mut self` methods returning `Result<(), DomainError>` |
| Domain error | `#[derive(Debug, thiserror::Error)] enum DomainError { #[error("EMPTY_ORDER")] EmptyOrder, ... }` with a `code()` method |
| Port | `trait OrderRepository` with `async fn` methods. Use generics (`PlaceOrder<R: OrderRepository>`) for static dispatch, or `#[async_trait]` when `dyn` is needed |
| Use case | Struct generic over its ports with `async fn execute(&self, cmd: PlaceOrderCommand) -> Result<OrderId, PlaceOrderError>` |
| Inbound validation | `serde` with `#[serde(deny_unknown_fields)]` plus `validator` or `garde` in the HTTP adapter |
| Database | `sqlx` with `$1` binds and `UNNEST` for child rows; pool `acquire_timeout`; `tokio::time::timeout` around outbound calls |
| Tests | `#[cfg(test)] mod tests` in domain files; `#[tokio::test]` with in-memory fakes for use cases |

No `.unwrap()` or `.expect()` outside tests; propagate with `?`.

## Install commands to report
```bash
cargo add thiserror uuid --features uuid/v4
cargo add sqlx --features runtime-tokio,postgres,uuid -p orders-adapters
cargo add tokio --features full
```
Add `axum` or `actix-web` only if named, and only to the adapters crate.
