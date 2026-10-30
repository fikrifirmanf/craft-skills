---
tags: [skill-creator]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, AskUserQuestion]
---

Add the ability to cancel an order. Only orders that are placed but not yet shipped can be cancelled.

Input files: docs/adr/0001-architecture.md, package.json, src/shared/kernel/domain-error.ts, src/modules/orders/index.ts, src/modules/orders/domain/{order,order-events,order-repository}.ts, src/modules/orders/application/place-order.ts, src/modules/orders/adapters/out/postgres/postgres-order-repository.ts
