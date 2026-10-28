# Visual richness with a purpose

Use this reference when a major new screen feels generic or fails to explain the product. Tokens keep a design consistent; hierarchy and meaningful content give it character. A quiet screen can still be effective. There is no minimum count of effects, typefaces, illustrations, or charts.

## Choose what the surface needs

Start with the user's task. Keep familiar navigation and interaction patterns when they help. Consider a different composition when it communicates the product more clearly, rather than requiring a departure from the category.

| Surface | Useful possibilities |
|---|---|
| Marketing | Product photography, a working sample, a diagram, a product screenshot, or expressive typography |
| App main screen | A clear summary, recognizable item identity, useful progress, and a prominent next action |
| Dashboard | Comparable values, trends, status cues, or a chart that answers a specific question |
| Forms and settings | Clear grouping, helpful previews, validation, and a specific completion state |

A text-led hero is valid when the message and typography carry the idea. Icons help distinguish items when they have recognizable meaning; assigning a different icon or color to every row is optional. Charts should answer a question that text alone answers poorly. Texture and motion should have a purpose and remain subordinate to content.

## Make the chosen idea survive implementation

Choose a recognizable visual decision that fits the product: a type treatment, composition, interaction, image treatment, or data presentation. Record it in design.md when creating a new system. Repeat it only where repetition helps the design; do not force a motif into unrelated components.

Use code-drawn graphics, supplied assets, or suitable image tools according to the subject. Code is useful for diagrams and data graphics; photography does not need to be replaced by invented shapes. Use the theme palette for drawn UI assets.

Text inside a graphic still needs scalable typography. On iOS use text styles, `relativeTo:`, or `@ScaledMetric`; on Android use `sp`; on web use scalable type tokens. Size graphics around the text. Derive displayed counts, chart values, and progress from the same data as their text equivalents. Provide accessible labels or descriptions for meaningful graphics and hide decorative ones from assistive technology.

## Inspect the render

- At a glance, is the primary content or action clear?
- Do hierarchy and grouping survive at a small scale?
- Does the imagery or data presentation explain something specific?
- Does the screen retain its intended character without compromising readability?
- Would removing an effect improve clarity? Would a useful demonstration explain more than another paragraph?

Fix the biggest visible weakness. Add visual content when it earns its space; remove it when it competes with the task.
