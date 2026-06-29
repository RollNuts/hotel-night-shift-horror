"""Create a lightweight 15-second ReturnRoute trailer proof sequence.

This does not add gameplay, a new room, or external media. It turns the
existing production-map ReturnRoute beat into a short camera/proof pass so PRs
can validate motion readability without rendering a full trailer.
"""

from __future__ import annotations

import math

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"
CINEMATICS_DIR = "/Game/Hotel/Cinematics"
SEQUENCE_NAME = "LS_ReturnRoute_TrailerBeat_15s"
MRQ_CONFIG_NAME = "MRQ_ReturnRouteTrailerProofPng"
SEQUENCE_PATH = f"{CINEMATICS_DIR}/{SEQUENCE_NAME}"
MRQ_CONFIG_PATH = f"{CINEMATICS_DIR}/{MRQ_CONFIG_NAME}"
PUBLIC_SEQUENCE_AUTHOR = "Hotel Night Shift Horror Project"
FPS = 24
SECONDS = 15
END_FRAME = FPS * SECONDS


RETURN_ROUTE_ACTOR_KEYS = {
    "RETURN_Route_RightWall_BackKnockShadow_Echo": [
        (0, (3292, 276, 144), (0, 0, 0), (1.04, 1.0, 0.78)),
        (72, (3292, 276, 144), (0, 0, 0), (1.04, 1.0, 0.78)),
        (112, (3248, 276, 155), (0, -2, 0), (1.20, 1.0, 0.88)),
        (170, (3195, 276, 136), (0, 3, 0), (0.86, 1.0, 0.60)),
        (END_FRAME, (3195, 276, 136), (0, 3, 0), (0.86, 1.0, 0.60)),
    ],
    "RETURN_Route_RightWall_PalmDragShadow_BackKnock": [
        (0, (3100, 277, 160), (0, 0, 0), (0.46, 1.0, 0.46)),
        (96, (3100, 277, 160), (0, 0, 0), (0.46, 1.0, 0.46)),
        (150, (3068, 277, 128), (0, -5, 0), (0.76, 1.0, 0.76)),
        (220, (3038, 277, 112), (0, -7, 0), (0.54, 1.0, 0.58)),
        (END_FRAME, (3038, 277, 112), (0, -7, 0), (0.54, 1.0, 0.58)),
    ],
    "RETURN_Route_WallStatusSlip_ReportAfterHall": [
        (0, (3136, 268, 132), (0, 0, 0), (0.62, 1.0, 0.66)),
        (116, (3136, 268, 132), (0, 0, 0), (0.62, 1.0, 0.66)),
        (148, (3128, 262, 138), (0, -4, 0), (0.76, 1.0, 0.78)),
        (190, (3142, 265, 126), (0, 3, 0), (0.66, 1.0, 0.68)),
        (END_FRAME, (3142, 265, 126), (0, 3, 0), (0.66, 1.0, 0.68)),
    ],
    "RETURN_Route_WallStatusSlip_FranticWriting": [
        (0, (3135, 260, 132), (0, 0, 0), (0.10, 1.0, 0.12)),
        (126, (3135, 260, 132), (0, 0, 0), (0.10, 1.0, 0.12)),
        (154, (3135, 260, 132), (0, 0, 0), (0.54, 1.0, 0.50)),
        (190, (3135, 260, 132), (0, 0, 0), (0.78, 1.0, 0.76)),
        (END_FRAME, (3135, 260, 132), (0, 0, 0), (0.78, 1.0, 0.76)),
    ],
    "RETURN_Route_Floor_AuthoredBackstepSmear_Foreground": [
        (0, (2885, -38, 3), (0, 0, 0), (1.0, 1.0, 1.0)),
        (64, (2885, -38, 3), (0, 0, 0), (1.0, 1.0, 1.0)),
        (108, (2868, -74, 6), (0, -4, 0), (1.08, 1.08, 1.0)),
        (158, (2842, -102, 4), (0, -7, 0), (0.92, 0.92, 1.0)),
        (END_FRAME, (2842, -102, 4), (0, -7, 0), (0.92, 0.92, 1.0)),
    ],
}

