# Layout, spacing and shape

## Contents
1. Spacing scale
2. Grouping and rhythm
3. Grids and composition
4. Page composition (marketing and content)
5. App shells (product, mobile, desktop)
6. Radius families
7. Responsive behaviour

---

## 1. Spacing scale

- Base 4px (dense UIs) or 8px (most UIs). Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.
- Keep the token set small (corpus median 5 named steps). Every extra step is a chance for inconsistency.
- Odd values (6, 10, 14) are acceptable *inside* tight components (icon gaps, badge padding) if they are tokens.

## 2. Grouping and rhythm

Spacing communicates structure. The rule: **space within a group < space between groups < space between sections**, with each step about 1.5–2× the one before it.

Example: label → input 6–8px; field → field 16–20px; field group → field group 32px; section → section 64–96px.

Section padding on desktop marketing pages is commonly 64–128px (corpus median 96px), scaled down by about 40–50% on mobile.

## 3. Grids and composition

- Desktop marketing content: max width 1120–1280px, centred, 12-column grid, gutters 16–32px.
- Reading content: 640–720px column.
- **Break the equal-grid default.** Prefer:
  - asymmetric splits: 7/5, 8/4, 65/35
  - one wide card beside one or two narrow ones (bento)
  - a featured item spanning two columns, then regular items
  - a list or table where a card grid was the reflex
- Use three equal cards only when the content really is three equal peers.
- **Close every row.** If a 3-column grid has a card spanning 2 columns, the item count must fill complete rows: with one 2-wide card use 5 cards (2+1, 1+1+1), or with 4 cards make the last one span 2 as well (2+1, 1+2). Six cards would leave an orphaned gap. The same applies to any column count: total spans must be a multiple of the column count.
- Align to shared edges. Count the distinct left edges on a screen; fewer is calmer.
- Visual weight: one dominant element per view (a headline, a product shot, a key metric). If everything is large, nothing is.

## 4. Page composition (marketing and content)

A typical high-quality page arc:
1. **First view:** a clear statement (headline plus one line), one primary action and one secondary, and a proof object (product screenshot, live demo, key visual). Navigation stays quiet.
2. **Proof strip:** logos, a metric or a testimonial.
3. **Feature bands:** alternate layouts (split, bento, list, a single large visual). Don't repeat the same block 5 times.
4. **A rhythm break:** one inverted (dark or colour) band, a full-bleed image, or an oversized quote. Corpus systems typically allow 1–2 of these per page.
5. **Depth:** pricing, comparison, FAQ.
6. **Closing CTA band**, then the footer.

Navbar options (pick deliberately and write it down): edge-to-edge square bar, bounded floating capsule, transparent over the hero becoming solid on scroll, or a centred bounded bar. Each has a different personality. The corpus treats "don't convert the navbar shape" as an important guardrail.

## 5. App shells (product, mobile, desktop)

- **Web app / desktop:** sidebar (220–280px, collapsible to icons) plus content; or three-pane (sidebar, list 280–360px, detail). Top bar 48–56px. Content padding 16–32px.
- **Mobile:** bottom tab bar (3–5 destinations) or a top app bar with navigation drawer; primary actions within thumb reach; sheets for secondary tasks; safe-area insets respected.
- **Density modes:** comfortable rows 44–52px, compact 32–36px. Give data-heavy tools a compact default.
- **Empty space is still designed:** empty states, first-run, zero-data dashboards (see components-states.md).

## 6. Radius families

Choose 2–4 radii, each with a role:

| Role | Typical | Notes |
|---|---|---|
| Small (badges, checkboxes, inline code) | 4–6px | |
| Control (buttons, inputs, selects) | 6–12px (median 8) | Inputs and buttons usually match, so they sit flush in a row |
| Container (cards, sheets, dialogs) | 12–24px (median 16) | Larger than controls |
| Pill | 9999px | Tags, chips, avatars, capsule CTAs |
| Square | 0 | A deliberate choice for media, navbars, tables, technical styles |

- Nested radii: inner radius = outer radius − padding (a card at 16px with 8px padding holds an image at 8px).
- Selective squareness or roundness is identity: sharp media frames in a soft UI, or pill buttons in a square UI.
- Platform shapes: iOS uses continuous ("squircle") corners (`.continuous` in SwiftUI); Material 3 has a shape scale (4/8/12/16/28dp).

## 7. Responsive behaviour

Write what changes at each breakpoint, not only what exists:
- Common web breakpoints: 640, 768, 1024, 1280px (or container queries per component).
- Columns stack; asymmetric splits become a single column with the dominant element first.
- Display type steps down (64 → 40px); section padding shrinks (96 → 56px).
- Sidebars become drawers or bottom sheets; tables become stacked cards or scroll horizontally with a sticky first column.
- Hover-only affordances need a touch equivalent.
- Mobile: no horizontal page scroll; 16px minimum side gutters; 16px minimum input font size on iOS web (prevents zoom).
