# Veripsa Task: T2026-0629-FRONT-DESK-ART-DENSITY-PASS

## Summary

- Task ID: T2026-0629-FRONT-DESK-ART-DENSITY-PASS
- Owner: Codex
- Status: Ready for PR
- Product goal: Reduce the front-desk blockout look and make the post-report lobby-door beat read through physical prop motion, not only light/audio.
- Hotel area: Front desk, report log, phone, back shelf, and lobby glass door in `L_HotelNightShift_Slice`.
- Core action affected: Existing phone/report/post-report desk-wait flow.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`
  - `LICENSE_AND_ASSET_POLICY.md`
  - `ART_AUDIO_QUALITY_BAR.md`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Materials/M_Hotel_TarnishedBrass_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_DullDeskMetal_v0.uasset`
  - `Content/Hotel/Materials/M_Hotel_AgedLedgerRed_v0.uasset`
- Non-goals:
  - No Fab, Marketplace, Quixel, paid, AI, or unverified third-party raw assets.
  - No new gameplay stage, room, enemy, inventory, save flow, UI framework, online feature, or private SDK.
  - No claim that the resulting blockout is store/trailer final art.

## Quality Axes

- Gameplay: Keeps the existing loop and interaction gates unchanged.
- Visual: Adds curved phone dial/cups/cord loops, service bell, lamp silhouette, binder rings, ink smear, key hooks/tag, and lobby-door rattle hardware.
- Camera: Existing 10 MRQ evidence cameras remain the capture set; front-desk and lobby-door shots should show increased prop density.
- Animation: Adds bounded transform rattle for lobby-door handle/latch/tape during the desk-wait anomaly and automation proof that it moves and settles.
- VFX: No new Niagara; existing light cue remains secondary to physical prop motion.
- SFX: Reuses existing generated lobby-door rattle SFX.
- Music/ambience: No change.
- UI feedback: No change.
- Level context: Production hotel spine map only; no small-room or isolated test map.
- Performance: Tiny cached actor arrays, one-shot transform animation during the existing anomaly.
- Capture readiness: Verifier and LiveMap test enforce new actors/tags/mobility/movement before PR merge.

## Risk And Compliance

- Placeholder impact: Raises blockout quality but remains placeholder and blocked from store/trailer use.
- License impact: Project-authored materials/code and Unreal Engine stock primitive references only; external free asset policy documented for future intake.
- Public repo risk: No secrets, local paths, paid assets, or restricted raw assets.
- Security/secret risk: Text and binary scans required before PR.
- Paid tool/asset risk: None.
- Small-room risk: None.

## Evidence

- Screenshot/video/log path:
  - Local MRQ output under `Saved/MovieRenders/HotelSpineSlice/` remains ignored.
- Performance note:
  - No persistent heavy effect; one-shot transform update over three lobby-door actors.
- Verification steps:
  - Python compile of edited automation scripts.
  - Regenerate hotel spine map.
  - Hotel spine verifier with MapCheck.
  - Unreal editor target build.
  - `Hotel.FrontDesk.PhoneResponse.LiveMap` automation test.
  - MRQ evidence render and PNG gate.
  - Public repo safety scans.

## Completion Statement

The front desk now reads less like a cube grid, and the lobby-door anomaly has visible object motion that supports horror readability while keeping all assets public-repo-safe.
