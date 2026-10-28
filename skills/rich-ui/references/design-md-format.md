# The design.md format

Use this format for a new system or substantial redesign. Small fixes do not require a new document. For an established product, reuse its native tokens and update only decisions that change.

Start from `assets/design.md.template`. Define reusable tokens in frontmatter and explain their roles in the nine sections. Keep sections short; "None" is enough for unused motion or effects. Do not repeat token tables in prose. The full example in `assets/examples/harbor-ledger.design.md` is optional.

## Frontmatter

Required groups for the full-document linter: `name`, `description`, `colors`, `typography`, `spacing`, `rounded`, and `components`. Include only the roles the product uses. `platforms`, `motion`, and `elevation` are optional.

- Name tokens by role. Record exact colors, type styles, spacing steps, radii, and reusable component values. One typeface or a small scale can be sufficient.
- Add dark overrides under `colors.dark` or `dark.colors`. The contrast checker merges overrides with the base palette.
- Values such as `{colors.accent}` document references, but scripts do not resolve those references as colors. Keep color definitions as literal hex or rgb/rgba values.
- Tokenize reusable decisions. Local illustration geometry, intrinsic image sizes, and calculated layouts need not become tokens.

## Explicit contrast pairs

Record actual uses to avoid checking combinations that never appear together:

```yaml
contrast:
  body-on-page:
    foreground: text-primary
    background: background
    usage: text
  action-label:
    foreground: on-accent
    background: accent
    usage: text
  focus-on-page:
    foreground: focus
    background: background
    usage: ui
```

Names refer to keys in the active color palette. Each pair is checked in every theme. `usage` is `text` (4.5:1), `large-text` (3:1), or `ui` (3:1); it defaults to `text`. Only use `large-text` at 24 CSS px or larger, or 18.66 CSS px bold or larger, with equivalent platform sizing. Small muted text still requires 4.5:1.

A nonempty `contrast` map replaces inferred pairings. Include all relevant foreground/background uses; an omitted pair is unchecked. Missing tokens, invalid usages, and unparseable colors fail. Backgrounds must be opaque; check transparent layers against their actual composite manually. Without the map, pairings are inferred from names and may miss cases or report unused combinations. Images, gradients, focus behavior, and rendered font size need separate inspection.

## Nine sections

| Section | Record only the decisions needed to build |
|---|---|
| Overview | Product, audience, direction, and recognizable visual decision |
| Composition | First view, reading order, primary action, and section or pane structure |
| Colors | Field, surface, text, accent, semantic roles, and affected theme differences |
| Typography | Families and roles, scale, line length, and font scaling |
| Layout | Density, grid, spacing rhythm, radius roles, and responsive behavior |
| Components | Required variants, states, and reuse of existing components |
| Graphics & Effects | Imagery and effects with their purpose and placement, or none |
| Motion | Relevant transitions and reduced-motion behavior, or none |
| Guardrails | Specific constraints that protect this product's identity; no required count |

For example: "Use `accent` for the primary action and active navigation" is more useful than "Use color consistently." Prefer concrete decisions over explanations of general design principles.

For an existing product, inspect its theme and a render first. `find_offscale.py src/` can inventory recognized raw values, but frequency alone does not make a value a design token. Preserve deliberate exceptions.
