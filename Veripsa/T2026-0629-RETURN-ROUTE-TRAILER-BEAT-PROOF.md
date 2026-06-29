# Return Route Trailer Beat Proof

## Summary

- Task ID: `T2026-0629-RETURN-ROUTE-TRAILER-BEAT-PROOF`
- Owner: Codex
- Status: In PR
- Product goal: Prove the existing ReturnRoute beat can read as a 15-second internal trailer-style horror moment, not only a static MRQ still.
- Hotel area: Production guest hall return route after Room 203 refusal
- Core action affected: Return through the hall, listen, understand the back-knock response, then continue to report

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_return_route_trailer_beat_assets.py`
  - `Automation/Tools/check_return_route_trailer_proof_pngs.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
  - `Veripsa/T2026-0629-RETURN-ROUTE-TRAILER-BEAT-PROOF.md`
- Binary Unreal assets claimed:
  - `Content/Hotel/Cinematics/LS_ReturnRoute_TrailerBeat_15s.uasset`
  - `Content/Hotel/Cinematics/MRQ_ReturnRouteTrailerProofPng.uasset`
- Non-goals:
  - No new room
  - No new gameplay verb
  - No new runtime system
  - No modification to the stable ten-shot hotel evidence MRQ lane
  - No third-party media, Fab, Marketplace, Megascans, paid asset, online service, private SDK, account system, or public trailer approval claim

## Quality Axes

- Gameplay: Deepens the existing return/report fear loop without adding mechanics.
- Visual: Reuses the production ReturnRoute floor/wall/slip evidence, de-emphasizes competing Room 203 paper clutter only inside this sequence, and animates the ReturnRoute wall/floor/slip evidence through Sequencer for motion readability.
- Camera: Adds a dedicated moving CineCamera sequence that begins down the guest hall and ends on the existing ReturnRoute evidence composition.
- Animation: Uses Sequencer transform tracks on existing ReturnRoute evidence actors; no humanoid animation claim.
- VFX: Uses existing project-authored glow/light cues only; no new Niagara dependency.
- SFX: No new sound asset in this slice; audio quality remains covered by the existing ReturnRoute sound/light placeholder.
- Music/ambience: No music or ambience change.
- UI feedback: No UI change.
- Level context: All proof is generated against `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Performance: MRQ proof renders stepped PNGs from a 15-second sequence; no runtime per-frame cost added.
- Capture readiness: A dedicated PNG gate rejects blank, static, too-dark, short, or misbound ReturnRoute trailer-proof output.

## Risk And Compliance

- Placeholder impact: Adds `ph.return_route_trailer_proof_v0`; store/trailer use remains `No`.
- License impact: Project-authored scripts and generated Unreal assets only; official Epic Sequencer/MRQ/editor tooling.
- Public repo risk: No auth material, local private files, platform SDKs, paid assets, or account data intended.
- Security/auth risk: No networked code, telemetry, install step, or credential handling.
- Paid tool/asset risk: None.
- Small-room risk: None; proof targets the production hotel map and existing ReturnRoute actors.
- Veripsa Core role: traffic coordination and path/scope/index checks only; not code/art/product review.

## Evidence

- Screenshot/video/log path:
  - `Saved/Logs/return_route_trailer_assets_r3.log`
  - `Saved/Logs/return_route_trailer_verify_r1.log`
  - `Saved/Logs/return_route_trailer_mrq_render_r3.log`
  - `Saved/MovieRenders/ReturnRouteTrailerBeat/return_route_trailer_proof_*.png`
- Verification steps:
  - Python compile
  - Unreal trailer-proof asset generation
  - Production-map verifier
  - MRQ render of `LS_ReturnRoute_TrailerBeat_15s` with `MRQ_ReturnRouteTrailerProofPng`
  - ReturnRoute trailer-proof PNG gate
  - Existing hotel MRQ PNG gate check against the stable ten-shot evidence output
  - Public repo safety scan

## Completion Statement

The ReturnRoute beat should be inspectable as a short internal capture: the camera advances through the real guest hall, the back-knock pressure answers from the wall/floor/slip evidence, and the final frame lands on the existing ReturnRoute proof subject. This does not clear the footage for public marketing; it makes the next art/audio pass harder to fake with static or box-like placeholders.
