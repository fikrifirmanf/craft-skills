---
name: rich-ui
description: Design, build, or refine web and native interfaces with deliberate typography, layout, color, and visual hierarchy. Use for new screens, visual redesigns, design systems, or interfaces that look generic. Preserve established product styles. Excludes backend-only work and behavior-only fixes.
---

# Rich UI

Make visual decisions that fit the product, carry them into code, and inspect the rendered result. Preserve the user's scope and existing design language.

## Choose the smallest useful workflow

| Request | Workflow |
|---|---|
| Small visual fix or component adjustment | Read the affected component and existing tokens. Make the change and inspect the affected states. No new design.md or reference reading required. |
| New screen in an established product | Reuse its theme and components. Add only missing tokens; update an existing design.md only when decisions change. If useful, record new decisions briefly in the project's existing documentation. |
| New product, design system, or substantial redesign | Choose a direction, write a concise design.md, implement, render, and verify as below. |
| Review only | Inspect renders and relevant source. Report actionable findings ranked by impact. Create files or change code only when requested. |

## Full design workflow

1. **Understand the context.** Inspect the target platform, existing theme, relevant components, audience, and primary task. Follow provided references. Choose reasonable defaults when the brief leaves room; state only consequential assumptions.
2. **Choose a direction.** Define the visual hierarchy, density, typography, palette, and one recognizable design decision. It might be a product demonstration, distinctive type, information-rich chart, or composition. Familiar conventions are useful when they help users. Do not invent interactions or add decoration just to look different.
3. **Record decisions once.** For a new system, use `assets/design.md.template` and `references/design-md-format.md`. Keep prose brief; document tokens and decisions that affect implementation. Omit unused effects and motion tokens. Read `assets/examples/harbor-ledger.design.md` only if the format remains unclear. Existing native theme files remain the implementation source of truth; avoid maintaining duplicate token inventories for minor changes.
4. **Implement the requested surface.** Map reusable decisions into native theme tokens, then reference them in components. Keep primary, secondary, and utility actions visually distinct; variants may share a component. Build the relevant loading, empty, error, disabled, focus, and overflow states. Use realistic content without inventing testimonials, customer counts, or product claims. Compute displayed metrics from their underlying data.
5. **Render and inspect.** Check the affected screen at a narrow and wide supported size, and supported themes when affected. Look for hierarchy, alignment, readable density, overflow, and consistency with the chosen direction. For a small fix, inspect the affected breakpoint and state. If rendering is unavailable, report that limitation and what remains unverified.
6. **Verify and fix concrete issues.** Use the checks below when applicable. Recheck after changes that could invalidate a result; avoid rerunning unchanged checks. Stop when requested behavior works, visible defects are addressed, and relevant checks succeed. Report what was inspected and any remaining limitations.

## Design decisions that matter

- Give the screen a clear first focus and a readable path to its primary action. Use accent colors for defined roles; semantic and data colors may need separate roles.
- Choose type for the product and language. One family can be enough. Set a clear scale, readable line lengths, and appropriate tracking; allow native typography conventions.
- Reuse spacing and radius roles. Choose density by task. Equal grids suit equal peers; asymmetry should serve content. In a three-column grid with one two-column card, use five cards, or make the final card span two columns when there are four; never use six.
- Add imagery, charts, texture, or motion when they explain the product or establish its identity. A text-led hero or quiet form can be the right choice. There is no quota of visual treatments.
- Keep depth and effects coherent. Use meaningful grouping and alignment before adding shadows or decoration.
- Tokenize reusable visual decisions. Allow local geometry, intrinsic dimensions, and calculated layouts where appropriate; do not create tokens for every incidental number. In utility frameworks, prefer theme-backed classes for reusable colors, spacing, type, and radii.
- Use visible keyboard focus, semantic controls, accessible labels, and status cues beyond color. Normal text needs 4.5:1 contrast; large text and meaningful non-text UI need 3:1. Support reduced motion and platform font scaling, including text inside graphics. Use platform hit-target conventions and check required RTL layouts.

## Checks and their limits

For a newly created full design.md:

```bash
python3 <skill-dir>/scripts/lint_design_md.py path/to/design.md
```

This checks the full document structure and calls the contrast checker. Errors need correction; stylistic warnings are advisory and do not require changing an intentional design or writing justifications. Run the contrast checker separately only when checking palette changes without the full linter:

```bash
python3 <skill-dir>/scripts/check_contrast.py path/to/design.md
```

Prefer explicit `contrast` pairings for colors actually used together (see `references/design-md-format.md`). Without them, the checker infers pairings from token names. It cannot prove accessibility of a render, gradients, images, or unlisted pairings.

For token drift in changed source, exclude token definitions and use strict mode to catch recognized literals even when they match token values:

```bash
python3 <skill-dir>/scripts/find_offscale.py path/to/design.md src/ --strict-literals --exclude '*/tokens.css'
```

Without `--strict-literals`, this checks value membership only. It is a regex scan, not proof of token usage; review geometry exceptions and unsupported syntax manually. Scope scans to affected source. Run the project's relevant build and behavior checks too.

## Read references only when needed

Do not load the reference collection upfront. Select the file that answers the current design question; skip references when the existing system already answers it.

| Question | Reference |
|---|---|
| How should a new full design.md be structured? | `references/design-md-format.md` and `assets/design.md.template` |
| Need possible visual directions? | `references/style-families.md` |
| Does a major new screen need a stronger visual explanation? | `references/richness.md` |
| Need palette, type, layout, or component details? | The relevant file: `color.md`, `typography.md`, `layout-spacing.md`, or `components-states.md` under `references/` |
| Need effects, motion, platform mapping, or design guardrails? | The relevant file: `effects-motion.md`, `platforms.md`, or `guardrails.md` under `references/` |
| Need historical numeric ranges? | `references/token-ranges.md`; optional heuristics, not requirements |
