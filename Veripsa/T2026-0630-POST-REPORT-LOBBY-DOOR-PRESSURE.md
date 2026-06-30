# Post-Report Lobby Door Pressure

## Summary

- Task ID: `T2026-0630-POST-REPORT-LOBBY-DOOR-PRESSURE`
- Owner: Codex
- Status: Complete
- Product goal: Make the existing post-report lobby hold beat read on screen as a physical hotel glass door under pressure, not a cluster of boxy placeholder bars.
- Hotel area: Production front desk and lobby glass door
- Core action affected: The post-report wait after the player files the Room 203 report

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Automation/Unreal/create_post_report_lobby_door_pressure_proof_assets.py`
  - `Automation/Tools/check_post_report_lobby_door_pressure_proof_pngs.py`
  - `SourceAssets/GeometryGenerated/SM_LobbyDoor_CrackWeb_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_LobbyDoor_LatchPlate_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_LobbyDoor_PalmSmear_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_LobbyDoor_SmudgedGlassPane_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_LobbyDoor_TornTapeCross_v0.obj`
  - `SourceAssets/TextureGenerated/TX_Hotel_LobbyDoorSmudgedGlass_v0.png`
  - `Content/Hotel/Meshes/SM_LobbyDoor_*.uasset`
  - `Content/Hotel/Textures/TX_Hotel_LobbyDoorSmudgedGlass_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_LobbyDoor*.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_PostReportLobbyDoorPressureProof_6s.uasset`
  - `Content/Hotel/Cinematics/MRQ_PostReportLobbyDoorPressureProofPng.uasset`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Veripsa/T2026-0630-POST-REPORT-LOBBY-DOOR-PRESSURE.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Meshes/SM_LobbyDoor_CrackWeb_v0.uasset`
  - `Content/Hotel/Meshes/SM_LobbyDoor_LatchPlate_v0.uasset`
  - `Content/Hotel/Meshes/SM_LobbyDoor_PalmSmear_v0.uasset`
  - `Content/Hotel/Meshes/SM_LobbyDoor_SmudgedGlassPane_v0.uasset`
  - `Content/Hotel/Meshes/SM_LobbyDoor_TornTapeCross_v0.uasset`
  - `Content/Hotel/Textures/TX_Hotel_LobbyDoorSmudgedGlass_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_LobbyDoorAgedTape_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_LobbyDoorCrackLight_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_LobbyDoorHandOil_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_LobbyDoorSmudgedGlass_v0.uasset`
  - `Content/Hotel/Cinematics/LS_PostReportLobbyDoorPressureProof_6s.uasset`
  - `Content/Hotel/Cinematics/MRQ_PostReportLobbyDoorPressureProofPng.uasset`
- Non-goals:
  - No new genre decision
  - No new room
  - No new gameplay verb
  - No monster, chase, humanoid animation, AI, inventory, or UI system
  - No third-party media, Fab, Marketplace, Megascans, paid asset, private SDK, online service, account system, music, or public trailer approval claim

## Quality Axes

- Gameplay: Keeps the existing post-report hold beat and only replaces weak visual evidence around the lobby glass door.
- Visual: Adds authored smudged glass, crack web, palm smear, torn tape, latch plate, darker glass/tape/oil/crack materials, and removes old boxy cue props from the proof sequence.
- Camera: Adds a 6-second internal proof sequence that frames the lobby door from the production front desk.
- Animation: Sequencer proof gives visible door-pressure motion through rattling crack/latch actors and camera push-in; runtime interaction state is unchanged in this slice.
- VFX: Uses material/emissive/light treatment only; no Niagara dependency.
- SFX: Reuses the existing lobby glass rattle cue; no new sound asset.
- Music/ambience: No change.
- UI feedback: No new UI system.
- Level context: All runtime/proof work targets `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Performance: Adds small static mesh/material assets and proof-only Sequencer tracks; no persistent runtime system.
- Capture readiness: Adds an internal Sequencer/MRQ proof lane and a PNG gate for blank/dark/static/short output and lobby-door ROI detail.

## Risk And Compliance

- Placeholder impact: Adds `ph.post_report_lobby_door_pressure_visual_v0` and `ph.post_report_lobby_door_pressure_proof_v0`; store/trailer use remains `No`.
- License impact: Project-authored OBJ/PNG/material/map/proof assets only; official Epic Unreal, Sequencer, and Movie Render Queue tooling.
- Public repo risk: No auth material, local private files, personal data, or credentials intended.
- Security/secret risk: No networked runtime code, telemetry, install step, or credential handling.
- Paid tool/asset risk: None.
- Small-room risk: None; the production hotel lobby/front desk map is used.
- Veripsa Core role: traffic coordination and path/scope/index checks only; not code, art, or product review.

## Evidence

- Screenshot/log path:
  - `Saved/Logs/post_report_lobby_door_pressure_create_r9.log`
  - `Saved/Logs/post_report_lobby_door_pressure_assets_r10.log`
  - `Saved/Logs/post_report_lobby_door_pressure_mrq_render_r11.log`
  - `Saved/Logs/post_report_lobby_door_pressure_verify_r10.log`
  - `Saved/Logs/post_report_lobby_door_pressure_livemap_r5.log`
  - `Saved/MovieRenders/PostReportLobbyDoorPressure/post_report_lobby_door_pressure_proof_*.png`
- Verification steps:
  - Python compile for updated Unreal automation and proof PNG gate
  - Production-map generation completed with `MapCheck: 0 errors, 0 warnings`
  - MRQ render of `LS_PostReportLobbyDoorPressureProof_6s`: completed 1 job
  - Manual visual spot check accepted frames `0000`, `0060`, and `0138` after removing the oversized black pane/white-stick look from the proof
  - Post-report lobby-door proof PNG gate: passed 24 PNGs with 24 unique frames
  - Production-map verifier: verified 112 assets, 241 required actors, 217 tagged actors, 19 audio actors, 64 movable feedback meshes, 157 non-interactive polish actors, and 52 authored mesh references
  - LiveMap automation: `Hotel.FrontDesk.PhoneResponse.LiveMap` succeeded in PIE

## Completion Statement

The post-report lobby hold moment now has a project-authored glass-door pressure pass in the production hotel map: the proof shot shows a greenish smudged lobby glass surface, crack web, latch, grime, tape, and pressure motion rather than relying on square placeholder bars. This is still an internal authored-baseline pass, not final store or trailer art.
