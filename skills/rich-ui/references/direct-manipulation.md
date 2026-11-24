# Direct manipulation and interruptible motion

Use this for interfaces where people drag, flick, scrub, or redirect a moving surface. Prefer an existing platform interaction or accessible component when it already provides the behavior.

## Press, track, and cancel

- Show feedback on press. Keep ordinary buttons on native activation so release, dragging away, keyboard activation, and assistive technology retain their expected semantics.
- For a custom web drag, record the grab offset and track the active `pointerId` with Pointer Events. Use pointer capture once appropriate for the control. Express allowed browser panning with `touch-action` on the gesture region. For example, a horizontal carousel can allow `pan-y` so the page still scrolls vertically. Preserve zoom and scrolling elsewhere.
- For competing gestures, track movement from the first sample and use a small distance and direction threshold before committing. Around 8–10 CSS pixels is a starting point for touch, subject to device testing. Once engaged, follow the pointer 1:1 within bounds. Suppress the click associated with a completed drag and clean up on `pointercancel` or lost capture.
- If the boundary benefits from a soft stop, apply progressively smaller movement beyond it. For signed overshoot `x`, a positive reference dimension `L`, and a resistance constant `k` around `0.55`, try `x * L * k / (L + k * Math.abs(x))`. Use a hard bound where exact values or safety require it.
- Use a shared position value for drag and settling. Update cheap visual properties such as `transform` and `opacity`. Batch manual rendering with `requestAnimationFrame` when useful and sample timestamps from input events. Profile before adding `will-change` or animated filters.

## Release, project, and retarget

1. Estimate release velocity from recent timestamped movement, in units per second. Treat a pause before release as a stop. If the visible position is rubber-banded, hand off its velocity after resistance.
2. For momentum-sensitive snapping, project the release position and choose a valid snap point from that projection. Apple’s example uses exponential decay. For a velocity `v` in px/s and a per-millisecond decay factor `d`, project `current + (v / 1000) * d / (1 - d)`. Tune `d` to the component, travel range, and snap spacing. A factor of `0.998` is a scroll-like starting point. Restrict projected skips when the interaction promises one step at a time.
3. Pass the sampled velocity to the spring in the units its API expects. For APIs that expect velocity normalized to distance, use `v / (target - current)` and handle a zero-distance target explicitly. Run separate axis values and velocity components for two-dimensional motion.
4. On re-grab, start tracking from the live rendered value and preserve the new grab offset. On an animated retarget, carry the spring's current velocity. Cancel stale completions so a previously closing sheet cannot unmount a reopened sheet. Keep reversal, dismissal, and focus behavior available during transitions.

Start with a critically damped spring. Add slight overshoot where momentum makes it meaningful. Apple's damping ratio describes the shape of the decay, and response controls its speed. Neither maps directly to a library's physical damping coefficient or fixed duration. In Motion, use a physics spring or a supported `visualDuration` spring to retain velocity. The `duration` option starts at rest. Check the project's version and verify the result with a flick and a mid-flight retarget. [Motion spring documentation](https://motion.dev/docs/spring)

## Show the destination and preserve access

- Anchor a popover to its trigger and a sheet to its relevant edge. Preserve the spatial relationship on exit and make intermediate drag positions indicate where the surface can settle.
- Provide a keyboard, assistive, and pointer alternative for gestures that perform an action. A reorder control can expose move buttons, and a swipe-to-dismiss sheet can expose a close button. Keep focus and final state equivalent under reduced motion. Remove inertia and elastic travel where needed, keeping intentional direct control and clear feedback.
- Where the project uses sound or haptics, tie them to a meaningful event such as commit or snap. Coordinate them with visual feedback and keep the state understandable if either channel is unavailable or disabled.

## Verify the interaction

Prototype with working input and inspect it on the relevant hardware. Try a slow drag, a quick flick, a paused release, reversal during settle, pointer cancellation, and ordinary scrolling next to the control. Check keyboard activation, focus after dismissal, and reduced motion. Use a recording or slow playback to investigate visible jumps. Wait for the observable end state in automated checks. Use separate checks for mid-flight interruption.

[Apple's Designing Fluid Interfaces](https://developer.apple.com/videos/play/wwdc2018/803/) covers response, redirection, and momentum projection.
