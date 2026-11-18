# Sources

Rules added in the hierarchy, layout, color, typography, imagery, form-control, empty-state and review sections were distilled from three books. They are original summaries in this repo's wording, not copies of the books. None of these rules has been validated by the skill's evals; treat them as design heuristics, and defer to an existing product's system when one exists.

| Source | Used for |
|---|---|
| Adam Wathan and Steve Schoger, *Refactoring UI* | `hierarchy.md`; labels as a last resort; text on colored fills; shade-scale construction; fixed sidebar and `max-width` layouts; proportional line-height; text over images; fewer borders; empty states |
| Michael Filipiuk, *UI Design Principles* (2021) | Control choice (radio, dropdown, switch); 44pt touch targets; finishing touches; the tinted-grey and no-pure-black cross-checks |
| Joel Parker Henderson (ed.), *UI/UX Design Guide: Concepts, Terminology, Tactics* (2024) | The review heuristic pass in `guardrails.md` (Nielsen's heuristics, dark patterns, cognitive load). The book says it was written with AI assistance, so only well-established material was used |

## Where the sources were not followed

- Filipiuk's flat 1.6 body line-height, 12-column grid, 4/8pt linear spacing and "skip a weight" pairing rule are replaced by the proportional line-height, selective grid and non-linear guidance already in these references.
- Refactoring UI's five shadow levels and HSL-first color workflow are not adopted; the references keep 2–3 elevation levels and prefer OKLCH where supported.
- Validation timing stays on blur or submit rather than inline on every keystroke.
