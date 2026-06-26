# Asset License Ledger

Record every asset before it enters product work, including free assets and AI-assisted material.

| Asset ID | Path | Type | Source/Creator | Cost | License | Commercial Use | Public Repo Redistribution | Modified? | Attribution Required | Allowed Use | Review Date | Reviewer | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `asset.project_docs` | `*.md` | Documentation | Project-authored | Free | Project-owned | Yes | Yes | N/A | No | Public repo | 2026-06-26 | Codex | Initial public-safe docs. |
| `asset.hotel_spine_level_v0` | `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`; `Content/Hotel/Materials/*.uasset` | Unreal map/material assets | Project-authored by Codex using Unreal Engine stock primitives | Free | Project-owned; depends on Unreal Engine runtime/editor license for use in Unreal project | Yes | Yes | N/A | No | internal-only | 2026-06-26 | Codex | Production-intent hotel spine blockout with project-authored practical glow materials; not cleared for store/trailer. |
| `asset.audio_generated_v0` | `SourceAssets/AudioGenerated/*_v0.wav`; `Content/Hotel/Audio/*_v0.uasset` | Synthetic SFX/ambience | Project-authored by Codex via deterministic waveform generation | Free | Project-owned | Yes | Yes | N/A | No | internal-only | 2026-06-27 | Codex | Placeholder audio only, now including the phone pickup click and phone-line static/thin-voice cue; must be replaced or explicitly approved before demo/store/trailer. |
| `asset.unreal_engine_stock_primitives` | `/Engine/BasicShapes/Cube.Cube` | Engine stock mesh reference | Epic Games Unreal Engine install | Free with Unreal Engine | Unreal Engine EULA | Yes, within Unreal Engine product terms | No engine asset redistribution in repo; referenced only | No | No | internal-only | 2026-06-26 | Codex | Used for early blockout geometry inside generated map. |
| `asset.first_loop_runtime_code_v0` | `Source/HotelNightShiftHorror/**`; `Config/DefaultInput.ini`; `Config/DefaultEngine.ini`; `HotelNightShiftHorror.uproject` | Runtime code/config | Project-authored by Codex | Free | Project-owned | Yes | Yes | N/A | No | internal-only | 2026-06-26 | Codex | Minimal C++ runtime layer for first hotel loop; no third-party code or downloaded assets introduced. |
| `asset.hotel_mrq_capture_pipeline_v0` | `Automation/Unreal/create_hotel_mrq_evidence_assets.py`; `Automation/Tools/check_hotel_mrq_capture_pngs.py`; `Content/Hotel/Cinematics/LS_HotelSpine_Stills.uasset`; `Content/Hotel/Cinematics/MRQ_HotelEvidencePng.uasset`; `HotelNightShiftHorror.uproject` | Unreal cinematic/render automation | Project-authored by Codex using official Epic Movie Render Queue plugin | Free | Project-owned scripts/assets; depends on Unreal Engine EULA for MRQ plugin use | Yes | Yes | N/A | No | internal-only | 2026-06-27 | Codex | Produces ignored local evidence PNGs under `Saved/MovieRenders/HotelSpineSlice`; now gates four shots including the phone-response close-up. No third-party media introduced. |
| `asset.front_desk_phone_response_v0` | `Source/HotelNightShiftHorror/**`; `Automation/Unreal/create_hotel_spine_slice.py`; `Automation/Unreal/verify_hotel_spine_slice.py`; `Content/Hotel/Maps/L_HotelNightShift_Slice.umap` | Runtime/level slice | Project-authored by Codex using Unreal Engine project code and stock primitives | Free | Project-owned; depends on Unreal Engine EULA for runtime/editor use | Yes | Yes | N/A | No | internal-only | 2026-06-27 | Codex | Product-map phone response extension: ring cutoff, pickup click trigger, call lamp, desk line status, transition floor/walls, and stricter state gating. Not final art/audio. |
| `asset.front_desk_phone_live_response_v0` | `Source/HotelNightShiftHorror/Private/Tests/HotelFrontDeskPhoneResponseAutomationTest.cpp`; `Source/HotelNightShiftHorror/**`; `Automation/Unreal/create_hotel_spine_slice.py`; `Automation/Unreal/verify_hotel_spine_slice.py`; `Content/Hotel/Maps/L_HotelNightShift_Slice.umap`; `Content/Hotel/Audio/SFX_PhoneLineStatic_v0.uasset`; `SourceAssets/AudioGenerated/SFX_PhoneLineStatic_v0.wav` | Runtime/automation/audio slice | Project-authored by Codex using Unreal Engine project code, official automation framework, stock primitives, and deterministic waveform generation | Free | Project-owned; depends on Unreal Engine EULA for runtime/editor use | Yes | Yes | N/A | No | internal-only | 2026-06-27 | Codex | Live production-map phone response proof: answer cuts ring, lifts movable receiver cue, connects/disconnects placeholder phone-line audio, and automation verifies phone/monitor/Room203/report progression. Not final art/audio. |

## Allowed Use Values

- `internal-only`
- `public-repo`
- `playtest`
- `demo`
- `store`
- `trailer`
- `release`

If license status is unclear, do not import the asset.
