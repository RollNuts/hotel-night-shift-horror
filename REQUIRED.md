# REQUIRED

These rules are required for all work in this repository.

## Product Lock

- Genre: first-person, single-location, night-shift work horror.
- Setting: old business hotel.
- Core experience: front desk work, surveillance, room response, patrol, lock decisions, guest admission/refusal, hiding/closing/fleeing, and incident reporting.
- Structure: one complete night.
- Target playtime: 2-4 hours first clear, 5-8 hours with multiple endings.
- First platform: Steam.
- Sales model: offline-first buy-to-own.
- Future console expansion may be considered, but the first product must stay Steam-focused.

## Absolute Do Not Build

- Do not inherit Fourfold Echoes or Unity-era design.
- Do not build an open world.
- Do not build a live service.
- Do not require permanent servers.
- Do not add owned accounts.
- Do not make co-op or online play a product assumption.
- Do not add broad subsystems that do not deepen the hotel work/fear loop.
- Do not count test rooms as product progress.
- Do not count placeholder art, sound, lighting, UI, or level work as complete.

## Allowed Core Actions

Only these major actions are approved by default:

- Answer the phone.
- Watch security cameras.
- Check a request or incident.
- Go to the location.
- Decide whether to open a door.
- Decide whether to admit or refuse a guest.
- Patrol a floor.
- Hide, close, or flee.
- Record or report what happened.

New features must deepen one of these actions and improve both the work loop and fear loop.

## Feature Approval Filter

Before adding a feature, answer yes to all:

- Does it deepen an existing approved action?
- Can a player understand it immediately?
- Can it work without a large new UI explanation?
- Does it create a strong hotel screenshot or 15-second video beat?
- Does it support horror and hotel work at the same time?
- Is it feasible for one developer to test, tune, and maintain?
- Can it be proven in the production hotel level, not only a test map?

If any answer is no, cut or redesign the feature.

## Product Progress Definition

Progress counts only when it works in the hotel production context:

- Real hotel level or product-intent slice.
- First-person camera.
- Final-intent lighting.
- Final-intent audio/ambience or an approved silence reason.
- UI feedback that supports the work loop.
- Screenshot or video evidence.
- Performance note.
- Placeholder status.
- License status.

## Asset And Tool Safety

Allowed:

- Free official tools.
- Already installed safe tools.
- Free assets, music, SFX, and 3D models with clear commercial-use licenses.
- Original assets created for this project.
- AI-assisted drafts when recorded and reviewed.

Forbidden:

- Any paid service or paid asset purchase without explicit user approval.
- Any license-unclear asset.
- Any asset whose terms forbid commercial game use.
- Any raw paid/restricted asset committed to the public repo unless redistribution is explicitly allowed.
- Any secret, token, signing key, Steamworks credential, console SDK material, or private sales strategy in git.
- Any security workaround, credential exposure, or terms-of-service violation.

All assets must be tracked in `Ledgers/ASSET_LICENSE_LEDGER.md`.

## Completion Report Requirement

Do not report only "implemented" or "works."

Every completion report must include:

- What improved for the player.
- How it looks in the hotel level.
- How it sounds.
- What became scarier or clearer.
- Screenshot/video/log evidence.
- Performance impact.
- Remaining placeholders.
- License status.
- Next quality risk.

## Daily Question

Every change must make this more true:

> The first Steam screenshot and first trailer segment are stronger because of this work.

