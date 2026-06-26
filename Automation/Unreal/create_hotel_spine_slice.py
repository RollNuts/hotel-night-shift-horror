"""Create the first production-intent hotel spine level.

This script uses only project-authored/generated assets and Unreal Engine
stock primitives. It is intentionally a production-context slice, not a
small-room test map.
"""

from __future__ import annotations

import math
import pathlib
import struct
import wave

import unreal


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE_AUDIO_DIR = PROJECT_ROOT / "SourceAssets" / "AudioGenerated"
MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"


def log(message: str) -> None:
    unreal.log(f"[HotelSpineSlice] {message}")


def ensure_dirs() -> None:
    for path in [
        "/Game/Hotel",
        "/Game/Hotel/Maps",
        "/Game/Hotel/Materials",
        "/Game/Hotel/Audio",
        "/Game/Hotel/Blueprints",
        "/Game/Hotel/Data",
        "/Game/Hotel/UI",
        "/Game/Hotel/VFX",
    ]:
        unreal.EditorAssetLibrary.make_directory(path)
    SOURCE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def write_wav(path: pathlib.Path, seconds: float, sample_func, sample_rate: int = 44100) -> None:
    frame_count = int(seconds * sample_rate)
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for index in range(frame_count):
            t = index / sample_rate
            value = max(-1.0, min(1.0, sample_func(t)))
            wav.writeframesraw(struct.pack("<h", int(value * 32767)))


def generate_source_audio() -> dict[str, pathlib.Path]:
    def phone_ring(t: float) -> float:
        cycle = t % 1.25
        active = cycle < 0.38 or 0.55 < cycle < 0.93
        if not active:
            return 0.0
        env = 0.65
        return env * (math.sin(2 * math.pi * 440 * t) + 0.45 * math.sin(2 * math.pi * 480 * t)) * 0.45

    def lobby_hum(t: float) -> float:
        slow = math.sin(2 * math.pi * 0.17 * t) * 0.08
        return 0.18 * math.sin(2 * math.pi * 60 * t) + 0.06 * math.sin(2 * math.pi * 120 * t) + slow

    def hallway_drone(t: float) -> float:
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 0.11 * t)
        return 0.16 * math.sin(2 * math.pi * 82 * t) + 0.035 * pulse * math.sin(2 * math.pi * 610 * t)

    def door_knock(t: float) -> float:
        total = 0.0
        for start in (0.18, 0.42, 0.91):
            dt = t - start
            if 0.0 <= dt <= 0.16:
                total += math.exp(-dt * 28.0) * (math.sin(2 * math.pi * 135 * dt) + 0.35 * math.sin(2 * math.pi * 260 * dt))
        return 0.55 * total

    sources = {
        "SFX_PhoneRing_v0": (2.5, phone_ring),
        "AMB_LobbyFluorescentHum_v0": (6.0, lobby_hum),
        "AMB_GuestHallDrone_v0": (6.0, hallway_drone),
        "SFX_DoorKnock203_v0": (1.4, door_knock),
    }

    output: dict[str, pathlib.Path] = {}
    for name, (seconds, sample_func) in sources.items():
        path = SOURCE_AUDIO_DIR / f"{name}.wav"
        write_wav(path, seconds, sample_func)
        output[name] = path
    return output


def import_audio(source_paths: dict[str, pathlib.Path]) -> dict[str, unreal.SoundWave]:
    tasks = []
    sounds: dict[str, unreal.SoundWave] = {}
    for name, path in source_paths.items():
        existing_asset = unreal.EditorAssetLibrary.load_asset(f"/Game/Hotel/Audio/{name}")
        if existing_asset:
            sounds[name] = existing_asset
            continue
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(path))
        task.set_editor_property("destination_path", "/Game/Hotel/Audio")
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        tasks.append(task)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    for name in source_paths:
        if name in sounds:
            continue
        asset = unreal.EditorAssetLibrary.load_asset(f"/Game/Hotel/Audio/{name}")
        if asset:
            sounds[name] = asset
    return sounds


