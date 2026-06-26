"""Create Movie Render Queue still-capture assets for the hotel spine.

The assets generated here use the production hotel map and its existing
`CAPTURE_*` camera anchors. They are not gameplay features and they do not
introduce a test room; they provide a reliable evidence path for PRs.
"""

from __future__ import annotations

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"
CINEMATICS_DIR = "/Game/Hotel/Cinematics"
SEQUENCE_NAME = "LS_HotelSpine_Stills"
MRQ_CONFIG_NAME = "MRQ_HotelEvidencePng"
SEQUENCE_PATH = f"{CINEMATICS_DIR}/{SEQUENCE_NAME}"
MRQ_CONFIG_PATH = f"{CINEMATICS_DIR}/{MRQ_CONFIG_NAME}"

CAPTURE_CAMERAS = [
    "CAPTURE_FrontDesk_FirstSteamShotCandidate",
    "CAPTURE_GuestDoor_15SecondBeatCandidate",
    "CAPTURE_MonitorToHall_MismatchCandidate",
]


def log(message: str) -> None:
    unreal.log(f"[HotelMRQEvidenceAssets] {message}")


def fail(message: str) -> None:
    raise RuntimeError(f"[HotelMRQEvidenceAssets] {message}")


def try_set_property(obj, name: str, value) -> None:
    try:
        obj.set_editor_property(name, value)
    except Exception:
        pass


def delete_existing_asset(path: str) -> None:
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        if not unreal.EditorAssetLibrary.delete_asset(path):
            fail(f"Unable to delete existing generated asset: {path}")


def find_actor_by_label(label: str):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def camera_binding_id(binding) -> unreal.MovieSceneObjectBindingID:
    binding_id = unreal.MovieSceneObjectBindingID()
    binding_id.set_editor_property("Guid", binding.get_id())
    return binding_id


def create_still_sequence() -> unreal.LevelSequence:
    delete_existing_asset(SEQUENCE_PATH)
    sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        SEQUENCE_NAME,
        CINEMATICS_DIR,
        unreal.LevelSequence,
        unreal.LevelSequenceFactoryNew(),
    )
    if not sequence:
        fail("Unable to create MRQ still LevelSequence.")

    sequence.set_playback_start(0)
    sequence.set_playback_end(len(CAPTURE_CAMERAS) + 1)
    try:
        sequence.set_display_rate(unreal.FrameRate(24, 1))
        sequence.set_tick_resolution(unreal.FrameRate(24, 1))
    except Exception:
        pass

    camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)
    if not camera_cut_track:
        fail("Unable to create camera cut track.")

    for frame_number, camera_label in enumerate(CAPTURE_CAMERAS):
        camera = find_actor_by_label(camera_label)
        if not camera:
            fail(f"Missing camera actor in hotel map: {camera_label}")

        binding = sequence.add_possessable(camera)
        cut = camera_cut_track.add_section()
        cut.set_end_frame(frame_number + 1)
        cut.set_start_frame(frame_number)
        cut.set_editor_property("CameraBindingID", camera_binding_id(binding))

    unreal.EditorAssetLibrary.save_asset(SEQUENCE_PATH)
    return sequence


def create_mrq_config() -> unreal.MoviePipelinePrimaryConfig:
    delete_existing_asset(MRQ_CONFIG_PATH)
    config = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        MRQ_CONFIG_NAME,
        CINEMATICS_DIR,
        unreal.MoviePipelinePrimaryConfig,
        unreal.MoviePipelinePrimaryConfigFactory(),
    )
    if not config:
        fail("Unable to create MRQ PNG config.")

    output = config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output.output_resolution = unreal.IntPoint(1280, 720)
    output.file_name_format = "hotel_spine_evidence_{frame_number}"
    output.output_directory.path = "{project_dir}/Saved/MovieRenders/HotelSpineSlice"
    output.override_existing_output = True
    output.zero_pad_frame_numbers = 4
    output.flush_disk_writes_per_shot = True

    render_pass = config.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
    try_set_property(render_pass, "add_default_layer", False)

    config.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)

    anti_aliasing = config.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
    try_set_property(anti_aliasing, "render_warm_up_frames", False)
    try_set_property(anti_aliasing, "use_camera_cut_for_warm_up", False)

    console_variables = config.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
    console_variables.add_or_update_console_variable("r.AntiAliasingMethod", 2.0)
    console_variables.add_or_update_console_variable("r.TemporalAA.Upsampling", 0.0)

    game_overrides = config.find_or_add_setting_by_class(unreal.MoviePipelineGameOverrideSetting)
    try_set_property(game_overrides, "cinematic_quality_settings", True)
    try_set_property(game_overrides, "flush_streaming_managers", True)

    unreal.EditorAssetLibrary.save_asset(MRQ_CONFIG_PATH)
    return config


def main() -> None:
    unreal.EditorAssetLibrary.make_directory(CINEMATICS_DIR)
    unreal.EditorLevelLibrary.load_level(MAP_PATH)
    create_still_sequence()
    create_mrq_config()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    log(f"Created {SEQUENCE_PATH} and {MRQ_CONFIG_PATH}.")


main()
