---
name: diagram-craft
description: Create diagrams that explain architecture, data flow, option tradeoffs, or state transitions in HTML, Markdown, and technical docs. Use when a diagram can make the mechanism easier to follow.
---

# Diagram Craft

Draw like the engineer who has to live with the decision, not like a decorator. A diagram earns its place when it lets a cold reader see a mechanism they would otherwise assemble from prose: where data flows, which components talk, what changes between two options, what states a request moves through. If one sentence says it faster, write the sentence.

## What to draw

- **Show the mechanism, not its name.** A box labeled "cache" says little. Draw the path a request takes, the two stores it sits between, and the arrow that vanishes when the cache is removed. Include the parts the argument hinges on (the boundary crossed, the hop added, the data moved) and drop the rest.
- **Comparing options? Draw the difference.** Two architectures side by side, a before and after, or the one edge each option adds or removes. A separate labeled box per option with nothing connecting it to the system just restates a list.
- **Match complexity to the stakes.** A one-hop question is three boxes. A migration that reroutes writes through a queue needs the queue, writer, reader and ordering arrow. Neither forced minimalism nor a full system inventory.
- **Label every arrow.** `writes`, `invalidates`, `polls every 30s` carry information, and an unlabeled arrow only says "related". Add a legend only when the same encoding (dashed, colored, doubled) repeats. Otherwise put the meaning on the mark.

## Choose the output format

Follow the requested format and the project’s documentation conventions. Use inline SVG for a self-contained HTML figure when the target permits it. Use Mermaid for flowcharts and sequences when the target renderer or the project build supports it. If the target strips SVG or cannot render Mermaid, supply a supported image with alt text or a text diagram.

## Inline SVG mechanics (HTML pages)

Hand-author native `<svg>` with `rect`, `circle`, `line`, `polyline`, `path` and `<text>`. No libraries, no runtime, no external images.

- **Size by `viewBox`.** `viewBox="0 0 W H"`, scaled with CSS (`max-width: 100%; height: auto`). Choose W and H for the content. Wide flows read left to right and layered stacks top to bottom.
- **Theme with `currentColor`.** Strokes, text and arrowheads inherit the page foreground in both themes. Use a theme token for meaningful emphasis and check its contrast in each supported theme.
- **Arrowheads** are a `<marker>` in `<defs>` referenced by `marker-end="url(#flow-arrow)"`, or a small `<polygon>`. Use document-unique IDs when several inline diagrams share a page.
- **Keep text legible.** About 11-13px at drawn scale, `text-anchor` for alignment, labels of one to three words. Longer explanation goes in the caption.
- **Align to a grid.** Shared baselines and even gaps make a hand diagram look deliberate.
- **One figure, one claim.** Wrap in `<figure>` with a `<figcaption>` stating what the picture shows. Give the `<svg>` `role="img"` and an `aria-label` with the same claim.
- **Stay self-contained.** No `<script>`, `<style>` or `<foreignObject>` inside the SVG. Gradients, patterns and `<use>` reference same-fragment ids. Long decorative path data means the drawing needs a real graphics tool, so simplify.
- Wide diagrams sit in their own `overflow-x: auto` container.

## Review checklist

- [ ] Can a reader state the claim from the figure alone?
- [ ] Every arrow labeled?
- [ ] Options compared as a difference, not a list of boxes?
- [ ] Legible at the intended reading size and in supported themes?
- [ ] Caption and accessible text present?
