# T2026-0626-FIRST-LOOP-RUNTIME

## Summary

- Task ID: T2026-0626-FIRST-LOOP-RUNTIME
- Owner: Codex
- Status: Implemented, needs in-editor capture proof
- Product goal: make the first hotel work loop playable in the production hotel map instead of remaining a static map.
- Hotel area: front desk, surveillance monitor, Room 203 door, report log, guest hallway lighting.
- Core action affected: answer phone, watch cameras, go to location, refuse/keep door closed, record/report.

## Scope

- Files/assets touched:
  - `Source/HotelNightShiftHorror.Target.cs`
  - `Source/HotelNightShiftHorrorEditor.Target.cs`
  - `Source/HotelNightShiftHorror/HotelNightShiftHorror.Build.cs`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftGameMode.h`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftHUD.h`
  - `Source/HotelNightShiftHorror/Public/HotelNightShiftPawn.h`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftHorror.cpp`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftGameMode.cpp`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftHUD.cpp`
  - `Source/HotelNightShiftHorror/Private/HotelNightShiftPawn.cpp`
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Config/DefaultEngine.ini`
  - `Config/DefaultInput.ini`
  - `HotelNightShiftHorror.uproject`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
- Binary Unreal assets claimed:
  - None in this task.
- Non-goals:
  - No enemies.
  - No inventory.
  - No extra hotel areas.
  - No final UI, final audio, or final animation claim.
  - No online, account, server, or Fourfold/Unity carryover.

## Quality Axes

- Gameplay: the player can move in first person, answer the phone, check the monitor, refuse Room 203, and record the incident.
- Visual: the loop uses the existing front desk, monitor, Room 203 door, report log, and hallway light in the production hotel map.
- Camera: interaction prompts are driven by the first-person camera line trace.
- Animation: final hand/door/receiver animation is not implemented; current feedback is state/UI/audio/light based.
- VFX: no new VFX; hallway light intensity changes create a minimal abnormal cue.
- SFX: phone ring and door knock reuse the existing placeholder hotel audio actors.
- Music/ambience: existing lobby and guest-hall ambience remain unchanged.
- UI feedback: a minimal night-log HUD shows objective, work message, fear pressure, and current interaction.
- Level context: no test room; interactions are anchored to production hotel
  positions and the generation script now adds future-facing hotel Actor tags.
- Performance: no broad subsystem; one pawn tick line trace and small HUD draw only.
- Capture readiness: Editor and Game C++ targets build; screenshot/video still
  blocked by current local UnrealEditor-Cmd startup.

## Risk And Compliance

- Placeholder impact: adds `ph.first_loop_runtime_ui_v0` and `ph.first_loop_runtime_feedback_v0`.
- License impact: adds `asset.first_loop_runtime_code_v0`; no third-party or downloaded assets.
- Public repo risk: no secrets, credentials, tokens, local absolute paths, or paid assets introduced.
- Security/secret risk: none.
- Paid tool/asset risk: none.
- Small-room risk: low; code binds to production hotel anchors/tags, not a test harness.
- Veripsa Core note: this adds new source/config paths. Core traffic may remain
  `Unknown` until the app can index this Unreal project surface; that is a
  coordination signal, not a product review.

## Evidence

- Screenshot/video/log path:
  - Build log: `Build.sh HotelNightShiftHorrorEditor Mac Development ... -NoUBA` succeeded.
  - Game build log: `Build.sh HotelNightShiftHorror Mac Development ... -NoUBA`
    succeeded when run outside the filesystem sandbox. The sandboxed attempt
    compiled and linked, then failed during Xcode `.app` finalization.
  - Runtime capture: not yet available.
- Performance note:
  - Expected runtime cost is low: one first-person pawn, one line trace per tick, timer-based phone ring replay, and HUD text draw.
- Verification steps:
  - Built `HotelNightShiftHorrorEditor` successfully with UnrealBuildTool.
  - Built `HotelNightShiftHorror` Game target successfully with UnrealBuildTool.
  - Removed Editor-only `GetActorLabel()` runtime dependency after Game target
    compilation exposed it as invalid for product builds.
  - Added Actor tags to the hotel generation script for future regenerated maps;
    current runtime remains compatible with the existing map by using production
    hotel position anchors.
  - Re-tried Unreal commandlet verification with `-NullRHI`; current local `UnrealEditor-Cmd` startup still blocks before script execution.
  - Updated placeholder and asset license ledgers for runtime UI/feedback/code.

## Completion Statement

The first hotel map is no longer only a static layout: the player has a front-desk work loop that begins with a ringing phone, turns the monitor into a decision tool, makes Room 203 a refusal beat, and brings the player back to the report log.
