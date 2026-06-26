# T2026-0627-HOTEL-MRQ-CAPTURE-EVIDENCE

## Summary

- Task ID: T2026-0627-HOTEL-MRQ-CAPTURE-EVIDENCE
- Owner: Codex
- Status: Implemented locally; PR traffic coordination pending
- Product goal: make the production hotel spine produce usable still-image evidence from real in-map cameras instead of dark diagnostic captures.
- Hotel area: front desk work hub, Room 203 guest hallway, monitor-to-hall mismatch view.
- Core action affected: answer phone, check monitor, leave desk, approach Room 203, decide whether to open or refuse, return/report.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/create_hotel_mrq_evidence_assets.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Automation/Tools/check_hotel_mrq_capture_pngs.py`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
  - `HotelNightShiftHorror.uproject`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
- Binary Unreal assets claimed:
  - `/Game/Hotel/Maps/L_HotelNightShift_Slice`
  - `/Game/Hotel/Cinematics/LS_HotelSpine_Stills`
  - `/Game/Hotel/Cinematics/MRQ_HotelEvidencePng`
- Non-goals:
  - No new genre decision.
  - No enemies.
  - No online/server/account/live-service work.
  - No extra floor, sandbox test room, or small-room detour.
  - No final art claim.
  - No store/trailer use claim.
  - No paid or third-party asset import.

## Quality Axes

- Gameplay: keeps the same first hotel work loop and makes its evidence shots repeatable.
- Visual: adds capture-readability lights and Room 203 door-frame geometry so the hallway shot reads as a door decision point.
- Camera: fixes Python rotator ordering for all generated actors and creates a three-shot MRQ still sequence from the production map.
- Animation: none; interaction motion still belongs to a later product slice.
- VFX: none beyond existing fog/post-process; no abnormal effect added.
- SFX: no new sound assets imported; existing placeholder phone, ambience, and knock remain in the level.
- Music/ambience: unchanged.
- UI feedback: unchanged.
- Level context: all evidence cameras and actors live in `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Performance: MRQ renders three 1280x720 frames in about 10 seconds after map load on the local Mac editor; runtime gameplay profiling still required.
- Capture readiness: official Movie Render Queue output now passes the project gate for non-dark, unique PNG evidence.

## Risk And Compliance

- Placeholder impact: `ph.hotel_spine_geometry_v0` remains active; the geometry is readable proof, not final hotel art.
- License impact: project-authored scripts and Unreal assets only; the MRQ plugin is an official Epic Unreal Engine plugin enabled in the project.
- Public repo risk: no secrets, private local paths, Epic account data, platform tokens, paid SDK contents, or third-party media intended for commit.
- Security/secret risk: none introduced.
- Small-room risk: low; this is a production hotel-map evidence path.
- Veripsa Core GitHub App traffic result: Pending on PR readiness. Core is traffic coordination only; it is not gameplay, art, code, or product review.

## Evidence

- Previous failure addressed:
  - `Automation/Unreal/capture_hotel_spine_slice.py` produced three dark, duplicate-looking diagnostic PNGs and failed the brightness gate.
  - Unreal high-res screenshot commandlet path hung/crashed and is not used as the evidence path.
- New evidence path:
  - `Automation/Unreal/create_hotel_mrq_evidence_assets.py` creates `/Game/Hotel/Cinematics/LS_HotelSpine_Stills` and `/Game/Hotel/Cinematics/MRQ_HotelEvidencePng`.
  - `Automation/Tools/check_hotel_mrq_capture_pngs.py` gates the MRQ output with a stdlib PNG parser, resolution check, luma/RGB thresholds, visible-pixel count, and uniqueness check.
  - Final ignored render outputs:
    - `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0000.png`
    - `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0001.png`
    - `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0002.png`
- Final capture metrics:
  - `hotel_spine_evidence_0000.png`: average luma `37.1`, average RGB energy `96.1`, peak RGB energy `711`, visible pixels `587618/921600`, SHA-256 `7cb13094670d38d139b047b546eabe8d18aa7726b0e6482c19a4b1f65148f263`.
  - `hotel_spine_evidence_0001.png`: average luma `37.0`, average RGB energy `108.0`, peak RGB energy `762`, visible pixels `586425/921600`, SHA-256 `a72be107c5c9b69d5a0bcb599880ca0e504cae406484c40dbb4bcb48f99d7ad4`.
  - `hotel_spine_evidence_0002.png`: average luma `41.4`, average RGB energy `104.2`, peak RGB energy `765`, visible pixels `528671/921600`, SHA-256 `72c7016cc48e5d66a11b665e20d1e7cfa7071faefccb207603d00806947a7c7a`.
- Checks run before PR:
  - Python syntax validation for the updated automation scripts.
  - Unreal map generation commandlet completed with 0 errors and deprecation warnings only.
  - Unreal MRQ asset generation commandlet completed with 0 errors and deprecation warnings only.
  - Official MRQ render completed with three camera cuts and `Movie Pipeline completed`.
  - MRQ PNG gate passed for three unique 1280x720 PNGs.

## Completion Statement

This task does not finish hotel art. It removes the main production blocker for visual evidence: Codex can now prove hotel-map work with repeatable Movie Render Queue shots, and future product slices can be judged against real front-desk, Room 203, and monitor-to-hall images instead of text-only claims.
