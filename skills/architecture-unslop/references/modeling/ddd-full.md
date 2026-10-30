# Full DDD (strategic + tactical)

## Picker card
Bounded contexts with their own language and model, a context map of how they relate, plus the tactical building blocks inside each context.

## When it fits
Several business domains whose words mean different things ("customer" in sales vs. support), domain experts available to talk to, and a system expected to live for years.

## Rules (HARD BANS)
Everything in `ddd-tactical.md`, plus:
- **Every context is named and bounded:** one module or service per context, listed in `context-map.md` with what it owns.
- **The same word may mean different things in different contexts.** Do not force one shared `Customer` class across contexts; each keeps its own model.
- **The context map names each relationship:** partnership, customer–supplier, conformist, anti-corruption layer, open host service/published language, shared kernel, separate ways.
- **Anti-corruption layer** wherever a context consumes a model it does not control (legacy system, third party, an upstream context that changes often).
- **Shared kernel stays tiny** and is changed only with every owning team's agreement.
- **Ubiquitous language is written down:** a short glossary per context in `context-map.md`, and code names match it. Rename code when the business renames a concept.

## Layout additions
```
docs/
└── context-map.md     # contexts, ownership, relationships, glossary per context
```

## Overkill warning
With one domain and no domain experts involved, say once: "Strategic DDD (context map, multiple models) has nothing to separate yet; Tactical DDD gives the aggregate and value-object benefits now."