def ensure_material(
    name: str,
    color: unreal.LinearColor,
    roughness: float,
    emissive: unreal.LinearColor | None = None,
) -> unreal.MaterialInterface:
    path = f"/Game/Hotel/Materials/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.EditorAssetLibrary.load_asset(path)

    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name,
        "/Game/Hotel/Materials",
        unreal.Material,
        unreal.MaterialFactoryNew(),
    )

    base = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant3Vector, -360, -120
    )
    base.set_editor_property("constant", color)
    unreal.MaterialEditingLibrary.connect_material_property(base, "", unreal.MaterialProperty.MP_BASE_COLOR)

    rough = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant, -360, 80
    )
    rough.set_editor_property("r", roughness)
    unreal.MaterialEditingLibrary.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)

    if emissive:
        glow = unreal.MaterialEditingLibrary.create_material_expression(
            material, unreal.MaterialExpressionConstant3Vector, -360, 260
        )
        glow.set_editor_property("constant", emissive)
        unreal.MaterialEditingLibrary.connect_material_property(glow, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)

    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_asset(path)
    return material


def prepare_level() -> None:
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorLevelLibrary.load_level(MAP_PATH)
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not isinstance(actor, unreal.WorldSettings):
                unreal.EditorLevelLibrary.destroy_actor(actor)
    else:
        unreal.EditorLevelLibrary.new_level(MAP_PATH)


def tag_actor(actor: unreal.Actor, *tags: str) -> None:
    if not tags:
        return
    actor.tags = [unreal.Name(tag) for tag in tags]


def try_set_property(obj, name: str, value) -> None:
    try:
        obj.set_editor_property(name, value)
    except Exception:
        pass


def add_cube(label: str, location, size, material: unreal.MaterialInterface, tags=()) -> unreal.Actor:
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    component = actor.static_mesh_component
    component.set_static_mesh(cube)
    component.set_material(0, material)
    component.set_editor_property("mobility", unreal.ComponentMobility.STATIC)
    tag_actor(actor, *tags)
    return actor


def add_light(
    label: str,
    cls,
    location,
    rotation,
    intensity: float,
    color: unreal.Color,
    tags=(),
    attenuation_radius: float = 1400.0,
    source_width: float | None = None,
    source_height: float | None = None,
):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        cls,
        unreal.Vector(*location),
        unreal.Rotator(*rotation),
    )
    actor.set_actor_label(label)
    component_name = "light_component"
    if hasattr(actor, "rect_light_component"):
        component_name = "rect_light_component"
    component = actor.get_editor_property(component_name)
    component.set_editor_property("intensity", intensity)
    component.set_editor_property("light_color", color)
    try_set_property(component, "mobility", unreal.ComponentMobility.MOVABLE)
    try_set_property(component, "attenuation_radius", attenuation_radius)
    if source_width is not None:
        try_set_property(component, "source_width", source_width)
    if source_height is not None:
        try_set_property(component, "source_height", source_height)
    tag_actor(actor, *tags)
    return actor


def add_camera(label: str, location, rotation, fov: float = 62.0) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(*location),
        unreal.Rotator(*rotation),
    )
    actor.set_actor_label(label)
    try:
        component = actor.get_editor_property("camera_component")
        component.set_editor_property("field_of_view", fov)
    except Exception:
        pass
    return actor


def add_audio(label: str, sound: unreal.SoundWave, location, auto_activate: bool, tags=()) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.AmbientSound,
        unreal.Vector(*location),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    component = actor.get_editor_property("audio_component")
    component.set_editor_property("sound", sound)
    component.set_editor_property("auto_activate", auto_activate)
    tag_actor(actor, *tags)
    return actor


