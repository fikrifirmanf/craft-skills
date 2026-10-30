# TypeScript / JavaScript

**Detect:** `package.json`, `tsconfig.json`. Prefer TypeScript with `strict: true` for new projects.

## Spelling the layout
- kebab-case files (`place-order.ts`), PascalCase types, camelCase functions.
- Folders exactly as in the base reference: `src/modules/orders/{domain,application,adapters/in,adapters/out}`.
- A module's public entry is `src/modules/<context>/index.ts`. Other modules import only that path.
- Composition root: `src/main.ts`.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | Branded type `type OrderId = string & { readonly __brand: 'OrderId' }` with a validating `asOrderId()` |
| Value object | `class Money` with `private constructor` and `static of()`; `readonly` fields; methods return new instances |
| Aggregate | `class Order` with `private constructor`, `static draft()` / `static restore()`, private mutable state, `toSnapshot()` |
| Domain error | `class DomainError extends Error { constructor(readonly code: string) }` |
| Port | `interface OrderRepository` |
| Use case | Class with constructor-injected ports and one `execute(command)` |
| Inbound validation | Zod (or Valibot/TypeBox) `.strict()` schema; `safeParse` in the handler |
| Database | `pg` Pool with `$1` parameters; `unnest()` for bulk child rows; pool `statement_timeout` |
| Tests | `node:test` + `node:assert/strict`, or Vitest if the project uses it |

Use `import type` for ports and events so the domain has no runtime imports from other layers.

## Install commands to report
```bash
npm install pg zod
npm install -D typescript tsx @types/node @types/pg
```
Add a framework (`express`, `fastify`, `@nestjs/core`, `hono`) only if the user named one. Its code lives in `adapters/in/http` and `main.ts`.

## Extra boundary tooling
`dependency-cruiser` can enforce the same rules in CI if the project wants it. Path aliases (`@/modules/...`) are fine; the checker reads the folder names in them.
