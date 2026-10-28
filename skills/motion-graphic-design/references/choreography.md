# Choreography and visual language

## Story and rhythm

Make the sequence an argument expressed through action. Useful structures include a question becoming a demonstration, a problem becoming a visible solution, a familiar object opening to reveal its mechanism, or a repeated motif transforming into the final mark. Establish the subject before multiplying detail.

A short product film can move through hook, demonstrated behavior, proof, and resolution. An explainer can move from event to scale, personal consequence, escalation, and callback. These are options, not a fixed five-scene template. Reduce copy and beats before speeding everything up.

Distinguish arrival time, action time, reading time, and handoff time. Text that is technically present while streaking past is not readable. Test the actual words at the intended viewing size and in the sound-off version. A camera move can continue while a label remains screen-stable. A dramatic pause before a result can sharpen it; do not fill every pause with motion.

For narration, the emphasized word should coincide with the visible event. Regenerating voice changes the schedule: recheck the affected cues and seams. For music, distinguish beat, bar, phrase, accent, and silence. Align important changes with meaningful accents rather than making every object bounce to every beat. Verify any scientific, historical, or product assertion independently of the creative prompt.

## Typography as geometry

- Establish a type hierarchy and a stable line layout before splitting text. Reserve word positions so revealing a phrase does not recenter it repeatedly.
- For a masked rise, clip a line/word wrapper and translate its child from below. Allow for ascenders, descenders, accents, italic overhangs, and shadow/filter extents.
- Split letters only for scripts whose shaping survives it. Prefer words or shaped runs for connected scripts; preserve an accessible unsplit text alternative in browser experiences.
- Make stagger serve reading order. Word motion is often clearer than character motion for longer copy. Bound total stagger; a long headline must not take several seconds just because each character inherited a delay.
- A short word may be the moving subject: stretch, rotate, replace, or let it become a diagram or object. Keep a stable readable interval around the transformation.
- Separate text from its texture and depth effects. Blur at a swap can hide a seam; blur throughout a reading interval destroys the message.
- Fit variable copy by measuring the actual font and shaped text. Prefer a purposeful reflow or less text over shrinking every title into a tiny line.

Useful exploratory starting ranges, to be tuned in the rendered context: 20–60 ms between short text units; 0.3–0.8 s for an authored entrance; 0.2–0.7 s for a brisk scene handoff. They are not acceptance thresholds and do not replace timing to the voice, reading, or brand.

## Motion character

Use a shared set of distance, duration, ease, scale, and blur tokens. Match tokens by semantic role, not by rounding unrelated values to the nearest number. A large panel and a tiny punctuation mark can share a family while moving at different speeds.

| Intent | Motion choice | Watch for |
| --- | --- | --- |
| Arrival and clarity | Quick initial response, eased settling | Slow start that delays the message |
| Moving within an established scene | Smooth acceleration and deceleration | Abrupt stop or drifting target |
| Gesture and direct manipulation | Direct tracking, velocity-aware spring release | Input lockout or snap on interruption |
| Mechanical or time-based process | Linear or physically explained progression | Decorative easing that falsifies rate |
| Playful character action | Anticipation, arcs, squash/stretch, follow-through | Rubber motion applied to rigid machinery |
| Reveal or impact | Contrast in scale/speed, short anticipation, clear consequence | Everything peaking at once |

Apply animation principles selectively: staging makes the important silhouette legible; anticipation makes an action predictable; overlap suggests joints and mass; arcs explain paths; follow-through shows energy being absorbed. Exaggeration should preserve the subject's identity and mechanical meaning.

For ordinary product controls embedded in a demo, make the demonstrated UI behave credibly. Routine press feedback is usually much shorter than a cinematic shot. Do not import a film's dramatic camera or delay into the live product interaction.

## Scene continuity

Plan a boundary as outgoing state → carrier → incoming state. The carrier can be a word, cursor, diagram node, card, logo fragment, camera trajectory, or a repeated contour. A carrier is strongest when position, scale, and velocity agree across the boundary.

For a continuous lateral handoff, carry motion along the same signed axis. For a depth handoff, distinguish growing from shrinking scale: an outgoing push paired with an incoming pull produces a visible reversal. Keep incoming child animations from fighting the wrapper's direction during that interval.

A practical lateral study is a partial-frame accelerating exit followed by a decelerating entrance continuing the same direction. Match measured velocities at the cut; merely using related easing names does not guarantee equality if distances, durations, or sampling phases differ. Prefer short travel when a full-screen slide adds no information.

A small vocabulary might include:
- **Shared-object morph:** the same object changes function or layout, keeping the viewer oriented.
- **Cut in motion:** swap while the eye follows a trajectory; align position and speed.
- **Depth pass:** move through a subject to reveal a deeper layer; preserve scale direction.
- **Occlusion reveal:** an object or mask covers the change and then clears it.
- **Word cascade:** the reading order becomes the transition path.
- **Direct cut or dissolve:** use for a chapter, contrast, time passage, or an intentional mood change.

Use optical blur or a focus pull as an accent. Keep the swap near the designed blur peak and inspect adjacent frames for double images. Composite against an intentional stage background: partial opacity can expose the page ground and cause a flash. A continuous-motion style is a creative option; it is not a universal ban on cuts, dissolves, or stillness.

## Specialized treatments

**Cursor-led product demo:** aim the visible tip at the true target. Show arrival, a readable press, and a response on the causing cue. Prevent cursor overlap with copy. Use actual product states; do not imply a feature exists because a mockup can animate it.

**Data and statistics:** animate values together with their marks and units. Keep a consistent scale and baseline. Do not let elastic bars suggest negative values or changing totals. Preserve the final data long enough to read.

**Blueprint/whiteboard:** introduce structure, point to the relevant area, show the specific change, then resolve the visual. Draw enough geometry to explain the subject without tracing every stroke at the same speed. A continuous single-screen explanation can be stronger than a parade of title cards.

**Glass, chrome, and refraction:** readable reflection and lighting establish the material. A chrome object needs something to reflect. Use translucency sparingly behind type; verify contrast over the full moving background. Expensive filters are a deliberate budget item, not a polish default.

**ASCII:** map luminance to a selected glyph ramp, account for character aspect ratio, and keep cell dimensions stable. Treat it as a visual language with designed contrast, not a label applied to random text.

**Captions and overlays:** distinguish verbatim subtitles, emphasis words, and explanatory labels. Avoid duplicating all three for the same sentence. Check platform overlays and critical-content collisions without forcing an arbitrary blank band into every composition. Preserve subtitle completeness when accessibility or verbatim captions are requested.
