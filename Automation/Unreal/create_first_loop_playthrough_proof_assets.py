"""Create a 24-second first-loop first-person-height proof sequence.

This is an internal capture/proof lane for the production hotel map. It does
not add a gameplay feature, new room, test map, or public trailer approval; it
lets PRs prove that the existing first work loop can be judged as a connected
cinematic route instead of isolated unit checks or disconnected stills.
"""

from __future__ import annotations

import math

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"
CINEMATICS_DIR = "/Game/Hotel/Cinematics"
SEQUENCE_NAME = "LS_FirstLoop_PlaythroughProof_24s"
MRQ_CONFIG_NAME = "MRQ_FirstLoopPlaythroughProofPng"
SEQUENCE_PATH = f"{CINEMATICS_DIR}/{SEQUENCE_NAME}"
MRQ_CONFIG_PATH = f"{CINEMATICS_DIR}/{MRQ_CONFIG_NAME}"
PUBLIC_SEQUENCE_AUTHOR = "Hotel Night Shift Horror Project"
FPS = 24
SECONDS = 24
END_FRAME = FPS * SECONDS

POV_CAMERA_KEYS = [
    (0, (-505.0, -704.0, 178.0), (0.5, 128.0, 0.0), 58.0),
    (24, (-505.0, -700.0, 178.0), (0.4, 128.1, -0.1), 55.0),
    (48, (-503.0, -696.0, 179.0), (0.2, 128.3, 0.1), 52.0),
    (72, (-500.0, -692.0, 179.0), (0.2, 128.5, -0.1), 49.0),
    (96, (-497.0, -688.0, 179.0), (0.1, 128.7, 0.0), 47.0),
    (120, (-494.0, -684.0, 179.0), (0.1, 128.9, 0.0), 45.0),
    (144, (-210.0, -620.0, 165.5), (-2.0, 24.0, 0.4), 70.0),
    (168, (430.0, -320.0, 164.5), (-1.0, 38.0, -0.8), 74.0),
    (196, (780.0, -430.0, 165.2), (-8.0, 58.0, 0.7), 70.0),
    (216, (790.0, -410.0, 166.0), (-12.0, 58.0, -0.2), 66.0),
    (228, (820.0, -360.0, 166.0), (-12.0, 55.0, 0.2), 66.0),
    (240, (2668.0, -248.0, 158.0), (0.5, 43.0, 0.0), 54.0),
    (252, (3185.0, -205.0, 164.0), (1.5, 30.0, 0.0), 52.0),
    (264, (3222.0, -214.0, 165.0), (1.3, 29.2, 0.0), 47.0),
    (276, (3227.0, -219.0, 166.0), (0.9, 28.8, 0.2), 44.0),
    (288, (3223.0, -216.0, 165.0), (1.2, 29.4, -0.1), 46.0),
    (304, (3234.0, -225.0, 166.0), (0.9, 28.6, 0.0), 44.0),
    (316, (3242.0, -230.0, 167.0), (0.7, 28.4, 0.0), 44.0),
    (324, (2668.0, -248.0, 158.0), (0.5, 43.0, 0.0), 52.0),
    (336, (2788.0, -238.0, 158.0), (0.3, 43.0, -0.2), 52.0),
    (348, (2920.0, -228.0, 158.0), (0.2, 43.5, 0.2), 52.0),
    (360, (3060.0, -218.0, 158.0), (0.2, 43.8, -0.1), 52.0),
    (372, (3180.0, -210.0, 158.0), (0.2, 44.0, 0.0), 52.0),
    (384, (-62.0, -728.0, 184.0), (-11.0, 132.0, 0.0), 48.0),
    (396, (-61.0, -728.0, 184.0), (-11.2, 132.1, 0.0), 47.5),
    (408, (-59.0, -727.0, 183.0), (-11.4, 132.3, 0.0), 47.0),
    (420, (-62.0, -728.0, 184.0), (-11.0, 132.0, 0.0), 48.0),
    (432, (-61.0, -728.0, 184.0), (-11.2, 132.1, 0.0), 47.5),
    (444, (-61.0, -728.0, 184.0), (-11.2, 132.1, 0.0), 47.5),
    (456, (-497.0, -688.0, 179.0), (0.1, 128.7, 0.0), 47.0),
    (480, (-674.0, -650.0, 166.2), (1.0, 31.0, 0.6), 69.0),
    (512, (-58.0, -726.0, 183.0), (-11.5, 132.5, 0.0), 46.8),
    (528, (-58.0, -726.0, 183.0), (-11.5, 132.5, 0.0), 46.8),
    (548, (-57.0, -726.0, 183.0), (-11.4, 132.5, 0.0), 46.8),
    (END_FRAME, (-57.0, -726.0, 183.0), (-11.4, 132.5, 0.0), 46.8),
]

