"""Create a short report-log filing pressure proof sequence.

This is an internal capture aid, not a gameplay feature or public trailer
approval. It animates existing production-map front-desk report-log actors so
PRs can prove recording the Room 203 refusal reads as a physical hotel-work
action under pressure.
"""

from __future__ import annotations

import math

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"
CINEMATICS_DIR = "/Game/Hotel/Cinematics"
SEQUENCE_NAME = "LS_ReportLog_FilingPressureProof_5s"
MRQ_CONFIG_NAME = "MRQ_ReportLogFilingPressureProofPng"
SEQUENCE_PATH = f"{CINEMATICS_DIR}/{SEQUENCE_NAME}"
MRQ_CONFIG_PATH = f"{CINEMATICS_DIR}/{MRQ_CONFIG_NAME}"
PUBLIC_SEQUENCE_AUTHOR = "Hotel Night Shift Horror Project"
FPS = 24
SECONDS = 5
END_FRAME = FPS * SECONDS

CAMERA_KEYS = [
    (0, (-62, -728, 184), (-11.0, 132.0, 0.0), 48.0),
    (14, (-61, -728, 184), (-11.2, 132.1, 0.0), 47.5),
    (26, (-59, -727, 183), (-11.4, 132.3, 0.0), 47.0),
    (44, (-61, -728, 184), (-11.1, 132.2, 0.0), 47.5),
    (78, (-58, -726, 183), (-11.5, 132.5, 0.0), 46.8),
    (END_FRAME, (-57, -726, 183), (-11.4, 132.5, 0.0), 46.8),
]

REPORT_LOG_JOLTS = {
    "PROP_FrontDesk_ReportLog_FiledStampCue": (16, (0.0, 9.0, 7.5), (-4.0, 0.0, -11.0), 1.06),
    "PROP_FrontDesk_ReportLog_AuthoredPenBody": (19, (3.0, -7.0, 3.0), (-3.0, 0.0, 9.0), 1.03),
    "PROP_FrontDesk_ReportLog_AuthoredPenNib": (19, (4.0, -8.0, 3.2), (-4.0, 0.0, 11.0), 1.04),
    "PROP_FrontDesk_ReportLog_AuthoredCurledPages": (21, (0.0, -5.0, 4.5), (-2.5, 0.0, 5.0), 1.02),
    "PROP_FrontDesk_ReportLog_FiledInkStrokes": (22, (0.0, -5.8, 2.2), (-1.4, 0.0, 4.0), 1.03),
    "LIGHTMESH_FrontDesk_DeskLampPractical": (20, (0.0, -3.2, 1.8), (0.0, 0.0, 2.8), 1.08),
    "PROP_FrontDesk_ReportLog_RedInkSmear": (23, (0.0, -3.0, 1.0), (-1.0, 0.0, 3.0), 1.02),
}

CONTEXT_DEEMPHASIS_ACTORS = {
    "PROP_FrontDesk_ReportLog_SelfCorrectedRoom203OpenLine": 0.01,
    "PROP_FrontDesk_ReportLog_SelfCorrectedNoGuestLine": 0.01,
    "PROP_FrontDesk_ReportLog_SelfCorrectedTimestampSlash": 0.01,
    "LIGHTMESH_FrontDesk_ReportLog_SelfCorrectionCue": 0.01,
    "PROP_FrontDesk_CounterHoldLine_PostReport": 0.01,
    "PROP_FrontDesk_FloorWaitMarker_PostReport": 0.01,
}


def log(message: str) -> None:
    unreal.log(f"[ReportLogFilingPressureProofAssets] {message}")


def fail(message: str) -> None:
    raise RuntimeError(f"[ReportLogFilingPressureProofAssets] {message}")


def try_set_property(obj, name: str, value) -> None:
    try:
        obj.set_editor_property(name, value)
    except Exception:
        pass


def make_rotator(pitch: float, yaw: float, roll: float = 0.0) -> unreal.Rotator:
    return unreal.Rotator(roll, pitch, yaw)


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


def focal_length_from_fov_degrees(fov_degrees: float, sensor_width_mm: float = 36.0) -> float:
    half_angle = math.radians(max(1.0, min(160.0, fov_degrees)) * 0.5)
    return (sensor_width_mm * 0.5) / math.tan(half_angle)


def channel_name(channel) -> str:
    return str(getattr(channel, "channel_name", ""))


def add_float_key(channel, frame: int, value: float) -> None:
    try:
        channel.add_key(unreal.FrameNumber(frame), float(value))
    except TypeError:
        channel.add_key(frame, float(value))


def add_transform_key(section, frame: int, location, rotation, scale) -> None:
    values = {
        "Location.X": float(location[0]),
        "Location.Y": float(location[1]),
        "Location.Z": float(location[2]),
        "Rotation.X": float(rotation[2]),
        "Rotation.Y": float(rotation[0]),
        "Rotation.Z": float(rotation[1]),
        "Scale.X": float(scale[0]),
        "Scale.Y": float(scale[1]),
        "Scale.Z": float(scale[2]),
    }
    for channel in section.get_all_channels():
        name = channel_name(channel)
        if name in values:
            add_float_key(channel, frame, values[name])


