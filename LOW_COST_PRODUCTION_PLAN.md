# LOW COST PRODUCTION PLAN

Status: active for the hotel night-shift horror product.

## Codex Decision Frame

- Build: a compact single-hotel game with a few repeated actions, strong atmosphere, stable saves/settings, and clear release evidence.
- Do not build: recurring-service dependencies, broad infrastructure, online play, large procedural systems, or feature volume outside the hotel loop.
- Market reason: a focused horror product can sell through clarity, atmosphere, streamer readability, and player judgment stories.
- Unreal reason: use engine-native first-person presentation, Lumen, audio, Blueprint, Sequencer, and Niagara instead of custom services.
- Solo-dev/low-cost reason: one building, one night, limited actions, local save, and no servers keep production controllable.
- Art/audio bar: cost is controlled by fewer finished spaces and sounds, not by accepting cheap-looking output.
- No-small-room bar: production value is proven in the hotel level.
- Steam quality bar: every milestone must improve screenshot/trailer/demo readiness.
- Veripsa unit: each task must show hotel-loop value, release-risk reduction, or evidence creation.

## Cost Model

The project avoids fixed monthly operations:

- Offline-first gameplay.
- Local save/profile data.
- No permanent game server.
- No owned account system.
- No external database.
- No external API dependency.
- No live events.
- No content moderation pipeline.

One-time free or paid-free tools/assets may be used only when they are legal, safe, and recorded. Paid purchases, subscriptions, or services require explicit user approval before use.

## Scope Budget

Initial product budget:

- One hotel.
- One night.
- 2-4 hour first clear.
- 5-8 hour replay/ending total.
- Core actions limited to the list in `REQUIRED.md`.
- Small cast, mostly heard or implied unless a character is essential.
- Reusable hotel props with strong art direction.
- A small set of high-impact abnormal events.
- No combat system.
- No online system.

## Asset Strategy

Allowed:

- Free official tools.
- Existing installed tools.
- Free assets with clear commercial-use rights.
- Original project-made props, textures, SFX, music, and 3D models.
- AI-assisted drafts that are recorded and reviewed.

Required:

- Every asset goes into `Ledgers/ASSET_LICENSE_LEDGER.md`.
- Free assets must still declare redistribution rights before entering the public repo.
- Marketplace/Fab/Quixel/free packs must be adapted to the hotel's tone.
- If a fitting free asset does not exist, create a simple original asset rather than importing unclear material.

Forbidden:

- Unclear-license assets.
- Paid purchases without explicit approval.
- Raw paid/restricted assets in public git unless redistribution is explicitly allowed.
- AI-looking final capsule art, key screenshots, logo, monster/guest identity, or representative audio without human review.

## Milestone Plan

| Milestone | Purpose | Exit Gate |
| --- | --- | --- |
| M0: Public Repo Baseline | Public-safe Unreal project, required rules, ledgers, PR/issue templates | Repo is public, no secrets/restricted assets, `REQUIRED.md` present |
| M1: Hotel Production Slice Plan | Define the first product slice around front desk, phone, monitor, and one guest-room response | Slice has level area, actions, evidence, placeholder, and asset lists |
| M2: Unreal Baseline Smoke | Open project in UE 5.8 and confirm settings, folders, and source control are clean | Editor opens, no missing required plugin, no restricted content |
| M3: First Hotel Loop Slice | Phone rings, request appears, player checks camera/log, reaches a door, decides, records result | Works in product-intent hotel level with light/audio/UI evidence |
| M4: Fear Loop Pass | Add one abnormal variation that changes the same work loop | Trailer-readable 15-second beat, no new subsystem bloat |
| M5: Demo Candidate | Short polished playable shift segment | No visible placeholders, stable save/settings/restart |
| M6: Steam Page Proof | Store screenshots, trailer opening, copy, tags, price research | Wishlist reason is clear |
| M7: Launch Candidate | Complete single-night game | Quality, rights, build, save/settings, performance, and store gates passed |

## Next Minimum Work

The next product-aligned implementation work is not a test room. It is:

> Create the first hotel production-slice plan and then build only the front desk/phone/camera/first-door response path inside the actual hotel level.

Before that implementation starts, create or update:

- `HOTEL_LEVEL_PLAN.md`
- `FIRST_PRODUCT_SLICE.md`
- Asset list for front desk, phone, monitor, hallway, door, elevator/stair cues.
- SFX list for phone, fluorescent hum, hallway ambience, door, elevator.
- Veripsa task for the first production slice.

