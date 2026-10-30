# Picker

Ask all questions in one call. Translate every question, header, label and description into the user's language. Pattern names stay in English (with a translation in parentheses if it helps).

## With a structured question tool (Claude Code `AskUserQuestion`)

Limits: 1–4 questions per call, 2–4 options per question, headers of 12 characters or fewer. An "Other" choice for free text is added automatically, so never add one yourself. Previews work only on single-select questions.

### Q1: Base architecture (single-select, with previews)

Show 4 of the 6 bases: the recommended one first, then the 3 nearest to it in this order of weight: Layered/MVC → Vertical Slice → Hexagonal → Clean/Onion → Modular Monolith → Microservices. If an existing structure was detected, replace the furthest option with "Keep current (detected: …)". End the question text with the bases not shown, for example: "Other: Microservices, Vertical Slice, or your own."

| Label | Description (one line, then the reason if recommended) | Preview |
|---|---|---|
| Layered / MVC | Controllers → services → models. Fastest to build; rules spread out as the app grows. | `layered-mvc.md` Layout |
| Hexagonal | Domain in the center; database, HTTP and third parties plug in through ports and adapters. | `hexagonal.md` Layout |
| Clean / Onion | Rings of entities → use cases → adapters; one class per use case. | `clean-onion.md` Layout |
| Modular Monolith | One deployable, one module per business domain, each with its own boundary. | `modular-monolith.md` Layout |
| Microservices | One service per domain with its own data and deploy. Pays off with several teams. | `microservices.md` Layout |
| Vertical Slice | One folder per feature, from request to database; little sharing between features. | `vertical-slice.md` Layout |

Previews are the base reference's Layout tree, trimmed to 15 lines and using the user's core concept instead of `orders` when known.

### Q2: Domain modeling (single-select)

| Label | Description |
|---|---|
| Full DDD | Bounded contexts, ubiquitous language, aggregates, domain events, context map. For several domains. |
| Tactical DDD | Aggregates, value objects, repositories and domain events inside one domain. |
| Simple models | Plain data classes with validation; logic in services. For data entry and CRUD. |

### Q3: Add-ons (multi-select)

| Label | Description |
|---|---|
| CQRS | Separate write model and read model for read-heavy screens. |
| Event Sourcing | Store every change as an event; rebuild state and history from them. |
| Event-Driven | Parts react to published events instead of calling each other. |
| None | No add-ons; can be added later with a new ADR. |

Mark recommended add-ons with "(Recommended)" and a reason. If the user selects None together with others, ignore None. Ask which context an add-on applies to only if there are several contexts and the prompt does not make it obvious.

### Q4: Stack (single-select, skipped when known)

Show the 4 most likely from the prompt. With no hint, use TypeScript, Python, Go and Java/Kotlin, and end the question with "Other: Rust, C#, PHP, Ruby." Accepted values for the ADR: `typescript`, `python`, `go`, `rust`, `jvm`, `csharp`, `php`, `ruby`.

### Example (English, for a wallet idea)

```
Q1 header "Architecture"  question "Which base architecture should the wallet use? Other: Microservices, Vertical Slice, or your own."
  ● Hexagonal (Recommended)  You mentioned transfers and bank payouts: rules stay isolated from the bank API and database.
  ○ Layered / MVC            Controllers → services → models. Fastest to build; rules spread out as the app grows.
  ○ Clean / Onion            Rings of entities → use cases → adapters; one class per use case.
  ○ Modular Monolith         One deployable, one module per business domain.
Q2 header "Modeling"      ● Tactical DDD (Recommended) …
Q3 header "Add-ons"       ☑ Event Sourcing (Recommended) "every balance change must be traceable" …
Q4 skipped: go.mod found.
```

## Without a structured question tool

Print a numbered list and stop. Do not continue until the user replies.

```
Before I set up the structure, choose one option per group (for example "1b 2b 3a,3c 4a").
You can also type your own.

1. Base architecture
   a) Layered / MVC: controllers → services → models; fastest, rules spread out later
   b) Hexagonal (recommended): you mentioned transfers and bank payouts …
   c) Clean / Onion: entities → use cases → adapters
   d) Modular Monolith: one deploy, one module per domain
   e) Microservices: one service per domain, own data and deploy
   f) Vertical Slice: one folder per feature
2. Domain modeling
   a) Full DDD   b) Tactical DDD (recommended)   c) Simple models
3. Add-ons (several allowed)
   a) CQRS   b) Event Sourcing (recommended)   c) Event-Driven   d) None
4. Stack (skipped: go.mod found)
```

The same list in Bahasa Indonesia starts like this. Translate the rest the same way:

```
Sebelum saya siapkan strukturnya, pilih satu opsi per grup (misalnya "1b 2b 3a,3c 4a").
Anda juga bisa mengetik pilihan sendiri.

1. Arsitektur dasar
   a) Layered / MVC: controller → service → model; paling cepat, aturan bisnis tersebar nanti
   b) Hexagonal (disarankan): Anda menyebut transfer dan pencairan ke bank …
```

Without a tool, show all 6 bases, since the 4-option limit does not apply.
