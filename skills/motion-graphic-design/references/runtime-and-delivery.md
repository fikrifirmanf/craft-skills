# Runtime, reproducibility, and delivery

## One clock

Separate authoring time from playback time. The renderer samples a requested time; a browser playback loop is only one caller. Define duration, fps, and frame count explicitly. For N frames, export frame indices 0 through N−1 at t = frame/fps. Do not append a duplicate endpoint just to close a loop.

A robust browser capture contract is:

```js
// An implementation contract to supply, not an assumed library API.
window.motion = {
  ready,                 // Promise: fonts, textures, media, shaders ready
  duration,              // seconds
  fps,
  seek: async (seconds) => { /* set all state, then draw */ },
};
```

The capture runner awaits `ready`, sets the fixed viewport and device scale, calls and awaits `seek(frame/fps)`, and captures only after drawing is complete. Do not guess readiness with an arbitrary timeout. Video decoding, asynchronous asset loading, and GPU work may need engine-specific synchronization.

Initialize every property that can vary: visibility, transform, color, material uniforms, camera, counters, and any mask. For piecewise motion, clamp progress on both sides of the active interval. Hidden future scenes should not appear on frame zero or after backward seeking.

Use stable seeded values for particle identity and spatial arrangement. Generate them once from configuration; do not generate new randomness while rendering each frame. If noise changes over time, derive it from time and seed. Replaying the same timestamp must not depend on how many frames were visited before it.

## GSAP and HTML

Use one paused master timeline with named cues and intentional child ownership. Initialize starting state deliberately, then seek the master at capture time. Ensure child timelines are attached to the master instead of also playing autonomously. Avoid callbacks that mutate essential visual state only when a playhead crosses an event: a skipped or reversed seek may produce different results. Use deterministic property assignments/tweens or explicit frame evaluation.

Use nested wrappers when centering/layout transforms and animated transforms would otherwise overwrite each other. Scope selectors. Clean up timelines, observers, input handlers, and animation frames on unmount. In React, follow the installed GSAP integration's context/lifecycle guidance; keep animation work out of normal render and avoid rendering React state at playback frequency just to move a DOM node.

Scroll position can map to the same timeline for a scroll experience. Test viewport changes, pin boundaries, font loading, and reduced motion. Do not add smooth scrolling or scroll locking unless the experience calls for it. A scroll demo and a fixed-duration film have different controllers even when they share visual scenes.

## Remotion

Inspect the installed version and current official guidance before selecting components or APIs. Keep Remotion packages compatible with each other. Use the composition frame and configured fps to derive timing; isolate frame subscriptions to the smallest practical components. Preserve local versus global frame coordinates when nesting sequences.

CSS animations, timers, uncontrolled video playback, and real-time shader clocks do not become frame-driven just because they are placed inside React. Adapt the visual to the frame clock and use the version's supported media components/readiness mechanisms.

Make scenes and important elements useful editing units. Keep content, assets, and cue times configurable. Reuse product components where they render reliably; create a frame-driven visual equivalent when a component relies on live asynchronous state or its own animation clock. Do not silently alter the real application component to make a film render.

Use the project's established render command. The current official source exposes `npx remotion still` and `npx remotion render`; inspect local CLI help for flags rather than inventing options. Bundle once for multiple preview frames when the tool supports it.

Official authored references examined during skill creation:
- [Remotion markup](https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/remotion-markup/REFERENCE.md)
- [Remotion rendering](https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/remotion-render/REFERENCE.md)

## HyperFrames, Lottie, SVG, and Blender

For HyperFrames, inspect its installed composition contract, current CLI help, registry, and preview/render workflow. Reuse an appropriate existing block when it fits; inspect its timing, assets, and editability. Do not assume that scripts mentioned in another author's skill are installed here. Keep the master clock authoritative and the stage ground intentional, including scene visibility during overlaps.

For Lottie, validate the actual JSON and play it in the target runtime. AE feature support varies between players; masks, mattes, effects, fonts, and export size need inspection. Do not promise that a file works cross-platform based only on JSON validity. Verify alpha in the actual delivery format. SVG morphing requires compatible topology or a suitable morph engine; unrelated path strings will not necessarily interpolate well.

For Blender, set units, fps, frame range, camera, color management, and output paths before final rendering. Preserve the scene, rig, materials, and editable animation. Inspect cheap previews/contact sheets before expensive samples. Use frame-indexed evaluation when assembling Blender output into a code-driven film.

## Performance

For browser playback, use an explicit target and representative resolution/device. At 60 fps the whole frame budget is about 16.7 ms; at 30 fps about 33.3 ms. Measure a trace or actual frame times before claiming the target is met. Offline encoding speed and live playback fps are different measurements.

Prefer transform and opacity for DOM motion, but profile actual compositing. They are not automatic guarantees of GPU acceleration. Clip paths, blur, shadows, large transparent surfaces, inherited CSS variables, and many layers can be costly. Batch geometry reads before writes; avoid per-frame layout queries. Add `will-change` only where it helps, and remove unnecessary promoted layers.

Use instancing/batched buffers for many similar 3D objects. Reuse geometry/materials, cap pixel ratio according to the brief, control post-processing, and avoid per-frame allocations. A prompt's particle count is not a performance requirement unless the user makes it one. Test a modest count first.

## Audio

Skip audio when the piece is silent. When audio is requested, obtain the real track/voice assets and align to measured timestamps. Use word timings for narration cues and actual waveform/transient analysis for musical accents; BPM alone does not locate the first downbeat.

Keep dialogue intelligible with gain automation or ducking, fades at edits, and deliberate SFX peaks. Check loudness and true peak for the destination. A fixed dB offset does not guarantee the right mix; listen to the encoded file. Keep sound-off meaning for social/product pieces when appropriate. Confirm music/asset usage rights; use an authorized voice or ordinary TTS instead of inferring permission for voice cloning from a source prompt.

## Visual verification and export

Use a low-cost review loop:
1. Stills for start, each beat's arrival/action/settle, and ending.
2. Boundary frames at cut−2, cut−1, cut, cut+1, cut+2 frames.
3. A draft at lower resolution or samples with the real timing and sound.
4. Final render and inspection of the encoded artifact.

Exercise nonsequential seeks such as 0 → 70% → 20% → 70% → final → 0. Compare the repeated state, including camera and particles. Check the first/last cycle handoff at normal speed. A seamless loop means state and velocity continue across the period; it does not require duplicating the first image as the last frame.

Check with a suitable media probe: dimensions, fps, duration, frame count, video codec/pixel format, audio tracks, and any required color tags. Inspect decoded frames when matching a webpage background; color conversions can shift dark colors. For transparent delivery, select a format/codec that supports alpha and verify over a checkerboard. Ordinary H.264 MP4 does not carry the alpha expected from a transparent animation.

If useful tools are unavailable, deliver the editable source and the exact remaining export step. Report verification limits plainly. Keep versions in the project rather than overwriting the only approved master.
