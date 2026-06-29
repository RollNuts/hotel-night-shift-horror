# T2026-0629 Return Route Evidence Shot Polish

## Summary

- Task ID: T2026-0629-RETURN-ROUTE-EVIDENCE-SHOT-POLISH
- Owner: Codex
- Status: Ready for PR
- Product goal: Make the existing ReturnRoute back-knock beat read as a physical hallway response in the production evidence shot, not as abstract blockout marks.
- Hotel area: Guest hall return path after Room 203 refuses entry.
- Core action affected: The existing post-refusal return-route anomaly remains unchanged as a loop gate; the visual cue now moves with the back-knock.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteFloorEcho_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteWallEcho_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteHandShadow_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteTornSlip_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteWarningUnderline_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteSlipWriting_v0.obj`
  - `SourceAssets/GeometryGenerated/SM_GuestHall_ReturnRouteFootprint_v0.obj`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteFloorEcho_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteWallEcho_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteHandShadow_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteTornSlip_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteWarningUnderline_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteSlipWriting_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteFootprint_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_ReturnRouteColdGlow_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_ReturnRouteSlipPaper_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Binary Unreal assets claimed:
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteFloorEcho_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteWallEcho_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteHandShadow_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteTornSlip_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteWarningUnderline_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteSlipWriting_v0.uasset`
  - `Content/Hotel/Meshes/SM_GuestHall_ReturnRouteFootprint_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_ReturnRouteColdGlow_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_ReturnRouteSlipPaper_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Non-goals:
  - No new room, test map, hallway branch, enemy, chase, inventory, save system, HUD mode, or new player verb.
  - No new MRQ shot count; the existing ReturnRoute evidence camera is refined.
  - No downloaded model, Fab, Marketplace, Quixel/Megascans, paid asset, online service, analytics, or private SDK dependency.

## Quality Axes

- Gameplay: The report gate and ReturnRoute resolution timing remain the same.
- Visual: Adds project-authored floor smear, wall-echo, hand-shadow, torn-slip, slip-paper material, frantic-writing, underline, and footprint meshes so the back-knock has a non-box physical signature in the guest hall.
- Camera: Tightens `CAPTURE_ReturnRoute_BackKnockCandidate` to favor the back-knock evidence while keeping Room 203 context.
- Animation: Tagged ReturnRoute feedback props move during the existing anomaly and return to rest on resolution.
- Lighting: Adds cold glow and slip-paper materials plus a local wall skim light for the ReturnRoute evidence subject.
- SFX: Reuses `SFX_ReturnRouteKnockback_v0`; no new audio asset.
- UI: No HUD change; existing report-gate messaging remains.
- Level context: Work stays in `L_HotelNightShift_Slice` and strengthens the production map rather than a small-room prototype.
- Capture readiness: MRQ evidence must still pass the 10-shot PNG gate, with `hotel_spine_evidence_0006.png` visibly stronger.

## Risk And Compliance

- Placeholder impact: Registered under `ph.return_route_evidence_polish_v0` and `ph.return_route_runtime_feedback_v0`.
- License impact: Registered as `asset.return_route_evidence_shot_polish_v0`.
- Public repo risk: New raw assets are deterministic project-authored OBJ files, safe for public redistribution.
- Security/secret risk: No credentials, local identity files, private SDKs, or networked runtime code.
- Paid tool/asset risk: Uses the existing Unreal Engine install and project-authored generation only.
- Small-room risk: None; the slice improves the production hotel spine and existing evidence shot.

## Evidence

- Screenshot/video/log path:
  - Local ignored evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0006.png`
- Required verification:
  - Python compile for changed automation scripts.
  - Map generation and spine verification.
  - C++ editor build.
  - `Hotel.FrontDesk.PhoneResponse.LiveMap` automation, including visible ReturnRoute feedback motion and reset.
  - MRQ asset regeneration, MRQ render, and 10-shot PNG gate.

## Completion Statement

The ReturnRoute beat should no longer read as a few rectangular floor marks. It should read as the hallway answering the player with a cold physical afterimage that moves in sync with the existing back-knock.
