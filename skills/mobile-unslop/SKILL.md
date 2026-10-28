---
name: mobile-unslop
description: Enforces production-grade native and cross-platform mobile engineering and eliminates crash-prone, rejected-at-review app code. Trigger whenever writing or modifying iOS (Swift, SwiftUI, UIKit), Android (Kotlin, Jetpack Compose, Java), React Native/Expo or Flutter code, Info.plist, AndroidManifest.xml, or app permissions.
---

# Mobile Anti-Slop Protocol

Mobile slop crashes on a user's phone, gets rejected by App Review or Play Console, or locks out VoiceOver/TalkBack users. None of that shows up in a simulator happy path.

## 1. Crash operators (HARD BANS outside tests)
- **Swift:** no `try!`, no `as!`. Avoid force unwraps `!` (`@IBOutlet` is the only idiom). Use `guard let`, `if let`, `??`, `do/catch`.
- **Kotlin:** avoid `!!`; use `?.let`, `?:`, `requireNotNull(x) { "why" }`.
- **Dart:** check `mounted` before `setState` after any `await`.

## 2. Threads & lifecycles (HARD BANS)
- **iOS:** never `DispatchQueue.main.sync`. UI work is `@MainActor`. Prefer `.task { }` over `.onAppear { Task { } }` so work is cancelled when the view goes away.
- **Android:** no `GlobalScope`, no `runBlocking`, no `Thread.sleep` in app code. Use `viewModelScope`/`lifecycleScope` and `delay()`. In Compose, state lives in `remember { mutableStateOf(...) }` (or `rememberSaveable`, or a ViewModel).
- No network or disk I/O on the main thread on any platform.

## 3. Layout, type & accessibility
- **Dynamic Type / font scale:** iOS text uses text styles (`.font(.body)`, `UIFont.preferredFont`); Android text uses `sp`. Layouts must survive the largest accessibility size.
- **No device-size hardcodes:** no `.frame(width: 375)`, no `UIScreen.main.bounds`. Use flexible frames, `containerRelativeFrame`, `GeometryReader`, window size classes.
- **Every icon-only control has a label:** SwiftUI `Label("Delete", systemImage: "trash")` or `.accessibilityLabel`; Compose `contentDescription = stringResource(...)`; RN `accessibilityRole="button"` + `accessibilityLabel`.
- **Touch targets:** at least 44x44pt (iOS) / 48x48dp (Android).
- **Strings are localisable:** Compose uses `stringResource`; SwiftUI `Text("...")` keys go into the String Catalog.
- **React Native lists** use `FlatList`/`FlashList`, not `ScrollView` + `.map`.

## 4. Security & privacy (HARD BANS)
- **Tokens and credentials** go in Keychain, EncryptedSharedPreferences/Keystore, `expo-secure-store` or `flutter_secure_storage`. Never UserDefaults, SharedPreferences or AsyncStorage.
- **HTTPS only:** no `NSAllowsArbitraryLoads`, no `usesCleartextTraffic="true"`. Scope exceptions to named debug domains.
- **No `android:debuggable` in the manifest**, and back up only what is safe (`dataExtractionRules`).
- **Release builds don't log:** use `os.Logger` / Timber / `debugPrint` instead of `print`, `NSLog`, `Log.d`, `println`.

## 5. Permissions are a contract
- Every protected API needs its declaration: an `NS...UsageDescription` (iOS) or `<uses-permission>` (Android). A missing purpose string crashes the app on first access.
- **Purpose strings are specific:** "Scan receipts to add expenses without typing" passes review; "This app needs camera access" does not.
- Ask at the moment of use, explain first, and handle denial gracefully.
- Declare required-reason APIs (UserDefaults, file timestamps, disk space, system uptime) in `PrivacyInfo.xcprivacy`.
- Components with an `<intent-filter>` declare `android:exported`.
- Remove permissions you do not use.

## 6. Mandatory verification loop
Before claiming a mobile task is complete:
1. Call `audit_mobile_slop` with every modified file or directory (omit `files` to audit git changes).
2. Call `verify_app_manifest` whenever a feature touches camera, photos, location, microphone, contacts, calendar, Bluetooth, health, motion, NFC, notifications or networking.
3. Call `verify_mobile_build` (fast `syntax` mode by default; `mode: "full"` before declaring a feature done when time allows).
4. On `FAIL`, fix every ERROR and re-run until `PASS`. Suppress a verified false positive with `// unslop-ignore RULE_ID -- reason`; a suppression without a reason is an ERROR.
5. `SKIPPED` means a toolchain (Xcode, Gradle, Flutter) is missing: tell the user the build was not verified.
