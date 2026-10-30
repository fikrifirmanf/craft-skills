---
name: architecture-unslop
description: Lets the user pick a backend architecture from an explained menu (Layered/MVC, Hexagonal, Clean/Onion, Modular Monolith, Microservices, Vertical Slice, DDD, CQRS, Event Sourcing, Event-Driven) with a recommendation drawn from their idea, records the choice as an ADR, scaffolds the folders with one working example slice, then enforces the chosen boundaries. Use when starting a backend project, service or module, adding a bounded context or a feature that crosses modules, designing aggregates, repositories or domain events, or when the user mentions architecture, DDD, bounded contexts, clean or hexagonal architecture, CQRS or event sourcing. Skip for small fixes inside an existing structure.
---

# Architecture Anti-Slop Protocol

Never apply patterns by default. Let the user choose with the trade-offs in front of them, recommend the lightest option that handles their idea, record the decision, and then hold every later change to it.

Speak the user's language in every question, option, explanation and in the ADR prose. Keep pattern names (Hexagonal, CQRS) and the ADR's decision table keys and values in English.

## 1. Check for a saved decision first

```bash
python3 <skill-dir>/scripts/find_adr.py <repo-root>
```

| Result | Action |
|---|---|
| `found: true` | Do not show the picker. Read the references listed for `active`, then go to §6. |
| `conflicts` not empty | Several ADRs say Accepted. Ask which one holds, and mark the others superseded. |
| `found: false`, and this is a new project, service, module or bounded context, or the user asks to choose | Go to §2. |
| `found: false`, small change in an existing codebase | Follow the structure already there. Mention once that the user can ask to record or change the architecture. Do not block the change on the picker. |
| The user asks to change the architecture, or asks for something the ADR rules out (adding CQRS, splitting a service) | Go to §2. The new ADR supersedes the old one (§4). |

## 2. Understand the idea

1. Read the user's prompt for signals using `references/signals.md`. Recommend from the prompt, not from habit.
2. If the prompt does not say what the software does, ask one short question in the user's language first, for example "What will the app do, and who uses it?" Do not show the picker until you have an answer, because a recommendation without signals is a guess.
3. Detect the stack from the prompt, or from the repo: `package.json`/`tsconfig.json`, `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`/`build.gradle(.kts)`, `*.csproj`/`*.sln`, `composer.json`, `Gemfile`.
4. Look up `references/domain-notes.md` for signals such as money, payouts, audit, booking or webhooks. Matching notes go into the picker's intro line (§3) and the ADR (§4), because the right architecture still needs the right domain rules.
5. Detect any existing structure (folders named `domain`, `application`, `adapters`, `modules`, `controllers`, `models`). If one exists, include "Keep current (detected: …)" as an option.

## 3. Show the picker

Read `references/picker.md` for the exact questions, option wording, previews and fallback, then ask everything in **one** call:

| # | Question | Kind | Options |
|---|---|---|---|
| 1 | Base architecture | single, with folder-tree preview | recommended first, plus the 3 nearest; the rest via Other |
| 2 | Domain modeling | single | Full DDD, Tactical DDD, Simple models |
| 3 | Add-ons | multi-select | CQRS, Event Sourcing, Event-Driven, None |
| 4 | Stack | single | Skip when the prompt or repo already names it |

- Open with one short intro line in the user's language: the signals you read, plus any domain notes (at most three, from `references/domain-notes.md`).
- Put the recommended option first, label it "(Recommended)", and put the reason in its description, tied to the user's own words.
- With a structured question tool (`AskUserQuestion` in Claude Code), its "Other" choice is the manual entry. Without one, print the numbered fallback from `references/picker.md` and wait for the reply. Do not continue until the user answers.

### Respond to the pick

- **Overkill.** If the pick matches a pattern's "Overkill warning" in its reference, warn once in two sentences, naming the cost and the lighter option. If the user keeps their choice, follow it and record the warning in the ADR. Never argue twice.
- **Invalid combination.** Event Sourcing without CQRS needs read models anyway, so offer to add CQRS for that context. Full DDD with Layered/MVC puts the domain at the bottom of a layer cake, so offer Hexagonal or Clean. Ask once.
- **Other.** Accept any pattern the user types. If no reference exists for it, apply §6's general rules, write its own boundary rules into the ADR, and tell the user there is no dedicated reference.

