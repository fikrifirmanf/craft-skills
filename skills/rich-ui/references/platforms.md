# Platforms and stacks

How to turn design.md tokens into each stack's native theme, which conventions to respect, and how to get a screenshot so you can actually look at the result.

## Contents
1. Token mapping by stack
2. Platform conventions
3. Rendering and screenshots

---

## 1. Token mapping by stack

The principle is the same everywhere: **one theme source, components read roles, never raw values.**

### Web: CSS custom properties (any framework)
```css
:root {
  --color-background: #FAF7F2; --color-surface: #FFFFFF;
  --color-text-primary: #1C1917; --color-text-secondary: #57534E;
  --color-accent: #C2410C; --color-on-accent: #FFFFFF; --color-border: #E7E5E4;
  --font-sans: "Instrument Sans", system-ui, sans-serif;
  --text-display: clamp(2.5rem, 1.6rem + 3.6vw, 4rem);
  --space-1: 4px; --space-2: 8px; --space-4: 16px; --space-6: 24px; --space-section: 96px;
  --radius-control: 8px; --radius-card: 16px; --radius-pill: 9999px;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1); --dur-fast: 150ms;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --color-background: #0C0A09; /* … */ } }
:root[data-theme="dark"] { --color-background: #0C0A09; /* … */ }
```

### Tailwind
v4: put the tokens in `@theme { --color-accent: …; --radius-card: …; }`. v3: use `theme.extend` in `tailwind.config` pointing at the CSS variables (`accent: 'var(--color-accent)'`). Then use `bg-accent`, `rounded-card`. Avoid arbitrary values (`text-[13px]`, `bg-[#123456]`) in components; each one is a missing token.

### React Native / Expo
A `theme.ts` exporting `colors`, `space`, `radii` and `typography` objects (light/dark keyed), provided through context or a library (Restyle, Tamagui, Unistyles). Use `useColorScheme()` for the theme. Font scaling: leave `allowFontScaling` on and test at large sizes.

### SwiftUI / UIKit
- Colours in the asset catalog with Any/Dark appearances, exposed as `extension Color { static let accentRole = Color("Accent") }`, or a `Theme` struct in the environment.
- Type: `extension Font { static let display = Font.custom("X", size: 56, relativeTo: .largeTitle) }` so Dynamic Type still scales.
- Spacing and radius: `enum Space { static let md: CGFloat = 16 }`; use `RoundedRectangle(cornerRadius: r, style: .continuous)`.
- UIKit: `UIColor(named:)`, `UIFontMetrics(forTextStyle:).scaledFont(for:)`.

### Jetpack Compose
- `MaterialTheme(colorScheme = lightColorScheme(primary = Accent, background = …), typography = Typography(displayLarge = TextStyle(…)), shapes = Shapes(small = RoundedCornerShape(8.dp), …))`.
- Tokens Material doesn't model (surface-alt, spacing, motion): a custom `@Immutable data class` provided through `staticCompositionLocalOf`.
- Use `sp` for text and `dp` for layout; dynamic colour (Material You) only if the brand allows it.

### Flutter
`ThemeData(colorScheme: ColorScheme(...), textTheme: TextTheme(...), extensions: [AppTokens(...)])`, with a `ThemeExtension<AppTokens>` for spacing, radius and extra colours; read via `Theme.of(context).extension<AppTokens>()!`. Provide both `theme` and `darkTheme`.

### Desktop
- Electron / Tauri: web tokens as above; respect OS dark mode (`nativeTheme` / `prefers-color-scheme`) and the platform title-bar conventions (traffic lights left on macOS; controls right on Windows).
- WinUI 3 / WPF: `ResourceDictionary` with ThemeResources (Light/Dark/HighContrast); WinUI uses Mica/Acrylic materials and Segoe UI Variable.
- macOS AppKit/SwiftUI: semantic system colours for chrome (`.windowBackgroundColor`), brand tokens for content.
- Qt: QML singleton `Theme { property color accent: … }` or QSS variables generated from the tokens.
- GTK/libadwaita: CSS named colours (`@define-color accent_bg_color …`).

## 2. Platform conventions

Respect the platform where users have muscle memory; express the brand in colour, type, imagery and content.

| | iOS | Android | Web | Desktop |
|---|---|---|---|---|
| Touch/click target | 44×44pt | 48×48dp | 24×24px minimum, 44px for touch | 24–32px rows, 28–32px controls |
| Navigation | Tab bar + stack, swipe back | Nav bar/rail/drawer, system back | URL is state; back button works | Sidebar, menus, shortcuts, multi-window |
| Text scaling | Dynamic Type | sp + font scale | rem + zoom | OS text scale |
| Sheets/dialogs | Sheets with detents | Bottom sheets, dialogs | Dialog + focus trap | Modal windows used sparingly; inspectors |
| Primary action placement | Nav bar trailing / bottom | FAB or bottom/top bar | In the content flow | Toolbar, default button (Enter) |
| Safe areas | Notch, home indicator | Status/nav bars, edge-to-edge insets | Mobile viewport units (`dvh`) | Title bar, resizable windows |

Desktop specifics: hover states matter, keyboard shortcuts and focus order matter more, windows resize freely (design at 800×600 up to ultrawide), multi-select and right-click context menus are expected, and density is higher.

## 3. Rendering and screenshots

You must look at the result. Choose what the environment has:

- **Web:** Playwright (`npx playwright screenshot --viewport-size=390,844 http://localhost:5173 shot-mobile.png`, and again at 1440×900; add `--color-scheme=dark`), Puppeteer, or a browser MCP or tool if one is connected. Static HTML can be opened directly as `file://`.
- **iOS:** `xcrun simctl boot "<device>"`, build and run, then `xcrun simctl io booted screenshot shot.png`; SwiftUI `#Preview` plus snapshot tests (swift-snapshot-testing); set appearance with `xcrun simctl ui booted appearance dark`.
- **Android:** `adb exec-out screencap -p > shot.png`; Compose `@Preview` with Paparazzi or Roborazzi for headless snapshots; dark mode with `adb shell cmd uimode night yes`.
- **Flutter:** `flutter test` with golden files (`matchesGoldenFile`), or `flutter screenshot` on a running device.
- **React Native:** the iOS/Android commands above on the simulator or emulator.
- **Desktop:** OS screenshot of the window (`screencapture -l <windowid>` on macOS), or Playwright for Electron (`_electron.launch`), or the web build of a Tauri app.

If no rendering path exists at all, say so plainly, review the code against design.md instead, and tell the user which screens to check by eye.

Check at minimum: the smallest and largest supported sizes, light and dark (if supported), one long-content case, and keyboard focus on one interactive screen.
