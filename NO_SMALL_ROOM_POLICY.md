# NO SMALL ROOM POLICY

Status: active production discipline.

Test rooms are allowed. Mistaking them for product progress is not.

## Codex Decision Frame

- Build: test harnesses only for verification and product slices only in product-intent context.
- Do not build: feature piles inside isolated rooms or tuning work without final camera/art/audio/UX context.
- Market reason: players buy the shown product experience, not isolated mechanics.
- Unreal reason: Unreal makes test maps easy, so the project needs explicit promotion gates into real scenes.
- Solo-dev/low-cost reason: isolated experiments consume time unless they remove a concrete production risk.
- Art/audio bar: a feature has no product value until it survives lighting, sound, camera, UI, and level context.
- No-small-room bar: test room evidence is never store/trailer/demo evidence.
- Steam quality bar: screenshots and clips must come from representative product scenes.
- Veripsa unit: label test harness tasks separately and prevent them from closing as product-complete.

## Principle

A test map can prove whether a function works. It cannot prove whether the game is worth buying.

Product progress only counts when the feature is shown in product-intent camera, lighting, art direction, audio, UI, level flow, and performance context.

## Allowed Test-Room Uses

Test rooms may be used for:

- Input verification.
- Collision and trace checks.
- Physics checks.
- Animation timing isolation.
- VFX timing isolation.
- Audio cue testing.
- Performance stress tests.
- Automated regression tests.
- Bug reproduction.

Test rooms may not be used for:

- Product judgment.
- Store screenshot claims.
- Trailer claims.
- Art direction approval.
- Final level-design approval.
- Completion claims.
- Feature-count progress.

## Product Context Requirement

Any player-facing feature must be evaluated in a product-intent context:

- Chosen product camera.
- Chosen lighting approach.
- Chosen art direction.
- Chosen audio mix approach.
- Chosen UI style.
- Real approach path.
- Real failure/retry flow.
- Performance capture.

If those are not chosen because genre is pending, the feature must not be implemented.

## Test Harness Labeling

All test maps, assets, and tools must be clearly labeled:

- File/folder name includes `Test`, `Harness`, or `Regression`.
- Veripsa task label includes `test-harness`.
- Documentation says what it verifies.
- Documentation says what it does not prove.

No evidence from a test harness may be used as store/trailer/demo evidence.

## Small-Room Warning Signs

Stop and reassess if work starts doing any of these:

- Adding enemy variants in a test map.
- Tuning gameplay values before product context exists.
- Adding UI panels to explain unfinished mechanics.
- Creating puzzle/combat arenas without art/audio/camera.
- Expanding debug controls.
- Treating "fun in the box" as enough.
- Building systems because they are technically interesting.

## Promotion From Test To Product

A test-room feature can be promoted only when:

- Genre is locked.
- Product slice exists.
- The feature is inserted into real level flow.
- Art/audio/UX/performance evidence is captured.
- Placeholder status is resolved or tracked.
- The feature improves the core product promise.

If promotion fails, cut the feature or keep it as internal test infrastructure only.

## Evidence Rules

Engineering evidence may include:

- Logs.
- Unit test output.
- Editor screenshots.
- Debug overlays.
- Performance captures.

Product evidence must include:

- Screenshot or clip from product-intent scene.
- Audio present if the feature has sound.
- No debug UI.
- No placeholder unless explicitly labeled internal.
- Performance context.

## Veripsa Enforcement

Veripsa Core should flag:

- Tasks with only test-map changes.
- Tasks without product evidence.
- Tasks that add mechanics without quality axes.
- Tasks that claim completion with placeholder labels.
- Tasks whose evidence is editor-only.

Such tasks may close as `verified-test-harness`, but not as `product-complete`.
