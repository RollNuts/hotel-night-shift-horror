# Hotel Night Shift

Unreal Engine commercial game project for a first-person, single-location, night-shift business hotel horror game.

The goal is a Steam-first, offline, buy-to-own game about front desk work, surveillance, guest-room response, patrols, lock decisions, incident reporting, and the fear that emerges when routine hotel work stops being trustworthy.

## Current Status

This repository is public by design, but the product is not public-release ready.

- Engine target: Unreal Engine 5.8.
- Genre: first-person night-shift work horror.
- Setting: old business hotel.
- Scope: one complete night.
- Playtime target: 2-4 hours first clear, 5-8 hours including multiple endings.
- Network: no permanent server, no owned account, no live service.

## Required Rules

Read [REQUIRED.md](REQUIRED.md) before changing gameplay, art, audio, level design, store material, or build/release tooling.

The short version:

- Do not inherit Fourfold Echoes or Unity-era design.
- Do not add online-first, open-world, live-service, or co-op assumptions.
- Do not treat test rooms as product progress.
- Do not treat placeholders as complete.
- Do not commit secrets, paid raw assets, unclear-license assets, or private commercial strategy.
- Do make every gameplay task prove visual, audio, UI, level, performance, and capture readiness in the hotel context.

## Project Files

- `HotelNightShift.uproject` is the Unreal project descriptor.
- `Config/` contains minimal project configuration.
- `REQUIRED.md` contains non-negotiable product rules.
- `Ledgers/` contains public-safe templates for asset/license and placeholder tracking.
- `Veripsa/` contains task templates for AI and PR coordination.
- Design policy docs live at the repo root until a later documentation pass moves them under `Docs/`.

## Asset Policy

Free assets, music, SFX, 3D models, and tools may be used only when their licenses are clear and commercial use is allowed. "Free" does not mean safe to redistribute in a public repository.

Every asset must be recorded in [Ledgers/ASSET_LICENSE_LEDGER.md](Ledgers/ASSET_LICENSE_LEDGER.md). If no suitable free asset exists, create an original asset and record its source and license status.
