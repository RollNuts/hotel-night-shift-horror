# T2026-0627 Transition Route Fear

## Summary

- Task ID: T2026-0627-TRANSITION-ROUTE-FEAR
- Owner: Codex
- Status: Implemented locally; ready PR traffic coordination pending
- Product goal: make the walk from the front desk toward Room 203 feel like a hotel transition with threat and route identity, not a neutral connector.
- Hotel area: production elevator, emergency stair, service shortcut, and guest-hall approach in `/Game/Hotel/Maps/L_HotelNightShift_Slice`.
- Core action affected: answer phone, check monitor, leave the front desk, pass the elevator/stair transition, reach Room 203, return, and file report.

## Scope

- Files/assets touched:
  - `Automation/Unreal/create_hotel_spine_slice.py`
  - `Automation/Unreal/verify_hotel_spine_slice.py`
  - `Automation/Unreal/create_hotel_mrq_evidence_assets.py`
  - `Automation/Tools/check_hotel_mrq_capture_pngs.py`
  - `Ledgers/ASSET_LICENSE_LEDGER.md`
  - `Ledgers/PLACEHOLDER_LEDGER.md`
- Binary Unreal/source assets claimed:
  - `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`
  - `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`
  - `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`
  - `Content/Hotel/Audio/AMB_ElevatorShaftGroan_v0.uasset`
  - `Content/Hotel/Audio/AMB_StairwellAir_v0.uasset`
  - `SourceAssets/AudioGenerated/AMB_ElevatorShaftGroan_v0.wav`
  - `SourceAssets/AudioGenerated/AMB_StairwellAir_v0.wav`
- Non-goals:
  - No elevator travel, stair navigation system, locked-route mechanic, new interaction prompt, enemy, inventory, or runtime state machine change.
  - No C++ changes.
  - No test room, side room, alternate prototype, or map branch.
  - No final signage art, final door/elevator meshes, final mix, trailer-ready audio, or store-page claim.
  - No paid, marketplace, third-party, externally downloaded, or licensed media import.
  - No Veripsa review assumption; Core is expected to coordinate PR traffic only.

## Quality Axes

- Gameplay: the existing route now has a readable fear beat between the front desk and Room 203 without adding a new rule to learn.
- Visual: the elevator, emergency stair, and locked service shortcut now have distinct visual cues: call panel, floor indicator, exit sign, door handle shadow, chain cue, and practical transition lighting.
- Camera: the MRQ evidence sequence now has six shots and includes `CAPTURE_Transition_ElevatorStair_AudioFearCandidate`.
- Animation: unchanged; this slice is static environmental readability only.
- VFX: unchanged; no supernatural effect added to this slice.
- SFX: adds deterministic project-authored elevator shaft groan and stairwell air ambience with tagged ambient sound actors.
- Music/ambience: expands area ambience identity for elevator and stair transition zones.
- UI feedback: unchanged; the work loop remains driven by the existing interaction HUD/state text.
- Level context: all work is in the production hotel map, not a small room or isolated test map.
- Performance: runtime cost is limited to two looping ambient sound actors, six simple transition cue meshes, and one additional point light for capture/readability.
- Capture readiness: MRQ now produces six unique 1280x720 PNGs and the PNG gate requires exactly six images.

## Risk And Compliance

- Placeholder impact:
  - `ph.hotel_spine_geometry_v0` remains active; elevator/stair/shortcut props are blockout geometry, not store/trailer art.
  - `ph.hotel_spine_audio_v0` remains active; transition ambience is synthetic placeholder audio.
  - The new transition evidence shot is internal proof only and not a store, trailer, or demo asset.
- License impact: project-authored scripts, deterministic WAV generation, generated Unreal assets, official Unreal editor scripting, stock primitives, and official Movie Render Queue only.
- Public repo risk: LevelSequence author metadata is sanitized to `Hotel Night Shift Horror Project`; no local user name, secrets, private files, platform SDKs, paid assets, marketplace downloads, or third-party media are intended for commit.
- Security/secret risk: no network service, account system, telemetry, credential use, or install step.
- Paid tool/asset risk: none introduced.
- Small-room risk: low; the slice is proven in `/Game/Hotel/Maps/L_HotelNightShift_Slice` and the production MRQ camera set.
- Veripsa Core concern: new binary/audio paths are expected and must be included in the PR; they are not unrelated assets.

## Evidence

