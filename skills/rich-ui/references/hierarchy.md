# Visual hierarchy

Use when a screen feels flat, noisy or "undesigned" and the fix is not a new color or font. Hierarchy comes from relative emphasis: decide what matters, then soften everything else.

## Contents
1. Emphasis tools beyond size
2. De-emphasize to emphasize
3. Labels are a last resort
4. Visual vs document hierarchy
5. Balancing weight and contrast
6. Actions by importance
7. Quick diagnosis

---

## 1. Emphasis tools beyond size

Size alone pushes primary content too big and secondary content too small. Combine size, weight and colour:
- Two or three text colours: primary (headings, key values), secondary (supporting copy), tertiary (metadata). Tertiary must still reach 4.5:1 for real text.
- Two weights are usually enough: regular (400/500) and emphasis (600/700).
- To de-emphasize, use a softer colour or a smaller size. Avoid weights under 400 for small UI text; they work only for large display text.
- On coloured backgrounds, do not use grey or white-at-low-opacity for secondary text. It looks washed out and lets images show through. Hand-pick a colour of the same hue with adjusted saturation and lightness.

## 2. De-emphasize to emphasize

When the main element does not stand out and nothing more can be added to it, reduce its competition:
- Soften inactive nav items instead of intensifying the active one.
- Remove the background of a sidebar that competes with the main content.
- Reduce secondary buttons to outline or link style before making the primary bigger.

## 3. Labels are a last resort

Avoid `Label: value` pairs that give every field equal weight.
- Drop the label when the format or context says it all (email, phone, price, a department under a name).
- Merge label and value: "12 left in stock", "3 bedrooms", "Updated 2h ago".
- When labels are needed for scanning (dashboards), make the value dominant and the label small, low-contrast and lighter.
- On spec sheets where users hunt for the label ("depth", "weight"), invert it: darker label, slightly lighter value.

## 4. Visual vs document hierarchy

Choose HTML elements for semantics and style them for hierarchy. An `h1` or `h2` does not have to be large. In application screens, section titles often act as labels for content and should be small; the content is the focus. A title can be visually hidden if it is kept for assistive technology and the content speaks for itself.

## 5. Balancing weight and contrast

Surface area reads as emphasis. Compensate on the other axis:
- Solid icons next to text feel heavy. Soften the icon colour rather than shrinking it.
- A thin 1px low-contrast border that is too faint: widen it slightly instead of darkening it.
- Bold text in a low-contrast colour can sit at the same level as regular text in a darker colour.

## 6. Actions by importance

Every page has a pyramid: usually one primary action, a few secondary, and rare tertiary ones. Design that pyramid before semantics.
- Primary: solid, high-contrast fill.
- Secondary: outline or low-contrast tonal fill.
- Tertiary: link-style text.
- Destructive does not automatically mean big, red and bold. If it is not the main action on the page, give it a secondary or tertiary look, and put the big red treatment on the confirmation step where it is the primary action.

## 7. Quick diagnosis

When a screen looks off, check in this order:
1. Is there one clear first focus? If three things look equally loud, soften two of them.
2. Is secondary text softened by colour, not just size?
3. Could any label be merged into its value or dropped?
4. Are headings competing with the content they introduce?
5. Do icons or borders outweigh the text beside them?
6. Does the primary action look different from the secondary and tertiary ones?
7. Does spacing group related items closer than unrelated ones (see layout-spacing.md §2)?