RETURN_ROUTE_SCALE_REVEALS = {
    "RETURN_Route_BackKnockDirectionStripe": [
        (0, 0.20),
        (84, 0.20),
        (126, 0.95),
        (190, 0.68),
        (END_FRAME, 0.68),
    ],
    "RETURN_Route_BackKnockDirectionStripe_Return": [
        (0, 0.15),
        (118, 0.15),
        (168, 0.92),
        (230, 0.64),
        (END_FRAME, 0.64),
    ],
    "RETURN_Route_WallStatusSlip_Underline": [
        (0, 0.10),
        (138, 0.10),
        (176, 1.04),
        (228, 0.78),
        (END_FRAME, 0.78),
    ],
    "RETURN_Route_FootprintBacktrackA": [
        (0, 0.18),
        (120, 0.18),
        (152, 0.82),
        (END_FRAME, 0.72),
    ],
    "RETURN_Route_FootprintBacktrackB": [
        (0, 0.12),
        (152, 0.12),
        (190, 0.78),
        (END_FRAME, 0.68),
    ],
    "RETURN_Route_FootprintBacktrackC": [
        (0, 0.08),
        (184, 0.08),
        (226, 0.72),
        (END_FRAME, 0.62),
    ],
}

CONTEXT_DEEMPHASIS_ACTORS = {
    "PROP_GuestHall_RightWall_AuthoredDampUnderPeel_Room203Approach": 0.36,
    "PROP_GuestHall_RightWall_AuthoredPeelingWallpaper_CameraReadable": 0.28,
    "PROP_GuestHall_RightWall_AuthoredPeelingWallpaper_Room203": 0.28,
    "PROP_GuestHall_RightWall_Room203AftershockLoosePaper": 0.28,
    "PROP_GuestHall_RightWall_Room203AftershockHighCurl": 0.34,
    "PROP_GuestHall_RightWall_Room203AftershockLowCurl": 0.34,
    "PROP_GuestHall_RightWall_Room203AftershockInteriorCuts": 0.52,
}

CAMERA_KEYS = [
    (0, (2890, -250, 165), (0.5, 57.0, 0.0), 58.0),
    (54, (2840, -250, 164), (0.5, 55.0, 0.0), 57.0),
    (104, (2788, -250, 163), (0.5, 52.0, 0.0), 56.0),
    (150, (2740, -248, 162), (0.5, 49.0, 0.0), 55.0),
    (218, (2705, -248, 160), (0.5, 46.0, 0.0), 54.0),
    (END_FRAME, (2668, -248, 158), (0.5, 43.0, 0.0), 52.0),
]


def log(message: str) -> None:
    unreal.log(f"[ReturnRouteTrailerBeatAssets] {message}")


def fail(message: str) -> None:
    raise RuntimeError(f"[ReturnRouteTrailerBeatAssets] {message}")


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
        "Generated by Automation/Unreal/create_return_route_trailer_beat_assets.py for internal ReturnRoute trailer proof.",
    )


def add_spawnable_trailer_camera(sequence: unreal.LevelSequence):
    first_location, first_rotation, first_fov = CAMERA_KEYS[0][1], CAMERA_KEYS[0][2], CAMERA_KEYS[0][3]
    temp_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CineCameraActor,
        unreal.Vector(*first_location),
        make_rotator(*first_rotation),
    )
    temp_camera.set_actor_label("TMP_ReturnRouteTrailerBeatCamera")
    try:
        cine_component = temp_camera.get_cine_camera_component()
        try_set_property(cine_component, "current_focal_length", focal_length_from_fov_degrees(first_fov))
        try_set_property(cine_component, "current_aperture", 8.0)
    except Exception:
        pass

    binding = sequence.add_spawnable_from_instance(temp_camera)
    binding.set_display_name("CAM_ReturnRoute_TrailerBeat_15s")

    transform_track = binding.add_track(unreal.MovieScene3DTransformTrack)
    transform_section = transform_track.add_section()
    transform_section.set_start_frame(0)
    transform_section.set_end_frame(END_FRAME)
    for frame, location, rotation, _fov in CAMERA_KEYS:
        add_transform_key(transform_section, frame, location, rotation, (1.0, 1.0, 1.0))

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


