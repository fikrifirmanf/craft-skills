# PHP

**Detect:** `composer.json`. PHP 8.2+ (readonly classes, enums).

## Spelling the layout
- PSR-4 `App\` → `src/`. Contexts as `src/Orders/{Domain,Application,Adapters/In/Http,Adapters/Out/Persistence}`, or `src/Modules/Orders/...` for a modular monolith.
- A module's public entry is `src/Modules/<Context>/Api/` (facade classes and DTOs).
- Composition root: the container configuration (`config/services.php`, a Laravel service provider, or a plain `bootstrap.php`).
- Laravel: keep `app/Http` and `app/Models` as adapters. Put the domain in `src/` (or `app/Modules`) with no `Illuminate\` imports. Eloquent models map to and from domain objects in the persistence adapter.
- Symfony: the domain has no Doctrine attributes. Use XML/PHP mapping in the adapter, or separate Doctrine entities.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | `final readonly class OrderId` wrapping a validated UUID string |
| Value object | `final readonly class Money` with a private constructor and `public static function of(int $cents, string $currency): self` |
| Aggregate | `final class Order` with private properties, `public static function draft(...)` / `restore(...)`, no setters |
| Domain error | `final class DomainError extends \DomainException` with `public readonly string $errorCode` |
| Port | `interface OrderRepository` in Domain |
| Use case | `final readonly class PlaceOrder` with constructor-injected ports and `public function __invoke(PlaceOrderCommand $cmd): OrderId` |
| Inbound validation | Symfony Validator, a Laravel FormRequest, or a hand-written request DTO in the HTTP adapter |
| Database | PDO or Doctrine DBAL with named/positional binds in the adapter; multi-row `INSERT` for child rows |
| Tests | PHPUnit or Pest; domain tests boot no framework |

Add `declare(strict_types=1);` to every file.

## Install commands to report
```bash
composer require doctrine/dbal symfony/validator
composer require --dev phpunit/phpunit
```

## Extra boundary tooling
Deptrac layers (`Domain`, `Application`, `Adapters`) enforce the same rules in CI.
