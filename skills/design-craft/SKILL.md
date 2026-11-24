---
name: design-craft
description: Design standalone HTML pages, interactive artifacts, dashboards, reports, and landing pages. Use when choosing a visual direction, responsive layout, typography, and theming for a browser or embedded host.
---

# Design Craft

Work like the design lead of a small studio. Give each page a visual identity matched to the task, with deliberate palette, type and layout choices specific to the subject.

## 1. Pick the treatment first

- **Utilitarian** (plan, memo, demo, report): polished but restrained. Real type hierarchy, considered spacing, a proper palette. No giant hero.
- **Editorial** (landing page, game, app or tool people keep or share): opinionated, with one real aesthetic risk.
- Unsure: a well-composed page is always acceptable. An over-designed identity sometimes isn't.
Follow the user’s requested format and the project’s existing design system, repository instructions, tokens, and theme files.

## 2. Delivery format

- For a standalone HTML file, include the doctype, document language, charset, viewport, and descriptive title. Inline CSS and JavaScript when the deliverable must be a single file. If it must work offline, inline or bundle assets and use local font fallbacks.
- In an existing app, use its components, styling, and build pipeline. For an embedded artifact, check whether the host expects a document or fragment and whether its sandbox permits scripts, network requests, storage, downloads, and external assets. For a Claude Artifact destination, consult [Claude Artifact HTML delivery](references/claude-artifacts.md).
- Account for safe-area insets where the content reaches screen edges. Keep the page usable in the supported viewport when an optional asset or API is unavailable.
- Call clipboard APIs from the user’s click, handle rejection, and offer selectable text as a fallback.

## 3. Theming (three states)

Define every color as a token on bare `:root` (light), then redefine only tokens in:

```css
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { /* tokens */ color-scheme: dark } }
:root[data-theme="dark"] { /* same dark tokens */ color-scheme: dark }
body { background: var(--bg); color: var(--fg) }
```

- `body` always has an explicit token background. A transparent body inherits whatever is behind the page.
- No literal color that works in only one theme. No color defined only inside a media or `[data-theme]` block.
- Don't simply invert the dark theme. Keep contrast legible and the accent working on both grounds.
- A dark-first design mirrors the whole shape. A deliberately single-look design may drop the dark blocks but must still set every color explicitly.

## 4. Design plan lives in the file

Open `<style>` with a `:root` token block:
- **Layout concept**: one-line comment above the tokens.
- **Color**: 4-6 named tokens. Neutrals have a slight hue bias toward the accent, not pure mid-grey.
- **Type**: 2+ roles (display with restraint, body, optional utility/data face). Inter + Space Grotesk is the fallback default only when nothing in the subject says otherwise. Always declare real fallback stacks.

The plan is working material. Don't recite hex values or font names to the user. One plain sentence on direction is the most to say.

## 5. Typography and layout

- Body text near 65ch. Set a type scale and keep to it. Use `text-wrap: balance` on headings, a little letter-spacing on uppercase labels, and `font-variant-numeric: tabular-nums` where digits align.
- Use flex or grid with `gap` instead of per-element margins.
- Rows wrap or stack to one column at ~400px. Flex/grid children holding text, code or tables get `min-width: 0`. Images and aspect-ratio boxes get `max-width: 100%`.
- Only tables, code and diagrams may be wider than the screen, each in its own `overflow-x: auto` container. The body never scrolls sideways.
- Repeated elements share edges, baselines and padding. Choose a column count the items fill, so nothing sits alone in a row.
- Use border, fill, radius and shadow by role, not on every block. Open with big-number tiles only when the numbers are the point.
- Size one-screen apps to their container when embedded. In a standalone document, account for mobile browser chrome and let content scroll when it exceeds the viewport.

## 6. Make the first frame complete

- Everything meant to be read is visible at rest. Animations start from a visible state, never `opacity: 0` waiting on an observer.
- Size heroes to content, not `100vh`.
- Tools open in a realistic working state. Clearly label examples and provide a useful empty state for an actual empty dataset.
- Include at least one detail only this subject would have (its units, document conventions, terms of art). Never use lorem ipsum.

## 7. Avoid the AI-design clichés

Unless the user asks for them, avoid: cream background with serif display and terracotta accent; near-black with one acid-green or vermilion pop; broadsheet hairlines with dense columns; purple-to-blue gradient hero on white; emoji section markers; everything centered; `rounded-lg` everywhere; accent rails on rounded cards; numbered markers (01/02/03) on content that isn't a real sequence.

## 8. When the page is a UI

- Summary before detail. Encode state in form (pill, chip, stripe), not only numbers.
- Semantic colors (good/warning/critical) are separate from the accent.
- Charts get type-level care: one scale for marks, ticks and labels, themed text colors, labels inside the viewBox, explicit fills on SVG shapes. A faint grid, an area fill and an emphasized endpoint help sparklines.
- Interactive elements look interactive and have a visible focus state. Every form control has a stable `id`. Respect `prefers-reduced-motion`.
- Use Canvas or WebGL for generative graphics, not long hand-written SVG paths.

## 9. Copy

Write from the user's side of the screen, in active voice. Controls state exactly what happens ("Publish", then a toast "Published"). Errors say what went wrong and how to fix it. Prefer plain and specific over clever. Avoid em-dash asides, "not X, but Y", colon-then-reveal, scare quotes and stock phrases.

## 10. Editorial pages only

- The hero states the thesis, using the most characteristic thing in the subject's world.
- Typography is the personality. Avoid the pairing you'd use on any other project.
- Use motion once, deliberately. Extra animation reads as AI-made.
- Put boldness in one place and keep the rest quiet. If the accent clashes, shift it analogous or desaturate it.
- Before building, check the plan against the subject. Revise anything generic inside the plan.

## 11. Build and verify

1. Define what the viewer can do. For persistence, live data, or privileged APIs, use `runtime-craft` if available. Otherwise confirm that the target supports the interaction and handle unavailable features in the UI.
2. Build from the visual plan and existing tokens. Preview in the target host or a browser when available. Check narrow layouts, supported themes, keyboard focus, and the primary interaction. Verify calculations and charts against representative data.
3. Deliver in the requested format. Use the host’s publishing flow when publication is part of the task and the necessary tools are available. A standalone HTML file can be handed over directly.