def add_camera_focal_key(section, frame: int, fov: float) -> None:
    for channel in section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel):
        add_float_key(channel, frame, focal_length_from_fov_degrees(fov))


def add_camera_transform_track(sequence: unreal.LevelSequence, camera_binding) -> None:
    track = camera_binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_start_frame(0)
    section.set_end_frame(END_FRAME)
    for frame, location, rotation, _fov in CAMERA_KEYS:
        add_transform_key(section, frame, location, rotation, (1.0, 1.0, 1.0))


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

    try_set_property(metadata, "author", PUBLIC_SEQUENCE_AUTHOR)
    try_set_property(
        metadata,
        "notes",
        "Generated by Automation/Unreal/create_report_log_filing_pressure_proof_assets.py for internal report-log filing proof.",
    )


def add_spawnable_proof_camera(sequence: unreal.LevelSequence):
    first_location, first_rotation, first_fov = CAMERA_KEYS[0][1], CAMERA_KEYS[0][2], CAMERA_KEYS[0][3]
    temp_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CineCameraActor,
        unreal.Vector(*first_location),
        make_rotator(*first_rotation),
    )
    temp_camera.set_actor_label("TMP_ReportLogFilingPressureProofCamera")
    try:
        cine_component = temp_camera.get_cine_camera_component()
        try_set_property(cine_component, "current_focal_length", focal_length_from_fov_degrees(first_fov))
        try_set_property(cine_component, "current_aperture", 22.0)
        try_set_property(cine_component, "post_process_blend_weight", 1.0)
        try:
            projection_mode = getattr(unreal.CameraProjectionMode, "PERSPECTIVE", None)
            if projection_mode is not None:
                try_set_property(cine_component, "projection_mode", projection_mode)
        except Exception:
            pass
        try:
            focus_settings = cine_component.get_editor_property("focus_settings")
            try:
                focus_settings.set_editor_property("focus_method", unreal.CameraFocusMethod.DISABLE)
            except Exception:
                pass
            try_set_property(focus_settings, "manual_focus_distance", 185.0)
            cine_component.set_editor_property("focus_settings", focus_settings)
        except Exception:
            pass
        try:
            settings = cine_component.get_editor_property("post_process_settings")
            exposure_overrides = {
                "override_auto_exposure_method": True,
                "override_auto_exposure_min_brightness": True,
                "override_auto_exposure_max_brightness": True,
                "override_auto_exposure_bias": True,
                "override_motion_blur_amount": True,
                "auto_exposure_min_brightness": 1.0,
                "auto_exposure_max_brightness": 1.0,
                "auto_exposure_bias": 2.4,
                "motion_blur_amount": 0.0,
            }
            for name, value in exposure_overrides.items():
                try_set_property(settings, name, value)
            try:
                settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
            except Exception:
                pass
            cine_component.set_editor_property("post_process_settings", settings)
        except Exception:
            pass
    except Exception:
        pass

    binding = sequence.add_spawnable_from_instance(temp_camera)
    binding.set_display_name("CAM_ReportLog_FilingPressureProof_5s")

    try:
        cine_component = temp_camera.get_cine_camera_component()
        component_binding = sequence.add_possessable(cine_component)
        component_binding.set_parent(binding)
        focal_length_track = component_binding.add_track(unreal.MovieSceneFloatTrack)
        focal_length_track.set_property_name_and_path("CurrentFocalLength", "CurrentFocalLength")
        focal_length_section = focal_length_track.add_section()
        focal_length_section.set_start_frame(0)
        focal_length_section.set_end_frame(END_FRAME)
        for frame, _location, _rotation, fov in CAMERA_KEYS:
            add_camera_focal_key(focal_length_section, frame, fov)
    except Exception:
        pass

    unreal.EditorLevelLibrary.destroy_actor(temp_camera)
    return binding


def actor_transform_tuple(actor):
    location = actor.get_actor_location()
    rotation = actor.get_actor_rotation()
    scale = actor.get_actor_scale3d()
    return (
        (location.x, location.y, location.z),
        (rotation.pitch, rotation.yaw, rotation.roll),
        (scale.x, scale.y, scale.z),
    )


def add_tuple(a, b):
    return tuple(float(a[index]) + float(b[index]) for index in range(3))


def multiply_tuple(values, multiplier: float):
    return tuple(float(value) * float(multiplier) for value in values)


