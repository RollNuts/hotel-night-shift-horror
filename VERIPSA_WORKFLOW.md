# VERIPSA WORKFLOW

Status: active workflow policy.

Veripsa Core is a GitHub App based development coordination tool. It is not a
runtime service and must not become part of the game.

Local files under `Veripsa/` are task records for humans and Codex. They are
not the Core coordination result. The authoritative Core signal is the GitHub
App check run or PR comment after the pull request is marked "ready for review"
in GitHub.

Core does not judge product quality, correctness, fun, art direction, or release
readiness. Core coordinates traffic: changed paths, reservations,
unknown/unindexed areas, possible collisions, and land-order risk.

## Codex Decision Frame

- Build: PR/task coordination that protects the hotel product, binary assets, placeholders, licenses, and evidence.
- Do not build: Veripsa-dependent gameplay or unnecessary process overhead.
- Market reason: coordinated AI work prevents visible quality debt from reaching the Steam page.
- Unreal reason: maps, Blueprints, materials, widgets, sounds, and VFX are collision-prone binary assets.
- Solo-dev/low-cost reason: Veripsa should reduce coordination burden and prevent rework.
- Art/audio bar: task records track missing visual, camera, SFX, ambience, UI,
  level, performance, and evidence; Core may only report coordination status for
  the files carrying that work.
- No-small-room bar: task records and PR descriptions must flag test-harness-only
  work and production-level omissions.
- Steam quality bar: release tasks require store evidence and rights status;
  Core only reports traffic state for the changed paths.
- Veripsa unit: one player-value or release-risk change with scope, non-goals, quality axes, and evidence.

## Required Task Fields

- Product goal.
- Core hotel action.
- Hotel area.
- Files/assets touched.
- Binary Unreal assets claimed.
- Non-goals.
- Gameplay/Visual/Camera/Animation/VFX/SFX/Ambience/UI/Level/Performance/Capture impact.
- Placeholder impact.
- License impact.
- Public repo risk.
- Paid/security/legal risk.
- Evidence path.

## Parallel Work And Subagents

Parallel PRs and subagent work are allowed when Veripsa Core can see the planned scope.

Rules:

- Open separate branches/PRs for independent work.
- Mark a PR ready for review when the Core coordination signal is needed; a
  draft PR may not trigger the GitHub App.
- After Core posts, read the PR check/comment before claiming reservations,
  unknowns, or collisions are understood.
- Claim binary Unreal assets before editing.
- Do not let two agents edit the same map, Blueprint, widget, material, Niagara system, sound cue, or Data Asset unless the Core coordination signal and human land order allow the sequence.
- Treat Veripsa Core coordination warnings as binding unless the user explicitly overrides them.
- Treat `Unknown` as unresolved traffic coordination. Add path evidence, split
  work, sequence branches, or ask the human to accept the coordination risk
  before merge.
- If Veripsa Core reports collisions, reservations, unknown/unindexed paths, or
  land-order risk, stop and resolve the coordination issue before continuing.
- Do not merge parallel PRs just because Git can merge text. Product quality, asset ownership, and evidence must be green.

## Required Labels

- `product-slice`
- `test-harness`
- `placeholder`
- `license-review`
- `asset-review`
- `store-evidence`
- `art-audio-required`
- `performance-risk`
- `small-room-risk`
- `public-repo-risk`
- `security-risk`

## Completion Language

Accepted:

- "The player now experiences..."
- "In the hotel level, this reads as..."
- "The action sounds like..."
- "The evidence is..."
- "Remaining placeholder/license risk is..."

Rejected:

- "Implemented."
- "Works in a test room."
- "Art later."
- "Sound later."
- "Placeholder for now."