## 4. Record the decision

Fill `assets/adr.md.template` and write it to `suggested_path` from `find_adr.py`. If the repo already keeps ADRs in another format, write in that folder and keep the template's marker line and decision table.

To supersede an earlier ADR, change only its status line to `Superseded by ADR-NNNN`, and fill `Supersedes` in the new one. Never delete old ADRs.

## 5. Scaffold with one example slice

Read the picked base reference's Layout section, `references/stacks/<stack>.md` and `references/example-slice.md`.

1. **Show the full tree first,** marking new files and existing ones that will be skipped. Create nothing until the user confirms.
2. **Never overwrite.** Skip files that exist and list them in the final report.
3. **One vertical slice through every layer,** built around the core concept of the user's idea (a `Transfer` for a wallet, a `Booking` for a clinic). Use `Order` only when the idea has no clearer core. The slice includes one value object, one aggregate with real invariants, the repository port and one adapter, one use case, one inbound adapter, domain tests that run without I/O, and a use case test with in-memory fakes.
4. **Framework-neutral** unless the user or repo names a framework. Then follow that framework's conventions at the edges only. The domain stays free of it.
5. **No installs.** Do not run package managers. List the commands the user needs (`npm install pg zod`, `go get …`) in the report.
6. Line-level backend rules (parameterized SQL, input validation, timeouts, no swallowed errors) come from `backend-unslop` when it is installed. Follow them in the slice either way.

## 6. Enforce the boundaries on every change

These rules hold for any choice that has a domain layer. The picked references add their own HARD BANS.

- **Dependencies point inward:** adapters → application → domain. The domain imports no ORM, HTTP, queue, framework, environment or clock.
- **Ports in the core, adapters at the edge.** Repository and gateway interfaces sit in the domain or application layer. Their implementations sit in adapters.
- **Thin inbound adapters:** validate, call one use case, map the result. No business rules in handlers or controllers.
- **One module per bounded context.** Another context is reached only through its public entry (`index`, `api` package, published events), never its internals or its tables.
- **Ubiquitous language.** Name things after the business term. No `Manager`, `Helper`, `Util` or `Processor` in the domain.
- **New features follow the ADR.** If a request would break it, say which decision it breaks and offer to update the ADR. Do not quietly bend the structure.

## 7. Verify before claiming done

1. Run the boundary check on the changed source roots:
   ```bash
   python3 <skill-dir>/scripts/check_boundaries.py src/
   ```
   It recognises layers and contexts by folder name in TypeScript/JavaScript, Python, Go, Rust, Java/Kotlin, C#, PHP and Ruby, and skips test files.
2. On `status: FAIL`, fix each ERROR at its root: move the code, add a port, or go through the other context's public entry. Re-run until `PASS`.
3. A verified false positive may be suppressed on the line or the line above with `unslop-ignore RULE_ID -- why this is safe`. A suppression without a reason is itself an ERROR.
4. `status: SKIPPED` means no layer or module folders were found, so nothing was verified. Say so, and never report it as passing.
5. If the project already has an architecture linter (dependency-cruiser, import-linter, ArchUnit, NetArchTest, Deptrac, go-arch-lint), run it too.
6. Run the project's build and tests. Domain tests must pass without a database, network or framework. If one needs them, the dependency rule is broken.

## Read references only when needed

| Need | Reference |
|---|---|
| Turning the prompt into a recommendation | `references/signals.md` |
| Picker wording, previews, fallback list | `references/picker.md` |
| Domain advice for money, audit, booking, webhooks | `references/domain-notes.md` |
| Rules and layout for the picked base | `references/base/<layered-mvc, hexagonal, clean-onion, modular-monolith, microservices, vertical-slice>.md` |
| Modeling rules | `references/modeling/<ddd-full, ddd-tactical, simple-models>.md` |
| Add-on rules | `references/addons/<cqrs, event-sourcing, event-driven>.md` |
| Naming, folders and idioms per language | `references/stacks/<typescript, python, go, rust, jvm, csharp, php, ruby>.md` |
| What the example slice must contain | `references/example-slice.md` |

Load only the files for the current choice, not the whole folder.
