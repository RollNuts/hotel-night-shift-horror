# Horror Reference Visual Audit

## Summary

- Task ID: `T2026-0701-HORROR-REFERENCE-VISUAL-AUDIT`
- Owner: Codex
- Status: Complete
- Product goal: Recalibrate first-loop visual proof against current public horror games before accepting low-poly or placeholder-looking footage.
- Scope: Official Steam pages, official Steam screenshots, and official Steam CDN 480p trailers for comparable low-budget or stylized horror games.
- Non-goal: No third-party media, trailer frames, screenshots, or downloaded reference files are committed to the repo.

## References Checked

Reviewed on 2026-07-01.

- `Mouthwashing` (`2475490`): official Steam page, official screenshots, official Steam trailer media. Release date observed from Steam API: 2024-09-26. Steam recommendations observed: 33,292.
- `Fears to Fathom - Ironbark Lookout` (`2506160`): official Steam page, official screenshots, official Steam trailer media. Release date observed from Steam API: 2023-10-20. Steam recommendations observed: 5,772.
- `[Chilla's Art] The Closing Shift | 閉店事件` (`1843090`): official Steam page, official screenshots, official Steam trailer media. Release date observed from Steam API: 2022-03-18. Steam recommendations observed: 2,892.
- `No, I'm not a Human` (`3180070`): official Steam page, official screenshots, official Steam trailer media. Release date observed from Steam API: 2025-09-15. Steam recommendations observed: 25,707.

## Method

- Queried Steam public metadata through store search/appdetails APIs.
- Downloaded official screenshots and 480p trailers only to local temporary folders outside the repo for visual review and measurement.
- Used `ffprobe`, `ffmpeg`, and local image sampling to compare trailer duration, sampled luma, dark-frame ratio, saturation, and edge density.
- Reviewed current `Saved/MovieRenders/FirstLoopPlaythrough/first_loop_playthrough_proof.mp4` against the same rough metrics.
- Did not copy, trace, convert, import, or commit any third-party visual/audio material.

## Video Metric Snapshot

These metrics are direction checks, not a legal or quality substitute for human review.

| Source | Duration | Median luma | Median dark fraction | Median saturation | Median edge |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mouthwashing official trailer | 38.80s | 18.4 | 0.86 | 0.58 | 8.84 |
| Fears to Fathom Ironbark official trailer | 80.00s | 45.4 | 0.44 | 0.33 | 7.32 |
| The Closing Shift official trailer | 32.97s | 31.8 | 0.79 | 0.31 | 10.74 |
| No, I'm not a Human official trailer | 85.01s | 34.3 | 0.59 | 0.56 | 7.46 |
| Current HotelNightShift first-loop proof | 24.00s | 69.4 | 0.42 | 0.43 | 13.12 |

Interpretation: the current proof is not failing because it is too dark. It is brighter and edge-heavier than the references, but the edges come from exposed simple geometry and close foreground blockout-like props. The problem is composition, material credibility, and subject choice.

## Market Observations

- Low-budget horror can sell with stylization, but each shot still needs a deliberate subject: a face, sign, door, light cone, readable text, silhouette, or tactile surface.
- Darkness works when it hides nonessential areas and directs the eye. It fails when it hides player intent or leaves the foreground dominated by unfinished shapes.
- Stylized games make their low fidelity intentional through texture, palette, posterization, UI treatment, grain, character art, or bold composition.
- Realistic low-budget games avoid raw close-ups by leaning on weather, reflections, wet ground, practical lights, signage, readable interiors, and long shadow shapes.
- Store screenshots usually show a complete visual promise in one image. They do not ask the viewer to trust a test description.

## Decisions For This Project

- Do not present smooth boxes, simple cylinders, or low-poly fixture close-ups as main proof frames.
- First-loop visual proof must prefer readable hotel surfaces, door-state evidence, diegetic text, monitor content, paper/log detail, lamp pools, and hallway silhouettes over close prop geometry.
- Any first-person proof frame with a foreground prop must pass one of these tests:
  - strong authored silhouette,
  - texture/decal wear,
  - readable diegetic text,
  - meaningful animation contact,
  - or intentional stylized treatment.
- Internal cinematic proof may remain lower than store quality, but it still cannot use blockout-looking close-ups as its primary evidence.
- The next actual product slice should be one visually convincing first-person beat, not another broad minimal proof. Recommended beat: `phone -> monitor -> Room203 door/result -> report log`, with one store-screenshot candidate and one local ignored MP4.
- Free external assets are not automatically approved. Use only project-authored assets or assets with explicit commercial and public-repo redistribution clearance recorded in the asset ledger.

## Sources

- `https://store.steampowered.com/app/2475490/Mouthwashing/`
- `https://store.steampowered.com/app/2506160/Fears_to_Fathom__Ironbark_Lookout/`
- `https://store.steampowered.com/app/1843090/Chillas_Art_The_Closing_Shift/`
- `https://store.steampowered.com/app/3180070/No_Im_not_a_Human/`
- `https://www.fab.com/eula`

## Completion Statement

This audit changes the acceptance bar: functionally correct proof is not enough, and current first-loop footage must avoid raw low-poly close-ups before it is suitable for a ready PR.
