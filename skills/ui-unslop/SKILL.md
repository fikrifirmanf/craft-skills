---
name: ui-unslop
description: Enforces UI design craft and accessibility and eliminates generated-looking interfaces. Trigger whenever designing, building, restyling or reviewing a screen, page, component, landing page, dashboard or design system in any web stack (HTML/CSS, Tailwind, React, Vue, Svelte, Astro).
---

# UI Anti-Slop Protocol

A generated UI is recognisable by its defaults: purple gradients, glass cards, emoji icons, centred everything, gray-on-white text nobody can read. Design from the content and the user's task instead.

## 1. Before you draw anything
- **Find the system first.** Read the existing tokens (CSS variables, `@theme`, `tailwind.config`) and components. Call `analyze_design_tokens` on the project to see the real palette, type scale, radii and spacing in use. Extend that system; do not invent a parallel one.
- **One idea per screen.** Decide the primary action and the single most important piece of information. Hierarchy (size, weight, position, contrast) serves that, not decoration.

## 2. Color & contrast (HARD RULES)
- **Every text/background pair meets WCAG AA:** 4.5:1 for body text, 3:1 for large text (>=24px, or >=18.66px bold) and for UI boundaries (input borders, focus rings, icons that carry meaning). Check unfamiliar pairs with `check_contrast` before using them; it accepts Tailwind names and returns the nearest passing shade.
- **Check both themes.** A `dark:` pair is a separate pair.
- **Muted is not faint.** Secondary text on white starts around `gray-600`, not `gray-400`. White text on mid-tone fills (`emerald-600`, `amber-500`) usually fails; use the -700 shade.
- **Color is never the only signal.** Errors get an icon or text, not just red.
- **No gradient-filled headline text, no frosted glass cards (`bg-white/10 backdrop-blur`), no ambient blurred blobs.** Solid surfaces with clear borders read as designed.

## 3. Type & layout
- **Type scale:** 4-6 sizes total. Body copy 16px (14px minimum for dense UI), never below 12px for anything. Line length 45-75 characters (`max-w-prose`).
- **Spacing on the grid:** multiples of 4px (Tailwind's scale). No `p-[13px]`.
- **Left-align** body text and most headings; centre only short, isolated lines.
- **Mobile viewport:** `min-h-dvh`, not `h-screen`/`100vh`. Never disable zoom (`maximum-scale=1`, `user-scalable=no`).
- **Stacking:** a small z-index scale (e.g. dropdown 10, sticky 20, modal 50, toast 60), not `z-[9999]`.

## 4. Interaction & accessibility (HARD RULES)
- **Real controls:** actions are `<button>`, navigation is `<a href>`. No `onClick` on `div`/`span`.
- **Every control has a name:** icon-only buttons get `aria-label`; inputs get a `<label>` (placeholders are hints, not labels).
- **Visible focus:** if you remove the outline, replace it (`focus-visible:ring-2 focus-visible:ring-ring`). Never `tabindex` > 0.
- **Images:** meaningful `alt`, or `alt=""` when decorative.
- **States:** hover, focus-visible, active, disabled, loading, empty and error are all designed.
- **Motion:** transition specific properties (`transition-colors`, `transition-transform`), 150-250ms, and honour `prefers-reduced-motion`. No `animate-bounce`/`animate-ping` to beg for clicks.
- **No emoji as icons.** Use the project's icon set, or nothing.

## 5. Mandatory verification loop
Before claiming a UI task is complete:
1. Call `audit_ui_slop` with every modified markup/style file or directory (omit `files` to audit git changes).
2. For any color pair the audit cannot see (CSS variables, translucent backgrounds, images behind text), call `check_contrast` explicitly.
3. If you added colors, sizes, radii or shadows, re-run `analyze_design_tokens` and consolidate if it reports `SPRAWL`.
4. On `FAIL`, fix every ERROR and re-run until `PASS`. A verified false positive may be suppressed with `unslop-ignore RULE_ID -- reason` on or above the line; a suppression without a reason is an ERROR.
