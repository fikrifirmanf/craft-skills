---
version: "1"
name: "Harbor Ledger"
description: "Warm paper-toned light system for a small-business bookkeeping app, with a tight grotesk UI, tabular mono figures, one deep harbor-teal accent reserved for actions and focus, and a single ink-navy summary band as its signature."
platforms: ["web", "ios", "android"]
colors:
  background: "#F6F3EE"
  surface: "#FFFFFF"
  surface-alt: "#EFEAE2"
  surface-inverse: "#16202B"
  text-primary: "#1B1F24"
  text-secondary: "#545B63"
  text-tertiary: "#61676E"
  text-on-inverse: "#F2EFEA"
  text-secondary-on-inverse: "#A9B3BD"
  border: "#E2DCD2"
  border-strong: "#8F887D"
  accent: "#0F6A6B"
  accent-hover: "#0B5455"
  on-accent: "#FFFFFF"
  focus: "#0F6A6B"
  success: "#2F7A3E"
  warning: "#9A6200"
  danger: "#B3261E"
  dark:
    background: "#121518"
    surface: "#1A1E22"
    surface-alt: "#22272C"
    text-primary: "#ECE8E1"
    text-secondary: "#A8AFB6"
    text-tertiary: "#8C939A"
    border: "#2C3238"
    accent: "#4FB3B0"
    on-accent: "#0B1E1E"
    focus: "#4FB3B0"
    accent-hover: "#60C4C1"
    surface-inverse: "#22272C"
typography:
  display:
    fontFamily: "Instrument Sans"
    fontSize: "44px"
    fontWeight: 600
    lineHeight: "1.08"
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Instrument Sans"
    fontSize: "28px"
    fontWeight: 600
    lineHeight: "1.2"
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Instrument Sans"
    fontSize: "18px"
    fontWeight: 600
    lineHeight: "1.35"
  body:
    fontFamily: "Instrument Sans"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: "1.55"
  label:
    fontFamily: "Instrument Sans"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: "1.4"
  figure:
    fontFamily: "JetBrains Mono"
    fontSize: "15px"
    fontWeight: 500
    lineHeight: "1.4"
    letterSpacing: "-0.01em"
  eyebrow:
    fontFamily: "JetBrains Mono"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: "1.4"
    letterSpacing: "0.08em"
spacing:
  base: "4px"
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  2xl: "48px"
  section: "64px"
rounded:
  control: "8px"
  card: "14px"
  pill: "9999px"
elevation:
  strategy: "hairline"
  overlay: "0 1px 2px rgba(22, 32, 43, 0.06), 0 12px 32px rgba(22, 32, 43, 0.12)"
motion:
  fast: "140ms"
  base: "220ms"
  slow: "360ms"
  easing-standard: "cubic-bezier(0.2, 0, 0, 1)"
  easing-enter: "cubic-bezier(0.16, 1, 0.3, 1)"
components:
  button-primary:
    background: "{colors.accent}"
    text-color: "{colors.on-accent}"
    radius: "{rounded.control}"
    height: "40px"
    padding: "0 16px"
  button-secondary:
    background: "{colors.surface}"
    text-color: "{colors.text-primary}"
    border: "1px solid {colors.border-strong}"
    radius: "{rounded.control}"
    height: "40px"
  button-ghost:
    background: "transparent"
    text-color: "{colors.text-secondary}"
    radius: "{rounded.control}"
    height: "40px"
  input:
    background: "{colors.surface}"
    border: "1px solid {colors.border-strong}"
    radius: "{rounded.control}"
    height: "40px"
  card-ledger:
    background: "{colors.surface}"
    border: "1px solid {colors.border}"
    radius: "{rounded.card}"
    padding: "24px"
  band-summary:
    background: "{colors.surface-inverse}"
    text-color: "{colors.text-on-inverse}"
    radius: "{rounded.card}"
    padding: "32px"
  table-row:
    height: "44px"
    border-bottom: "1px solid {colors.border}"
---
# Harbor Ledger

## Overview
A bookkeeping app for owners of small businesses who are not accountants and open it with mild dread. The design should feel like a calm, well-kept paper ledger: warm, orderly and quietly confident. It is a Dense Workbench shell with an Editorial Warm surface. Two signature moves: every money figure is set in a tabular monospace, so numbers line up like a printed ledger, and each screen has exactly one ink-navy summary band that answers "how am I doing?" at a glance. It is not a fintech neon dashboard, and it never uses red/green colour floods to make money feel dramatic.

## Composition
Web and tablet use a 240px sidebar (sections, then the account switcher at the bottom) beside a content column of at most 1120px. Each screen opens with a page title and one primary action at top right, then the navy summary band (three or four key figures in a row), then the working area: a filterable ledger table, or a 8/4 split of table and detail panel. On phones the sidebar becomes a five-item bottom tab bar, the summary band becomes a horizontally swipeable strip of figure cards, and table rows become stacked list rows. We deliberately rejected a grid of equal KPI cards: one band holding the figures reads as a single statement rather than six competing ones.

