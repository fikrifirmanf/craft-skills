---
name: motion-graphic-design
description: >-
  Design, build, refine, and render motion graphics: kinetic typography, product launch films, animated explainers, logo stings, data animations, looping visuals, and interactive 3D demonstrations. Use for authored animated sequences, motion direction, storyboards, or improving their choreography. Ordinary static UI and isolated routine hover or modal transitions are outside the main scope.
---

# Motion Graphic Design

Turn a brief into an editable, deliberately choreographed animation and the requested delivery artifact. Think as a director, typographer, animator, and rendering engineer. The story, layout, and motion must agree.

## Choose the right path

Respect the requested stack and existing project. Inspect available tools, dependencies, assets, and render commands before introducing another engine.

| Need | Suitable approach |
| --- | --- |
| Short code-driven typography, diagrams, logos, or a standalone animation | HTML/SVG/Canvas with a controllable timeline; GSAP when orchestration warrants it |
| React composition, frame-accurate reusable videos, repeatable exports | Remotion |
| Existing HyperFrames project or requested Studio workflow | HyperFrames; consult its actual installed guidance |
| Interactive 3D product, cutaway, particles, or a browser world | Three.js, with separate playback and interaction modes |
| Rigged character, complex geometry, photoreal materials or optics | Blender scene and renders; assemble with the project's video tools |
| Small portable vector animation | SVG or Lottie, verified in the intended player |

Do not require unavailable sibling skills, house-specific scripts, a particular model, a paid service, or a universal default engine. Verify version-specific APIs against the installed package and official documentation.

Read [choreography.md](references/choreography.md) for visual direction, typography, scene timing, and transitions. Read [runtime-and-delivery.md](references/runtime-and-delivery.md) when implementing or exporting. For interactive geometry, characters, or procedural scenes, also read [three-dimensional.md](references/three-dimensional.md). Read [prompt-patterns.md](references/prompt-patterns.md) when translating a vague brief into a concrete sequence or adapting the studied examples. [sources.md](references/sources.md) records research coverage and links; it is not a required reading list for every invocation.

## Establish a brief with useful defaults

Extract the subject, audience, message, exact copy, visual references, duration, dimensions, fps, output format, looping behavior, sound/voice needs, asset restrictions, and existing brand language. Ask only for missing information that materially blocks the result. Otherwise state a small set of assumptions and proceed.

Distinguish these deliverables early:
- A playable browser animation needs working playback and interaction.
- A rendered film needs an actual encoded file and frame-driven visuals.
- A direction or storyboard request needs an actionable sequence; do not start implementing unless asked.

A single HTML file does not automatically mean offline: clarify through the implementation whether fonts, scripts, or media are external. Preserve explicit no-model/no-texture constraints without pretending that script dependencies are embedded.

For a new piece, write a compact `motion-plan.md` before implementation, or use the project's existing design/film spec. Include:
- One sentence stating what the audience should understand or feel.
- Canvas, duration, fps, delivery, and assumptions.
- Visual tokens: typography, palette, spacing, material, lighting, depth, and motion character, derived from the project when available.
- A beat table: time range, message, visible subject, action, camera, audio cue, and exit/handoff.
- A short list of assets and any facts needing verification.

This is a working spec, not an approval gate. Continue within the user's authorization.

## Direct the sequence

1. **Compose the strongest still first.** Establish hierarchy, silhouette, contrast, and readable type at delivery size. Motion cannot rescue an incoherent frame.
2. **Block the story.** Make the opening establish a question or subject; each subsequent beat changes understanding; the ending resolves it. Choose the number of beats from the duration and message.
3. **Assign attention.** Give each beat one dominant subject. Support it with staggered information, a motivated camera move, or a visible process. Keep actual reading time.
4. **Design handoffs before isolated entrances.** Name the outgoing carrier, incoming target, direction, and reason for each boundary. Match position and velocity when continuity is intended. A deliberate cut or dissolve is valid when it serves the film.
5. **Animate with contrast.** Anticipation, action, overshoot, settle, and a readable hold are ingredients, not mandatory phases for every object. Use a small repeated vocabulary and reserve the loudest move for the payoff.
6. **Bind to evidence.** Use narration word times and measured music accents when present. Use real product behavior and sourced data; a prompt is not evidence for a technical or historical claim.

Avoid defaulting to a series of independent cards that fade and rise, gratuitous camera orbit, interchangeable glows/particles, arbitrary direction changes, or idle wobble added to fill a timing gap. Ambient motion is appropriate when it depicts a living world or an explicit mood. Intentional stillness is appropriate for reading, tension, or release.

## Build one controllable animation

For rendered work, make visual state a reproducible function of frame/time, parameters, and a fixed seed. One master clock drives child timelines, camera, particles, captions, and visualized counters. No wall-clock timers, accumulated deltas, uncontrolled CSS animation, unseeded randomness, or incidental React state may determine the rendered frame.

For an interactive preview, let the playback controller advance time and call the same render/seek function. Keep user controls responsive and provide reset. Dynamic simulation must have a deterministic sampling or replay strategy if it also needs arbitrary seeking/export.

Keep copy, colors, dimensions, cues, and asset paths editable. Separate layout transforms from animated transforms when they would overwrite each other. Initialize all properties needed for seeking, including visibility, and await asset/font readiness before capture.

For browser experiences, provide pause/replay and a reduced-motion presentation that preserves the information. Do not apply an operating-system preference silently to alter a commissioned MP4. Avoid intense flashes, unsupported alpha promises, and motion that blocks essential interaction.

## Inspect, revise, deliver

- Render representative style frames, each major beat, and frames immediately around every scene boundary. Inspect the images at target size; sampling code alone cannot judge motion.
- Watch a low-cost draft at normal speed, then inspect suspect seams slowly. Check hierarchy, clipping, text reflow, collisions, unintended still gaps, and visual cause/effect.
- Seek forward and backward in a nonsequential order. Revisit the same time and check that it produces the same state.
- Check the loop across its wrap if applicable. Test controls/reset and a reduced-motion path for interactive work.
- Watch the actual encoded deliverable, with sound when present; verify dimensions, duration, fps, codec, and alpha requirements. Compare decoded colors when seamless embedding matters.

Fix observed problems and recheck affected beats and boundaries. Do not claim playback, render quality, or performance was verified unless it was observed. If rendering is unavailable, deliver the editable source with exact run/export instructions and identify the unverified step.

Return links to the requested output and editable source, a brief description of the direction, and any material limitation. Do not substitute a storyboard for an authorized finished animation or describe browser playback as an MP4 export.
