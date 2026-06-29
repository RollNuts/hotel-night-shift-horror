# Room 203 Refusal Motion Pass

## Summary

- Task ID: `T2026-0629-ROOM203-REFUSAL-MOTION-PASS`
- Owner: Codex
- Status: ready-for-pr
- Product goal: make the Room 203 refusal beat feel like something presses against the door without allowing the door to open
- Hotel area: production guest hallway and Room 203 door in `L_HotelNightShift_Slice`
- Core action affected: refusing the Room 203 request after the patrol-listen requirement is satisfied

## Scope

- Files/assets touched: production-map Room 203 cue props, runtime refusal motion, verifier, LiveMap automation, placeholder/license ledgers
- Binary Unreal assets claimed: `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`; refreshed MRQ evidence assets if regenerated
- Non-goals: no new room, no new gameplay verb, no open-door mechanic, no new SFX, no third-party animation, no Fab/Marketplace asset, no paid asset, no final store art claim, no MRQ shot-count change

## Quality Axes

- Gameplay: preserves the existing refuse-and-keep-closed loop and state progression
- Animation: refusal now has latch-first motion, chain-delayed motion, door-edge/notice surface response, and a settle back to rest
- Visual: uses production Room 203 framing and existing door readability props
- SFX: reuses existing Room 203 knock; no new audio asset
- Camera: existing guest-door MRQ evidence camera remains the still-proof path
- Level context: all work is in the production hotel level, not a small-room map
- Compliance: no downloaded media, no paid tools, no private SDKs, no secret-bearing output

## Verification Required

- Python compile for Unreal automation scripts
- Unreal `create_hotel_spine_slice.py`
- Unreal `verify_hotel_spine_slice.py`
- C++ editor build
- `Hotel.FrontDesk.PhoneResponse.LiveMap`
- MRQ evidence asset regeneration, MRQ render, PNG gate
- public repo safety scan, LFS attr check, text/binary secret/path scans
- Ready PR with Veripsa passing before merge

## Completion Statement

The Room 203 refusal beat should now read as a held-closed door under pressure: the latch jumps first, the chain catches a moment later, the dark door edge and notice corner react, and everything returns to rest. This remains internal baseline animation, not final door/hand/lock art.
