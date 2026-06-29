# T2026-0629 Return Route Anomaly

## Summary

- Task ID: T2026-0629-RETURN-ROUTE-ANOMALY
- Owner: Codex
- Status: Ready for PR
- Product goal: Make the first hotel loop require a return-through-the-hall beat after Room 203 refuses entry before the report can be filed.
- Hotel area: Room 203 guest hall back toward the front desk.
- Core action affected: After refusing Room 203, the player must pass through the guest hall and let the back-knock resolve before the report log accepts filing.

## Scope

- Files/assets touched:
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Automation/Unreal/create_hotel_mrq_evidence_assets.py`
  - `Automation/Tools/check_hotel_mrq_capture_pngs.py`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `SourceAssets/AudioGenerated/SFX_ReturnRouteKnockback_v0.wav`
  - `Content/Hotel/Audio/SFX_ReturnRouteKnockback_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Binary Unreal assets claimed:
  - `Content/Hotel/Audio/SFX_ReturnRouteKnockback_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Non-goals:
  - No test map, small room, new room, or isolated prototype surface.
  - No enemy, chase, combat, inventory, save system, new UI framework, or new core action.
  - No paid assets, third-party media, store capsule art, trailer capture, online service, analytics, or private SDK dependency.

## Quality Axes

- Gameplay: The report log refuses filing after Room 203 refusal until the return-route anomaly resolves in the guest hall.
- Visual: The production map now includes a return floor cold patch, back-knock direction stripes, wall status slip, backtrack footprints, and cold pulse cue.
- Camera: Eight MRQ evidence stills were refreshed, including `CAPTURE_ReturnRoute_BackKnockCandidate`.
- Animation: No final character animation added; the slice uses runtime state, light intensity, and audio as the product-facing feedback.
- VFX: Return-route feedback uses a cold light pulse placeholder; no Niagara/VFX system added.
- SFX: Adds project-authored deterministic `SFX_ReturnRouteKnockback_v0` as a one-shot return-route cue.
- Music/ambience: Existing hotel ambience remains; no music added.
- UI feedback: Existing HUD objective/status/prompt now blocks early reporting and tells the player to return through the hall.
- Level context: Work stays in `L_HotelNightShift_Slice` and does not create a small-room test surface.
- Performance: Runtime work is limited to the existing pawn tick, one proximity check during `DoorRefused`, one light update while active, and one one-shot sound.
- Capture readiness: MRQ render and PNG gate passed for all eight evidence images; still placeholder art/audio, not store/trailer-ready.

## Risk And Compliance

- Placeholder impact: Registered in `PLACEHOLDER_LEDGER.md` under geometry, audio, HUD, and runtime feedback placeholders.
- License impact: Registered in `ASSET_LICENSE_LEDGER.md` as project-authored, free, internal-only, no third-party media.
- Public repo risk: No secrets, tokens, personal files, private SDKs, or downloaded paid assets added.
- Security/secret risk: No networked runtime code, credentials, local-machine paths, or private identifiers committed.
- Paid tool/asset risk: Uses existing Unreal Engine installation and official editor/MRQ tooling only.
- Small-room risk: None; gameplay and capture remain in the production hotel spine map.

## Evidence

- Screenshot/video/log path:
  - Local ignored evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0000.png` through `hotel_spine_evidence_0007.png`
  - Return route evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0006.png`
- Performance note:
  - MRQ render completed 8 shots in about 27 seconds at 1280x720.
- Verification steps:
  - Python compile: passed for hotel spine generation, verification, MRQ asset generation, and PNG gate scripts.
  - Map generation: passed; saved `L_HotelNightShift_Slice`.
  - Spine verifier: passed with 22 assets, 120 required actors, 86 tagged actors, 13 audio actors, 6 movable feedback meshes, 50 non-interactive polish actors, map check 0 errors and 0 warnings.
  - C++ build: `HotelNightShiftHorrorEditor Mac Development` succeeded.
  - Automation: `Hotel.FrontDesk.PhoneResponse.LiveMap` passed, including early report rejection, return-route active state, return-route resolution, and final report filing.
  - MRQ assets: `LS_HotelSpine_Stills` and `MRQ_HotelEvidencePng` regenerated and validated.
  - MRQ PNG gate: passed 8 evidence PNGs.

## Completion Statement

The Room 203 refusal no longer collapses immediately back into paperwork: the player must carry the refusal back through the guest hall, hear the hotel answer from the route behind them, and only then record the incident at the desk.
