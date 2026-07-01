# Playable First-Person Proof Acceptance Target

## Summary

- Task ID: `T2026-0701-PLAYABLE-FIRST-PERSON-PROOF-ACCEPTANCE`
- Owner: Codex
- Status: Ready
- Product goal: Define the next proof target as a playable first-person player POV acceptance pass in the production map, not a teleport-only evidence set or isolated cinematic proof.
- Hotel area: Production front desk, monitor, patrol/listen transition, Room203 guest hall, return route, and report desk.
- Core action affected: `phone -> monitor -> patrol/listen -> Room203 -> return route -> report`

## Scope

- Files/assets touched:
  - `Veripsa/T2026-0701-PLAYABLE-FIRST-PERSON-PROOF-ACCEPTANCE.md`
- Binary Unreal assets claimed: None for this documentation-only task.
- Non-goals:
  - No code, automation, map, Blueprint, material, widget, audio, or generated media changes in this task.
  - No new room, mechanic, enemy, UI system, asset pack, package, or public trailer/store claim.
  - No acceptance based only on debug teleporting, Sequencer-only camera jumps, or disconnected stills.

## Quality Axes

- Gameplay: The future proof must be played from first-person input through the full chain: phone, monitor, patrol/listen, Room203, return route, and report.
- Visual: Each beat must be readable from normal first-person player POV in the production hotel context.
- Camera: Acceptance evidence must keep the player camera as the primary proof; cinematic or debug cameras can support diagnosis but cannot replace playable POV evidence.
- Animation: No final animation claim is required by this document, but any acceptance evidence should expose missing first-person hand/body feedback instead of hiding it with cuts.
- VFX: No VFX change in this task.
- SFX: The patrol/listen and return/report beats should be judged with normal in-game audio state when the future proof is captured.
- Music/ambience: Existing production-map ambience remains part of the acceptance context.
- UI feedback: Objectives, prompts, and report feedback should be visible only as the player would normally see them.
- Level context: The target map is `/Game/Hotel/Maps/L_HotelNightShift_Slice`; small-room or test-map proof does not satisfy this acceptance target.
- Performance: No runtime cost in this documentation-only task; future proof should note whether the playable route introduces hitches or stalls.
- Capture readiness: Generated screenshots, video, and logs must stay local and ignored, such as under `Saved/` or ignored private evidence folders.

## Risk And Compliance

- Placeholder impact: None in this task; the future proof may reveal placeholder gaps but must not promote them to store/trailer quality.
- License impact: No media or assets added; future generated proof media must remain local/ignored and must not include third-party downloads.
- Public repo risk: No generated PNG, MP4, log, local machine path, credential, or private capture is committed by this task.
- Security/secret risk: No network, account, telemetry, credential, or platform SDK handling.
- Paid tool/asset risk: None.
- Small-room risk: The acceptance target explicitly rejects small-room, teleport-only, or disconnected proof evidence.
- Veripsa Core role: Traffic coordination only for this documentation file; future implementation work must claim touched code, automation, and binary Unreal assets separately.

## Evidence

- Screenshot/video/log path:
  - This task generates none.
  - Future local/ignored target examples: `Saved/MovieRenders/PlayableFirstPersonProof/` and `Saved/Logs/playable_first_person_proof_*.log`
- Performance note: No runtime or editor performance impact from this documentation-only task.
- Verification steps:
  - Review this Veripsa task file for the playable first-person acceptance target.
  - Future proof must start in the production map and show first-person traversal through `phone -> monitor -> patrol/listen -> Room203 -> return route -> report`.
  - Future proof must make clear that progression is player-driven and not satisfied by teleport-only evidence.
  - Future generated media must remain local/ignored and be referenced only by path in task evidence.

## Completion Statement

The next proof unit now has a concrete acceptance bar: the player should be able to experience the first hotel loop in the production map from first-person player POV, following phone -> monitor -> patrol/listen -> Room203 -> return route -> report, with local ignored media proving normal play rather than teleport-only coverage.
