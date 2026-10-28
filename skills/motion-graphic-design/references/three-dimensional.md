# 3D, mechanisms, characters, and particles

## Choose geometry for the explanation

Choose Three.js for a browser-controlled scene and Blender for an editable rig/material/camera production where its tools fit better. A flat illustration with modest parallax may need only SVG or layered 2D; do not build a heavy 3D scene merely to label a piece cinematic.

For a mechanical explainer, write a named parts inventory first. Identify visible shell, moving parts, pivots, internals, coordinate system, units, and constraints. Source dimensions when accuracy matters and label simplified geometry honestly. Check clearances, collisions, enclosure fit, and pivot placement before adding a dramatic animation.

Give parts stable identifiers and local rest transforms. Group by actual mechanical relationships: a limb attaches at its joint, a hinged shell rotates around its hinge, and a propeller spins around its shaft. Keep exploded offsets separate from rest transforms so reset/reassembly restores exact state rather than accumulating rounding errors.

## Explain through staged states

A useful interactive sequence is exterior → specific control → opening → mechanism → exploded view → operation → reassembly. Adapt it to the subject; seven stages is an example, not a requirement.

Represent stage selection and transitions explicitly. Define targets from the model's rest state, allow direct stage selection, and make interruption deterministic. Test nonadjacent jumps as well as next/previous. Reset must restore geometry, camera, labels, lighting, simulation parameters, and time.

Pair camera work with the lesson: move to expose a hidden control, approach a cutaway, or retreat to show assembly. Keep a point of interest readable during an orbit; a permanent orbit can conceal exactly what a viewer is trying to understand. Constrain user camera controls where clipping through the subject would break the explanation, without disabling useful inspection.

Show cause and order: a vessel fills before it sinks, a latch moves before a panel opens, airflow follows a coherent path, and labels identify the actual component. A historical or physical claim in a prompt needs separate verification. If time is compressed, preserve causal order and label the compression where useful.

## Materials, light, and staging

Test silhouette and hierarchy with simple materials. Then add the material behavior needed for the intended look: roughness, metalness, transmission, reflectors, and background contrast. Chrome and glass need a coherent environment; they cannot be made convincing solely by increasing highlights.

Use restrained depth of field. Focus the important moving part, allow for its full trajectory, and inspect close-ups for clipping and unexpected focus drift. Fix near/far planes and the camera envelope for all planned shots. Large zooms also require adequate canvas/render-target resolution; a close-up should not clip a globe or reveal a low-resolution texture by accident.

For an isometric SVG treatment, maintain projection, face shading, and painter's order. Draw solids with consistent top/side/front tones. Animate assembly relationships instead of scattering unrelated decorative components.

## Characters and small worlds

Begin with one subject, one setting, and one readable action or visual joke. Block key poses, expressions, camera framing, and the final pose before detailed modeling. Build or rig the body parts needed by those poses, then add secondary motion.

Maintain identity: silhouette, face, proportions, material, and directional consistency. Squash/stretch can convey a jelly mascot's mass; use joint constraints and rigid shapes for a machine. Ground contact and weight transfer matter more than adding a constant bob. Preserve the approved ending pose and scene when exporting.

A day/night or seasonal transformation needs a coherent light source and changes that reinforce it: key direction, shadow, sky, atmosphere, emissive windows, and moving environmental elements. Do not key every light independently without a shared story time.

## Rewindable particles and simulation

For a deterministic burst, assign each particle a stable origin, direction, speed, birth time, and seed. Evaluate progress from requested time. For a ballistic approximation, evaluate position analytically from origin, velocity, gravity, and elapsed time. Use deliberate interpolation back to rest when the effect needs exact reassembly.

Interactive gravity changes should recompute the intended trajectory from parameters, or restart/replay from a documented initial condition. Arbitrary backward seeking cannot be implemented by simply passing a negative delta to a stateful physics engine. For collisions, fluids, cloth, or skeletal simulation, use baked/cache data, deterministic fixed-step replay with checkpoints, or another verified seekable approach.

Separate story time from ambient time only when the narrative needs it, such as rewinding an event while a surrounding world continues. Both clocks must still derive from the master sample and explicit parameters for reproducible export.

Scale particle count to the measured device budget. Use instances or GPU buffers, avoid a DOM element per particle, and verify reset and repeated timestamps. For realistic basketball or other collision scenes, test the physical behaviors requested; a scripted parabola is a stylized animation, not proof of a working collision simulation.
