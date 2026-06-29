# T2026-0629-ROOM203-AUTHORED-DOOR-MESH-PASS

## Objective

Replace the most cube-like visible Room 203 door elements in the production hotel spine with project-authored, reproducible mesh silhouettes.

## Scope

- Generate deterministic source OBJ meshes for:
  - paneled Room 203 door
  - linked door chain
  - torn paper notice
  - worn handle lever
- Import the generated meshes into `/Game/Hotel/Meshes`.
- Place the meshes in `L_HotelNightShift_Slice`.
- Keep the existing Room 203 refusal gameplay branch and closed-door beat.
- Tag the authored meshes for capture readability, Room 203 art density, and refusal motion.
- Verify the production map does not reference common raw Fab, Marketplace, Megascans, or sample-project asset roots.

## Non-Goals

- Do not add a new room.
- Do not add a new gameplay verb.
- Do not make the door open.
- Do not import Fab, Marketplace, Quixel/Megascans, sample-project, paid, private, or unclear-license assets.
- Do not promote these meshes to store/trailer-cleared final art.
- Do not change runtime C++ unless verification exposes a product bug.

## Quality Bar

- The Room 203 capture must read less like a flat rectangular block.
- The handle, chain, notice, and door paneling must support the existing refusal motion.
- All generated geometry must be reproducible from repo scripts and ledgered as project-authored.
- The verifier must fail if the product map uses unapproved external asset roots.

## Verification

- Python compile for updated automation scripts.
- Unreal generation of the production map and mesh assets.
- Unreal verifier success with authored mesh reference checks.
- MRQ evidence refresh and PNG gate.
- Public repo safety scan.
- LFS check for new `.uasset`/`.umap` files.

## Completion Statement

Complete only when a Ready PR passes Veripsa, is merged to `main`, and no draft/open PR is left behind.
