# T2026-0629 Patrol Listen Anomaly

## Summary

- Task ID: T2026-0629-PATROL-LISTEN-ANOMALY
- Owner: Codex
- Status: Ready for PR
- Product goal: Make the first hotel loop require attentive listening in the patrol transition before Room 203.
- Hotel area: Front desk to elevator/stair transition to Room 203 route.
- Core action affected: After monitor check, the player must hold at the taped patrol line and listen before the Room 203 refusal interaction can proceed.

## Scope

- Files/assets touched:
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `SourceAssets/AudioGenerated/SFX_PatrolListenDrop_v0.wav`
  - `Content/Hotel/Audio/SFX_PatrolListenDrop_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Binary Unreal assets claimed:
  - `Content/Hotel/Audio/SFX_PatrolListenDrop_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Non-goals:
  - No new room, test map, or isolated graybox progress.
  - No enemy, combat, inventory, save system, elevator travel, stair navigation system, or new UI framework.
  - No paid assets, third-party media, store capsule art, trailer capture, online service, or analytics.

## Quality Axes

- Gameplay: Room 203 remains blocked until the player holds still at the taped patrol line after monitor check.
- Visual: Existing patrol stop-line and decision props remain in the production map; the feedback light is now tagged as `Hotel.Feedback.PatrolListenLight` so runtime control is deterministic.
- Camera: Seven MRQ evidence stills were refreshed, including the patrol decision cue shot.
- Animation: No final character animation added; the slice uses runtime state, light intensity, and audio as the product-facing feedback.
- VFX: Patrol-line feedback uses an authored light pulse placeholder; no Niagara/VFX system added.
- SFX: Adds project-authored deterministic `SFX_PatrolListenDrop_v0` as a one-shot listen cue.
- Music/ambience: Existing elevator/stair patrol bleed ambience remains; no music added.
- UI feedback: Existing HUD objective and desk status now tell the player to hold/listen and return if they leave the line.
- Level context: Work stays in `L_HotelNightShift_Slice` and does not create a small-room test surface.
- Performance: Runtime work is limited to the existing pawn tick, one proximity check, one light intensity update while active, and one one-shot sound.
- Capture readiness: MRQ render and PNG gate passed for all seven evidence images; still placeholder art/audio, not store/trailer-ready.

## Risk And Compliance

- Placeholder impact: Registered in `PLACEHOLDER_LEDGER.md` under audio, HUD, and runtime feedback placeholders.
- License impact: Registered in `ASSET_LICENSE_LEDGER.md` as project-authored, free, internal-only, no third-party media.
- Public repo risk: No secrets, tokens, personal files, private SDKs, or downloaded paid assets added.
- Security/secret risk: No networked runtime code, credentials, or local-machine paths committed.
- Paid tool/asset risk: Uses existing Unreal Engine installation and official editor/MRQ tooling only.
- Small-room risk: None; gameplay and capture remain in the production hotel spine map.

## Evidence

- Screenshot/video/log path:
  - Local ignored evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0000.png` through `hotel_spine_evidence_0006.png`
  - Patrol route evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0004.png`
- Performance note:
  - MRQ render completed 7 shots in about 24 seconds at 1280x720.
- Verification steps:
  - Python compile: passed for hotel spine generation, verification, MRQ asset generation, and PNG gate scripts.
  - Map generation: passed; saved `L_HotelNightShift_Slice`.
  - Spine verifier: passed with 21 assets, 108 required actors, 75 tagged actors, 12 audio actors, 6 movable feedback meshes, 50 non-interactive polish actors, map check 0 errors and 0 warnings.
  - C++ build: `HotelNightShiftHorrorEditor Mac Development` succeeded.
  - Automation: `Hotel.FrontDesk.PhoneResponse.LiveMap` passed, including patrol listen movement/leave negative gates and hold-to-resolve path.
  - MRQ assets: `LS_HotelSpine_Stills` and `MRQ_HotelEvidencePng` regenerated and validated.
  - MRQ PNG gate: passed 7 evidence PNGs.

## Completion Statement

The first hotel loop now contains a real listening beat before Room 203: the player cannot rush the patrol transition, gets readable HUD/audio/light feedback at the taped line, and only progresses after holding still long enough to hear the hotel respond.
