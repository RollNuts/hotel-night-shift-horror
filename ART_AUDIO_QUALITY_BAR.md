# ART AND AUDIO QUALITY BAR

Status: active. This file prevents code-only completion.

## Codex Decision Frame

- Build: visual, animation, VFX, audio, camera, UI, and level-context quality together with gameplay.
- Do not build: silent, unlit, unanimated, debug-looking, or placeholder-facing features counted as done.
- Market reason: perceived quality drives screenshots, trailers, wishlists, reviews, and streamer interest.
- Unreal reason: use Lumen, materials, Niagara, animation tools, Sequencer, and audio routing to raise finish without huge content volume.
- Solo-dev/low-cost reason: polish fewer assets and interactions deeply instead of producing many weak variants.
- Art/audio bar: every player-facing action needs an explicit visible and audible decision.
- No-small-room bar: test-room captures are engineering evidence, not art/audio approval.
- Steam quality bar: public assets must be final-intent, readable, licensed, and representative of the build.
- Veripsa unit: label missing art/audio/UX/performance/evidence as blockers, not polish wishes.

## Principle

The game is not complete when it functions. It is complete when the player can see, hear, understand, and feel the intended moment inside a product-quality context.

Art, sound, animation, camera, lighting, VFX, and UI are not polish after implementation. They are implementation.

## Product Image Bar

Every public-facing scene must satisfy:

- A screenshot communicates the fantasy without caption text.
- The focal subject is clear at thumbnail size.
- Lighting supports both mood and readability.
- Color choices are intentional and not a random asset mix.
- Materials share a coherent art direction.
- Composition has foreground, subject, and background hierarchy.
- UI does not cover the moment being sold.
- No placeholder, debug, or unlicensed asset is visible.

If the scene cannot produce at least one store-page candidate screenshot, it is not product progress.

## Motion Bar

Every player-facing action must define:

- Anticipation.
- Action.
- Impact or result.
- Recovery.
- Cancel or input buffering behavior where relevant.
- Camera response where relevant.
- VFX response.
- SFX response.
- UI/diegetic feedback response.

If the action only changes numbers or collision state, it is unfinished.

## Front Desk Art Density Animation Bar

Front-desk art density is not complete because the desk has more objects. Props that imply use must either read as deliberate still dressing or have product-intent motion.

For phone, log, bell, drawers, keys, monitor controls, lamps, papers, and guest-service props:

- Pivots, scale, contact points, and collision must support believable motion.
- Motion must include readable start state, action, settle, and no sliding, clipping, or popping.
- Animation timing must be checked from the first-person front-desk camera.
- SFX, light, UI, or material response must be planned or implemented for player-facing motion.
- Default, test, unretargeted, or linear placeholder motion does not clear the bar.

If a front-desk prop is visible in store/trailer/demo evidence, unresolved motion quality is `animation-missing` or placeholder debt, not final art density.

## Audio Bar

Every repeated or important event must have an audio decision:

- Player input confirmation.
- Successful action.
- Failed or unavailable action.
- Phone ring, receiver, keypad, camera monitor, door, lock, elevator, stairwell, guest knock, and report/log state changes.
- Danger warning.
- Reward or completion.
- Menu navigation.
- Ambience or room tone.

Audio must be:

- Short enough for repeated play.
- Mixed so critical cues remain readable.
- Thematically consistent.
- Licensed and tracked.
- Replaced before store/trailer/demo if placeholder.

## VFX Bar

VFX must clarify, not decorate.

Acceptable VFX:

- Shows an abnormal hotel state or environmental response.
- Clarifies monitor interference, light failure, reflection, doorway change, or impossible movement.
- Supports a trailer-readable fear beat.
- Creates a memorable product image without hiding gameplay.

Reject VFX that:

- Obscures hotel navigation or door/guest decisions.
- Adds GPU cost without meaning.
- Looks like default engine particles.
- Competes with UI or target readability.
- Exists only because Niagara can do it.

## UI/UX Bar

UI should be sparse, readable, and integrated with the experience.

Required:

- Controller-readable text sizes.
- Clear focus states.
- Minimal but sufficient feedback.
- No debug labels in product builds.
- Pause/settings/restart flows that do not break immersion.
- Visual language consistent with art direction.

Rejected:

- Placeholder fonts in product builds.
- Raw debug values.
- Unstyled widgets.
- Walls of instruction text.
- UI that explains what art/sound/level design should have taught.

## Level Context Bar

Mechanics must be evaluated in a real product context:

- First-person product-intent camera.
- Product-intent lighting.
- Product-intent scale.
- Product-intent collision.
- Product-intent audio space.
- Real hotel approach path: front desk, monitor, elevator/stair, hallway, guest-room door, or back-of-house route.
- Real failure/retry path.

A test map can prove a bug fix. It cannot prove product value.

## Store Evidence Bar

Each major feature must produce at least one of:

- Screenshot candidate.
- 15-second clip candidate.
- Before/after feel capture.
- Performance capture.
- Audio mix capture.
- QA replay evidence.

Evidence that only shows an editor viewport, wireframe, or debug map is engineering evidence, not market evidence.

## Minimum Acceptance Template

For any gameplay-facing feature, Codex must report:

- Player experience improvement.
- How it looks in product context.
- How it sounds.
- How it changes operation or feel.
- Screenshot/video evidence path.
- Performance impact.
- Placeholder status.
- License status.
- Next quality risk.

"Implemented" is not an acceptable completion report.

## Quality Debt Labels

Use these labels in Veripsa Core:

- `art-missing`: no production-intent visual.
- `audio-missing`: no production-intent sound.
- `animation-missing`: motion/pose timing incomplete.
- `vfx-missing`: event lacks visible feedback.
- `camera-unverified`: not checked in product camera.
- `ui-placeholder`: visible UI not final-quality.
- `lighting-placeholder`: lighting not production-intent.
- `store-evidence-missing`: no screenshot/clip proof.
- `license-unverified`: asset/source rights not cleared.

Any task with one of these labels cannot be called product complete.
