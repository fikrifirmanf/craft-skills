# Design guardrails

Use guardrails to preserve a product's identity when another person or agent extends it. Write only the constraints the design needs. Name the affected token or component and explain the reason briefly.

For example: "Keep money amounts in the `figure` style with tabular numerals so table columns align."

Avoid vague instructions such as "make it polished." Avoid rules based only on a preferred count of fonts, effects, or components.

## Possible constraints

- **Color roles.** Reserve `accent` for named actions or states. Give data and semantic colors separate roles when needed.
- **Corners.** Assign radii by component role. Preserve intentional differences between controls and containers.
- **Type.** Record where each family belongs. Use scalable text styles, including labels inside charts.
- **Surfaces.** Keep depth consistent. Specify which overlays need shadows and which panels stay flat.
- **Imagery.** Preserve the chosen subject and treatment when they identify the product. Use consistent icon weight and sizing.
- **Layout.** Keep shared alignments, readable widths, responsive behavior, and complete grid rows.
- **Motion.** State which transitions matter and how reduced motion changes them.

These are possibilities, not a required list. A simple form may need only a few rules. A complex product may need more.

## Review for generic choices

Treat familiar patterns as a prompt to inspect the result, not automatic defects. Equal cards suit equal peers. A single system font can be appropriate. Judge whether the choices serve this content.

Look for these problems:

- The hero could belong to any product; its message or visual explains nothing specific.
- Several elements compete equally for attention.
- Accent color appears everywhere, making actions hard to distinguish.
- Shadows, radii, spacing, and type vary without clear roles.
- Every section uses the same card pattern despite different content.
- Decorative motion distracts from reading or using controls.
- Copy contains filler or claims without supporting facts.
- State, contrast, overflow, or font scaling fails in the render.

## Heuristic pass for reviews

For review-only requests, scan with these in addition to the render:
- **Status and feedback:** show relevant progress, completion, warnings, or errors. Check that the feedback appears close to the action and in time to guide the next step.
- **Control:** can the user undo, cancel or go back? Is there an escape from modals and flows?
- **Wayfinding and mapping:** can people identify their location, next options, and way back? Put controls near what they affect and use labels that name the destination or action.
- **Consistency:** the same action looks and is worded the same everywhere.
- **Error prevention and recovery:** confirmations only where the cost is high; error text says what happened and how to fix it, without codes.
- **Recognition over recall:** options are visible, not memorised; defaults and examples are provided.
- **Minimal:** no information competing with the task. Reduce cognitive load by removing steps and options before adding help.
- **Dark patterns:** false urgency, hidden costs, pre-ticked extras, confusing opt-outs, a hard-to-find cancel. Flag them; do not design them.
- **Not colour alone, and touch targets of at least 44pt.**

Fix concrete weaknesses in the requested surface. Preserve intentional conventions and useful existing patterns.

Related source: [Apple's Principles of great design](https://developer.apple.com/videos/play/wwdc2026/250/).
