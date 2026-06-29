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
PUBLIC_SEQUENCE_AUTHOR = "Hotel Night Shift Horror Project"

CAPTURE_CAMERAS = [
    "CAPTURE_FrontDesk_FirstSteamShotCandidate",
    "CAPTURE_ReportLog_ReadabilityCandidate",
    "CAPTURE_PhoneResponse_LiftReceiverCandidate",
    "CAPTURE_Transition_ElevatorStair_AudioFearCandidate",
    "CAPTURE_PatrolRoute_DecisionCueCandidate",
    "CAPTURE_GuestDoor_15SecondBeatCandidate",
    "CAPTURE_ReturnRoute_BackKnockCandidate",
    "CAPTURE_PostReportMonitorMismatchCandidate",
    "CAPTURE_PostReportDeskWait_DoNotAnswerCandidate",
    "CAPTURE_PostReportLogSelfCorrectionCandidate",
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


def get_actor_camera_fov(actor) -> float:
    for component_getter in (
        "get_cine_camera_component",
        "get_camera_component",
    ):
        getter = getattr(actor, component_getter, None)
        if not getter:
            continue
        try:
            component = getter()
            return float(component.get_editor_property("field_of_view"))
        except Exception:
            pass

    try:
        component = actor.get_editor_property("camera_component")
        return float(component.get_editor_property("field_of_view"))
    except Exception:
        return 62.0


def focal_length_from_fov_degrees(fov_degrees: float, sensor_width_mm: float = 36.0) -> float:
    # CineCamera stores lens angle through focal length. Keep the spawned
    # evidence camera visually close to the authored map camera FOV.
    import math

    half_angle = math.radians(max(1.0, min(160.0, fov_degrees)) * 0.5)
    return (sensor_width_mm * 0.5) / math.tan(half_angle)


def set_float_channel_default(section, channel_name: str, value: float) -> None:
    for channel in section.get_all_channels():
        if str(getattr(channel, "channel_name", "")) == channel_name:
            channel.set_default(value)
            return


def set_transform_defaults(section, location, rotation) -> None:
    transform_defaults = {
        "Location.X": float(location.x),
        "Location.Y": float(location.y),
        "Location.Z": float(location.z),
        "Rotation.X": float(rotation.roll),
        "Rotation.Y": float(rotation.pitch),
        "Rotation.Z": float(rotation.yaw),
        "Scale.X": 1.0,
        "Scale.Y": 1.0,
        "Scale.Z": 1.0,
    }
    for channel_name, value in transform_defaults.items():
        set_float_channel_default(section, channel_name, value)


def add_spawnable_evidence_camera(sequence: unreal.LevelSequence, camera_label: str, frame_number: int):
    source_camera = find_actor_by_label(camera_label)
    if not source_camera:
        fail(f"Missing camera actor in hotel map: {camera_label}")

    location = source_camera.get_actor_location()
    rotation = source_camera.get_actor_rotation()
    fov_degrees = get_actor_camera_fov(source_camera)

    temp_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CineCameraActor,
        location,
        rotation,
    )
    temp_camera.set_actor_label(f"TMP_MRQ_{camera_label}")
    try:
        cine_component = temp_camera.get_cine_camera_component()
        try_set_property(cine_component, "current_focal_length", focal_length_from_fov_degrees(fov_degrees))
        try_set_property(cine_component, "current_aperture", 8.0)
    except Exception:
        pass

    binding = sequence.add_spawnable_from_instance(temp_camera)
    binding.set_display_name(camera_label)

    transform_track = binding.add_track(unreal.MovieScene3DTransformTrack)
    transform_section = transform_track.add_section()
    transform_section.set_end_frame(frame_number + 2)
    transform_section.set_start_frame(frame_number - 1)
    set_transform_defaults(transform_section, location, rotation)

    try:
        cine_component = temp_camera.get_cine_camera_component()
        component_binding = sequence.add_possessable(cine_component)
        component_binding.set_parent(binding)
        focal_length_track = component_binding.add_track(unreal.MovieSceneFloatTrack)
        focal_length_track.set_property_name_and_path("CurrentFocalLength", "CurrentFocalLength")
        focal_length_section = focal_length_track.add_section()
        focal_length_section.set_end_frame(frame_number + 2)
        focal_length_section.set_start_frame(frame_number - 1)
        for channel in focal_length_section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel):
            channel.set_default(focal_length_from_fov_degrees(fov_degrees))
    except Exception:
        pass

    unreal.EditorLevelLibrary.destroy_actor(temp_camera)
    return binding


def sanitize_sequence_metadata(sequence: unreal.LevelSequence) -> None:
    metadata_class = getattr(unreal, "MovieSceneMetaData", None)
    if metadata_class is None:
        return

    metadata = None
    for method_name in ("find_or_add_meta_data_by_class", "find_or_add_metadata_by_class"):
        method = getattr(sequence, method_name, None)
        if not method:
            continue
        try:
            metadata = method(metadata_class)
            break
        except Exception:
            pass

    if metadata is None:
        return

    for property_name, value in (
        ("author", PUBLIC_SEQUENCE_AUTHOR),
        ("notes", "Generated by Automation/Unreal/create_hotel_mrq_evidence_assets.py for internal PR evidence."),
    ):
        try_set_property(metadata, property_name, value)


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
    sequence.set_playback_end(len(CAPTURE_CAMERAS))
    try:
        sequence.set_display_rate(unreal.FrameRate(24, 1))
        sequence.set_tick_resolution(unreal.FrameRate(24, 1))
    except Exception:
        pass

    camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)
    if not camera_cut_track:
        fail("Unable to create camera cut track.")

    for frame_number, camera_label in enumerate(CAPTURE_CAMERAS):
        binding = add_spawnable_evidence_camera(sequence, camera_label, frame_number)
        cut = camera_cut_track.add_section()
        cut.set_end_frame(frame_number + 1)
        cut.set_start_frame(frame_number - 1 if frame_number == 0 else frame_number)
        try:
            cut.set_camera_binding_id(sequence.get_binding_id(binding))
        except Exception:
            cut.set_editor_property("CameraBindingID", camera_binding_id(binding))

    # Adding camera cut sections can clamp the playback range in some editor
    # versions. Re-apply the full range so the final still is rendered.
    sequence.set_playback_start(0)
    sequence.set_playback_end(len(CAPTURE_CAMERAS))

    sanitize_sequence_metadata(sequence)
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
