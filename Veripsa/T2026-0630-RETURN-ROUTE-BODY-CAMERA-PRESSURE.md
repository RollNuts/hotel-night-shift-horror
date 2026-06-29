# Return Route Body Camera Pressure

## Summary

- Task ID: `T2026-0630-RETURN-ROUTE-BODY-CAMERA-PRESSURE`
- Owner: Codex
- Status: In PR
- Product goal: Make the existing ReturnRoute beat read as physical pressure in normal first-person play, not only as moving hallway props.
- Hotel area: Production guest hall return route after Room 203 refusal
- Core action affected: Return through the hall, feel the back-knock pressure, then continue to report

## Scope

- Files/assets touched:
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`
  - `Automation/Unreal/create_return_route_trailer_beat_assets.py`
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Veripsa/T2026-0630-RETURN-ROUTE-BODY-CAMERA-PRESSURE.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
- Non-goals:
  - No new room
  - No new gameplay verb
  - No new monster, chase, humanoid animation, or AI system
  - No new third-party asset, Fab, Marketplace, Megascans, paid media, private SDK, online service, or public trailer approval claim

## Quality Axes

- Gameplay: Keeps the established `DoorRefused -> ReturnRouteCleared -> ReportFiled` loop and only strengthens the existing return-route beat.
- Visual: Existing tagged ReturnRoute floor/wall/slip feedback moves as a delayed hallway wave so it does not read as one synchronized blockout twitch.
- Camera: The first-person camera briefly offsets and widens FOV during impact, then fully returns to rest after the anomaly.
- Animation: Uses procedural transform offsets on existing tagged feedback actors; no final animation claim.
- VFX: Uses existing lights/materials only.
- SFX: Reuses the existing ReturnRoute knockback and pursuit-tail sound lane; no new sound asset in this slice.
- Music/ambience: No change.
- UI feedback: No change.
- Level context: All proof remains in `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Performance: Adds a small active-only camera transform/FOV update during the existing 2.35 second anomaly; no persistent tick work beyond the existing pawn update path.
- Capture readiness: The internal ReturnRoute trailer-proof camera keys now include early body-pressure/FOV movement and must pass the PNG gate.

## Risk And Compliance

- Placeholder impact: Updates `ph.return_route_runtime_feedback_v0` and `ph.return_route_trailer_proof_v0`; store/trailer use remains `No`.
- License impact: Project-authored code/scripts/assets only; official Epic Unreal, Sequencer, Automation, and MRQ tooling.
- Public repo risk: No auth material, local private files, personal data, or credentials intended.
- Security/secret risk: No networked code, telemetry, install step, or credential handling.
- Paid tool/asset risk: None.
- Small-room risk: None; proof targets the production hotel map and existing ReturnRoute actors.
- Veripsa Core role: traffic coordination and path/scope/index checks only; not code/art/product review.

## Evidence

- Screenshot/video/log path:
  - `Saved/Logs/return_route_body_camera_build_r1.log`
  - `Saved/Logs/return_route_body_camera_assets_r2.log`
  - `Saved/Logs/return_route_body_camera_verify_r1.log`
  - `Saved/Logs/return_route_body_camera_livemap_r1.log`
  - `Saved/Logs/return_route_body_camera_mrq_render_r1.log`
  - `Saved/MovieRenders/ReturnRouteTrailerBeat/return_route_trailer_proof_*.png`
- Performance note: Active only during the existing ReturnRoute anomaly; no new persistent actor/component system. The MRQ command generated the full 30-frame PNG set but did not self-exit, so it was terminated after output and verified by the PNG gate.
- Verification steps:
  - Python compile
  - Unreal editor build
  - Unreal trailer-proof asset generation
  - Production-map verifier
  - LiveMap automation for first loop and ReturnRoute camera reset
  - MRQ render of `LS_ReturnRoute_TrailerBeat_15s`
  - ReturnRoute trailer-proof PNG gate
  - Public repo safety scan

## Completion Statement

The ReturnRoute beat should now read in normal play as pressure hitting the player's body and then crawling down the hall: the view lurches/widens, existing evidence props answer in a wave, the tail light/audio remains, and all feedback returns to rest before the report can be filed.
