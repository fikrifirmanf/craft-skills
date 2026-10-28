# Effects and motion

## Contents
1. Elevation strategies
2. Shadows
3. Glass and blur
4. Gradients, glows, texture
5. Imagery
6. Motion timing
7. What to animate
8. Reduced motion

---

## 1. Elevation strategies

Choose **one** main strategy and write it in design.md:

| Strategy | Look | Fits |
|---|---|---|
| Hairline | 1px borders, flat fills | Technical, editorial, dense tools, dark UIs |
| Shadow | Soft layered shadows, white cards on off-white | Quiet SaaS, consumer apps |
| Tonal | Surfaces step in lightness, no borders or shadows | Material-style apps, dark mode |
| Glass | Translucent fill plus backdrop blur plus inner highlight | Overlays over rich media, dark hero chrome |
| Hard offset | 2–3px outline plus a solid offset shadow | Neo-brutalist |

A secondary strategy is allowed for exactly one component class (for example, a hairline system where only dialogs get a shadow).

## 2. Shadows

- Layer two shadows: a tight contact shadow plus a soft ambient one.
  `0 1px 2px rgb(16 24 40 / 0.06), 0 8px 24px rgb(16 24 40 / 0.08)`
- Tint shadows with the field hue (navy- or brown-black), not pure black.
- 2–3 levels at most: raised (cards), overlay (menus, popovers), modal.
- Coloured glow (`0 0 0 1.5px accent/0.5`, `0 0 24px accent/0.3`) counts as an accent use. Ration it like the accent.
- Inset highlight on dark glass or buttons: `inset 0 1px 0 rgb(255 255 255 / 0.1)`.

## 3. Glass and blur

Glass only works over something worth blurring (imagery, gradients, scrolling content).
- Recipe: fill at 50–75% alpha of the surface colour, `backdrop-filter: blur(12–24px) saturate(1.1–1.5)`, a hairline border at 8–15% white, and an optional inset top highlight.
- Text on glass must pass contrast against the *worst-case* content behind it. Increase fill opacity until it does.
- Performance: avoid blur on large scrolling areas or many simultaneous layers, especially on mobile and low-end hardware.
- Native equivalents: SwiftUI `.background(.ultraThinMaterial)`; Android `RenderEffect.createBlurEffect` (API 31+); Windows Mica/Acrylic; macOS `NSVisualEffectView`.

## 4. Gradients, glows, texture

- **Confine them to a zone** (see color.md §6). Write the zone and maximum size in design.md.
- Hero washes: 2–3 radial gradients anchored at the corners, fading to transparent by about 70%, covering about 15–20% of the hero.
- Texture: grain (SVG noise at 3–6% opacity), dot grid (`radial-gradient(color 1px, transparent 1px) 0 0/16px 16px` at 4–10% alpha), or hairline grid. Keep it faint enough that it reads as a surface, not a pattern.
- Mesh or aurora backgrounds only when the brand calls for them, and never behind body text without a solid plate.

## 5. Imagery

Choose one primary image type: photography, 3D renders, flat illustration, line diagrams, or product screenshots. Write the treatment:
- Photography: a consistent colour grade; a scrim (black at 30–60%, or a gradient from the text side) when text overlaps.
- Product screenshots: inside device or browser frames, or a cropped detail at real UI scale; never a blurry full-page shrink.
- Illustration: one style, one stroke weight, using the palette's colours.
- Always give an aspect ratio, a fallback colour and alt text.

## 6. Motion timing

| Category | Duration | Easing |
|---|---|---|
| Micro (hover, press, toggle) | 100–180ms | ease-out / `cubic-bezier(0.2,0,0,1)` |
| Component (menu, tooltip, accordion) | 180–280ms | standard `cubic-bezier(0.4,0,0.2,1)` |
| Entrance (section reveal, dialog in) | 300–600ms | expressive `cubic-bezier(0.16,1,0.3,1)` |
| Exit | ~70% of the entrance time | ease-in |
| Page / route transition | 250–400ms | standard |
| Loops (shimmer, progress) | 1–2s | linear |

Corpus median: 220ms. Exits are faster than entrances. Stagger lists by 30–60ms per item, capped at about 6 items.

## 7. What to animate

- Animate `transform` and `opacity`; avoid width, height, top and left (layout thrash).
- Entrance: fade plus 8–16px translate, not large slides or scale-from-zero.
- Feedback motion must be immediate (start within 100ms of input).
- Springs suit direct manipulation (drag, sheet snap, iOS/Compose gestures). Bounce on brand-playful systems only, and on small elements.
- Don't animate on every scroll position (scroll-jacking); parallax at most once per page, subtly.
- Native: SwiftUI `.animation(.snappy)` / `.spring(duration:bounce:)`; Compose `animate*AsState` with `spring()` or `tween()`; Flutter `Curves.easeOutCubic`; Material motion tokens.

## 8. Reduced motion

Required on every platform:
- Web: `@media (prefers-reduced-motion: reduce)` swaps movement for opacity fades or nothing; stops loops and autoplay.
- iOS: `@Environment(\.accessibilityReduceMotion)`. Android: check the animator duration scale. Desktop: respect the OS setting.
- Never convey information *only* through motion.
