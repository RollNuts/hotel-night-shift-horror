# First Loop Proof Video

## Summary

- Task ID: `T2026-0630-FIRST-LOOP-PROOF-VIDEO`
- Owner: Codex
- Status: Complete
- Product goal: Make the first-loop proof reviewable as a continuous 24-second video, not only as PNG frames and test logs.
- Hotel area: Production front desk, monitor, route, Room 203, return route, report desk.
- Core action affected: Phone -> monitor -> patrol/listen -> Room 203 refusal -> return route -> report -> post-report anomaly.

## Scope

- Files/assets touched:
  - `Automation/Tools/check_first_loop_playthrough_proof_pngs.py`
  - `Tools/README.md`
  - `Veripsa/T2026-0630-FIRST-LOOP-PROOF-VIDEO.md`
- Binary Unreal assets claimed: None.
- Non-goals:
  - No new room, mechanic, UI, enemy, animation system, asset pack, or store/trailer approval.
  - No committed video, PNG, log, local engine path, or personal filesystem path.

## Quality Axes

- Gameplay: Does not alter runtime behavior; it provides a stronger review artifact for the existing production-map first-loop proof.
- Visual: Requires the existing MRQ PNG set and keeps the whole loop readable over time.
- Camera: Preserves the existing `LS_FirstLoop_PlaythroughProof_24s` timing by treating sampled MRQ PNGs as 2 fps source frames.
- Animation: Does not add animation; makes existing sequence-only motion cues easier to inspect.
- VFX: No new VFX.
- SFX: No audio track is added; this is a silent visual proof video.
- Music/ambience: No change.
- UI feedback: No change.
- Level context: Uses only the existing first-loop production-map capture output.
- Performance: Local tool only; no runtime cost.
- Capture readiness: Extends the existing first-loop PNG gate with optional `ffmpeg` encode and `ffprobe` verification for resolution, duration, and output frame count.

## Risk And Compliance

- Placeholder impact: None; generated MP4 remains ignored under `Saved/`.
- License impact: Uses locally installed free ffmpeg/ffprobe tools and project-authored PNG output.
- Public repo risk: Script contains no personal paths, credentials, private SDK hooks, or downloaded media.
- Security/secret risk: No network access, credentials, telemetry, or account integration.
- Paid tool/asset risk: None.
- Small-room risk: None; source frames come from the production hotel map proof.

## Evidence

- Screenshot/video/log path:
  - Local, uncommitted: `Saved/MovieRenders/FirstLoopPlaythrough/first_loop_playthrough_proof.mp4`
- Performance note: Local encode/review artifact only.
- Verification steps:
  - `python3 -m py_compile Automation/Tools/check_first_loop_playthrough_proof_pngs.py`
  - `python3 Automation/Tools/check_first_loop_playthrough_proof_pngs.py --encode-video`
  - `./Tools/smoke_project_files.sh`
  - `./Tools/check_public_repo_safety.sh`
  - `git diff --check`

## Completion Statement

The first-loop proof can now be reviewed as a continuous local MP4 generated from the existing MRQ frames. This closes the gap between "the test passed" and "the director can actually watch the loop," while keeping all generated media out of the public repository.
