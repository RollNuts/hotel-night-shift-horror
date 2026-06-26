# GitHub Usage

This public repository is used for source control, PR review, issue tracking, asset/license review, placeholder tracking, and AI work coordination.

## Defaults

- Main branch should stay releasable enough to open in Unreal.
- Gameplay work should happen through branches and pull requests.
- PRs must use `.github/PULL_REQUEST_TEMPLATE.md`.
- Product tasks should use the Product task issue template.
- Asset imports should use the Asset review issue template before product use.
- Git LFS tracks Unreal binary assets and common media/model formats.

## No Automatic CI Yet

No GitHub Actions workflow is enabled at repo creation time. This avoids surprise compute usage or accidental paid-service integration.

Add CI later only when:

- The exact checks are known.
- They use free/safe official tooling.
- They do not expose secrets.
- They do not upload restricted assets.
- They are approved for expected GitHub usage.

## Branch And PR Rules

Recommended branch naming:

- `product/<hotel-area>-<core-action>`
- `asset/<asset-name>`
- `docs/<topic>`
- `tech/<system>`

Parallel subagent branches are allowed, but Veripsa Core is the coordination authority for collisions, binary asset ownership, placeholder debt, license review, and production-evidence gaps. Do not ignore Core recommendations. If Core flags a conflict, sequence the PRs or split the work.

Each PR should state:

- Which hotel work/fear loop improves.
- Which binary Unreal assets were touched.
- What evidence proves the change.
- Placeholder and license impact.
- Paid/security/legal risk.

## Public Repo Safety

Never commit:

- Steamworks credentials.
- API tokens.
- Signing keys.
- Console SDK material.
- Paid/restricted raw assets unless redistribution is explicitly allowed.
- Private sales strategy.
- Unclear-license assets.
