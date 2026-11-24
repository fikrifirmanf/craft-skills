# Typography

## Contents
1. Choosing families
2. Pairing patterns
3. Building the scale
4. Tracking, line-height, measure
5. Weights
6. Treatments that add identity
7. Platform notes

---

## 1. Choosing families

Type is the largest single signal of a design's character. Choose by tone:

| Tone | Directions (examples; any licensed equivalent works) |
|---|---|
| Neutral, precise UI | Neo-grotesk: Inter, Geist, Switzer, Instrument Sans, SF Pro / system-ui |
| Friendly, modern | Geometric/rounded: Plus Jakarta Sans, Manrope, Satoshi, General Sans, Sora |
| Technical, quirky | Space Grotesk, Archivo, Epilogue, IBM Plex Sans |
| Editorial, literary | Serif: Lora, Source Serif, Newsreader, EB Garamond, IBM Plex Serif |
| Luxury, fashion | Didone / high-contrast: Playfair Display, Bodoni Moda, Cormorant, Instrument Serif |
| Impact, sport, cinema | Condensed: Oswald, Barlow Condensed, Bebas Neue, Archivo Narrow |
| Code, data, labels | Mono: JetBrains Mono, Geist Mono, IBM Plex Mono, DM Mono |

Inter is the most common family in the corpus, so it is a safe choice but not a distinctive one. If the brief calls for character, choose another face deliberately, or keep Inter for the UI and give the display role to something else.

Picking a face: prefer families with many weights (about 5+, or 10+ styles including italics), which usually signals care. Avoid condensed or short-x-height faces for UI body text. Display faces with tight spacing do not work at small sizes, but a wide-spaced text face can be tightened for headlines. When unsure, use the system stack or inspect the faces of sites you admire.

Check: language and script coverage (CJK, Arabic, Cyrillic, Devanagari), variable-font availability, licence, and file size on web (subset it, and use `font-display: swap`).

## 2. Pairing patterns

Use as few families as the product needs; one can be sufficient. Possible pairings:
1. **Single sans, many weights.** Cleanest. Identity comes from size contrast and tracking.
2. **Sans UI + serif italic accent.** One italic serif clause inside a sans headline ("Ship faster, *without the chaos*"), or serif only in pull quotes. Keep it rare: one occurrence per view.
3. **Serif display + sans body.** Editorial. The serif carries the voice and the sans carries the UI.
4. **Sans + mono labels.** Mono for eyebrows, tags, buttons or data; sans for everything else. Technical feel.
5. **Condensed display + humanist body.** High impact with readable copy.

Give each family exactly one job and write that job in design.md. "Mono is exclusively for eyebrows and code; never body" is the kind of rule that keeps a pairing coherent.

## 3. Building the scale

Pick the body size first (16px default; 14–15px for dense tools; 17–18px for reading-first products), then a ratio:
- 1.125–1.2 (major second, minor third) for dense apps and dashboards
- 1.25 (major third) for general product UI
- 1.333–1.5 for marketing and editorial pages, where the display may jump further

Define only the named styles the surface uses, such as headline, body, label, and caption. Check the hierarchy in a render rather than targeting a fixed number of styles.

Fluid sizes on the web: `clamp(2.5rem, 1.5rem + 4vw, 4.5rem)` for display. Keep body fixed or nearly fixed.

## 4. Tracking, line-height, measure

As size goes up, tracking and line-height come down:

| Size | Tracking | Line-height |
|---|---|---|
| ≤ 13px | 0 to +0.02em (all-caps: +0.06–0.12em) | 1.4–1.5 |
| 14–18px body | 0 | 1.45–1.6 (1.6–1.75 long-form) |
| 20–32px | 0 to −0.015em | 1.2–1.35 |
| 36–56px | −0.015 to −0.035em | 1.05–1.15 |
| 64px+ | −0.025 to −0.05em | 0.9–1.05 |

- Measure: 45–75 characters for reading text (`max-width: 65ch` is a good default). Keep paragraphs to this width even when the content area is wider because of images or tables.
- Leave `font-optical-sizing: auto` enabled for web fonts with an optical-size axis. Judge tracking and leading at each rendered size in the actual face. Give scripts with tall glyphs more leading when needed. [The details of UI typography](https://developer.apple.com/videos/play/wwdc2020/10175/)
- Line-height is proportional to measure as well as size: narrow columns can sit near 1.5, wide ones need up to 1.75–2. Small text needs more leading; big headlines can drop to about 1.
- Use `text-wrap: balance` for headings and `text-wrap: pretty` for paragraphs where supported.
- Tabular numerals (`font-variant-numeric: tabular-nums`) for any column of numbers, prices, timers.

- Mixed sizes on one line (a large title beside small actions or metadata) align on the **baseline**, not the vertical centre.
- Left-align body text. Centre only headlines and blocks of two or three lines; rewrite shorter instead of centring long text. Right-align numbers in tables. If you justify text, enable hyphenation.
- Not every link needs a colour. In link-dense UI use weight or a darker ink; ancillary links can show underline or colour only on hover.

## 5. Weights

Use 2–3 weights. Common sets: 400/500/600, 400/600/700, or 300/400 for a light-display editorial look.
- Hierarchy can come from **size and colour** rather than weight. A 64px headline at 500 often looks more refined than at 800.
- Inverting the convention (light display, heavier body) is a valid identity move, but say so in design.md.
- Variable fonts allow intermediate weights (450, 520). Use them to fine-tune optical balance between sizes.

## 6. Treatments that add identity

Pick at most one or two:
- Two-tone headline: the first line in primary ink, the second in muted ink or accent.
- Italic serif clause inside a sans headline.
- Mono or all-caps eyebrow above section titles (`01 / FEATURES`).
- An oversized numeral or wordmark as a graphic element.
- Underline-on-hover links with a custom offset and thickness.
- Small caps for labels in editorial systems.

## 7. Platform notes

- **iOS:** use SF Pro via system fonts unless the brand requires otherwise; support Dynamic Type (`.font(.body)` styles, or `UIFontMetrics` scaling for custom fonts).
- **Android:** Material type roles (displayLarge … labelSmall) mapped to your scale; use `sp` units so user font scaling works; test at 200%.
- **Desktop:** base 13–14px for dense apps (macOS system 13pt; Windows Segoe UI Variable 14px), with platform-native fonts for chrome.
- **Web:** use `rem` for font sizes and let containers reflow with larger text. Check wrapping and control height at increased text sizes before reaching for truncation.
