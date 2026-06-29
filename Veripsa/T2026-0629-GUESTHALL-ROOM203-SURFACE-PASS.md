# T2026-0629-GUESTHALL-ROOM203-SURFACE-PASS

## Objective

Make the production guest hall and Room 203 evidence shot read less like plain blockout by adding public-repo-safe surface detail around the target door.

## Scope

- Add project-authored surface materials for:
  - peeled wallpaper paper
  - damp wall stain
  - dark floor scuff
  - ceiling water stain
  - lighter door paint chip
- Add deterministic generated mesh surfaces for:
  - peeling wallpaper patch
  - floor scuff cluster
  - ceiling water stain
- Place static, non-interactive surface cues in `L_HotelNightShift_Slice`.
- Replace the earlier oval damp patch with an authored irregular under-peel mesh so the Room 203 shot does not trade boxes for a crude ellipse.
- Add capture-only evidence fill lights where MRQ shots were too dark for the existing PNG gate.
- Update MRQ still sequence generation to use spawnable CineCamera bindings instead of map-camera possessable bindings, preventing game-camera fallback.
- Keep the existing Room 203 closed-door/refusal loop unchanged.
- Tag the `CAPTURE_GuestDoor_15SecondBeatCandidate` camera and door evidence light for `Hotel.Capture.Room203Surface`.
- Verify all surface pass actors, tags, non-interactive status, and authored mesh references.

## Non-Goals

- Do not add a room, route, gameplay verb, or new player-facing UI.
- Do not add DecalActors unless verifier support is expanded first.
- Do not import Fab, Marketplace, Quixel/Megascans, sample-project, paid, private, or unclear-license assets.
- Do not promote these surfaces to store/trailer-cleared final art.
- Do not change runtime C++ unless generation or verification exposes an actual product bug.

## Quality Bar

- The Room 203 MRQ shot must show more old-business-hotel wear without muddying the target door.
- The added surfaces must be visible enough at 1280x720 to matter.
- The MRQ evidence sequence must bind to the authored capture cameras and pass ten-shot exposure/uniqueness gates.
- No surface actor may carry `Hotel.Interact.*`.
- All new materials and meshes must be project-authored and ledgered.
- The pass must remain low cost and public-repo safe.

## Verification

- Python compile for updated automation scripts.
- Unreal generation of the production map, materials, and mesh assets.
- Unreal verifier success with surface actor tags and authored mesh reference checks.
- LiveMap test success for the existing hotel loop.
- MRQ render refresh and PNG gate.
- Public repo safety scan and LFS check.

## Completion Statement

Complete only when a Ready PR passes Veripsa, is merged to `main`, and no draft/open PR is left behind.
