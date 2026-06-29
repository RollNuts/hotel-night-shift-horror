# Veripsa Task: T2026-0629-POST-REPORT-LOG-SELF-CORRECTION

## Summary

- Task ID: T2026-0629-POST-REPORT-LOG-SELF-CORRECTION
- Owner: Codex
- Status: Ready for PR
- Product goal: After the player files the night report and waits through the lobby-door anomaly, the filed log should contradict the world by adding a line the player did not write.
- Hotel area: Front desk report log in `L_HotelNightShift_Slice`.
- Core action affected: Existing report-log interaction after the report is filed.

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
  - `SourceAssets/AudioGenerated/SFX_PostReportLogSelfCorrection_v0.wav`
- Binary Unreal assets claimed:
  - `Content/Hotel/Audio/SFX_PostReportLogSelfCorrection_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
- Non-goals:
  - No new loop stage after `ReportFiled`.
  - No new interaction type, inventory, enemy, chase, save system, room, online feature, paid asset, or private SDK.
  - No claim that the current blockout geometry is store-facing final art.

## Quality Axes

- Gameplay: The self-correction is blocked until the monitor mismatch and desk-wait anomaly are resolved, then triggers once from the existing report-log action while keeping `ReportFiled` terminal.
- Visual: Three tagged movable log lines and an amber desk cue mark the impossible correction in the production front-desk context.
- Camera: MRQ evidence now includes `CAPTURE_PostReportLogSelfCorrectionCandidate`, raising the expected PNG count to 10.
- Animation: The new log lines slide and settle briefly as placeholder-diegetic motion; final hand/pen animation remains separate quality debt.
- VFX: A local amber point-light pulse supports the event without adding Niagara or GPU-heavy effects.
- SFX: `SFX_PostReportLogSelfCorrection_v0` is generated in-project and triggered once from the report-log moment.
- Music/ambience: Existing lobby ambience remains; no new music or licensed audio is introduced.
- UI feedback: Objective/status/message clarify that the player should not correct the added line and should wait for the next call.
- Level context: The beat occurs at the production front desk in the hotel spine map, not in a test room or small-room proxy.
- Performance: The runtime cost is a short one-shot animation/light pulse over already cached actors.
- Capture readiness: Local MRQ PNG evidence includes the 10th self-correction shot under `Saved/MovieRenders/HotelSpineSlice/`.

## Risk And Compliance

- Placeholder impact: Adds tracked placeholder log-line motion and generated SFX; not store-facing final art.
- License impact: Uses project-authored code/audio and Unreal stock primitives only; no third-party asset import.
- Public repo risk: No secrets, account paths, paid assets, private SDKs, or raw restricted third-party assets are introduced.
- Security/secret risk: Text and binary scans are required before PR.
- Paid tool/asset risk: None.
- Small-room risk: None; the feature is implemented and captured in `L_HotelNightShift_Slice`.

## Evidence

- Screenshot/video/log path:
  - `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0009.png` shows the self-correction capture locally and remains ignored.
- Performance note:
  - Uses existing tick path with a bounded one-shot animation and cached actor references.
- Verification steps:
  - Python compile of edited automation scripts.
  - Unreal editor target build.
  - `Hotel.FrontDesk.PhoneResponse.LiveMap` automation test.
  - Hotel spine verifier with MapCheck.
  - MRQ evidence render.
  - PNG evidence gate expecting 10 captures.

## Completion Statement

The filed night log now becomes unreliable after the player already followed procedure, turning the report itself into a fear beat while preserving the current loop endpoint and hotel-spine scope.
