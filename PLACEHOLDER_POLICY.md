# PLACEHOLDER POLICY

Status: active release safety policy.

Placeholders are allowed only as temporary development aids. They are never product-complete work.

## Codex Decision Frame

- Build: tracked temporary assets only when they unblock a defined verification or production step.
- Do not build: visible placeholder-dependent product claims, store assets, trailers, or demo content.
- Market reason: placeholder leakage makes the game look cheap, misleading, or AI-generated without care.
- Unreal reason: Unreal assets can spread through maps/materials/Blueprints, so placeholder status must be visible in names and ledgers.
- Solo-dev/low-cost reason: placeholders are acceptable only when they reduce risk and have a replacement plan.
- Art/audio bar: no temporary model, sound, UI, light, VFX, or animation counts as final.
- No-small-room bar: placeholders in test harnesses stay internal and cannot become product evidence.
- Steam quality bar: no public-facing placeholder appears in store, trailer, demo, or launch builds.
- Veripsa unit: each placeholder has owner, deadline, replacement condition, allowed use, and blocking label.

## Placeholder Definition

A placeholder is any asset, setting, sound, animation, UI, level, copy, or code path used in place of final-quality product material.

Examples:

- Blockout meshes.
- Default materials.
- Temporary SFX/music.
- AI-generated unreviewed images/audio.
- Marketplace assets not yet art-directed.
- Unstyled widgets.
- Debug text.
- Test animations.
- Temporary lighting.
- Temporary level dressing.
- Temporary store copy.

## Required Placeholder Record

Every placeholder must record:

- Placeholder ID.
- What it replaces.
- Owner.
- Date introduced.
- Replacement deadline or milestone.
- Required final-quality condition.
- License/source status.
- Allowed use: internal only, playtest, demo, store, trailer.
- Removal or replacement task ID.

Default allowed use is internal only.

## Public Build Rule

Store pages, trailers, public demos, press kits, and player-facing release builds must not include placeholders unless an explicit exception is approved in writing.

An exception must state:

- Why the asset is acceptable.
- What risk remains.
- How it is disclosed or controlled.
- Why replacement is not required.

## Placeholder Naming

Use clear prefixes:

- `PH_` for placeholder assets.
- `TMP_` for temporary local experiments.
- `TEST_` for test harness assets.
- `WIP_` for incomplete product-intent assets.

Any asset with these prefixes is automatically non-shipping until cleared.

## Replacement Quality Criteria

A placeholder can be cleared only when:

- It matches the art/audio direction.
- It has verified license status.
- It works in product camera and lighting.
- It has appropriate sound/motion/UI feedback if player-facing.
- It passes performance checks.
- It appears in evidence capture without obvious temporary quality.

Changing a filename is not clearing placeholder debt.

## Placeholder Budget

Each product slice has a placeholder budget:

- Internal foundation: placeholders allowed, tracked.
- Product Slice 0: placeholder allowed only outside the core player-facing moment.
- Steam page proof: no visible placeholders.
- Demo candidate: no player-facing placeholders.
- Launch candidate: no unresolved placeholders.

If placeholder count grows after a milestone, stop feature work and replace or cut.

## AI-Generated Placeholder Rule

AI-generated material starts as placeholder until:

- Tool and generation date are recorded.
- Terms allow commercial game use.
- Prompt/source inputs are recorded enough for review.
- Human transformation or selection notes are recorded.
- Style consistency is reviewed.
- Similarity/IP risk is checked.

Do not use AI-generated assets trained or prompted on identifiable copyrighted characters, brands, proprietary art, or unlicensed references.

## Veripsa Tracking

Every placeholder must be a Veripsa-tracked item or attached to a Veripsa task.

Required labels:

- `placeholder`
- `license-review` if rights are not fully cleared
- `store-blocker` if visible in any public-facing capture

No task may close as product-complete with a visible unapproved placeholder.
