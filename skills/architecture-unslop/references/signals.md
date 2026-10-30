# Signals: from the user's idea to a recommendation

Read the prompt for what the software must do, not for the technology it mentions. Note every signal found, then apply the decision order below. Quote the user's own words in the recommendation reason.

## Signal table

| Signal | Words in the prompt (any language) | Points to |
|---|---|---|
| Data entry and listing | CRUD, admin panel, back office, blog, CMS, form, catalog page, "simple", "quick", MVP, prototype | Layered/MVC, Simple models |
| Business rules | approval, workflow, policy, pricing rule, eligibility, quota, limit, state changes ("draft → submitted → approved") | Hexagonal or Clean, Tactical DDD |
| Several distinct domains | marketplace, ERP, "HR and payroll", "inventory and billing", platform with several sub-products | Modular Monolith, Full DDD |
| Money or regulated records | payment, wallet, ledger, balance, payout, invoice, claims, medical record, compliance, audit | Hexagonal + Tactical or Full DDD; Event Sourcing if history must be replayed |
| History is the product | audit trail, "who changed what", undo, time travel, versioned records, reconstruct past state | Event Sourcing (+ CQRS) |
| Reads differ from writes | dashboard, reporting, analytics, search, feed, leaderboard, "thousands read, few write" | CQRS for that context |
| Reactions and integration | notification, webhook, sync with another system, "when X happens do Y", IoT, tracking, chat | Event-Driven |
| Independent teams or scale | "several teams", "deploy separately", different scaling per part, different tech per part | Microservices, but only with a team or deploy reason |
| Many small independent features | many endpoints with little shared logic, "each screen does its own thing", feature teams | Vertical Slice |
| External systems shape the code | legacy system, third-party ERP, "integrate with SAP / Stripe / government API" | Hexagonal with an anti-corruption layer |
| Learning or teaching | "I want to learn DDD", "show me clean architecture" | What they asked to learn, at the smallest scope that shows it |

## Decision order

1. **Start at the lightest level:** Layered/MVC with Simple models.
2. **Move to Hexagonal** (or Clean, if the user mentions use cases or Uncle Bob) when there is at least one business-rule, money, or external-system signal.
3. **Move to Modular Monolith** when two or more distinct domains appear. Each domain is a module, and each module is internally Hexagonal.
4. **Microservices only** when there is an explicit team, deploy or scaling-difference signal. Otherwise recommend a Modular Monolith and note that modules can be split later.
5. **Vertical Slice** replaces Layered/Hexagonal when features are many and share little. It can coexist with a modular split.
6. **Modeling:** Simple models for data entry; Tactical DDD for rules within one domain; Full DDD when there are several domains or the user mentions bounded contexts or ubiquitous language.
7. **Add-ons** are per context, never global. Recommend CQRS only for the read-heavy context, Event Sourcing only for the context whose history matters, and Event-Driven when reactions cross contexts or systems. With no signal, recommend None.
8. **Ties:** choose the lighter option and name the heavier one as the alternative.

## Writing the reason

One sentence, under 20 words, tied to the prompt:

- Good: "You mentioned approval steps and Stripe payouts, so rules stay isolated from Stripe and the database."
- Bad: "Hexagonal is a flexible, scalable, industry-standard architecture."

If the user's prompt contains no signal for a question (for example, nothing about reads), recommend the lightest option for that question and say "No signal for X in your description" in its reason.
