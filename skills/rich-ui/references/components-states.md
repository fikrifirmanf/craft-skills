# Components and states

## Contents
1. Variants with distinct jobs
2. State checklist
3. Buttons
4. Inputs and forms
5. Cards
6. Navigation
7. Tables and lists
8. Overlays: dialogs, sheets, popovers, toasts
9. Empty, loading and error states
10. Iconography

---

## 1. Variants with distinct jobs

Define only the variants the product needs, with roles for their fill, size, and placement. Keep actions with different priorities visually distinct; variants can share one component implementation. Name the variants and their homes in design.md ("primary: one per view; nav utility: bordered white, top bar only").

## 2. State checklist

Check the states relevant to each component and platform:

| State | Requirement |
|---|---|
| Default | |
| Hover (pointer devices) | Subtle: a background tint, about 4–8% darker or lighter, or a border change. Not a jump. |
| Focus-visible | A 2px ring at 3:1 or more, offset 2px; never removed without a replacement |
| Pressed / active | A slightly darker shade, or scale(0.98) on touch platforms |
| Disabled | Reduced contrast (about 40% opacity, or a muted token), `cursor: not-allowed`, no hover effect; it must still be readable |
| Loading | A spinner or skeleton *in place*; keep the dimensions so nothing jumps; disable repeat submission |
| Selected / checked | Accent role; not colour alone (a check, weight change or indicator) |
| Error | Danger colour plus an icon plus a message that says how to fix it |

Content states: empty, one item, many items (thousands), very long strings (names, URLs, unbroken tokens), missing images, slow network, offline.

## 3. Buttons

- Heights: 32 (compact), 40, 44–48 (default and touch), 52–56 (hero). Horizontal padding about 1.5–2× the font size.
- Hierarchy: one primary per view; secondary (outline or tonal); ghost or text for tertiary; destructive as its own variant.
- Label: a verb plus an object ("Create invoice"), not "Submit" or "OK".
- An icon plus label gap of 6–8px; an icon-only button needs an accessible label and a tooltip on desktop.
- Width: hugging the content by default; full width only on mobile forms or narrow sheets.

## 4. Inputs and forms

- A visible label above the field, not placeholder-only. Placeholders are for examples.
- Field height matches button height in the same row. Outline at 3:1 or more against the surface.
- Helper text below; error text replaces or extends it in the danger colour with an icon; validate on blur or submit, not on every keystroke.
- Group related fields; use one column for most forms (faster to complete); mark the minority (optional *or* required, whichever is rarer).
- Correct input types and keyboards (email, tel, numeric), autocomplete attributes, and return-key actions on mobile.
- Long forms: sections with headings, sticky actions, saved progress.

## 5. Cards

Define card *types* by content, not one generic card:
- Feature card (icon, title, body), media card (image first), stat tile (big number, label, trend), list-row card (avatar, text, meta), CTA card (accent or inverted).
- Pick the elevation strategy (hairline, shadow, tonal or glass) and keep to it.
- A whole-card click target needs a single primary link with an expanded hit area, a visible hover state and correct semantics. Don't nest interactive elements inside a clickable card.
- Media inside cards: consistent aspect ratios (16:9, 4:3, 1:1); `object-fit: cover`; radius = card radius − padding.

## 6. Navigation

- Web marketing: logo, 3–6 links, one CTA; a mobile menu as a full sheet.
- Web app: a sidebar with sections, active state (accent indicator plus weight), collapsed icon mode with tooltips, and a breadcrumb or page title in the top bar.
- iOS: tab bar (3–5) plus navigation stack with large titles where it fits.
- Android: navigation bar (3–5), a navigation rail on medium widths, a drawer on large widths; Material top app bar.
- Desktop: a native menu bar or title-bar integration, sidebar source lists, and keyboard shortcuts shown in menus and tooltips.
- Always show where the user is (active state) and how to go back.

## 7. Tables and lists

- Left-align text, right-align numbers (tabular numerals), align headers with their columns.
- Row height 36–52px depending on density; zebra striping *or* hairline dividers, not both.
- Sticky header; sortable column indicators; truncate with an ellipsis plus a tooltip or expand.
- Row hover tint; a selection checkbox column; bulk actions appear when rows are selected.
- Mobile: change rows into stacked cards with label/value pairs, or keep a horizontal scroll with a sticky first column.

## 8. Overlays

- Dialog: for decisions that block. Title, short body, actions bottom-right on desktop (primary rightmost on Windows, web and macOS), focus trapped, Esc and backdrop close unless the action is destructive.
- Sheet or drawer: secondary tasks and filters; bottom sheets on mobile with a grab handle.
- Popover or menu: anchored, keyboard-navigable, closes on outside click.
- Toast: a brief non-blocking confirmation, 4–6s, with an undo for destructive actions, not used for errors that need action.
- Overlays sit on the highest surface level with the system's elevation treatment; the scrim is 30–60% black.

## 9. Empty, loading and error states

- **Empty:** explain what goes here, why it is empty, and the one action to fill it. Use an illustration or icon in the system's style, not a generic one.
- **Loading:** a skeleton matching the final layout for content; a spinner only for short, unknown waits; progress for long known ones. Avoid layout shift when content arrives.
- **Error:** what happened in plain words, what the user can do, and a retry. Keep the user's input.
- **Partial:** some data loaded, some failed. Show what you have and mark what's missing.

## 10. Iconography

- One icon set, one stroke width (1.5 or 2px at 24px), one corner style matching the radius family.
- Sizes on a grid: 16, 20, 24. Icons align optically with the cap height of adjacent text.
- Decorative icons are hidden from assistive technology; meaningful icon-only controls have labels.
