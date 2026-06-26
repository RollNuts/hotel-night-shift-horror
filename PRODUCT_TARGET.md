# PRODUCT TARGET

Status: genre locked.

This is a new Unreal Engine commercial game project. It does not inherit Fourfold Echoes, Unity-era assumptions, fixed-camera assumptions, four-ability systems, open-world structure, co-op, or action RPG design.

## Locked Product

- Genre: first-person, single-location, night-shift work horror.
- Setting: an old business hotel.
- Structure: one complete night.
- Expected playtime: 2-4 hours for a first clear, about 5-8 hours including multiple endings.
- Sales model: offline-first, buy-to-own premium game.
- First platform: Steam.
- Future: console expansion should remain possible, but the first product must not bloat into a multi-platform program.

## One-Sentence Product Promise

Work the night front desk of an old business hotel, decide who to help or refuse, patrol the building, and survive a single shift where routine service slowly becomes impossible to trust.

## Codex Decision Frame

- Build: a Steam-first offline Unreal horror game where a few hotel work actions create fear through repetition, judgment, sound, and environmental change.
- Do not build: Fourfold systems, multiplayer, open world, live-service features, large crafting/building/progression systems, or unrelated horror gimmicks.
- Market reason: a hotel night shift is immediately understandable in screenshots and videos, streamer-friendly, and feasible for one developer because the location is constrained.
- Unreal reason: Lumen, audio space, Sequencer, Niagara, Blueprint iteration, and first-person presentation can make a compact hotel feel premium.
- Solo-dev/low-cost reason: one facility, one night, no servers, limited cast, local saves, and a small action vocabulary keep production controllable.
- Art/audio bar: fear must come from lighting, sound, camera, UI restraint, and environmental staging, not just scripted jump events.
- No-small-room bar: progress counts only inside the production hotel context, not in isolated test rooms.
- Steam quality bar: the first screenshots and first trailer must show the front desk, camera monitor, hallway/guest-room response, and a clear abnormal event.
- Veripsa unit: track each task by hotel work loop value, production-level evidence, placeholder/license impact, and affected quality axes.

## Core Actions

Only these major player actions are approved unless a new action deepens an existing one:

- Answer the phone.
- Watch security cameras.
- Check a request or incident.
- Go to the location.
- Decide whether to open a door.
- Decide whether to admit or refuse a guest.
- Patrol a floor.
- Hide, close, or flee.
- Record or report what happened.

New features must deepen one of these actions. If the feature needs a new tutorial category, a new large UI surface, or a new subsystem, reject it by default.

## What We Are Building

- A compact, first-person business-hotel horror game.
- A loop of front desk work, surveillance, guest-room response, patrol, lock decisions, and incident reporting.
- A single night with branching outcomes based on judgment, mistakes, and abnormal-event handling.
- A production hotel level containing front desk, surveillance route, guest floors, back of house, elevator, emergency stairs, shortcut/lock logic, and sound-led unease points.
- Store-ready evidence: at least five real in-game screenshots and a trailer opening that communicates work plus fear quickly.
- A low-cost Unreal project that can ship without owned servers, accounts, or live operations.

## What We Are Not Building

- No Fourfold Echoes continuation.
- No Unity continuation.
- No open world.
- No co-op or online-required play.
- No permanent game server.
- No live service.
- No account system.
- No combat-first horror.
- No large inventory, skill tree, crafting, or shop economy.
- No complex NPC simulation.
- No procedural hotel sprawl.
- No test-room feature pile.
- No placeholder art, placeholder sound, placeholder UI, or marketplace-asset collage treated as complete.

## Workspace Boundary

Use this repository root for the public Unreal project.

Do not borrow mechanics, names, art direction, folder structures, or prototype logic from prior Fourfold, Unity, browser-prototype, or unrelated local projects.

Do not publish local machine paths, usernames, private directory structures, private strategy, credentials, or personal information in this public repository.

## Product Quality Bar

A feature is not complete when code works. It counts as product progress only when it is proven in the hotel production context:

- It works in the real hotel level or a clearly production-intent slice of it.
- It is readable in first-person camera.
- It has final-intent lighting.
- It has final-intent sound, ambience, or an approved silence reason.
- It has UI or diegetic feedback that does not over-explain.
- It improves either the work loop, fear loop, or both.
- It has screenshot or video evidence.
- It has performance, placeholder, and license status recorded.

## Daily Product Question

Every change must answer:

> Does this make the first Steam screenshot or first trailer segment stronger?

If not, it must either reduce a concrete release risk or be cut.
