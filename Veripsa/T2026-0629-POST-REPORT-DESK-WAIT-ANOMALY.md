# T2026-0629 Post-Report Desk Wait Anomaly

## Summary

- Task ID: T2026-0629-POST-REPORT-DESK-WAIT-ANOMALY
- Owner: Codex
- Status: Ready for PR
- Product goal: After the Room 203 refusal report and delayed monitor mismatch, make the player hold at the front desk while the lobby answers once from outside.
- Hotel area: Front desk counter and lobby glass door.
- Core action affected: Deepens the existing report, monitor, and wait loop; no new core action is introduced.

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
  - `SourceAssets/AudioGenerated/SFX_PostReportDeskWaitRattle_v0.wav`
  - `Content/Hotel/Audio/SFX_PostReportDeskWaitRattle_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Binary Unreal assets claimed:
  - `Content/Hotel/Audio/SFX_PostReportDeskWaitRattle_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Non-goals:
  - No new stage after `ReportFiled`.
  - No hallway or lobby `Hotel.Interact.*` target for answering or opening the door.
  - No test map, small room, new room, or isolated prototype surface.
  - No enemy, chase, combat, inventory, save system, new UI framework, or new core action.
  - No paid assets, third-party media, store capsule art, trailer capture, online service, analytics, or private SDK dependency.

## Quality Axes

- Gameplay: After the post-report monitor mismatch settles, holding still behind the front desk triggers a one-shot lobby-door rattle; leaving the counter does not trigger it, and `ReportFiled` remains terminal.
- Visual: The production lobby/front-desk view now includes a floor wait marker, counter hold line, taped lobby glass, outside palm smear, no-guest reflection cue, and cold rattle light.
- Camera: MRQ evidence expands to nine shots, adding `CAPTURE_PostReportDeskWait_DoNotAnswerCandidate`.
- Animation: No final hand or door animation added; the slice uses a short light pulse and HUD response as placeholder feedback.
- VFX: No Niagara/VFX system added; the lobby-door cold point-light pulse is the temporary feedback channel.
- SFX: Adds project-authored deterministic `SFX_PostReportDeskWaitRattle_v0` as a one-shot lobby glass/handle rattle.
- Music/ambience: Existing lobby ambience remains; no music added.
- UI feedback: Existing HUD objective/status/message now tells the player to stay behind the counter, not open the lobby door, and confirms no guest appears in the monitor.
- Level context: Work stays in `L_HotelNightShift_Slice` and does not create a small-room test surface.
- Performance: Runtime work is limited to the existing pawn tick, a ReportFiled-only proximity/velocity check, one one-shot sound, and one 1.25-second point-light pulse.
- Capture readiness: MRQ render and PNG gate passed for all nine evidence images; still placeholder art/audio, not store/trailer-ready.

## Risk And Compliance

- Placeholder impact: Registered in `PLACEHOLDER_LEDGER.md` under geometry, audio, HUD, and runtime feedback placeholders.
- License impact: Registered in `ASSET_LICENSE_LEDGER.md` as project-authored, free, internal-only, no third-party media.
- Public repo risk: No secrets, tokens, personal files, private SDKs, downloaded paid assets, or committed evidence PNGs added.
- Security/secret risk: No networked runtime code, credentials, local-machine paths, or private identifiers committed.
- Paid tool/asset risk: Uses existing Unreal Engine installation and official editor/MRQ tooling only.
- Small-room risk: None; gameplay and capture remain in the production hotel spine map.

## Evidence

- Screenshot/video/log path:
  - Local ignored evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0000.png` through `hotel_spine_evidence_0008.png`
  - Post-report desk wait evidence: `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0008.png`
- Performance note:
  - MRQ render completed 9 shots in +00:00:28.826 at 1280x720.
- Verification steps:
  - Python compile: passed for hotel spine generation, verification, MRQ asset generation, and PNG gate scripts.
  - Map generation: passed; saved `L_HotelNightShift_Slice`.
  - Spine verifier: passed with 24 assets, 136 required actors, 102 tagged actors, 15 audio actors, 6 movable feedback meshes, 62 non-interactive polish actors, map check 0 errors and 0 warnings.
  - C++ build: `HotelNightShiftHorrorEditor Mac Development` succeeded.
  - Automation: `Hotel.FrontDesk.PhoneResponse.LiveMap` passed, including post-report desk wait negative gate away from the counter, hold-to-trigger path at the counter, `ReportFiled` preservation, feedback settle, and Room 203 door regression blocking.
  - MRQ assets: `LS_HotelSpine_Stills` and `MRQ_HotelEvidencePng` regenerated and validated.
  - MRQ render: passed with 9 camera cuts and `Movie Pipeline completed`.
  - MRQ PNG gate: passed 9 evidence PNGs.
  - Manual visual check: `hotel_spine_evidence_0008.png` frames the front desk and lobby glass hold-closed cue with readable cold light and no blank frame.

## Completion Statement

After the report and the delayed monitor contradiction, the player now has to stay behind the counter while the lobby glass rattles once from outside; the game reinforces that the correct action is not to answer, not to open, and to distrust the empty monitor.
