# Native Apple UI

Identify the target platform, supported OS versions, UI framework, inputs, and form factors. Use the existing framework where it meets the workflow. Verify release-sensitive APIs and conventions against current Apple developer documentation, the deployment target, and the project's compatibility constraints. Give older supported versions a usable fallback when introducing a newer API.

## Build on system behavior

- Start with system buttons, navigation, toolbars, presentations, semantic colors, text styles, and safe areas. Style those controls within the product language. A custom replacement inherits responsibility for activation, keyboard and focus behavior, accessibility, cancellation, and state.
- Adapt to the actual inputs and layout. Account for iPad multitasking and pointer support, macOS window resizing and keyboard commands, and the focus and input models of watchOS, tvOS, or visionOS when targeted.
- Keep view state at a stable owner and make list identity independent of position. Pass read-only values for display and bindings when a child edits parent-owned state. Run side effects through actions or lifecycle APIs so rendering remains repeatable.
- Check navigation, cancellation, dismissal, and focus restoration. Use Dynamic Type-aware styles and check large text before choosing truncation or fixed dimensions. Treat safe areas, text direction, appearance, and accessibility preferences as layout inputs.
- Inspect the native accessibility tree for names, traits, values, reading order, adjustable actions, and focus. Use decorative-image hiding and label meaningful imagery or ambiguous icons.

## Design the macOS workflow

Choose the app's window and document model around the objects people work with. A document editor, library, utility, and multi-window workspace have different needs even when they share views with iPad. For a substantial surface, identify the applicable contracts before styling:

| Area | Design and verify |
|---|---|
| Commands | Standard menu placement and shortcuts, enabled state from the active window or focused editor, keyboard access to primary actions, and meaningful undo. |
| Windows and documents | Tie sheets to the appropriate window. Use an inspector for persistent supporting controls. Preserve standard window behavior and restore intentional arrangement and document state when applicable. |
| Selection and focus | Keyboard navigation, range and discontiguous selection where supported, contextual actions on the intended selection, and distinct focus and selection. Preserve native text editing. |
| Transfer and system integration | Use public pasteboard formats where useful. Exercise drag between windows or Finder, cancellation, invalid drops, and open/save or import/export when the workflow uses files. |

If SwiftUI cannot meet a required native contract on the supported OS, bridge the affected surface to UIKit or AppKit where appropriate. Verify the specific behavior before broadening the bridge.

### Unified window toolbar

When the main window has frequently used navigation, search, or actions that fit alongside the traffic lights, use a unified window toolbar. Place those controls in the same row as the native close, minimize, and zoom/full-screen buttons, so the title bar itself does useful work. Keep intentional spacing and a clear area for dragging the window. Let the native toolbar handle control groups and overflow as the window narrows, and retain the title when it identifies the document or window.

In SwiftUI, place items in the window toolbar and use `.windowToolbarStyle(.unified)` or `.unifiedCompact` for a denser row. In AppKit, attach an `NSToolbar` and set the window's `toolbarStyle` to `.unified` or `.unifiedCompact`. Choose the expanded style when the window title and controls need separate rows. At the minimum supported width, verify the traffic lights, window dragging, and access to primary actions through the toolbar or its overflow.

[SwiftUI window toolbar styles](https://developer.apple.com/documentation/swiftui/windowtoolbarstyle) · [AppKit unified toolbar](https://developer.apple.com/documentation/appkit/nswindow/toolbarstyle-swift.enum/unified)

## Gather target-specific evidence

Run the project's relevant build and tests when available. Exercise the primary task and its escape paths on the primary target and an applicable contrasting layout or input. Inspect larger text, dark appearance, Reduce Motion, Reduce Transparency, and Increase Contrast when the change affects them. Check the relevant accessibility behavior with VoiceOver or Accessibility Inspector. For macOS, use the keyboard-only path and verify window, menu, selection, transfer, or relaunch behavior when those contracts are in scope.

For settled-state tests, wait for the observable UI state, such as a sheet's dismissal and restored focus. A preview can show layout. Report separately what was exercised at runtime and what was inferred from the source. Tie review findings to the affected target and input.

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)
- [DXE Apple Native UI](https://github.com/kemiljk/skills/tree/main/skills/dxe-apple-native-ui) informed the target-specific workflow and verification checks.
