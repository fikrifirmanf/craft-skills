# Ruby

**Detect:** `Gemfile`, `config/application.rb` (Rails). Ruby 3.2+.

## Spelling the layout
- Plain Ruby: `lib/shop/orders/{domain,application,adapters}/`, loaded with Zeitwerk or `require_relative`.
- Rails: put contexts under `app/modules/orders/{domain,application,adapters}/`. Since `app/modules` is an autoload root, `app/modules/orders/domain/order.rb` defines `Orders::Domain::Order`. Controllers in `app/controllers` and ActiveRecord classes count as adapters.
- A module's public entry is `app/modules/<context>/api.rb` (`Orders::Api`).
- Composition root: an initializer (`config/initializers/container.rb`) or `lib/shop/container.rb`.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | `OrderId = Data.define(:value)` with validation in `initialize` |
| Value object | `Money = Data.define(:cents, :currency)` with a validating `initialize`; operations return new instances |
| Aggregate | Plain class (`class Order`) with `attr_reader` only, `self.draft` / `self.restore`, frozen exposed collections. **Never** inherits `ApplicationRecord` |
| Domain error | `class DomainError < StandardError` with `attr_reader :code` |
| Port | Duck-typed: document the repository methods in a module (`Orders::Domain::OrderRepository`) and test fakes against the same examples |
| Use case | `class PlaceOrder` with injected ports and `call(command)` |
| Inbound validation | `dry-validation`/`dry-schema` contract, or Rails strong parameters plus a form object, in the controller adapter |
| Database | An ActiveRecord class (`Orders::Adapters::Persistence::OrderRecord`) mapped to and from the domain object; `insert_all` for child rows |
| Tests | RSpec or Minitest; domain specs `require` only domain files and need no database |

No bare `rescue`; rescue specific errors.

## Install commands to report
```bash
bundle add dry-validation
bundle add rspec --group "development, test"
```

## Extra boundary tooling
Rails autoloading means most code has no `require` lines, so `check_boundaries.py` sees only `require` statements and `< ApplicationRecord` in the domain. Recommend `packwerk` to enforce constant-level boundaries between packs.
