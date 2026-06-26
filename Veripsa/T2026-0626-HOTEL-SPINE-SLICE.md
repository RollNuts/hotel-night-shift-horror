# T2026-0626-HOTEL-SPINE-SLICE

## Summary

- Task ID: T2026-0626-HOTEL-SPINE-SLICE
- Owner: Codex
- Status: Veripsa Core traffic Unknown
- Product goal: establish the first production-intent hotel spine for the front-desk-to-room-door loop.
- Hotel area: front desk, surveillance point, lobby edge, elevator/stair transition, guest hallway, target room door.
- Core action affected: answer phone, watch cameras, go to location, decide door/open/refuse, record/report.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/capture_hotel_spine_slice.py`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Materials/*.uasset`
  - `Content/Hotel/Audio/*_v0.uasset`
  - `SourceAssets/AudioGenerated/*_v0.wav`
  - `Config/DefaultEngine.ini`
  - `HotelNightShiftHorror.uproject`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
- Binary Unreal assets claimed:
  - `/Game/Hotel/Maps/L_HotelNightShift_Slice`
  - `/Game/Hotel/Materials/*_v0`
  - `/Game/Hotel/Audio/*_v0`
- Non-goals:
  - No enemies.
  - No online features.
  - No extra floors.
  - No final art claim.
  - No store/trailer use.
  - No test-room completion claim.

## Quality Axes

- Gameplay: creates spatial positions for the first work loop but does not implement interactions yet.
- Visual: establishes old business hotel composition with front desk, monitor, lobby threshold, elevator/stair doors, guest hallway, and Room 203.
- Camera: includes three capture candidate camera actors for first Steam screenshot, guest-door beat, and monitor/hall mismatch.
- Animation: none yet; future work must add phone/door/report feedback.
- VFX: subtle fog actor only; no abnormal VFX yet.
- SFX: generated placeholder phone ring and door knock assets placed as manual-trigger sound sources.
- Music/ambience: generated placeholder lobby hum and hallway drone placed as auto ambience sources.
- UI feedback: no UI yet; future work must add work-equipment flavored feedback.
- Level context: production hotel slice, not `TestHarness`.
- Performance: expected low geometry cost; requires Unreal runtime stat capture after map opens.
- Capture readiness: cameras exist and a reusable PNG capture script exists;
  screenshot/video capture still requires a successful Unreal rendering
  commandlet or interactive editor session.

## Risk And Compliance

- Placeholder impact: `ph.hotel_spine_geometry_v0` and `ph.hotel_spine_audio_v0` added.
- License impact: project-authored assets and Unreal stock primitive reference recorded.
- Public repo risk: no secrets, no local absolute paths in committed files, `Content/Developers/` ignored.
- Security/secret risk: no credentials or platform tokens introduced.
- Paid tool/asset risk: none.
- Small-room risk: low; map is under `/Game/Hotel/Maps` and covers real product areas.
- Veripsa Core GitHub App traffic result: `Unknown`; Core reported that new
  Unreal/script paths are not analyzed in main's graph yet. This is a
  coordination signal about unknown/unindexed paths, not a product-quality
  judgment.

## Evidence

- Screenshot/video/log path:
  - Generation log: Unreal commandlet run for `create_hotel_spine_slice.py` completed with 0 errors and deprecation warnings only.
  - Verification log: Unreal commandlet run for `verify_hotel_spine_slice.py` completed with 0 errors and deprecation warnings only.
  - Capture script: `capture_hotel_spine_slice.py` creates PNG evidence from
    the three in-map `CAPTURE_*` camera actors and performs a nonblack pixel
    sanity check.
  - Capture target: `Saved/Captures/HotelSpineSlice/` after a valid rendering
    pass. These captures are evidence artifacts, not source assets.
- Performance note: commandlet map load/import completed; runtime stat capture is still required after playable interaction work.
- Verification steps:
  - Ran Unreal Python generation script.
  - Verified `/Game/Hotel/Maps/L_HotelNightShift_Slice` exists.
  - Verified required hotel actors exist in the map.
  - Ran Python syntax validation for `capture_hotel_spine_slice.py`.
  - Attempted Unreal capture/verify commandlets after the capture script was
    added; current local UnrealEditor-Cmd startup is blocked before project
    script execution. Even `UnrealEditor-Cmd -help` reaches the same macOS
    service connection warning and then waits. This is an environment/tool
    startup blocker, not a capture-script result.
  - Confirmed the Unreal macOS Metal toolchain path works for Unreal commandlets.
  - Ran public repo safety scan before PR; no non-empty token, local path, or private key match was found in the intended committed files.
  - Confirmed Git LFS filter applies to `.umap`, `.uasset`, and `.wav` paths.
  - Marked PR #8 ready for review to trigger the Veripsa Core GitHub App.
  - Read the Veripsa Core PR comment/check; traffic result is `Unknown`.

## Completion Statement

The player-facing goal is to make the first night-shift loop physically legible: the phone and monitor sit at the front desk, the hotel transition has elevator/stair pressure, and the first guest-room door exists in a real hallway context.
