# Return Route Physical Evidence Polish

## Summary

- Task ID: `T2026-0630-RETURN-ROUTE-PHYSICAL-EVIDENCE-POLISH`
- Owner: Codex
- Status: In PR
- Product goal: Make the existing ReturnRoute evidence read less like boxes/abstract symbols and more like physical hallway contact in the old hotel.
- Hotel area: Production guest hall return route after Room 203 refusal
- Core action affected: Return through the hall, see physical evidence of the back-knock pressure, then continue to report

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Automation/Unreal/create_return_route_trailer_beat_assets.py`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteColdVein_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteDirectionScratch_v0.obj`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteColdVein_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteDirectionScratch_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Veripsa/T2026-0630-RETURN-ROUTE-PHYSICAL-EVIDENCE-POLISH.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteColdVein_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteDirectionScratch_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
- Non-goals:
  - No new room
  - No new gameplay verb
  - No new chase, creature, AI, animation system, VFX system, or runtime state
  - No downloaded model, Fab, Marketplace, Megascans, paid media, private SDK, online service, account system, or public trailer approval claim

## Quality Axes

- Gameplay: Keeps the existing ReturnRoute anomaly/report loop unchanged.
- Visual: Replaces rectangular cold patch/direction stripes with project-authored irregular cold-vein and scratch meshes, flattens the wall slip, thins the red writing, and softens wall echo/ripple scale.
- Camera: Reuses existing ReturnRoute evidence and trailer-proof cameras; only the proof sequence actor keys are softened to match the new physical evidence pass.
- Animation: Existing movable ReturnRoute feedback actors still participate in the back-knock wave; no new animation system.
- VFX: No new Niagara or particle dependency.
- SFX: No sound change.
- Music/ambience: No change.
- UI feedback: No change.
- Level context: All proof remains in `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Performance: Two small static mesh assets replace simple cube props; no runtime system cost.
- Capture readiness: Existing hotel MRQ and ReturnRoute trailer-proof PNG gates pass locally, but the updated ReturnRoute MRQ render could not be refreshed in this run because the approved elevated MRQ command timed out in permission review and the non-elevated MRQ launch produced no new PNG/log output. Do not treat the existing ReturnRoute PNGs as post-polish visual proof.

## Risk And Compliance

- Placeholder impact: Updates `ph.return_route_evidence_polish_v0` and `ph.return_route_trailer_proof_v0`; store/trailer use remains `No`.
- License impact: Project-authored deterministic OBJ assets only; official Unreal editor/import/Sequencer/MRQ tooling.
- Public repo risk: No auth material, local private files, personal data, or credentials intended.
- Security/secret risk: No networked code, telemetry, install step, or credential handling.
- Paid tool/asset risk: None.
- Small-room risk: None; proof targets the production hotel map and existing ReturnRoute actors.
- Veripsa Core role: traffic coordination and path/scope/index checks only; not code/art/product review.

## Evidence

- Screenshot/video/log path:
  - `Saved/Logs/return_route_physical_evidence_create_r1.log`
  - `Saved/Logs/return_route_physical_evidence_verify_r1.log`
  - `Saved/Logs/return_route_physical_evidence_assets_r1.log`
  - `Saved/Logs/return_route_physical_evidence_mrq_render_r1.log` attempted without the required map argument, reached game-window creation, and was terminated without new PNG output
  - `Saved/MovieRenders/ReturnRouteTrailerBeat/return_route_trailer_proof_*.png` existing local PNGs passed the gate, but their timestamps predate this polish pass
- Performance note: No new runtime system; production map actor count rises only by replacing old cube props with two authored mesh assets.
- Verification steps:
  - Python compile: passed
  - Production-map asset regeneration: passed
  - Production-map verifier: passed
  - Trailer-proof asset regeneration: passed
  - ReturnRoute trailer MRQ render refresh: not completed in this run; must be retried with the known-good map argument and elevated/local GUI render permission before claiming post-polish visual proof
  - ReturnRoute trailer-proof PNG gate: passed on existing pre-polish PNGs only
  - Existing hotel MRQ PNG gate: passed on existing ten-shot evidence PNGs
  - Manual representative-frame inspection: existing ReturnRoute PNGs still show the pre-polish origami-like slip and strong symbol bars, so they are not accepted as improved visual evidence
  - Public repo safety scan: passed for touched text files, generated OBJ files, map, cinematic assets, and touched ReturnRoute mesh assets

## Completion Statement

The ReturnRoute evidence should read more like disturbed hotel material: cold stain veins on the floor, scratched directional marks instead of bars, a flatter wall slip, thinner red writing, and softer wall contact marks, all still inside the established production hallway beat.
