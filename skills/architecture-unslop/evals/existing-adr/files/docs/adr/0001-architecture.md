<!-- architecture-unslop -->
# ADR-0001: Architecture for Shop

- Status: Accepted
- Date: 2026-10-01
- Supersedes: none

## Decision

| Key | Value |
|---|---|
| base | hexagonal |
| modeling | ddd-tactical |
| addons | none |
| stack | typescript |
| framework | none |

## Context

"An online shop where customers place orders and the warehouse ships them."

Signals: business rules (order states), external system (warehouse)

## Why

Order states and shipping rules need to stay out of the database and HTTP code.

## Consequences

- Domain rules are tested without a database.
- Each new storage or API integration needs a port and an adapter.

## Rules in force

- references/base/hexagonal.md
- references/modeling/ddd-tactical.md
- references/stacks/typescript.md

## Bounded contexts

| Context | Owns | Talks to others through |
|---|---|---|
| orders | orders, order lines | src/modules/orders/index.ts |
