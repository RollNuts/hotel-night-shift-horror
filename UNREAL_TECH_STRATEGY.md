# UNREAL TECH STRATEGY

Status: active for Unreal Engine 5.8.

## Codex Decision Frame

- Build: a Blueprint-first Unreal project for first-person hotel work horror.
- Do not build: engine demos, broad frameworks, World Partition by default, online systems, or speculative tooling.
- Market reason: Unreal should make the hotel look, sound, and feel premium in screenshots and short clips.
- Unreal reason: Lumen, first-person camera, audio space, Sequencer, Niagara, and Blueprints fit compact horror production.
- Solo-dev/low-cost reason: use engine-native tools and minimal C++.
- Art/audio bar: lighting, sound, UI, camera, and capture readiness are technical requirements.
- No-small-room bar: tests may exist, but acceptance happens in the hotel production level.
- Steam quality bar: packaging, settings, local save, controller consideration, and performance are planned early.
- Veripsa unit: binary assets, maps, Blueprints, materials, sounds, and widgets need ownership claims before edits.

## Engine Baseline

- Engine: Unreal Engine 5.8.
- Project type: Blueprint-first.
- C++: only for stable foundations or performance-critical code when Blueprints become hard to review or maintain.
- Input: Enhanced Input enabled.
- First platform: Windows PC on Steam.
- Controls: keyboard/mouse first, Xbox-style controller compatibility considered from early UI/input design.

## Unreal Feature Policy

Use:

- Blueprints for gameplay iteration and hotel interaction logic.
- C++ for save/settings/input foundations if needed.
- Lumen for hotel lighting and mood.
- Niagara for rare, memorable abnormal events.
- Sequencer for short in-game moments and trailer capture.
- Control Rig only for necessary animation fixes.
- Data Assets/Data Tables for tuning, requests, incidents, abnormal rules, SFX/VFX mappings, and endings.

Limit:

- Nanite to high-density props where profiling supports it.
- MetaHuman to essential major characters only.
- Level Streaming only if the hotel level requires it for performance or workflow.

Avoid by default:

- World Partition.
- Dedicated servers.
- Multiplayer framework work.
- Online platform dependencies.
- Heavy procedural generation.
- Plugin sprawl.
- Marketplace pack dumping without art direction.

## Project Structure

Expected Unreal content shape:

```text
Content/
  Hotel/
    Maps/
    Blueprints/
    Props/
    Materials/
    Audio/
    UI/
    Data/
    VFX/
  TestHarness/
    Maps/
Docs/
Ledgers/
Veripsa/
Evidence/
```

`TestHarness` assets cannot be used as product evidence.

## First Production Slice Technical Target

The first slice should prove:

- First-person movement in the hotel.
- Front desk phone interaction.
- Camera monitor or surveillance check.
- Request/incident information display.
- Walk from front desk to one guest-room door.
- Door open/refuse/close decision.
- Report/log completion.
- One abnormal variation.
- Lighting, SFX, ambience, UI feedback, and capture readiness.

Do not add enemies, combat, broad inventory, or multiple hotel floors before this slice works.

## Performance Policy

Targets:

- Mid-range PC at 1080p should hold stable performance in the hotel production slice.
- Steam Deck-like 1280x800 framing/readability should be checked before demo.
- Lumen, fog, mirrors, monitor feeds, and translucent effects must be profiled.

Every visual feature needs a performance note before product-complete status.