def add_actor_motion_track(sequence: unreal.LevelSequence, label: str, keys) -> None:
    actor = find_actor_by_label(label)
    if actor is None:
        fail(f"Missing ReturnRoute trailer actor: {label}")

    binding = sequence.add_possessable(actor)
    binding.set_display_name(label)
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_start_frame(0)
    section.set_end_frame(END_FRAME)
    for frame, location, rotation, scale in keys:
        add_transform_key(section, frame, location, rotation, scale)


def actor_transform_tuple(actor):
    location = actor.get_actor_location()
    rotation = actor.get_actor_rotation()
    scale = actor.get_actor_scale3d()
    return (
        (location.x, location.y, location.z),
        (rotation.pitch, rotation.yaw, rotation.roll),
        (scale.x, scale.y, scale.z),
    )


def add_actor_scale_multiplier_track(sequence: unreal.LevelSequence, label: str, keys) -> None:
    actor = find_actor_by_label(label)
    if actor is None:
        fail(f"Missing ReturnRoute trailer context actor: {label}")

    location, rotation, base_scale = actor_transform_tuple(actor)
    binding = sequence.add_possessable(actor)
    binding.set_display_name(label)
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_start_frame(0)
    section.set_end_frame(END_FRAME)
    for frame, multiplier in keys:
        scaled = (
            base_scale[0] * float(multiplier),
            base_scale[1] * float(multiplier),
            base_scale[2] * float(multiplier),
        )
        add_transform_key(section, frame, location, rotation, scaled)


def add_context_deemphasis_track(sequence: unreal.LevelSequence, label: str, multiplier: float) -> None:
    add_actor_scale_multiplier_track(sequence, label, [(0, multiplier), (END_FRAME, multiplier)])


def create_sequence() -> unreal.LevelSequence:
    delete_existing_asset(SEQUENCE_PATH)
    sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        SEQUENCE_NAME,
        CINEMATICS_DIR,
        unreal.LevelSequence,
        unreal.LevelSequenceFactoryNew(),
    )
    if not sequence:
        fail("Unable to create ReturnRoute trailer LevelSequence.")

    try:
        sequence.set_display_rate(unreal.FrameRate(FPS, 1))
        sequence.set_tick_resolution(unreal.FrameRate(FPS, 1))
    except Exception:
        pass
    sequence.set_playback_start(0)
    sequence.set_playback_end(END_FRAME)

    camera_binding = add_spawnable_trailer_camera(sequence)
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

    for label, keys in RETURN_ROUTE_ACTOR_KEYS.items():
        add_actor_motion_track(sequence, label, keys)
    for label, keys in RETURN_ROUTE_SCALE_REVEALS.items():
        add_actor_scale_multiplier_track(sequence, label, keys)
    for label, multiplier in CONTEXT_DEEMPHASIS_ACTORS.items():
        add_context_deemphasis_track(sequence, label, multiplier)

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
        fail("Unable to create ReturnRoute trailer MRQ config.")

    output = config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output.output_resolution = unreal.IntPoint(1280, 720)
    output.file_name_format = "return_route_trailer_proof_{frame_number}"
    output.output_directory.path = "{project_dir}/Saved/MovieRenders/ReturnRouteTrailerBeat"
    output.override_existing_output = True
    output.zero_pad_frame_numbers = 4
    output.flush_disk_writes_per_shot = True
    output.output_frame_step = 12

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
    create_sequence()
    create_mrq_config()
    log(f"Created {SEQUENCE_PATH} and {MRQ_CONFIG_PATH}.")


main()
