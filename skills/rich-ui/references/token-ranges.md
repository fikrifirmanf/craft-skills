# Historical token ranges

These figures were attributed to a study of 152 published design systems in the original skill. The source dataset and extraction method are not included here, so the statistics have not been independently verified. Treat them as optional historical heuristics. About three-quarters were extracted from live marketing and product websites; the rest are app and project systems. They describe what real, deliberate systems actually choose. Use them to sanity-check values and to pick sensible defaults, not as rules. Distinctive designs often sit at one end of a range on purpose.

p10/p90 = the 10th and 90th percentiles; "med" = median.

## Colour

| Measure | p10 | p25 | med | p75 | p90 |
|---|---|---|---|---|---|
| Colour tokens per system | 7 | 8 | 9 | 11 | 12 |
| Saturated hues per system | 1 | 1 | 2 | 4 | 5 |
| Contrast, primary text on background | 12.6 | 15.5 | 17.4 | 19.8 | 21 |
| Contrast, secondary text on background | 1.2* | 3.5* | 6.1 | 7.9 | 10.4 |
| Contrast, accent on background | 1.6 | 3.1 | 4.6 | 6.9 | 9.6 |

\* Many systems fail WCAG on secondary text. Don't copy that: keep secondary text at 4.5:1 or above.

- **Light vs dark default:** 100 light, 49 dark.
- **Pure vs tinted field:** 99 tinted or off-tones, 39 pure white, 14 pure black. Common dark fields: #0A0A0A, #09090B, #111111, #181818, plus blue-black tints like #070D18. Common light fields: #F4F4F4, #F5F5F7, #F8FAFC, plus warm paper tones like #F3EFEA, #EEEDEA, #FAF5F1.
- **Primary text:** 70% are off-black or off-white rather than pure.
- **Accent hues:** spread widely. Blue/indigo (210–270°) is the most common, then red/orange (0–60°) and cyan/teal (150–210°). Purple and magenta (270–330°) are rare, which is one reason a violet-gradient default looks generic.
- **Most common colour roles:** background, text-primary, surface, text-secondary, accent, border, surface-alt, text-tertiary/muted, success, danger, accent-hover, surface-dark/inverse.

## Typography

| Measure | p10 | p25 | med | p75 | p90 |
|---|---|---|---|---|---|
| Font families per system | 1 | 2 | 2 | 3 | 4 |
| Type styles defined | 4 | 5 | 6 | 6 | 7 |
| Body size (px) | 14.5 | 16 | 16 | 17 | 18 |
| Smallest size (px) | 12 | 13 | 14 | 16 | 18 |
| Largest size (px) | 20 | 36 | 58 | 69 | 96 |
| Display ÷ body ratio | 1.3 | 2.2 | 3.4 | 4.5 | 5.9 |

The weight mix, by number of styles: 400 (most common) > 500 > 700 > 600 > 300 > 900/800. Most systems use 2–3 weights. Variable fonts with odd weights (450, 520, 780) appear in the more crafted systems.

**Tracking and line-height by size** (tracking in em; negative = tighter):

| Size band | Tracking, med (p10 → p90) | Line-height, med (p25 → p75) |
|---|---|---|
| < 13px | 0 (0 → +0.10) | 1.4 (1.4 → 1.5) |
| 13–17px | 0 | 1.5 (1.4 → 1.5) |
| 17–24px | 0 (−0.018 → 0) | 1.4 (1.3 → 1.55) |
| 24–36px | 0 (−0.025 → 0) | 1.3 (1.2 → 1.4) |
| 36–56px | −0.02 (−0.041 → 0) | 1.1 (1.0 → 1.15) |
| 56–80px | −0.025 (−0.040 → 0) | 1.06 (1.0 → 1.1) |
| 80px+ | −0.032 (−0.050 → 0) | 1.0 (0.9 → 1.0) |

Small all-caps labels go the other way: +0.04 to +0.12em.

**Most frequent families:** Inter; a serif accent (Times-style, Instrument Serif, Lora, Playfair, Cormorant, IBM Plex Serif); system UI stacks; mono (JetBrains Mono, Geist Mono, DM Mono, IBM Plex Mono); Geist, Instrument Sans, Satoshi, Plus Jakarta Sans, Space Grotesk, Manrope, Sora, General Sans, Switzer. Inter is the most common, which is exactly why choosing *something else* on purpose is a cheap way to look less generic.

## Spacing

- **Base unit:** 8px (84 systems), 4px (35), others rare.
- **Most-used values:** 8, 16, 24, 4, 12, 32, 20, 10, 64, 6, 40, 96, 48.
- **On the grid:** 77% of all spacing values are multiples of 4; 53% are multiples of 8.
- **Section padding (marketing pages):** p25 48 · med 96 · p75 128 · p90 196px.
- **Spacing tokens defined:** median 5 (p90 7). Small scales are normal; a large scale invites inconsistency.

## Radius

| Role | p10 | p25 | med | p75 | p90 |
|---|---|---|---|---|---|
| Controls (button/input) | 4 | 6 | 8 | 12 | 19 |
| Cards / panels | 6 | 12 | 16 | 24 | 32 |

- 97 of 152 include a pill (9999px) token, used for tags, chips, avatars and often a capsule CTA.
- Only 3 systems are square everywhere, yet "keep this square" is a frequent guardrail for *specific* parts (navbars, media frames, inputs). Selective squareness is a strong identity move.
- A card radius above the control radius is the common pattern (nested elements should have smaller radii: inner = outer − padding).

## Components (frequency in token sets)

Button variants (541) ≫ cards (438) > navbar (50) > footer, badge, input, pill, panel, chip, modal, tabs, drawer, table, avatar. Systems typically define **3–5 button variants** and **3–6 card types**. Variety in these components is where their identity lives.

## Motion

- **Durations:** p10 120 · p25 150 · med 220 · p75 300 · p90 500ms.
- **Easings, by frequency:** `ease`, `cubic-bezier(0.4,0,0.2,1)` (standard), spring, `ease-out`, `linear` (for loops/progress), `cubic-bezier(0.16,1,0.3,1)` and `cubic-bezier(0.22,1,0.36,1)` (expressive ease-out for entrances).
- Systems with a strong identity often state "no bounce/spring" or "only opacity/transform".
