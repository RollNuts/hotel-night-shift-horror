# Phone Pickup Motion Quality Pass

## Summary

- Task ID: `T2026-0629-PHONE-PICKUP-MOTION-QUALITY`
- Owner: Codex
- Status: ready-for-pr
- Product goal: make the first front-desk horror beat read as a handled object, not a sliding block
- Hotel area: production front desk in `L_HotelNightShift_Slice`
- Core action affected: answering the ringing front-desk phone

## Scope

- Files/assets touched: phone receiver runtime motion, authored cord tug tag/mobility, production-map regeneration, verifier, LiveMap automation, placeholder ledger
- Binary Unreal assets claimed: `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
- Non-goals: no new room, no new gameplay verb, no hand rig, no Sequencer pass, no third-party animation, no Fab/Marketplace asset, no paid asset, no final store art claim, no MRQ shot-count change

## Quality Axes

- Gameplay: preserves the existing phone/monitor/report loop
- Animation: receiver pickup now has contact anticipation, active lift, overshoot/settle, and a visible cord tug
- Visual: uses the existing project-authored receiver and coiled cord in the production front-desk shot
- SFX: no new audio asset; existing pickup click, ring cutoff, and phone-line static remain unchanged
- Camera: existing phone-response MRQ camera remains the proof path
- Level context: all work is in the production hotel level, not a small-room map
- Compliance: no downloaded media, no paid tools, no private SDKs, no secret-bearing output

## Verification Required

- Python compile for Unreal automation scripts
- Unreal `create_hotel_spine_slice.py`
- Unreal `verify_hotel_spine_slice.py`
- C++ editor build
- `Hotel.FrontDesk.PhoneResponse.LiveMap`
- MRQ evidence asset regeneration, MRQ render, PNG gate
- public repo safety scan, LFS attr check, text/OBJ/binary secret/path scans
- Ready PR with Veripsa passing before merge

## Completion Statement

The phone answer beat should now read as contact, lift, and settle: the receiver first compresses against the cradle, lifts with readable rotation, settles into the held pose, and tugs the authored coiled cord. This still does not clear final first-person hand animation or store/trailer art quality.
