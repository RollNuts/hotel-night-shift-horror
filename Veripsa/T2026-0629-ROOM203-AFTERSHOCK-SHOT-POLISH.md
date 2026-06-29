# Room 203 Aftershock Shot Polish

## Summary

- Task ID: `T2026-0629-ROOM203-AFTERSHOCK-SHOT-POLISH`
- Owner: Codex
- Status: ready-for-pr
- Product goal: make the Room 203 refusal aftershock read faster and stronger in the production GuestDoor evidence shot and short video capture
- Hotel area: production guest hallway, Room 203 door, and right-wall torn wallpaper composition in `L_HotelNightShift_Slice`
- Core action affected: refusing Room 203 after the patrol-listen requirement is satisfied

## Scope

- Tighten `CAPTURE_GuestDoor_15SecondBeatCandidate` so the door, chain, refusal notice, and torn wallpaper occupy more of the frame.
- Reduce oversized loose-paper silhouettes that read like a large flat board in evidence captures.
- Add a local torn-paper rim light and increase the existing aftershock skim light so the paper edge, backing, and hole shape separate at Steam thumbnail distance.
- Add a smaller dark interior-cut tear island and use the darker tear-shadow material for the main aftershock backing so the torn shapes do not read as one flat paper board.
- Strengthen the existing delayed wallpaper flutter and light pulse so the aftershock reads in a 15-second clip.
- Keep MRQ shot count unchanged and reuse the production hotel map evidence path.

## Non-Goals

- No new room, Room 203 interior, enemy, human animation, hand rig, new gameplay verb, or door-opening branch.
- No Fab, Marketplace, Quixel/Megascans, paid asset, external audio, private SDK, or unclear-license media.
- No new MRQ shot count, trailer system, UI system, or small test room.
- No store/trailer quality claim; this is still internal proof unless explicit art/audio review promotes it.

## Verification Required

- Python compile for Unreal automation scripts.
- Unreal `create_hotel_spine_slice.py`.
- Unreal `verify_hotel_spine_slice.py`.
- C++ editor build.
- `Hotel.FrontDesk.PhoneResponse.LiveMap`, including video-readable wallpaper travel threshold.
- MRQ evidence regeneration/render and PNG gate with focus on `hotel_spine_evidence_0005.png`.
- Public repo safety scan and LFS attr check before PR.
- Ready PR with Veripsa/Core traffic coordination passing before merge.

## Quality Notes

- This PR is not a code-cleanup PR.
- The intended improvement is visible composition: less dark unused frame, less rectangular paper-board read, stronger torn-paper silhouette, and clearer delayed aftershock.
- Remaining placeholder status is intentional and recorded in the placeholder ledger.

## Verification Performed

- `python3 -m py_compile Automation/Unreal/create_hotel_spine_slice.py Automation/Unreal/verify_hotel_spine_slice.py Automation/Unreal/create_hotel_mrq_evidence_assets.py Automation/Tools/check_hotel_mrq_capture_pngs.py`: passed.
- `UnrealEditor-Cmd ... create_hotel_spine_slice.py`: success, 0 errors, 3 existing deprecation warnings.
- `UnrealEditor-Cmd ... verify_hotel_spine_slice.py`: success, 0 errors, 2 existing deprecation warnings; verified 205 required actors, 176 tagged actors, 27 movable feedback meshes, and 19 authored mesh references.
- `Build.sh HotelNightShiftHorrorEditor Mac Development ...`: succeeded; target up to date.
- `UnrealEditor-Cmd ... -ExecCmds="Automation RunTests Hotel.FrontDesk.PhoneResponse.LiveMap" -TestExit="Automation Test Queue Empty"`: `Hotel.FrontDesk.PhoneResponse.LiveMap` passed, 1 test performed; MapCheck 0 errors/0 warnings. Known non-fatal warnings: CoreAudio sample-rate query and `r.MotionVectorSimulation`.
- `UnrealEditor-Cmd ... create_hotel_mrq_evidence_assets.py`: success, 0 errors, 5 existing deprecation/reference-gathering warnings.
- MRQ render of `LS_HotelSpine_Stills` with `MRQ_HotelEvidencePng`: completed 10/10 evidence PNGs.
- `python3 Automation/Tools/check_hotel_mrq_capture_pngs.py --capture-dir Saved/MovieRenders/HotelSpineSlice`: passed 10 hotel MRQ evidence PNGs.
- Visual QA: inspected `Saved/MovieRenders/HotelSpineSlice/hotel_spine_evidence_0005.png`; right-edge oversized flat-board read is reduced, torn-paper dark cuts separate at thumbnail scale, and the production GuestDoor shot now frames Room 203 and aftershock paper tighter without changing shot count.
