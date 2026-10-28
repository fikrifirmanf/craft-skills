# Colour

## Contents
1. Building a palette
2. Rationing the accent
3. Neutrals and surfaces
4. Dark mode
5. Semantic colours
6. Gradients and colour washes
7. Contrast checklist

---

## 1. Building a palette

Work in this order. Each step constrains the next.

1. **Field temperature.** Warm (paper, cream, espresso-black), cool (slate, blue-black, lavender-white) or neutral. Pick one that fits the brand's tone. Warm reads human and editorial; cool reads technical and precise.
2. **Neutral ramp.** Derive 6–8 steps from the field hue, not from pure grey. Using OKLCH, keep the hue fixed, keep chroma very low (0.005–0.02), and vary lightness. Tinted neutrals are what make a palette feel intentional.
3. **One accent.** Pick a hue that is *not* the obvious default for the category if you can (fintech does not have to be blue). Check it on both the field and the surface, as a fill (with `on-accent` text) and as text or an icon.
4. **Accent states.** Hover/pressed: shift lightness by about 6–10% (darker on light themes, lighter on dark). A subtle tint for selected rows or backgrounds: the accent at 8–12% alpha, or mixed into the surface.
5. **Semantic set.** Success, warning, danger and info, tuned to sit at a similar lightness and chroma to the accent so nothing shouts louder than it should.
6. **Optional second hue.** Only with a defined job (data visualisation, a category system, a single highlight). Two accents competing for the same role is the most common colour failure.

## 2. Rationing the accent

Write the accent's roles down explicitly in design.md. Typical role set:
- primary action (one per view)
- focus ring
- active/selected state (nav item, tab underline, toggle)
- links in body text
- one emphasised word, numeral or icon per section, at most

Places the accent should *not* go by default: card backgrounds, large section fills, body text, headings, decorative icons, borders on everything. If a full colour band is wanted, use it once or twice per page as a deliberate composition move, and describe it in Composition.

Aim for the accent covering under 5% of the screen area. The corpus regularly quotes "under 3%" and "under 1%".

## 3. Neutrals and surfaces

- **Three text steps:** primary (headings, body), secondary (supporting copy, labels), tertiary (metadata, placeholders, disabled). All real text needs 4.5:1 or more against the surface it sits on. Use tertiary only for large text or non-essential decoration if it can't reach 4.5:1.
- **Surfaces:** base field, raised surface (cards, popovers), sunken or alt surface (wells, code blocks, inverted bands). On light themes, raised is often *pure white on an off-white field*. That small step gives depth without shadows.
- **Borders:** a hairline at about 1.2–1.5:1 against the surface for dividers. Interactive boundaries (input outlines, checkbox borders) need 3:1.
- Avoid pure #000 text on pure #FFF for long reading. Off-black (#111–#1C1C1C, or tinted) on white or off-white is easier on the eyes and looks more refined.

## 4. Dark mode

Dark mode is not inverted light mode.
- Field around #0A–#12 lightness; **raise surfaces by making them lighter** (each level +3–5% L), because shadows are nearly invisible on dark.
- Hairlines: white at 6–12% alpha.
- Primary text: around #EDEDED–#F5F5F5 (pure white can glare and bleed at small sizes); secondary text still needs 4.5:1. #A1A1AA on #0A0A0A is about 7.7:1, and #71717A on #0A0A0A is about 4.1:1, so it fails.
- The accent is often lightened or slightly desaturated to keep its contrast and reduce vibration.
- Images and illustrations may need dimming (opacity 0.9) or a dark-adapted variant.
- Provide both themes as the same token keys with different values. Components should never branch on the theme.

## 5. Semantic colours

- Pair every status colour with an icon or text label (colour-blind users, greyscale screens).
- Use tinted backgrounds (status at 8–14% alpha) with full-strength text or icons for banners and badges.
- Danger is reserved for destructive or error states; don't make the brand accent red if errors are red, or give them clearly different hues and lightness.
- Data visualisation needs its own categorical palette (5–8 hues, similar lightness, checked for colour-blind distinctness). Don't reuse the semantic set.

## 6. Gradients and colour washes

The corpus's most repeated rule: **a gradient lives in one bounded place.** Good homes: the hero's upper corners, a single CTA band, one feature card, a glow behind a product screenshot, a progress bar. Bad homes: the whole page background, every card, text everywhere.

Technique:
- Use radial gradients fading to transparent (`radial-gradient(40% 50% at 15% 10%, <accent at 0.35–0.8 alpha>, transparent 70%)`) to make light-like washes rather than hard linear stripes.
- Stay within one hue family, or shift between adjacent hues (indigo→violet, ember→amber). Complementary rainbow gradients are a style choice that needs a deliberate reason.
- Interpolate in OKLCH (`linear-gradient(in oklch, …)`) to avoid muddy middles.
- Text over a gradient must pass contrast at *every* point it covers. Check the lightest point.

## 7. Contrast checklist

Run `scripts/check_contrast.py design.md`. It checks explicit `contrast` pairings when supplied; otherwise it infers pairings from token names, in both themes. See `design-md-format.md` for the schema and limitations. In addition, check by eye on the render:
- text over images (needs a scrim or a solid plate)
- placeholder text in inputs
- disabled states (exempt from WCAG, but should still be readable enough to understand)
- focus rings against both the component and the page
- selected-row text on the selection tint
