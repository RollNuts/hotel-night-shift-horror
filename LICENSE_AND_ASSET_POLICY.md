# LICENSE AND ASSET POLICY

Status: active legal and repo hygiene policy.

This project may become public. It may also use commercial or restricted assets. Those facts must never collide.

## Codex Decision Frame

- Build: a rights-clean asset pipeline that can support public code and private commercial assets.
- Do not build: unlicensed asset mixes, secret leakage, unclear AI assets, or paid assets committed unsafely.
- Market reason: launch, press, store, and platform trust can fail if rights are unclear.
- Unreal reason: Unreal projects often include binary assets and Marketplace/Fab content that need strict ledgering.
- Solo-dev/low-cost reason: rights records prevent expensive cleanup and rework near release.
- Art/audio bar: asset quality includes style fit and license clarity, not only appearance or sound.
- No-small-room bar: test assets still need status if they might spread into product scenes.
- Steam quality bar: all visible/listenable public materials must be commercially cleared and representative.
- Veripsa unit: each imported asset or plugin is a task with source, license, allowed use, and public-repo risk.

## Core Rule

Only use assets, code, audio, fonts, plugins, and generated material with clear commercial-use rights.

If license status is unknown, the asset is not allowed in product work.

Free is not enough. A free asset is allowed only when commercial use, redistribution rules, attribution, modification rights, and public-repo suitability are understood and recorded.

Official free tools and already installed tools may be used when they do not create charges, expose credentials, violate platform terms, or add unsafe dependencies.

## CC0 And Free Asset Intake

Allowed provider classes for public-repo art-density work:

- Project-authored assets.
- Verified CC0/public-domain-style sources such as Poly Haven, ambientCG, and Kenney, checked on the asset page at intake time.
- Other free assets only when the specific license explicitly allows commercial use, modification, attribution compliance, and public source redistribution of raw or converted files.

Before importing or committing any free/CC0 asset:

- Add or update the asset ledger row.
- Record the asset page, creator/source, license, review date, and reviewer.
- Set public-repo redistribution to `Yes` only when raw/source redistribution is explicitly allowed.
- Keep required attribution notes with the ledger entry.
- Reject the asset if the license page, creator rights, or redistribution terms are unclear.

Fab/Marketplace commercial-use permission is not public-repo permission. Do not commit raw Fab, Marketplace, or other commercial pack assets to the public repo unless a specific license or written permission explicitly allows public source redistribution.

## Public Repo Separation

Safe for a public repo:

- Source code written for this project.
- Configuration that contains no secrets.
- Development docs that do not reveal private sales strategy.
- Tooling scripts.
- Placeholder records without restricted asset files.
- License summaries.

Not safe for a public repo:

- Paid Marketplace/Fab assets unless license permits redistribution as source.
- Raw commercial audio libraries.
- Secret keys.
- Steamworks credentials.
- Console SDK material.
- Private publisher/platform communication.
- Unreleased pricing/sales strategy if intentionally private.
- AI assets with unclear terms.
- Third-party reference boards containing copyrighted source images.

## Reference Media Rule

Commercial horror references may be inspected for market and quality analysis, but they are not project assets.

Allowed:

- Viewing official store pages, official trailers, official screenshots, and official developer/publisher materials.
- Temporarily downloading public reference screenshots or trailers to ignored/local temporary folders for measurement with tools such as `ffmpeg`, `ffprobe`, or image analysis scripts.
- Recording source links, app IDs, dates reviewed, and derived observations in repo documents.

Not allowed:

- Committing third-party screenshots, trailer frames, videos, thumbnails, art books, reference boards, or scraped media.
- Tracing, copying, recreating, or kitbashing another game's distinctive visual content.
- Treating "free to view" reference media as free game assets.
- Using reference analysis as a substitute for license review on any imported asset.

Reference findings may change art direction and acceptance criteria. They do not grant asset rights.

## Asset Ledger

Create an asset ledger before importing production assets. Each entry must include:

- Asset ID.
- File path.
- Source/vendor/tool.
- Creator if known.
- License.
- Commercial-use permission.
- Redistribution/source-control permission.
- Modification notes.
- Attribution requirement.
- Purchase/receipt location if applicable, kept private if needed.
- Allowed use: internal, demo, store, trailer, release.
- Review date.
- Reviewer.

## Unreal Marketplace, Fab, Quixel

Allowed only when:

- License permits the intended commercial use.
- Redistribution restrictions are understood.
- Raw/source redistribution is explicitly permitted before any asset file is committed to a public repo.
- Asset is adapted to the art direction.
- It is not used as an unmodified style anchor.
- It is recorded in the ledger.

If redistribution is not permitted, use a private local dependency, a documented placeholder record, or a project-authored/verified CC0 replacement instead.

Do not mix random asset packs. A coherent art direction matters more than asset volume.

For the hotel horror product, free assets must be adapted into a consistent old business hotel tone. If a free asset does not fit the tone or license, create a simple original asset instead.

## AI-Generated Material

AI-generated assets are allowed only after review:

- Tool name and version/service.
- Generation date.
- Terms/license at generation time.
- Prompt/source inputs.
- Confirmation that prompts did not request copyrighted characters, brands, living artists' protected style, or proprietary material.
- Human selection/editing notes.
- Similarity/IP risk review.
- Allowed use.

No AI-generated asset is public-facing until cleared.

## Fonts

Fonts must be licensed for:

- Commercial game embedding or rasterization.
- Store/trailer/marketing use.
- UI use.

Default engine fonts or free fonts still require ledger entries and license review.

## Audio

Audio assets must record:

- Source library/tool.
- License.
- Commercial-use permission.
- Modification.
- Attribution if any.
- Looping/stem status.
- Store/trailer permission.

Avoid using recognizable stock sounds without processing. The product should not sound generic.

## Code And Plugins

Plugins must be approved for:

- Commercial use.
- Source control inclusion rules.
- Platform support.
- Console compatibility risk.
- Maintenance risk.
- Security/privacy impact.

No plugin is added for convenience if Unreal already covers the requirement well enough.

No plugin, package, or service may be installed if it starts billing, requires unclear telemetry, weakens security, or conflicts with license terms.

## Secrets And Credentials

Never commit:

- Steamworks credentials.
- API keys.
- Signing certificates.
- Console SDK paths or secrets.
- Store tokens.
- Private account details.

Use local ignored files, environment variables, or secure secret storage when needed.

## License Gate

Before store/trailer/demo/release:

- All visible/listenable assets are ledgered.
- All asset licenses are reviewed.
- AI-generated assets are cleared.
- Required attribution is prepared.
- Public repo does not contain restricted source assets.
- Placeholder and unlicensed materials are excluded from builds.

Any unresolved rights item blocks public release.