def add_post_process_volume(label: str) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PostProcessVolume,
        unreal.Vector(2100, 0, 120),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    try_set_property(actor, "b_unbound", True)
    try_set_property(actor, "unbound", True)
    try_set_property(actor, "priority", 10.0)

    try:
        settings = actor.get_editor_property("settings")
    except Exception:
        settings = None
    if settings:
        exposure_overrides = {
            "override_auto_exposure_method": True,
            "override_auto_exposure_min_brightness": True,
            "override_auto_exposure_max_brightness": True,
            "override_auto_exposure_bias": True,
            "auto_exposure_min_brightness": 1.0,
            "auto_exposure_max_brightness": 1.0,
            "auto_exposure_bias": 1.2,
        }
        for name, value in exposure_overrides.items():
            try_set_property(settings, name, value)
        try:
            settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
        except Exception:
            pass
        try_set_property(actor, "settings", settings)

    tag_actor(actor, "Hotel.Capture.Readability")
    return actor


def build_level(sounds: dict[str, unreal.SoundWave]) -> None:
    prepare_level()

    materials = {
        "floor": ensure_material("M_Hotel_WornFloor_v0", unreal.LinearColor(0.15, 0.13, 0.11, 1.0), 0.92),
        "wall": ensure_material("M_Hotel_AgedWall_v0", unreal.LinearColor(0.42, 0.38, 0.31, 1.0), 0.86),
        "trim": ensure_material("M_Hotel_DarkTrim_v0", unreal.LinearColor(0.09, 0.08, 0.075, 1.0), 0.74),
        "desk": ensure_material("M_Hotel_FrontDeskWood_v0", unreal.LinearColor(0.19, 0.11, 0.065, 1.0), 0.68),
        "black": ensure_material("M_Hotel_BlackPlastic_v0", unreal.LinearColor(0.01, 0.012, 0.014, 1.0), 0.55),
        "screen": ensure_material("M_Hotel_MonitorGreen_v0", unreal.LinearColor(0.02, 0.18, 0.11, 1.0), 0.35),
        "door": ensure_material("M_Hotel_RoomDoorPaint_v0", unreal.LinearColor(0.23, 0.18, 0.13, 1.0), 0.77),
        "warn": ensure_material("M_Hotel_ServiceAmber_v0", unreal.LinearColor(0.75, 0.43, 0.12, 1.0), 0.63),
        "screen_glow": ensure_material(
            "M_Hotel_MonitorGreenGlow_v0",
            unreal.LinearColor(0.02, 0.22, 0.13, 1.0),
            0.28,
            unreal.LinearColor(0.0, 0.55, 0.28, 1.0),
        ),
        "warn_glow": ensure_material(
            "M_Hotel_ServiceAmberGlow_v0",
            unreal.LinearColor(0.85, 0.48, 0.14, 1.0),
            0.48,
            unreal.LinearColor(1.4, 0.62, 0.18, 1.0),
        ),
        "fluorescent_panel": ensure_material(
            "M_Hotel_FluorescentPanelGlow_v0",
            unreal.LinearColor(0.62, 0.72, 0.82, 1.0),
            0.22,
            unreal.LinearColor(1.45, 1.65, 1.95, 1.0),
        ),
        "desk_lamp": ensure_material(
            "M_Hotel_DeskLampGlow_v0",
            unreal.LinearColor(0.95, 0.72, 0.42, 1.0),
            0.35,
            unreal.LinearColor(1.9, 1.18, 0.48, 1.0),
        ),
    }

    # Front desk / lobby work hub.
    add_cube("AREA_FrontDesk_WorkHub_Floor", (0, 0, -10), (2500, 1600, 20), materials["floor"])
    add_cube("AREA_FrontDesk_BackWall_AgedBusinessHotel", (-900, 0, 140), (24, 1600, 280), materials["wall"])
    add_cube("AREA_FrontDesk_LeftWall_LobbyEdge", (0, -790, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_FrontDesk_RightWall_ServiceEdge", (0, 790, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_FrontDesk_Ceiling_LowPressure", (0, 0, 286), (2500, 1600, 20), materials["trim"])
    add_cube("PROP_FrontDesk_Counter_PlayerWorkSurface", (-430, -410, 55), (520, 120, 110), materials["desk"])
    add_cube("PROP_FrontDesk_BackShelf_KeyAndLogSilhouette", (-880, -400, 145), (30, 520, 170), materials["trim"])
    add_cube("PROP_FrontDesk_Phone_AnswerLoopPlaceholder", (-430, -525, 128), (58, 34, 22), materials["black"], ("Hotel.Interact.Phone",))
    add_cube("PROP_FrontDesk_Phone_ReceiverCue", (-430, -558, 150), (74, 14, 12), materials["black"])
    add_cube("PROP_Surveillance_Monitor_PlayerChecksHall", (-620, -525, 160), (130, 16, 72), materials["screen_glow"], ("Hotel.Interact.Monitor",))
    add_cube("PROP_ReportLog_ReturnAndRecordPoint", (-255, -522, 128), (96, 62, 10), materials["warn_glow"], ("Hotel.Interact.ReportLog",))
    add_cube("LIGHTMESH_FrontDesk_DeskLampPractical", (-320, -548, 176), (72, 18, 18), materials["desk_lamp"], ("Hotel.Capture.Readability",))
    add_cube("AREA_Lobby_GuestAdmissionThreshold", (780, 0, -8), (620, 1280, 16), materials["floor"])
    add_cube("PROP_Lobby_MainGlassDoor_Silhouette", (1080, -250, 110), (28, 270, 220), materials["screen_glow"])
    add_cube("PROP_Lobby_MainGlassDoor_RefuseLine", (1080, 250, 110), (28, 270, 220), materials["screen_glow"])

    # Controlled transition from work hub to guest-floor response.
    add_cube("TRANSITION_Elevator_Door_AudibleBeforeSeen", (1160, 565, 120), (34, 280, 240), materials["door"])
    add_cube("TRANSITION_Elevator_CallPanel_SoundCueAnchor", (1125, 385, 120), (12, 30, 80), materials["warn_glow"])
    add_cube("TRANSITION_EmergencyStair_Door_AlternateRoute", (1160, -565, 120), (34, 280, 240), materials["door"])
    add_cube("TRANSITION_ServiceBackHall_LockedShortcut", (430, 770, 110), (330, 26, 220), materials["trim"])

    # Guest hallway response line.
    add_cube("AREA_GuestHall_Floor_OneDoorSlice", (3250, 0, -10), (2500, 560, 20), materials["floor"])
    add_cube("AREA_GuestHall_LeftWall_CameraMismatchSide", (3250, -290, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_GuestHall_RightWall_DoorDecisionSide", (3250, 290, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_GuestHall_Ceiling_LowPressure", (3250, 0, 286), (2500, 560, 20), materials["trim"])
    add_cube("PROP_GuestHall_Camera_MonitorMismatchAnchor", (2600, -282, 220), (36, 20, 28), materials["black"])
    add_cube("PROP_GuestHall_RoomDoor203_OpenRefuseDecision", (3920, 302, 120), (260, 28, 240), materials["door"], ("Hotel.Interact.Room203Door",))
    add_cube("PROP_GuestHall_Room203_NumberPlate", (3840, 272, 178), (55, 8, 28), materials["warn_glow"])
    add_cube("LIGHTMESH_GuestHall_Room203DoorPractical", (3775, 268, 212), (96, 8, 24), materials["warn_glow"], ("Hotel.Capture.Readability",))
    add_cube("PROP_GuestHall_ServiceCart_BlockingSightline", (3380, -205, 58), (150, 82, 116), materials["trim"])
    add_cube("PROP_GuestHall_EndShadow_NoSmallRoomExtension", (4450, 0, 125), (44, 520, 250), materials["black"])
    add_cube("LIGHTMESH_GuestHall_FluorescentPanelA", (2820, 0, 274), (360, 44, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))
    add_cube("LIGHTMESH_GuestHall_FluorescentPanelB", (3920, 0, 274), (360, 44, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))
    add_cube("LIGHTMESH_FrontDesk_OverheadFluorescent", (-260, -330, 276), (460, 54, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))

    # Lighting and atmosphere: final-intent mood direction, still placeholder geometry.
    add_light("LIGHT_FrontDesk_TiredWarmCounter", unreal.RectLight, (-250, -440, 232), (-68, 0, 0), 6500.0, unreal.Color(255, 184, 116, 255), attenuation_radius=1250.0, source_width=360.0, source_height=90.0)
    add_light("LIGHT_FrontDesk_WorkSurfacePracticalFill", unreal.PointLight, (-330, -535, 178), (0, 0, 0), 950.0, unreal.Color(255, 190, 112, 255), ("Hotel.Capture.Readability",), attenuation_radius=520.0)
    add_light("LIGHT_Lobby_ColdExteriorSpill", unreal.RectLight, (1000, 0, 230), (-75, 0, 180), 2200.0, unreal.Color(120, 165, 255, 255), attenuation_radius=950.0, source_width=280.0, source_height=240.0)
    add_light("LIGHT_Elevator_SickAmberTransition", unreal.PointLight, (1120, 565, 210), (0, 0, 0), 1400.0, unreal.Color(255, 198, 90, 255), attenuation_radius=780.0)
    add_light("LIGHT_GuestHall_WeakFluorescentA", unreal.RectLight, (2820, 0, 262), (-90, 0, 0), 4800.0, unreal.Color(205, 225, 255, 255), attenuation_radius=1120.0, source_width=380.0, source_height=55.0)
    add_light("LIGHT_GuestHall_WeakFluorescentB_TargetDoor", unreal.RectLight, (3920, 0, 262), (-90, 0, 0), 3600.0, unreal.Color(178, 206, 255, 255), ("Hotel.Feedback.Room203Light",), attenuation_radius=1120.0, source_width=380.0, source_height=55.0)
    add_light("LIGHT_GuestHall_Room203PlatePractical", unreal.PointLight, (3785, 252, 205), (0, 0, 0), 620.0, unreal.Color(255, 178, 82, 255), ("Hotel.Capture.Readability",), attenuation_radius=430.0)

    fog = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.ExponentialHeightFog,
        unreal.Vector(2100, 0, 0),
        unreal.Rotator(0, 0, 0),
    )
    fog.set_actor_label("ATMOS_SubtleHotelDustFog")
    add_post_process_volume("PPV_HotelNightShift_ReadableHorrorExposure")

    player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(-260, -635, 92),
        unreal.Rotator(0.0, 54.0, 0.0),
    )
    player_start.set_actor_label("PLAYERSTART_FrontDesk_FacingPhoneAndMonitor")

    add_camera("CAPTURE_FrontDesk_FirstSteamShotCandidate", (160, -705, 170), (-3, 160, 0), 62.0)
    add_camera("CAPTURE_GuestDoor_15SecondBeatCandidate", (3600, -150, 165), (-2, 55, 0), 64.0)
    add_camera("CAPTURE_MonitorToHall_MismatchCandidate", (-715, -710, 172), (-4, 50, 0), 66.0)

    if "AMB_LobbyFluorescentHum_v0" in sounds:
        add_audio("AMB_Lobby_FluorescentHum_Source_v0", sounds["AMB_LobbyFluorescentHum_v0"], (-180, -450, 210), True)
    if "AMB_GuestHallDrone_v0" in sounds:
        add_audio("AMB_GuestHall_Drone_Source_v0", sounds["AMB_GuestHallDrone_v0"], (3380, 0, 210), True)
    if "SFX_PhoneRing_v0" in sounds:
        add_audio("SFX_PhoneRing_FrontDesk_ManualTrigger_v0", sounds["SFX_PhoneRing_v0"], (-430, -525, 150), False, ("Hotel.Audio.PhoneRing",))
    if "SFX_DoorKnock203_v0" in sounds:
        add_audio("SFX_DoorKnock203_ManualTrigger_v0", sounds["SFX_DoorKnock203_v0"], (3920, 285, 150), False, ("Hotel.Audio.Room203Knock",))

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)


def main() -> None:
    log("Preparing directories.")
    ensure_dirs()
    log("Generating project-authored placeholder WAV sources.")
    source_audio = generate_source_audio()
    log("Importing audio into /Game/Hotel/Audio.")
    sounds = import_audio(source_audio)
    log("Building production-intent hotel spine level.")
    build_level(sounds)
    log("Done.")


main()
