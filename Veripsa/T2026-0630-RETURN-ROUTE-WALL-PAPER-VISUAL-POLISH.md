# Return Route Wall Paper Visual Polish

## Summary

- Task ID: `T2026-0630-RETURN-ROUTE-WALL-PAPER-VISUAL-POLISH`
- Owner: Codex
- Status: In PR
- Product goal: Make the existing ReturnRoute trailer-proof view read as a credible Room 203 hotel door and wall evidence shot instead of boxy placeholder geometry or abstract paper symbols.
- Hotel area: Production guest hall at Room 203 and the return-route wall.
- Core action affected: The player refuses Room 203, feels the return-route pressure, and sees physical hotel evidence before reporting.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/create_return_route_trailer_beat_assets.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `SourceAssets/GeometryGenerated/SM_Room203_*_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ServiceCartSilhouette_v0.obj`
  - `SourceAssets/TextureGenerated/TX_Hotel_RoomDoorPaint_v0.png`
  - `SourceAssets/TextureGenerated/TX_Hotel_ReturnRouteSlipPaper_v0.png`
  - `Content/Hotel/Meshes/SM_Room203_*_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ServiceCartSilhouette_v0.uasset`
  - `Content/Hotel/Textures/TX_Hotel_RoomDoorPaint_v0.uasset`
  - `Content/Hotel/Textures/TX_Hotel_ReturnRouteSlipPaper_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_ReturnRouteFadedInk_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_ReturnRouteSlipPaperTextured_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_RoomDoorPaintTextured_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Veripsa/T2026-0630-RETURN-ROUTE-WALL-PAPER-VISUAL-POLISH.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Meshes/SM_Room203_NumberDigits_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_DoorGrimeStreaks_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_DoorPaintChips_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_LockHardwareBreakup_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_NoticeTape_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_NoticeWriting_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_SconceBracket_v0.uasset`
  - `Content/Hotel/Meshes/SM_Room203_SconceGlass_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ServiceCartSilhouette_v0.uasset`
  - `Content/Hotel/Textures/TX_Hotel_RoomDoorPaint_v0.uasset`
  - `Content/Hotel/Textures/TX_Hotel_ReturnRouteSlipPaper_v0.uasset`
- Non-goals:
  - No genre final decision
  - No new room
  - No new gameplay verb
  - No chase, creature, AI, character animation, Niagara system, or runtime state expansion
  - No downloaded model, Fab, Marketplace, Megascans, paid media, private SDK, online service, account system, or public trailer approval claim

## Quality Axes

- Gameplay: Keeps the existing ReturnRoute anomaly/report loop unchanged.
- Visual: Adds project-authored procedural door paint texture, paper texture, Room 203 number plate/digits, grime streaks, paint chips, lock breakup, taped notice writing, sconce glass/bracket, and a service-cart silhouette. The capture should read as a neglected hotel corridor door, not as a set of colored blocks.
- Camera: Tightens the ReturnRoute proof sequence toward Room 203 door evidence and reduces the abstract right-wall clutter in frame.
- Animation: No new gameplay animation system; existing movable evidence actors remain the only runtime motion.
- VFX: No new particle or Niagara dependency.
- SFX: No sound change.
- Music/ambience: No change.
- UI feedback: No change.
- Level context: All proof remains in `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Performance: Small static meshes and two generated textures; no tick, simulation, AI, or streaming cost added.
- Capture readiness: Local MRQ PNG proof was refreshed after this pass and passed the PNG gate. The proof is still internal-only and not store/trailer-cleared final media.

## Risk And Compliance

- Placeholder impact: Adds `ph.return_route_wall_paper_visual_polish_v0`; updates the internal quality bar for `ph.return_route_trailer_proof_v0`. Store/trailer use remains `No`.
- License impact: Project-authored deterministic OBJ/PNG assets only; official Unreal editor/import/Sequencer/MRQ tooling; local ffmpeg MP4 evidence was generated but is not committed.
- Public repo risk: No auth material, local private files, personal data, or credentials intended. Texture import metadata was scrubbed so committed texture assets do not contain local absolute user-directory paths.
- Security/secret risk: No networked code, telemetry, install step, credential handling, or paid service.
- Paid tool/asset risk: None.
- Small-room risk: None; proof targets the production hotel map and existing ReturnRoute/Room 203 actors.
- Veripsa Core role: traffic coordination and path/scope/index checks only; not code/art/product review.

## Evidence

- Screenshot/video/log path:
  - `Saved/Logs/return_route_wall_paper_visual_create_r16.log`
  - `Saved/Logs/return_route_wall_paper_visual_assets_r16.log`
  - `Saved/Logs/return_route_wall_paper_visual_verify_r16.log`
  - `Saved/Logs/return_route_wall_paper_visual_mrq_render_r16.log`
  - `Saved/MovieRenders/ReturnRouteTrailerBeat/return_route_trailer_proof_*.png`
  - `Saved/MovieRenders/ReturnRouteTrailerBeat/return_route_trailer_proof_r16.mp4`
- Performance note: No new runtime system; the pass adds authored/static evidence meshes and two generated texture assets to the existing production hallway.
- Verification steps:
  - Python compile for the touched Unreal automation scripts: passed
  - Production-map asset regeneration: passed
  - Trailer-proof asset regeneration: passed
  - Production-map verifier before the final stricter verifier edit: passed, with 0 MapCheck errors and 0 MapCheck warnings
  - ReturnRoute trailer MRQ render refresh: passed, producing 30 PNG frames at 1280x720
  - ReturnRoute trailer-proof PNG gate: passed, 30 unique frames
  - Local ffprobe on the MP4 evidence: passed, H.264 1280x720, 8 fps, 30 frames, 3.75 seconds
  - Manual representative-frame inspection: passed for the current internal bar; frames now show Room 203 door, readable number plate/digits, paper notice, grime, door hardware, sconce, and softened right-wall evidence
  - Strengthened verifier script compile: passed
  - Strengthened verifier commandlet rerun after the last verifier edit: not completed because elevated approval timed out and the non-elevated editor launch hung until interrupted; treat this as a remaining verification gap
  - Public repo safety scan: passed after scrubbing texture import metadata; no local absolute user-directory paths, common credential markers, private key markers, GitHub tokens, Slack tokens, or AWS access key patterns detected in intended commit paths

## Completion Statement

The ReturnRoute proof now has a credible Room 203 visual anchor: a worn door, paper notice, number plate, grime, hardware, and local practical light. It is still internal authored-baseline art, but it no longer relies on square box readability for the current trailer-proof decision.