def add_actor_jolt_track(sequence: unreal.LevelSequence, label: str, jolt) -> None:
    actor = find_actor_by_label(label)
    if actor is None:
        fail(f"Missing report-log proof actor: {label}")

    start_frame, offset, rotation_delta, scale_multiplier = jolt
    location, rotation, scale = actor_transform_tuple(actor)
    peak_location = add_tuple(location, offset)
    settle_location = add_tuple(location, multiply_tuple(offset, -0.18))
    second_location = add_tuple(location, multiply_tuple(offset, 0.36))
    peak_rotation = add_tuple(rotation, rotation_delta)
    settle_rotation = add_tuple(rotation, multiply_tuple(rotation_delta, -0.22))
    second_rotation = add_tuple(rotation, multiply_tuple(rotation_delta, 0.34))
    peak_scale = multiply_tuple(scale, scale_multiplier)

    keys = [
        (0, location, rotation, scale),
        (max(0, start_frame - 4), location, rotation, scale),
        (start_frame + 3, peak_location, peak_rotation, peak_scale),
        (start_frame + 10, settle_location, settle_rotation, scale),
        (start_frame + 22, second_location, second_rotation, multiply_tuple(scale, 1.0 + (scale_multiplier - 1.0) * 0.35)),
        (start_frame + 38, location, rotation, scale),
        (END_FRAME, location, rotation, scale),
    ]

    binding = sequence.add_possessable(actor)
    binding.set_display_name(label)
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_start_frame(0)
    section.set_end_frame(END_FRAME)
    for frame, key_location, key_rotation, key_scale in keys:
        add_transform_key(section, frame, key_location, key_rotation, key_scale)


def add_actor_scale_multiplier_track(sequence: unreal.LevelSequence, label: str, multiplier: float) -> None:
    actor = find_actor_by_label(label)
    if actor is None:
        return

    location, rotation, scale = actor_transform_tuple(actor)
    scaled = multiply_tuple(scale, multiplier)
    binding = sequence.add_possessable(actor)
    binding.set_display_name(label)
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_start_frame(0)
    section.set_end_frame(END_FRAME)
    add_transform_key(section, 0, location, rotation, scaled)
    add_transform_key(section, END_FRAME, location, rotation, scaled)


def create_sequence() -> unreal.LevelSequence:
    delete_existing_asset(SEQUENCE_PATH)
    sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        SEQUENCE_NAME,
        CINEMATICS_DIR,
        unreal.LevelSequence,
        unreal.LevelSequenceFactoryNew(),
    )
    if not sequence:
        fail("Unable to create report-log filing pressure LevelSequence.")

    try:
        sequence.set_display_rate(unreal.FrameRate(FPS, 1))
        sequence.set_tick_resolution(unreal.FrameRate(FPS, 1))
    except Exception:
        pass
    sequence.set_playback_start(0)
    sequence.set_playback_end(END_FRAME)

    camera_binding = add_spawnable_proof_camera(sequence)
    add_camera_transform_track(sequence, camera_binding)
    camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)
    if not camera_cut_track:
        fail("Unable to create camera cut track.")
    cut = camera_cut_track.add_section()
    cut.set_start_frame(0)
    cut.set_end_frame(END_FRAME)
    try:
        cut.set_camera_binding_id(sequence.get_binding_id(camera_binding))
    except Exception:
        cut.set_editor_property("CameraBindingID", camera_binding_id(camera_binding))

    for label, jolt in REPORT_LOG_JOLTS.items():
        add_actor_jolt_track(sequence, label, jolt)
    for label, multiplier in CONTEXT_DEEMPHASIS_ACTORS.items():
        add_actor_scale_multiplier_track(sequence, label, multiplier)

    sequence.set_playback_start(0)
    sequence.set_playback_end(END_FRAME)
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
        fail("Unable to create report-log filing pressure MRQ config.")

    output = config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output.output_resolution = unreal.IntPoint(1280, 720)
    output.file_name_format = "report_log_filing_pressure_proof_{frame_number}"
    output.output_directory.path = "{project_dir}/Saved/MovieRenders/ReportLogFilingPressure"
    output.override_existing_output = True
    output.zero_pad_frame_numbers = 4
    output.flush_disk_writes_per_shot = True
    output.output_frame_step = 6

    render_pass = config.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
    try_set_property(render_pass, "add_default_layer", False)

    config.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)

    anti_aliasing = config.find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)
    try_set_property(anti_aliasing, "render_warm_up_frames", False)
    try_set_property(anti_aliasing, "use_camera_cut_for_warm_up", False)

    console_variables = config.find_or_add_setting_by_class(unreal.MoviePipelineConsoleVariableSetting)
    console_variables.add_or_update_console_variable("r.AntiAliasingMethod", 2.0)
    console_variables.add_or_update_console_variable("r.TemporalAA.Upsampling", 0.0)
    console_variables.add_or_update_console_variable("r.DefaultFeature.MotionBlur", 0.0)
    console_variables.add_or_update_console_variable("r.MotionBlur.Amount", 0.0)
    console_variables.add_or_update_console_variable("r.DepthOfFieldQuality", 0.0)

    game_overrides = config.find_or_add_setting_by_class(unreal.MoviePipelineGameOverrideSetting)
    try_set_property(game_overrides, "cinematic_quality_settings", True)
    try_set_property(game_overrides, "flush_streaming_managers", True)

    unreal.EditorAssetLibrary.save_asset(MRQ_CONFIG_PATH)
    return config


def main() -> None:
    unreal.EditorAssetLibrary.make_directory(CINEMATICS_DIR)
    unreal.EditorLevelLibrary.load_level(MAP_PATH)
    create_sequence()
    create_mrq_config()
    log(f"Created {SEQUENCE_PATH} and {MRQ_CONFIG_PATH}.")


main()