## Colors
The field is warm paper (#F6F3EE, about 75% of the screen); white surfaces (#FFFFFF) lift tables and cards by tone alone. Ink steps: #1B1F24 for primary text, #545B63 for secondary text, #61676E for metadata. All three pass 4.5:1 on paper and white. Harbor teal (#0F6A6B) is reserved for the primary action, the focus ring, the active sidebar item and text links, and it stays under 3% of any screen. It never fills cards, never colours figures, and never tints headings. Ink-navy (#16202B) appears only as the summary band. Semantic colours mark state on badges and inline messages, always paired with an icon and a word ("Overdue"). Negative amounts use a minus sign and parentheses, not red text, because colour alone must not carry meaning. In dark mode, surfaces step lighter as they rise, the accent brightens to #4FB3B0 to keep its contrast, and the summary band becomes the highest surface (#22272C) with a hairline.

## Typography
Instrument Sans handles all UI and reading text: display 44/600 at −0.03em for the few large moments (onboarding, empty states); headline 28/600 for page titles; title 18/600 for card and panel titles; body 15/400 at 1.55; label 13/500 for table headers and form labels. JetBrains Mono has two jobs only: money figures (`figure`, tabular numerals, right-aligned) and the uppercase `eyebrow` above section titles, tracked +0.08em. It never sets body copy or buttons. The scale is compact (display ÷ body ≈ 2.9) because this is a working tool, not a marketing page.

## Layout
4px base unit; component padding comes from 8/16/24 and section gaps are 48–64px. Tables use 44px rows (36px in compact density, a user setting). Content stays at 1120px or less. Breakpoints: below 1024px the detail panel becomes a sheet; below 768px the sidebar becomes a tab bar and the tables become lists. Radius family: controls 8px; cards, sheets and the band 14px; pills for status badges and filter chips. Table cells and media stay square.

## Components
- **Primary button:** teal fill, white label, 40px (48px on touch), 8px radius. One per screen, top right of the page header or at the bottom of forms.
- **Secondary button:** white with a 1px #8F887D outline (3:1 boundary). Used for "Export" and "Filter".
- **Ghost button:** text-secondary label, no chrome; for row actions and "Cancel".
- **Input:** 40px, white, 1px #8F887D border, 8px radius, label above, helper text below; error shows the danger border plus an icon plus a message.
- **Ledger card:** white, 1px #E2DCD2 hairline, 14px radius, 24px padding; title, optional eyebrow, content. No shadow.
- **Summary band:** ink-navy, 14px radius, 32px padding, three or four figures (eyebrow label above, 28px mono figure, a small delta in secondary-on-inverse with an arrow icon).
- **Ledger table:** sticky 36px header in label style; 44px rows with a hairline bottom border; right-aligned mono amounts; a row hover tint of surface-alt; a selection checkbox column; bulk actions slide into the header when rows are selected.
- **Status badge:** pill, 12% tint of the semantic colour plus full-strength icon and text.
- **Empty state:** a line illustration in the border-strong stroke, one sentence explaining the screen, one primary action ("Connect your bank").

## Graphics & Effects
Elevation is hairline-first: depth comes from paper to white tonal steps and 1px borders. Only overlays (menus, dialogs, sheets) get the two-layer navy-tinted shadow. There are no gradients, glass or glows anywhere, because trust here comes from plainness. Illustrations are single-weight (1.5px) line drawings in border-strong with one teal detail, used only in empty states and onboarding. Icons: one outline set, 1.5px stroke at 20px, rounded joins.

## Motion
Micro-interactions (hover, press, checkbox) take 140ms on opacity, colour and transform. Menus and sheets enter over 220ms with easing-enter and exit faster (160ms). Number changes in the summary band cross-fade; they never count up. No bounce, parallax or looping animation. With reduced motion, all movement becomes an instant change or a short opacity fade.

## Guardrails
- Never fill cards, headings or figures with `accent` (#0F6A6B); it marks the next action, the focus ring and the active nav item only.
- Keep every money amount in the `figure` mono style, right-aligned with tabular numerals; never show amounts in the sans.
- Use exactly one `band-summary` per screen; don't add a second navy surface or turn KPI figures into a grid of equal cards.
- Do not signal negative or positive amounts with red or green text alone; use a sign, parentheses and, for status, an icon plus a label.
- No gradients, glass, glow or decorative shadows; `card-ledger` stays flat with a 1px `border` hairline, and only overlays cast a shadow.
- Keep the radius family: 8px controls, 14px containers, pills for badges only. Table cells and media stay square.
- Mono is for figures and eyebrows only; never for body copy, buttons or headings.
