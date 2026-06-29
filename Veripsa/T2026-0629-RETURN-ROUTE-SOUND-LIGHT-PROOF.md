# Return Route Sound Light Proof

## Summary

- Task ID: `T2026-0629-RETURN-ROUTE-SOUND-LIGHT-PROOF`
- Owner: Codex
- Status: In PR
- Product goal: Make the existing ReturnRoute back-knock beat readable as a short in-game horror moment, not only a still image.
- Hotel area: Guest hall return route after Room 203 refusal
- Core action affected: Return through the hall, listen, then report

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`
  - `SourceAssets/AudioGenerated/SFX_ReturnRoutePursuitTail_v0.wav`
  - `Content/Hotel/Audio/SFX_ReturnRoutePursuitTail_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Audio/SFX_ReturnRoutePursuitTail_v0.uasset`
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
- Non-goals:
  - No new room
  - No new player verb
  - No online/account/service dependency
  - No imported third-party asset
  - No final-store audio claim

## Quality Axes

- Gameplay: Deepens the existing return/report gate; the player still only returns, listens, and reports.
- Visual: Adds a cold pursuit-tail light cue in the real guest hall so the beat reads beyond a single static mark.
- Camera: Uses the existing ReturnRoute evidence camera and production map.
- Animation: Keeps lightweight prop motion on cached tagged actors; no humanoid animation claim.
- VFX: Uses project-authored light pulse and glow material only; no Niagara dependency added.
- SFX: Adds a generated one-shot pursuit tail after the initial back-knock so the sound appears to travel behind and ahead.
- Music/ambience: Leaves the broader hallway ambience unchanged.
- UI feedback: Updates existing objective/status text during the tail; no new UI system.
- Level context: All work is in `L_HotelNightShift_Slice`, not a test room.
- Performance: Reuses cached actors and light components; no per-frame world scans.
- Capture readiness: LiveMap proves main light, tail light, and multiple visible props react in the production map.

## Risk And Compliance

- Placeholder impact: Updates existing ReturnRoute runtime/audio placeholders; store/trailer use remains `No`.
- License impact: Generated in-repo WAV and Unreal assets are project-authored; no external media.
- Public repo risk: No auth material, local private files, platform SDKs, paid assets, or account data intended.
- Security/auth risk: No networked code, auth material, telemetry, or install step.
- Paid tool/asset risk: None.
- Small-room risk: None; production hotel map only.

## Evidence

- Screenshot/video/log path:
  - `Saved/Logs/return_route_sound_light_create_r1.log`
  - `Saved/Logs/return_route_sound_light_verify_r1.log`
  - `Saved/Logs/return_route_sound_light_livemap_r2.log`
  - `Saved/Logs/return_route_sound_light_mrq_render_r1.log`
  - MRQ evidence path remains `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0006.png`
- Performance note: Adds one cached audio actor, one cached light actor, and constant-time light/actor updates during the existing anomaly.
- Verification steps:
  - Python compile
  - Unreal map generation
  - Production-map verifier
  - Unreal editor build
  - `Hotel.FrontDesk.PhoneResponse.LiveMap`
  - MRQ PNG gate
  - Public repo safety scan

## Completion Statement

The ReturnRoute beat should now play less like a one-frame marker and more like a short horror response: the first knock hits, the light follows cold through the hall, the paper/marks answer from ahead, and the player understands to keep moving until the hallway quiets before filing the report.
