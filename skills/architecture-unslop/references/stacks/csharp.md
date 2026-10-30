# C# / .NET

**Detect:** `*.sln`, `*.csproj`, `global.json`. .NET 8+.

## Spelling the layout
- One project per layer, so project references enforce the direction:
  ```
  src/Shop.Orders.Domain/          # no package references to EF Core or ASP.NET
  src/Shop.Orders.Application/     # references Domain
  src/Shop.Orders.Adapters/        # references both; EF Core, HTTP clients (or name it Infrastructure)
  src/Shop.Api/                    # Program.cs composition root, endpoints
  tests/Shop.Orders.Domain.Tests/
  ```
  The checker splits `Shop.Orders.Domain` on dots, so these names are recognised.
- A modular monolith repeats the set per module (`Shop.Billing.*`), and other modules reference only `Shop.<Module>.Contracts`.
- PascalCase everything; one public type per file.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | `readonly record struct OrderId(Guid Value)` |
| Value object | `sealed record Money` with a private constructor and `static Money Of(long cents, string currency)` that validates |
| Aggregate | `sealed class Order` with `private` setters, `static Draft(...)` / `Restore(snapshot)`, `IReadOnlyList<OrderLine>` exposed |
| Domain error | `sealed class DomainException(string code) : Exception(code) { public string Code { get; } = code; }` |
| Port | `interface IOrderRepository` in Domain |
| Use case | `sealed class PlaceOrder` with injected ports and `Task<OrderId> Execute(PlaceOrderCommand cmd, CancellationToken ct)` |
| Inbound validation | FluentValidation or DataAnnotations on the request DTO in the API project |
| Database | EF Core `DbContext` and Fluent configuration (`IEntityTypeConfiguration<T>`) in Adapters, mapping to domain types without attributes in Domain; or Dapper with `@param` binds. Command timeout set in `Program.cs` |
| Tests | xUnit; Domain tests reference only the Domain project |

Pass `CancellationToken` through every async call.

## Install commands to report
```bash
dotnet new sln -n Shop
dotnet add src/Shop.Orders.Adapters package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add src/Shop.Api package FluentValidation
```

## Extra boundary tooling
NetArchTest tests (`Types.InAssembly(...).ShouldNot().HaveDependencyOn("Microsoft.EntityFrameworkCore")`).
