# VERIPSA WORKFLOW

Status: active workflow policy.

Veripsa Core is a development coordination tool only. It is not a runtime service and must not become part of the game.

## Codex Decision Frame

- Build: PR/task coordination that protects the hotel product, binary assets, placeholders, licenses, and evidence.
- Do not build: Veripsa-dependent gameplay or unnecessary process overhead.
- Market reason: coordinated AI work prevents visible quality debt from reaching the Steam page.
- Unreal reason: maps, Blueprints, materials, widgets, sounds, and VFX are collision-prone binary assets.
- Solo-dev/low-cost reason: Veripsa should reduce review burden and prevent rework.
- Art/audio bar: Veripsa tracks missing visual, camera, SFX, ambience, UI, level, performance, and evidence as blockers.
- No-small-room bar: Veripsa flags test-harness-only work and production-level omissions.
- Steam quality bar: release tasks require store evidence and rights status.
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
- Claim binary Unreal assets before editing.
- Do not let two agents edit the same map, Blueprint, widget, material, Niagara system, sound cue, or Data Asset unless Veripsa Core explicitly clears the sequence.
- Treat Veripsa Core recommendations as binding unless the user explicitly overrides them.
- If Veripsa Core warns about collisions, placeholder debt, missing license review, missing production-level evidence, or small-room drift, stop and resolve the warning before continuing.
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
