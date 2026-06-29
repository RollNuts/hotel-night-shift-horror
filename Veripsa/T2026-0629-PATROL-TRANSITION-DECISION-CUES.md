# T2026-0629 Patrol Transition Decision Cues

## Summary

- Task ID: T2026-0629-PATROL-TRANSITION-DECISION-CUES
- Owner: Codex
- Status: Implemented locally; PR traffic coordination pending
- Product goal: make the elevator/stair transition read as a patrol decision beat inside the production hotel route without adding a new mechanic before the product slice needs it.
- Hotel area: production elevator/stair transition in `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Core action affected: leave the front desk after the phone/monitor beat, read the unsafe route split, continue toward Room 203, return, and file the report.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Automation/Unreal/create_hotel_mrq_evidence_assets.py`
  - `Automation/Tools/check_hotel_mrq_capture_pngs.py`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Veripsa/T2026-0629-PATROL-TRANSITION-DECISION-CUES.md`
- Binary Unreal/source assets claimed:
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
  - `Content/Hotel/Materials/M_Hotel_WornRouteTape_v0.uasset`
- Non-goals:
  - No elevator travel, stair navigation, patrol route choice state, inventory/key pickup, new objective text, new UI prompt, enemy, or route lock.
  - No C++ changes.
  - No new room, test room, alternate prototype map, or detached demo scene.
  - No final modular architecture, final decal set, final prop meshes, final audio mix, trailer capture, or Steam store claim.
  - No paid asset, marketplace import, third-party media, or externally downloaded content.
  - No assumption that Veripsa Core reviews correctness; Core coordinates PR traffic only.

## Quality Axes

- Gameplay: the existing route gains a readable listen-before-moving beat while preserving the current phone, monitor, Room 203, and report loop.
- Visual: adds non-interactive stop-line, footprints, dropped key tag, night-audit clipboard marks, wall arrows, and stair-door cold light leak using blockout primitives.
- Camera: MRQ evidence now has seven shots and includes `CAPTURE_PatrolRoute_DecisionCueCandidate` for the patrol decision readability beat.
- Animation: unchanged; no runtime animation or movement state added.
- VFX: unchanged; the cold stair leak is material/light readability, not a new effect system.
- SFX: adds two extra ambient sound placements using existing project-authored elevator/stair ambience so the split reads spatially.
- Music/ambience: strengthens route identity through local elevator groan and stair air bleed sources, still placeholder.
- UI feedback: unchanged; no new text prompt or HUD instruction was added.
- Level context: all additions are in the production hotel spine map, not a small room or isolated test map.
- Performance: runtime cost is limited to simple static meshes, one point light, and two ambient sound actors in an already-small production slice.
- Capture readiness: MRQ output is exactly seven 1280x720 PNGs; the new patrol shot passed automated brightness/visibility gates and manual visual inspection.

## Risk And Compliance

- Placeholder impact:
  - `ph.hotel_spine_geometry_v0` remains active; patrol decision props are blockout readability cues and are blocked from store/trailer use.
  - `ph.hotel_spine_audio_v0` remains active; added sound placements reuse placeholder generated ambience and are blocked from public demo/store/trailer use until approved or replaced.
- License impact: project-authored scripts/assets, deterministic generated audio already in project, Unreal Engine stock primitives, official editor scripting, and official Movie Render Queue only.
- Public repo risk: no intentionally committed local absolute paths, personal identifiers, secret tokens, platform SDKs, paid assets, marketplace downloads, or third-party media.
- Security/secret risk: no credential use, network service, account system, telemetry, or install step.
- Paid tool/asset risk: none introduced.
- Small-room risk: low; the work modifies `/Game/Hotel/Maps/L_HotelNightShift_Slice` and is proven through the production MRQ camera set and live-map automation.
- Veripsa Core concern: Core coordinates branch/PR traffic and does not replace implementation review, validation, or product judgment.

## Evidence

- Python syntax:
  - `python3 -m py_compile Automation/Unreal/create_hotel_spine_slice.py Automation/Unreal/create_hotel_mrq_evidence_assets.py Automation/Unreal/verify_hotel_spine_slice.py Automation/Tools/check_hotel_mrq_capture_pngs.py`
  - Result: success.
- Map generation:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -ExecutePythonScript=Automation/Unreal/create_hotel_spine_slice.py`
  - Result: success; map saved; map check reported 0 errors and 0 warnings.
- Map verification:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -ExecutePythonScript=Automation/Unreal/verify_hotel_spine_slice.py`
  - Result: verified 20 assets, 107 required actors, 74 tagged actors, 11 audio actors, 6 movable feedback meshes, and 50 non-interactive polish actors.
- MRQ asset generation:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -ExecutePythonScript=Automation/Unreal/create_hotel_mrq_evidence_assets.py`
  - Result: success; created `LS_HotelSpine_Stills` and `MRQ_HotelEvidencePng`; content validation completed with 0 validation errors.
- MRQ render:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -LevelSequence=/Game/Hotel/Cinematics/LS_HotelSpine_Stills.LS_HotelSpine_Stills -MoviePipelineConfig=/Game/Hotel/Cinematics/MRQ_HotelEvidencePng.MRQ_HotelEvidencePng`
  - Result: seven camera cuts rendered; Movie Pipeline completed in `+00:00:23.994`; executor finished in `+00:00:24.242`.
- MRQ PNG gate:
  - `python3 Automation/Tools/check_hotel_mrq_capture_pngs.py --capture-dir Saved/MovieRenders/HotelSpineSlice`
  - Result: passed 7 hotel MRQ evidence PNGs.
- Live map automation:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -ExecCmds="Automation RunTests Hotel.FrontDesk.PhoneResponse.LiveMap" -TestExit="Automation Test Queue Empty"`
  - Result: `Hotel.FrontDesk.PhoneResponse.LiveMap` success; 1 test performed.

## Evidence PNG Metrics

- `hotel_spine_evidence_0000.png`: average luma `36.0`, average RGB energy `94.6`, peak RGB energy `719`, visible pixels `541761/921600`.
- `hotel_spine_evidence_0001.png`: average luma `99.2`, average RGB energy `295.2`, peak RGB energy `724`, visible pixels `771165/921600`.
- `hotel_spine_evidence_0002.png`: average luma `28.2`, average RGB energy `69.1`, peak RGB energy `708`, visible pixels `404839/921600`.
- `hotel_spine_evidence_0003.png`: average luma `31.4`, average RGB energy `71.8`, peak RGB energy `750`, visible pixels `612631/921600`.
- `hotel_spine_evidence_0004.png`: average luma `38.5`, average RGB energy `100.7`, peak RGB energy `679`, visible pixels `701652/921600`.
- `hotel_spine_evidence_0005.png`: average luma `36.9`, average RGB energy `107.7`, peak RGB energy `762`, visible pixels `584179/921600`.
- `hotel_spine_evidence_0006.png`: average luma `42.4`, average RGB energy `105.7`, peak RGB energy `765`, visible pixels `536787/921600`.

## Completion Statement

This slice makes the existing hotel route feel less like a neutral corridor and more like a shift-worker patrol decision: the player can read elevator noise, stair cold air, floor traces, and a night-audit note before continuing toward Room 203, while the implemented gameplay loop remains unchanged and verified.