- Python syntax:
  - `python3 -m py_compile Automation/Unreal/create_hotel_spine_slice.py Automation/Unreal/verify_hotel_spine_slice.py Automation/Unreal/create_hotel_mrq_evidence_assets.py Automation/Tools/check_hotel_mrq_capture_pngs.py`
  - Result: success.
- Diff whitespace:
  - `git diff --check`
  - Result: success.
- Map generation:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -run=pythonscript -script=Automation/Unreal/create_hotel_spine_slice.py`
  - Result: success, 0 errors, existing EditorLevelLibrary deprecation warnings only.
- Map verification:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -run=pythonscript -script=Automation/Unreal/verify_hotel_spine_slice.py`
  - Result: verified 19 assets, 88 required actors, 56 tagged actors, 9 audio actors, 6 movable feedback meshes, and 35 non-interactive polish actors.
- MRQ asset generation:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -run=pythonscript -script=Automation/Unreal/create_hotel_mrq_evidence_assets.py`
  - Result: success, 0 errors, existing generated-asset replacement and deprecation warnings only.
- MRQ render:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -LevelSequence=/Game/Hotel/Cinematics/LS_HotelSpine_Stills.LS_HotelSpine_Stills -MoviePipelineConfig=/Game/Hotel/Cinematics/MRQ_HotelEvidencePng.MRQ_HotelEvidencePng`
  - Result: Movie Pipeline completed in `+00:01:29.573`; executor finished in `+00:01:36.761`.
- MRQ PNG gate:
  - `python3 Automation/Tools/check_hotel_mrq_capture_pngs.py --capture-dir Saved/MovieRenders/HotelSpineSlice`
  - Result: passed 6 hotel MRQ evidence PNGs.
- Live map automation:
  - `UnrealEditor-Cmd HotelNightShiftHorror.uproject -ExecCmds="Automation RunTests Hotel.FrontDesk.PhoneResponse.LiveMap" -TestExit="Automation Test Queue Empty"`
  - Result: `Hotel.FrontDesk.PhoneResponse.LiveMap` success, 1 test performed.
- Public metadata smoke:
  - Method: scanned the generated LevelSequence asset for local user names, absolute local paths, secret-token prefixes, and platform SDK strings.
  - Result: author metadata is present only as `Hotel Night Shift Horror Project`; local user and absolute local path strings were not present.

## Evidence PNG Metrics

- `hotel_spine_evidence_0000.png`: average luma `36.2`, average RGB energy `95.0`, peak RGB energy `719`, visible pixels `543744/921600`, SHA-256 `5f934f11a6d655301022470f346cb2251c888296ae13322ba7cb6f0eba6bad0b`.
- `hotel_spine_evidence_0001.png`: average luma `99.2`, average RGB energy `295.1`, peak RGB energy `724`, visible pixels `770492/921600`, SHA-256 `7a938edb9c83302c9a3a28018776c4923e151caba225b3956cc6a05edd1a224f`.
- `hotel_spine_evidence_0002.png`: average luma `28.2`, average RGB energy `69.1`, peak RGB energy `708`, visible pixels `404872/921600`, SHA-256 `5b969f43c1d5cc141c9d19628639898638db624e72e9fad9d427d2cff0f30828`.
- `hotel_spine_evidence_0003.png`: average luma `23.4`, average RGB energy `52.8`, peak RGB energy `750`, visible pixels `550717/921600`, SHA-256 `d8728e1d6152c1a3600c1f368d8daf6ab5d090adf9ac5b4e0711c728161f6dcc`.
- `hotel_spine_evidence_0004.png`: average luma `39.4`, average RGB energy `114.8`, peak RGB energy `762`, visible pixels `606009/921600`, SHA-256 `b0d84463ebb77ec00c016f8bf0ef4e119a495c73ebec5f3f446be23210b4d6e4`.
- `hotel_spine_evidence_0005.png`: average luma `42.3`, average RGB energy `105.4`, peak RGB energy `765`, visible pixels `535293/921600`, SHA-256 `7ebddd18bd930d06e49a2aa518b0b9c11048a160f7c2e62d9a9984825ec4cda1`.

## Completion Statement

This slice deepens the existing work loop by making the transition from front desk to Room 203 read as an unsafe hotel route. The player now crosses an elevator/stair/shortcut zone with distinct visual anchors and low-cost ambient sound identities, while the runtime loop remains unchanged and proven by the existing live-map automation.
