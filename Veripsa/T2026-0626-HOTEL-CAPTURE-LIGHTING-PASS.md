# T2026-0626-HOTEL-CAPTURE-LIGHTING-PASS

## Summary

- Task ID: T2026-0626-HOTEL-CAPTURE-LIGHTING-PASS
- Owner: Codex
- Status: Implemented locally; PR traffic coordination pending; Steam-ready capture proof still failing
- Product goal: make the first hotel spine easier to read from real capture cameras without turning the game into a bright test room.
- Hotel area: front desk work surface, lobby threshold, elevator transition, guest hallway, Room 203 door.
- Core action affected: watch camera, answer phone, leave desk, approach guest room, judge door state, return/report.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/capture_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Materials/M_Hotel_*Glow_v0.uasset`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
- Binary Unreal assets claimed:
  - `/Game/Hotel/Maps/L_HotelNightShift_Slice`
  - `/Game/Hotel/Materials/M_Hotel_DeskLampGlow_v0`
  - `/Game/Hotel/Materials/M_Hotel_FluorescentPanelGlow_v0`
  - `/Game/Hotel/Materials/M_Hotel_MonitorGreenGlow_v0`
  - `/Game/Hotel/Materials/M_Hotel_ServiceAmberGlow_v0`
- Non-goals:
  - No new genre decision.
  - No enemies.
  - No online/server/account/live-service work.
  - No extra floor or test room.
  - No final art claim.
  - No store/trailer use claim.
  - No paid or third-party asset import.

## Quality Axes

- Gameplay: preserves the same first hotel work loop; no feature sprawl.
- Visual: adds practical glow materials, readable fluorescent panels, desk lamp cue, front-desk ceiling pressure, and Room 203 plate emphasis.
- Camera: moves the three capture candidate cameras into plausible in-level positions with narrower, product-facing framing.
- Animation: none; future interaction tasks still need phone, monitor, door, and report motion/feedback.
- VFX: keeps fog/post-process subtle; no abnormal VFX added.
- SFX: no new audio imported; existing placeholder audio assets are reused instead of churned.
- Music/ambience: no mix change in this task.
- UI feedback: none; unchanged first-loop HUD placeholder remains.
- Level context: work is in `/Game/Hotel/Maps/L_HotelNightShift_Slice`, not a small test room.
- Performance: added simple stock-primitive light meshes and a small number of local lights; runtime profiling still required.
- Capture readiness: capture script now tries multiple SceneCapture modes and warms the render target, but the current commandlet output is still too dark for Steam-quality evidence.

## Risk And Compliance

- Placeholder impact: `ph.hotel_spine_geometry_v0` remains active; this pass improves readability but does not finish final art.
- License impact: project-authored Unreal assets only; no downloaded asset, paid asset, music pack, model pack, or marketplace content introduced.
- Public repo risk: no secrets, private user paths, Epic account data, platform tokens, or paid SDK contents intended for commit.
- Security/secret risk: none introduced.
- Small-room risk: low; the work stays in the production hotel spine map.
- Veripsa Core GitHub App traffic result: Pending on PR readiness. Core is traffic coordination only; it is not gameplay, art, or code review.

## Evidence

- Checks run before PR:
  - Python syntax validation for `create_hotel_spine_slice.py`, `verify_hotel_spine_slice.py`, and `capture_hotel_spine_slice.py`.
  - `git diff --check`.
  - Public repo safety scan over non-binary intended paths.
  - Git LFS filter check for new `.uasset` files and the touched `.umap`.
  - Unreal generation commandlet completed with 0 errors and deprecation warnings only.
  - Unreal verification commandlet completed with 0 errors and deprecation warnings only.
- Capture result:
  - The capture commandlet exports diagnostic PNGs, but the quality gate still rejects them as too dark.
  - Current dark-frame metrics remain average luma `1.0/12.0`, average RGB energy `3.1/36.0`, peak RGB energy `39/60`, visible samples `2/5`.
  - A `render_in_main_renderer` attempt was rejected because it triggered a RenderGraph assertion, so that path is not kept.
  - Current captures are diagnostics only and must not be used for Steam, trailer, capsule, or public demo proof.
- Performance note:
  - Commandlet generation/verification succeeded. Runtime stat capture remains required after visual capture is fixed.

## Completion Statement

This pass moves the hotel slice toward product-readable horror lighting and capture framing, but it is not a finished evidence pass. The next implementation slice must make commandlet or editor capture produce non-dark hotel screenshots from the real map, then attach those captures as proof before any store-facing claim.