POV_EXPOSURE_BIAS = 3.2

ACTOR_JOLTS = {
    "PROP_FrontDesk_Phone_ReceiverAuthoredSilhouette": (52, (26.0, -10.0, 18.0), (-8.0, 3.0, -12.0), 1.0),
    "PROP_FrontDesk_Phone_AuthoredCoiledCord": (58, (5.0, -4.0, 5.0), (0.0, 0.0, -3.0), 1.01),
    "PROP_Surveillance_Monitor_CheckScanlineSweepA": (104, (0.0, 0.0, -26.0), (0.0, 0.0, 0.0), 1.08),
    "PROP_Surveillance_Monitor_CheckScanlineSweepB": (112, (0.0, 0.0, 22.0), (0.0, 0.0, 0.0), 1.06),
    "PROP_Surveillance_Monitor_CheckRoom203TargetBox": (116, (-10.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1.12),
    "PROP_Surveillance_Monitor_CheckNoGuestUnderline": (120, (8.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1.08),
    "PROP_GuestHall_Room203_NumberDigits_Authored": (270, (0.0, -6.8, 3.0), (0.8, 0.0, -5.0), 1.02),
    "PROP_GuestHall_Room203_DoNotOpenNotice": (276, (0.0, -7.2, 3.4), (1.0, 0.0, 5.6), 1.03),
    "LIGHTMESH_GuestHall_Room203DoorPractical": (282, (0.0, -4.2, 2.8), (0.0, 0.0, 3.8), 1.12),
    "PROP_GuestHall_RightWall_Room203AftershockLoosePaper": (298, (0.0, -8.0, 7.0), (4.0, 0.0, 6.0), 1.04),
    "RETURN_Route_RightWall_BackKnockShadow_Echo": (338, (-40.0, 0.0, 8.0), (0.0, -2.0, 0.0), 1.15),
    "RETURN_Route_RightWall_PalmDragShadow_BackKnock": (356, (-32.0, 0.0, -30.0), (0.0, -5.0, 0.0), 1.20),
    "RETURN_Route_WallStatusSlip_ReportAfterHall": (376, (-6.0, -4.0, 3.0), (0.0, -2.0, 0.0), 1.16),
    "PROP_FrontDesk_ReportLog_FiledStampCue": (410, (0.0, -8.0, 10.0), (0.0, 0.0, -8.0), 1.05),
    "PROP_Surveillance_Monitor_PostReportStaticBarA": (468, (0.0, 0.0, 18.0), (0.0, 0.0, 0.0), 1.12),
    "PROP_Surveillance_Monitor_PostReportOpenDoorGlyph": (474, (-8.0, 0.0, 0.0), (0.0, 0.0, 0.0), 1.14),
    "PROP_FrontDesk_ReportLog_SelfCorrectedRoom203OpenLine": (532, (0.0, -6.0, 4.0), (0.0, 0.0, 0.0), 1.10),
    "PROP_FrontDesk_ReportLog_SelfCorrectedNoGuestLine": (540, (0.0, -5.0, 4.0), (0.0, 0.0, 0.0), 1.08),
    "PROP_FrontDesk_ReportLog_SelfCorrectedTimestampSlash": (548, (0.0, -4.0, 3.0), (0.0, 0.0, -5.0), 1.08),
}

REPORT_TEXT_CUES = [
    (
        384,
        448,
        "TXT_FirstLoop_ReportFiled_ReadableCue",
        "NIGHT LOG\nROOM 203 REFUSED\nSTAMP: FILED",
        (-150.0, -548.0, 182.0),
        (0.0, -90.0, 0.0),
        3.4,
        (180, 140, 70, 255),
    ),
    (
        512,
        END_FRAME,
        "TXT_FirstLoop_PostReportSelfCorrection_ReadableCue",
        "LOG CHANGED\n203 OPEN\nNO GUEST FOUND",
        (-150.0, -548.0, 184.0),
        (0.0, -90.0, 0.0),
        3.3,
        (160, 210, 120, 255),
    ),
]


def log(message: str) -> None:
    unreal.log(f"[FirstLoopPlaythroughProofAssets] {message}")


def fail(message: str) -> None:
    raise RuntimeError(f"[FirstLoopPlaythroughProofAssets] {message}")


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


def add_tuple(a, b) -> tuple[float, float, float]:
    return tuple(float(a[index]) + float(b[index]) for index in range(3))


def multiply_tuple(values, multiplier: float) -> tuple[float, float, float]:
    return tuple(float(value) * float(multiplier) for value in values)


def get_text_render_component(actor):
    for getter_name in ("get_text_render", "get_text_render_component"):
        getter = getattr(actor, getter_name, None)
        if getter:
            try:
                return getter()
            except Exception:
                pass

    try:
        return actor.get_component_by_class(unreal.TextRenderComponent)
    except Exception:
        return None


def set_text_render_text(component, text: str) -> None:
    for method_name in ("set_text", "k2_set_text"):
        method = getattr(component, method_name, None)
        if not method:
            continue
        try:
            method(text)
            return
        except Exception:
            pass

    try_set_property(component, "text", text)


def configure_text_render_component(component, text: str, world_size: float, color) -> None:
    set_text_render_text(component, text)

    for method_name, value in (
        ("set_world_size", world_size),
        ("set_x_scale", 0.86),
        ("set_y_scale", 0.86),
        ("set_horiz_spacing_adjust", 1.0),
        ("set_vert_spacing_adjust", -0.5),
    ):
        method = getattr(component, method_name, None)
        if method:
            try:
                method(value)
            except Exception:
                pass

    try_set_property(component, "world_size", world_size)
    try_set_property(component, "x_scale", 0.86)
    try_set_property(component, "y_scale", 0.86)
    try_set_property(component, "horiz_spacing_adjust", 1.0)
    try_set_property(component, "vert_spacing_adjust", -0.5)
    try_set_property(component, "b_always_render_as_text", True)

    text_color = unreal.Color(*color)
    color_method = getattr(component, "set_text_render_color", None)
    if color_method:
        try:
            color_method(text_color)
        except Exception:
            pass
    try_set_property(component, "text_render_color", text_color)


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
        "Generated by Automation/Unreal/create_first_loop_playthrough_proof_assets.py for internal first-loop production-map proof.",
    )


def add_first_person_height_route_camera(sequence: unreal.LevelSequence) -> object:
    start_frame, location, rotation, fov = POV_CAMERA_KEYS[0]
    if start_frame != 0:
        fail("First-person-height route camera must start at frame 0.")

    temp_camera = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CineCameraActor,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    temp_camera.set_actor_label("TMP_FirstLoopFirstPersonHeight_ContinuousRoute")
    try:
        cine_component = temp_camera.get_cine_camera_component()
        try_set_property(cine_component, "current_focal_length", focal_length_from_fov_degrees(fov))
        try_set_property(cine_component, "current_aperture", 8.0)
        try_set_property(cine_component, "post_process_blend_weight", 1.0)
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
                "auto_exposure_bias": POV_EXPOSURE_BIAS,
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
    binding.set_display_name("CAM_FirstLoop_FirstPersonHeight_ContinuousRoute")

    transform_track = binding.add_track(unreal.MovieScene3DTransformTrack)
    transform_section = transform_track.add_section()
    transform_section.set_start_frame(0)
    transform_section.set_end_frame(END_FRAME)
    for frame, key_location, key_rotation, key_fov in POV_CAMERA_KEYS:
        add_transform_key(transform_section, frame, key_location, key_rotation, (1.0, 1.0, 1.0))

    try:
        cine_component = temp_camera.get_cine_camera_component()
        component_binding = sequence.add_possessable(cine_component)
        component_binding.set_parent(binding)
        focal_length_track = component_binding.add_track(unreal.MovieSceneFloatTrack)
        focal_length_track.set_property_name_and_path("CurrentFocalLength", "CurrentFocalLength")
        focal_length_section = focal_length_track.add_section()
        focal_length_section.set_start_frame(0)
        focal_length_section.set_end_frame(END_FRAME)
        for frame, key_location, key_rotation, key_fov in POV_CAMERA_KEYS:
            add_camera_focal_key(focal_length_section, frame, key_fov)
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


def add_actor_jolt_track(sequence: unreal.LevelSequence, label: str, jolt) -> None:
    actor = find_actor_by_label(label)
    if actor is None:
        fail(f"Missing playthrough proof actor: {label}")

    start_frame, offset, rotation_delta, scale_multiplier = jolt
    location, rotation, scale = actor_transform_tuple(actor)
    peak_location = add_tuple(location, offset)
    settle_location = add_tuple(location, multiply_tuple(offset, -0.22))
    second_location = add_tuple(location, multiply_tuple(offset, 0.38))
    peak_rotation = add_tuple(rotation, rotation_delta)
    settle_rotation = add_tuple(rotation, multiply_tuple(rotation_delta, -0.28))
    second_rotation = add_tuple(rotation, multiply_tuple(rotation_delta, 0.35))
    peak_scale = multiply_tuple(scale, scale_multiplier)

    keys = [
        (0, location, rotation, scale),
        (max(0, start_frame - 4), location, rotation, scale),
        (start_frame + 5, peak_location, peak_rotation, peak_scale),
        (start_frame + 16, settle_location, settle_rotation, scale),
        (start_frame + 28, second_location, second_rotation, multiply_tuple(scale, 1.0 + (scale_multiplier - 1.0) * 0.35)),
        (start_frame + 42, location, rotation, scale),
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


def add_text_cue_track(sequence: unreal.LevelSequence, cue) -> None:
    start_frame, end_frame, label, text, location, rotation, world_size, color = cue
    hidden_location = (location[0], location[1], -1200.0)
    peak_location = (location[0], location[1] - 2.0, location[2] + 2.0)
    settle_location = (location[0], location[1], location[2])

    temp_text = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.TextRenderActor,
        unreal.Vector(*hidden_location),
        make_rotator(*rotation),
    )
    temp_text.set_actor_label(label)
    component = get_text_render_component(temp_text)
    if component is None:
        unreal.EditorLevelLibrary.destroy_actor(temp_text)
        fail(f"Unable to configure text cue actor: {label}")
    configure_text_render_component(component, text, world_size, color)

    binding = sequence.add_spawnable_from_instance(temp_text)
    binding.set_display_name(label)
    track = binding.add_track(unreal.MovieScene3DTransformTrack)
    section = track.add_section()
    section.set_start_frame(0)
    section.set_end_frame(END_FRAME)
    for frame, key_location, key_scale in (
        (0, hidden_location, (0.01, 0.01, 0.01)),
        (max(0, start_frame - 5), hidden_location, (0.01, 0.01, 0.01)),
        (start_frame + 4, peak_location, (1.04, 1.04, 1.04)),
        (start_frame + 16, settle_location, (1.0, 1.0, 1.0)),
        (max(start_frame + 16, end_frame - 2), settle_location, (1.0, 1.0, 1.0)),
        (min(END_FRAME, end_frame + 1), hidden_location, (0.01, 0.01, 0.01)),
        (END_FRAME, hidden_location, (0.01, 0.01, 0.01)),
    ):
        add_transform_key(section, frame, key_location, rotation, key_scale)

    unreal.EditorLevelLibrary.destroy_actor(temp_text)


def create_sequence() -> unreal.LevelSequence:
    delete_existing_asset(SEQUENCE_PATH)
    sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        SEQUENCE_NAME,
        CINEMATICS_DIR,
        unreal.LevelSequence,
        unreal.LevelSequenceFactoryNew(),
    )
    if not sequence:
        fail("Unable to create first-loop playthrough proof LevelSequence.")

    try:
        sequence.set_display_rate(unreal.FrameRate(FPS, 1))
        sequence.set_tick_resolution(unreal.FrameRate(FPS, 1))
    except Exception:
        pass
    sequence.set_playback_start(0)
    sequence.set_playback_end(END_FRAME)

    camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)
    if not camera_cut_track:
        fail("Unable to create camera cut track.")

    binding = add_first_person_height_route_camera(sequence)
    cut = camera_cut_track.add_section()
    cut.set_start_frame(0)
    cut.set_end_frame(END_FRAME)
    try:
        cut.set_camera_binding_id(sequence.get_binding_id(binding))
    except Exception:
        cut.set_editor_property("CameraBindingID", camera_binding_id(binding))

    for label, jolt in ACTOR_JOLTS.items():
        add_actor_jolt_track(sequence, label, jolt)

    for cue in REPORT_TEXT_CUES:
        add_text_cue_track(sequence, cue)

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
        fail("Unable to create first-loop playthrough proof MRQ config.")

    output = config.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    output.output_resolution = unreal.IntPoint(1280, 720)
    output.file_name_format = "first_loop_playthrough_proof_{frame_number}"
    output.output_directory.path = "{project_dir}/Saved/MovieRenders/FirstLoopPlaythrough"
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
    console_variables.add_or_update_console_variable("r.DefaultFeature.MotionBlur", 0.0)
    console_variables.add_or_update_console_variable("r.MotionBlur.Amount", 0.0)

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
