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
SOURCE_MESH_DIR = PROJECT_ROOT / "SourceAssets" / "GeometryGenerated"
MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"


def log(message: str) -> None:
    unreal.log(f"[HotelSpineSlice] {message}")


def ensure_dirs() -> None:
    for path in [
        "/Game/Hotel",
        "/Game/Hotel/Maps",
        "/Game/Hotel/Materials",
        "/Game/Hotel/Meshes",
        "/Game/Hotel/Audio",
        "/Game/Hotel/Blueprints",
        "/Game/Hotel/Data",
        "/Game/Hotel/UI",
        "/Game/Hotel/VFX",
    ]:
        unreal.EditorAssetLibrary.make_directory(path)
    SOURCE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_MESH_DIR.mkdir(parents=True, exist_ok=True)


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

    def phone_pickup(t: float) -> float:
        click = 0.0
        for start, pitch in ((0.025, 840), (0.105, 360), (0.205, 1200)):
            dt = t - start
            if 0.0 <= dt <= 0.055:
                click += math.exp(-dt * 55.0) * math.sin(2 * math.pi * pitch * dt)
        cable = 0.12 * math.sin(2 * math.pi * 180 * t) if 0.12 <= t <= 0.36 else 0.0
        return 0.48 * click + cable

    def phone_line_static(t: float) -> float:
        hiss = 0.05 * math.sin(2 * math.pi * 3100 * t) + 0.035 * math.sin(2 * math.pi * 4970 * t)
        cable = 0.045 * math.sin(2 * math.pi * 126 * t)
        whisper_gate = 1.0 if 0.35 < t < 1.8 else 0.0
        whisper = whisper_gate * (0.08 * math.sin(2 * math.pi * 178 * t) + 0.035 * math.sin(2 * math.pi * 221 * t))
        clicks = 0.0
        for start in (0.18, 1.92, 2.34):
            dt = t - start
            if 0.0 <= dt <= 0.035:
                clicks += math.exp(-dt * 85.0) * math.sin(2 * math.pi * 920 * dt)
        return hiss + cable + whisper + 0.34 * clicks

    def hallway_drone(t: float) -> float:
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 0.11 * t)
        return 0.16 * math.sin(2 * math.pi * 82 * t) + 0.035 * pulse * math.sin(2 * math.pi * 610 * t)

    def elevator_shaft_groan(t: float) -> float:
        motor_gate = 0.45 + 0.55 * math.sin(2 * math.pi * 0.08 * t)
        cable = 0.12 * math.sin(2 * math.pi * 47 * t) + 0.07 * math.sin(2 * math.pi * 93 * t)
        brake_ticks = 0.0
        for start in (0.8, 2.55, 4.2):
            dt = t - start
            if 0.0 <= dt <= 0.08:
                brake_ticks += math.exp(-dt * 34.0) * math.sin(2 * math.pi * 310 * dt)
        return 0.7 * motor_gate * cable + 0.26 * brake_ticks

    def stairwell_air(t: float) -> float:
        vent = 0.09 * math.sin(2 * math.pi * 71 * t) + 0.035 * math.sin(2 * math.pi * 143 * t)
        flutter = (0.5 + 0.5 * math.sin(2 * math.pi * 0.21 * t)) * 0.035 * math.sin(2 * math.pi * 520 * t)
        distant = 0.045 * math.sin(2 * math.pi * 38 * t)
        return vent + flutter + distant

    def door_knock(t: float) -> float:
        total = 0.0
        for start in (0.18, 0.42, 0.91):
            dt = t - start
            if 0.0 <= dt <= 0.16:
                total += math.exp(-dt * 28.0) * (math.sin(2 * math.pi * 135 * dt) + 0.35 * math.sin(2 * math.pi * 260 * dt))
        return 0.55 * total

    def report_log_filed(t: float) -> float:
        stamp = 0.0
        for start, pitch in ((0.035, 190), (0.085, 520), (0.16, 132)):
            dt = t - start
            if 0.0 <= dt <= 0.11:
                stamp += math.exp(-dt * 38.0) * math.sin(2 * math.pi * pitch * dt)
        scratch = 0.05 * math.sin(2 * math.pi * 1550 * t) if 0.18 <= t <= 0.38 else 0.0
        paper = 0.08 * math.sin(2 * math.pi * 240 * t) if 0.10 <= t <= 0.34 else 0.0
        return 0.48 * stamp + scratch + paper

    def patrol_listen_drop(t: float) -> float:
        floor_bloom = 0.18 * math.sin(2 * math.pi * 54 * t) * math.exp(-t * 1.2)
        elevator_reply = 0.0
        for start, pitch in ((0.18, 112), (0.62, 74), (1.08, 92)):
            dt = t - start
            if 0.0 <= dt <= 0.42:
                elevator_reply += math.exp(-dt * 5.2) * math.sin(2 * math.pi * pitch * dt)
        dry_click = 0.0
        for start in (0.06, 0.42, 1.35):
            dt = t - start
            if 0.0 <= dt <= 0.035:
                dry_click += math.exp(-dt * 95.0) * math.sin(2 * math.pi * 720 * dt)
        stair_breath = 0.05 * math.sin(2 * math.pi * 186 * t) if 1.2 <= t <= 2.2 else 0.0
        return floor_bloom + 0.28 * elevator_reply + 0.24 * dry_click + stair_breath

    def return_route_knockback(t: float) -> float:
        total = 0.0
        for start, pitch in ((0.04, 96), (0.34, 141), (0.72, 83), (1.18, 128)):
            dt = t - start
            if 0.0 <= dt <= 0.18:
                total += math.exp(-dt * 24.0) * (math.sin(2 * math.pi * pitch * dt) + 0.24 * math.sin(2 * math.pi * (pitch * 2.1) * dt))
        reverse_hum = 0.07 * math.sin(2 * math.pi * 58 * t) * math.exp(-max(0.0, t - 0.55) * 0.8)
        cold_scrape = 0.035 * math.sin(2 * math.pi * 690 * t) if 0.92 <= t <= 1.42 else 0.0
        return 0.52 * total + reverse_hum + cold_scrape

    def post_report_monitor_mismatch(t: float) -> float:
        scan = 0.045 * math.sin(2 * math.pi * 2860 * t) + 0.028 * math.sin(2 * math.pi * 4120 * t)
        low_relay = 0.0
        for start, pitch in ((0.06, 116), (0.28, 74), (0.74, 103)):
            dt = t - start
            if 0.0 <= dt <= 0.18:
                low_relay += math.exp(-dt * 18.0) * math.sin(2 * math.pi * pitch * dt)
        frame_skip = 0.0
        for start in (0.18, 0.42, 0.66, 0.92):
            dt = t - start
            if 0.0 <= dt <= 0.025:
                frame_skip += math.exp(-dt * 120.0) * math.sin(2 * math.pi * 960 * dt)
        dead_air = 0.05 * math.sin(2 * math.pi * 52 * t) if 0.55 <= t <= 1.25 else 0.0
        return scan + 0.42 * low_relay + 0.30 * frame_skip + dead_air

    def post_report_desk_wait_rattle(t: float) -> float:
        glass = 0.0
        for start, pitch in ((0.05, 162), (0.18, 91), (0.42, 126), (0.68, 73)):
            dt = t - start
            if 0.0 <= dt <= 0.22:
                glass += math.exp(-dt * 20.0) * (
                    math.sin(2 * math.pi * pitch * dt) + 0.28 * math.sin(2 * math.pi * (pitch * 3.1) * dt)
                )
        handle_tick = 0.0
        for start in (0.11, 0.55, 0.92):
            dt = t - start
            if 0.0 <= dt <= 0.035:
                handle_tick += math.exp(-dt * 95.0) * math.sin(2 * math.pi * 780 * dt)
        outside_air = 0.055 * math.sin(2 * math.pi * 46 * t) * math.exp(-max(0.0, t - 0.25) * 0.9)
        return 0.48 * glass + 0.26 * handle_tick + outside_air

    def post_report_log_self_correction(t: float) -> float:
        paper_drag = 0.0
        for start, pitch in ((0.04, 420), (0.16, 680), (0.32, 510)):
            dt = t - start
            if 0.0 <= dt <= 0.16:
                paper_drag += math.exp(-dt * 26.0) * math.sin(2 * math.pi * pitch * dt)
        pen_tick = 0.0
        for start in (0.22, 0.48, 0.82):
            dt = t - start
            if 0.0 <= dt <= 0.028:
                pen_tick += math.exp(-dt * 120.0) * math.sin(2 * math.pi * 1120 * dt)
        low_page = 0.06 * math.sin(2 * math.pi * 73 * t) * math.exp(-t * 1.6)
        dry_line = 0.04 * math.sin(2 * math.pi * 1780 * t) if 0.36 <= t <= 0.98 else 0.0
        return 0.36 * paper_drag + 0.24 * pen_tick + low_page + dry_line

    sources = {
        "SFX_PhoneRing_v0": (2.5, phone_ring),
        "SFX_PhonePickup_v0": (0.45, phone_pickup),
        "SFX_PhoneLineStatic_v0": (3.2, phone_line_static),
        "AMB_LobbyFluorescentHum_v0": (6.0, lobby_hum),
        "AMB_GuestHallDrone_v0": (6.0, hallway_drone),
        "AMB_ElevatorShaftGroan_v0": (6.0, elevator_shaft_groan),
        "AMB_StairwellAir_v0": (6.0, stairwell_air),
        "SFX_DoorKnock203_v0": (1.4, door_knock),
        "SFX_ReportLogFiled_v0": (0.55, report_log_filed),
        "SFX_PatrolListenDrop_v0": (2.4, patrol_listen_drop),
        "SFX_ReturnRouteKnockback_v0": (1.7, return_route_knockback),
        "SFX_PostReportMonitorMismatch_v0": (1.55, post_report_monitor_mismatch),
        "SFX_PostReportDeskWaitRattle_v0": (1.65, post_report_desk_wait_rattle),
        "SFX_PostReportLogSelfCorrection_v0": (1.25, post_report_log_self_correction),
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
        asset_path = f"/Game/Hotel/Audio/{name}"
        existing_asset = (
            unreal.EditorAssetLibrary.load_asset(asset_path)
            if unreal.EditorAssetLibrary.does_asset_exist(asset_path)
            else None
        )
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


def write_obj(path: pathlib.Path, vertices: list[tuple[float, float, float]], faces: list[tuple[int, ...]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Project-authored procedural mesh for Hotel Night Shift Horror.\n")
        f.write("# Generated by Automation/Unreal/create_hotel_spine_slice.py; no third-party geometry.\n")
        for x, y, z in vertices:
            f.write(f"v {x:.5f} {y:.5f} {z:.5f}\n")
        for face in faces:
            f.write("f " + " ".join(str(index + 1) for index in face) + "\n")


def rounded_ring(width: float, depth: float, z: float, segments: int = 32, power: float = 0.36) -> list[tuple[float, float, float]]:
    points: list[tuple[float, float, float]] = []
    for index in range(segments):
        theta = 2.0 * math.pi * index / segments
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        x = math.copysign(abs(cos_t) ** power, cos_t) * width * 0.5
        y = math.copysign(abs(sin_t) ** power, sin_t) * depth * 0.5
        points.append((x, y, z))
    return points


def create_phone_body_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    segments = 32
    rings = [
        rounded_ring(106.0, 72.0, -12.0, segments),
        rounded_ring(112.0, 76.0, -4.0, segments),
        rounded_ring(92.0, 62.0, 8.0, segments),
        rounded_ring(64.0, 48.0, 18.0, segments),
    ]
    vertices = [vertex for ring in rings for vertex in ring]
    faces: list[tuple[int, ...]] = []
    for ring_index in range(len(rings) - 1):
        base = ring_index * segments
        next_base = (ring_index + 1) * segments
        for index in range(segments):
            faces.append((base + index, base + ((index + 1) % segments), next_base + ((index + 1) % segments), next_base + index))
    faces.append(tuple(reversed(range(segments))))
    top_base = (len(rings) - 1) * segments
    faces.append(tuple(top_base + index for index in range(segments)))
    return vertices, faces


def create_receiver_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    length_segments = 18
    radial_segments = 12
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for length_index in range(length_segments + 1):
        u = length_index / length_segments
        x = -50.0 + 100.0 * u
        arch = math.sin(math.pi * u)
        end_weight = 1.0 - arch
        center_y = -5.5 * arch
        center_z = 5.5 * arch
        radius_y = 7.8 + 9.2 * end_weight
        radius_z = 5.6 + 7.4 * end_weight
        for radial_index in range(radial_segments):
            theta = 2.0 * math.pi * radial_index / radial_segments
            vertices.append((
                x,
                center_y + math.cos(theta) * radius_y,
                center_z + math.sin(theta) * radius_z,
            ))

    for length_index in range(length_segments):
        base = length_index * radial_segments
        next_base = (length_index + 1) * radial_segments
        for radial_index in range(radial_segments):
            faces.append((
                base + radial_index,
                base + ((radial_index + 1) % radial_segments),
                next_base + ((radial_index + 1) % radial_segments),
                next_base + radial_index,
            ))
    faces.append(tuple(reversed(range(radial_segments))))
    end_base = length_segments * radial_segments
    faces.append(tuple(end_base + index for index in range(radial_segments)))
    return vertices, faces


def create_coiled_cord_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    path_segments = 72
    radial_segments = 8
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for path_index in range(path_segments + 1):
        u = path_index / path_segments
        theta = 2.0 * math.pi * 6.0 * u
        center = (
            -50.0 + 100.0 * u,
            math.sin(theta) * 10.0,
            math.cos(theta) * 6.0,
        )
        for radial_index in range(radial_segments):
            radial_theta = 2.0 * math.pi * radial_index / radial_segments
            vertices.append((
                center[0],
                center[1] + math.cos(radial_theta) * 2.6,
                center[2] + math.sin(radial_theta) * 2.6,
            ))

    for path_index in range(path_segments):
        base = path_index * radial_segments
        next_base = (path_index + 1) * radial_segments
        for radial_index in range(radial_segments):
            faces.append((
                base + radial_index,
                base + ((radial_index + 1) % radial_segments),
                next_base + ((radial_index + 1) % radial_segments),
                next_base + radial_index,
            ))
    return vertices, faces


def create_curled_pages_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    columns = 12
    rows = 8
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for layer_z in (0.0, -4.0):
        for row in range(rows + 1):
            y_norm = row / rows
            y = -35.0 + 70.0 * y_norm
            for column in range(columns + 1):
                x_norm = column / columns
                x = -50.0 + 100.0 * x_norm
                right_curl = max(0.0, x_norm - 0.72) ** 2 * 38.0
                lower_corner = max(0.0, 0.18 - y_norm) ** 2 * 34.0
                page_wave = math.sin(x_norm * math.pi * 2.0) * math.sin(y_norm * math.pi) * 1.2
                z = layer_z + (right_curl + lower_corner + page_wave if layer_z == 0.0 else 0.0)
                vertices.append((x, y, z))

    stride = columns + 1
    top_offset = 0
    bottom_offset = (rows + 1) * stride
    for row in range(rows):
        for column in range(columns):
            a = top_offset + row * stride + column
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
            faces.append((bottom_offset + d, bottom_offset + c, bottom_offset + b, bottom_offset + a))

    for column in range(columns):
        top_a = top_offset + column
        top_b = top_a + 1
        bottom_a = bottom_offset + column
        bottom_b = bottom_a + 1
        faces.append((bottom_a, bottom_b, top_b, top_a))

        top_c = top_offset + rows * stride + column
        top_d = top_c + 1
        bottom_c = bottom_offset + rows * stride + column
        bottom_d = bottom_c + 1
        faces.append((top_c, top_d, bottom_d, bottom_c))

    for row in range(rows):
        top_a = top_offset + row * stride
        top_b = top_a + stride
        bottom_a = bottom_offset + row * stride
        bottom_b = bottom_a + stride
        faces.append((top_a, top_b, bottom_b, bottom_a))

        top_c = top_offset + row * stride + columns
        top_d = top_c + stride
        bottom_c = bottom_offset + row * stride + columns
        bottom_d = bottom_c + stride
        faces.append((bottom_c, bottom_d, top_d, top_c))

    return vertices, faces


def generate_source_meshes() -> dict[str, pathlib.Path]:
    mesh_builders = {
        "SM_FrontDesk_OldPhoneBody_v0": create_phone_body_mesh,
        "SM_FrontDesk_CurvedReceiver_v0": create_receiver_mesh,
        "SM_FrontDesk_CoiledPhoneCord_v0": create_coiled_cord_mesh,
        "SM_FrontDesk_CurledLedgerPages_v0": create_curled_pages_mesh,
    }

    output: dict[str, pathlib.Path] = {}
    for name, builder in mesh_builders.items():
        path = SOURCE_MESH_DIR / f"{name}.obj"
        vertices, faces = builder()
        write_obj(path, vertices, faces)
        output[name] = path
    return output


def import_static_meshes(source_paths: dict[str, pathlib.Path]) -> dict[str, unreal.StaticMesh]:
    meshes: dict[str, unreal.StaticMesh] = {}
    tasks = []
    for name, path in source_paths.items():
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(path))
        task.set_editor_property("destination_path", "/Game/Hotel/Meshes")
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        tasks.append(task)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    for name in source_paths:
        if name in meshes:
            continue
        asset = unreal.EditorAssetLibrary.load_asset(f"/Game/Hotel/Meshes/{name}")
        if asset:
            meshes[name] = asset
    return meshes


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


def make_rotator(pitch: float, yaw: float, roll: float = 0.0) -> unreal.Rotator:
    return unreal.Rotator(roll, pitch, yaw)


def add_cube(
    label: str,
    location,
    size,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
) -> unreal.Actor:
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        make_rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    component = actor.static_mesh_component
    component.set_static_mesh(cube)
    component.set_material(0, material)
    component.set_editor_property("mobility", mobility)
    if no_collision:
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
    tag_actor(actor, *tags)
    return actor


def add_mesh(
    label: str,
    mesh_path: str,
    location,
    size,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
    rotation=(0.0, 0.0, 0.0),
) -> unreal.Actor:
    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    component = actor.static_mesh_component
    component.set_static_mesh(mesh)
    component.set_material(0, material)
    component.set_editor_property("mobility", mobility)
    if no_collision:
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
    tag_actor(actor, *tags)
    return actor


def add_cylinder(
    label: str,
    location,
    diameter: float,
    height: float,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
    rotation=(0.0, 0.0, 0.0),
) -> unreal.Actor:
    return add_mesh(
        label,
        "/Engine/BasicShapes/Cylinder.Cylinder",
        location,
        (diameter, diameter, height),
        material,
        tags,
        mobility,
        no_collision,
        rotation,
    )


def add_sphere(
    label: str,
    location,
    size,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
) -> unreal.Actor:
    return add_mesh(
        label,
        "/Engine/BasicShapes/Sphere.Sphere",
        location,
        size,
        material,
        tags,
        mobility,
        no_collision,
    )


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
        make_rotator(*rotation),
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
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    try:
        component = actor.get_editor_property("camera_component")
        component.set_editor_property("field_of_view", fov)
        component.set_editor_property("post_process_blend_weight", 1.0)
        settings = component.get_editor_property("post_process_settings")
        exposure_overrides = {
            "override_auto_exposure_method": True,
            "override_auto_exposure_min_brightness": True,
            "override_auto_exposure_max_brightness": True,
            "override_auto_exposure_bias": True,
            "auto_exposure_min_brightness": 1.0,
            "auto_exposure_max_brightness": 1.0,
            "auto_exposure_bias": 2.0,
        }
        for name, value in exposure_overrides.items():
            try_set_property(settings, name, value)
        try:
            settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
        except Exception:
            pass
        component.set_editor_property("post_process_settings", settings)
    except Exception:
        pass
    return actor


def add_audio(label: str, sound: unreal.SoundWave, location, auto_activate: bool, tags=()) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.AmbientSound,
        unreal.Vector(*location),
        make_rotator(0.0, 0.0, 0.0),
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
        make_rotator(0.0, 0.0, 0.0),
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
            "auto_exposure_bias": 2.0,
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


def add_authored_mesh(
    label: str,
    mesh: unreal.StaticMesh,
    location,
    scale,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
    rotation=(0.0, 0.0, 0.0),
) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    component = actor.static_mesh_component
    component.set_static_mesh(mesh)
    component.set_material(0, material)
    component.set_editor_property("mobility", mobility)
    if no_collision:
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
    tag_actor(actor, *tags)
    return actor


def build_level(sounds: dict[str, unreal.SoundWave], meshes: dict[str, unreal.StaticMesh]) -> None:
    prepare_level()

    materials = {
        "floor": ensure_material("M_Hotel_WornFloor_v0", unreal.LinearColor(0.15, 0.13, 0.11, 1.0), 0.92),
        "wall": ensure_material("M_Hotel_AgedWall_v0", unreal.LinearColor(0.42, 0.38, 0.31, 1.0), 0.86),
        "trim": ensure_material("M_Hotel_DarkTrim_v0", unreal.LinearColor(0.09, 0.08, 0.075, 1.0), 0.74),
        "desk": ensure_material("M_Hotel_FrontDeskWood_v0", unreal.LinearColor(0.19, 0.11, 0.065, 1.0), 0.68),
        "black": ensure_material("M_Hotel_BlackPlastic_v0", unreal.LinearColor(0.01, 0.012, 0.014, 1.0), 0.55),
        "brass": ensure_material("M_Hotel_TarnishedBrass_v0", unreal.LinearColor(0.62, 0.43, 0.20, 1.0), 0.58),
        "dull_metal": ensure_material("M_Hotel_DullDeskMetal_v0", unreal.LinearColor(0.30, 0.29, 0.27, 1.0), 0.72),
        "deep_red": ensure_material("M_Hotel_AgedLedgerRed_v0", unreal.LinearColor(0.46, 0.045, 0.032, 1.0), 0.82),
        "paper": ensure_material("M_Hotel_AgedCallSlipPaper_v0", unreal.LinearColor(0.72, 0.64, 0.48, 1.0), 0.81),
        "button": ensure_material("M_Hotel_PhoneBoneButton_v0", unreal.LinearColor(0.58, 0.54, 0.46, 1.0), 0.62),
        "route_mark": ensure_material("M_Hotel_WornRouteTape_v0", unreal.LinearColor(0.46, 0.42, 0.32, 1.0), 0.88),
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
    phone_visual_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.PhoneResponseVisual")

    add_cube("PROP_FrontDesk_DeskMat_UnderPhoneAndLog", (-352, -529, 118), (310, 130, 8), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_BaseHeavyOldDeskSet", (-430, -525, 126), (108, 68, 18), materials["black"], ("Hotel.Capture.Readability",))
    add_cube("PROP_FrontDesk_Phone_AnswerLoopPlaceholder", (-430, -525, 140), (82, 48, 22), materials["black"], ("Hotel.Interact.Phone", "Hotel.Capture.Readability"))
    add_cube("PROP_FrontDesk_Phone_Keypad_ReadableCue", (-430, -523, 154), (56, 32, 5), materials["button"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_ButtonRowTop", (-430, -535, 160), (44, 5, 4), materials["paper"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_ButtonRowBottom", (-430, -516, 160), (44, 5, 4), materials["paper"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CradleLeftHook", (-465, -550, 154), (10, 18, 12), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CradleRightHook", (-395, -550, 154), (10, 18, 12), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_HookSwitch_DepressedCue", (-430, -548, 158), (34, 10, 8), materials["button"], phone_visual_tags, no_collision=True)
    authored_mesh_tags = ("Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk", "Hotel.ArtSource.AuthoredMesh")
    authored_receiver_tags = (
        "Hotel.Feedback.PhoneReceiver",
        "Hotel.Capture.Readability",
        "Hotel.ArtDensity.FrontDesk",
        "Hotel.ArtSource.AuthoredMesh",
    )
    if "SM_FrontDesk_OldPhoneBody_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_Phone_AuthoredCurvedBody",
            meshes["SM_FrontDesk_OldPhoneBody_v0"],
            (-430, -525, 143),
            (1.0, 1.0, 1.0),
            materials["black"],
            authored_mesh_tags,
            no_collision=True,
        )
    if "SM_FrontDesk_CurvedReceiver_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_Phone_ReceiverAuthoredSilhouette",
            meshes["SM_FrontDesk_CurvedReceiver_v0"],
            (-430, -558, 153),
            (0.92, 1.0, 1.0),
            materials["black"],
            authored_receiver_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube(
        "PROP_FrontDesk_Phone_ReceiverCue",
        (-430, -558, 150),
        (74, 14, 12),
        materials["black"],
        ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"),
        unreal.ComponentMobility.MOVABLE,
    )
    add_cube(
        "PROP_FrontDesk_Phone_ReceiverLeftCap",
        (-466, -558, 151),
        (18, 22, 16),
        materials["black"],
        ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"),
        unreal.ComponentMobility.MOVABLE,
    )
    add_cube(
        "PROP_FrontDesk_Phone_ReceiverRightCap",
        (-394, -558, 151),
        (18, 22, 16),
        materials["black"],
        ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"),
        unreal.ComponentMobility.MOVABLE,
    )
    add_cube("PROP_FrontDesk_Phone_CradleShadow", (-430, -547, 138), (86, 44, 12), materials["trim"])
    add_cube("PROP_FrontDesk_Phone_CoiledCordCue", (-378, -556, 137), (42, 8, 8), materials["trim"])
    add_cube("PROP_FrontDesk_Phone_CoiledCordLoopA", (-354, -553, 137), (16, 8, 8), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CoiledCordLoopB", (-336, -560, 137), (16, 8, 8), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CoiledCordLoopC", (-318, -553, 137), (16, 8, 8), materials["trim"], phone_visual_tags, no_collision=True)
    front_desk_art_tags = ("Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk")
    receiver_art_tags = ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk")
    if "SM_FrontDesk_CoiledPhoneCord_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_Phone_AuthoredCoiledCord",
            meshes["SM_FrontDesk_CoiledPhoneCord_v0"],
            (-356, -558, 140),
            (0.74, 0.7, 0.7),
            materials["black"],
            authored_mesh_tags,
            no_collision=True,
        )
    add_cylinder("PROP_FrontDesk_Phone_RoundedDialPlate", (-430, -523, 162), 54, 7, materials["button"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerHoleTop", (-430, -542, 167), 9, 4, materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerHoleLeft", (-448, -523, 167), 9, 4, materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerHoleRight", (-412, -523, 167), 9, 4, materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerStop", (-400, -542, 168), 6, 18, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_ReceiverLeftRoundCup", (-466, -558, 159), 26, 10, materials["black"], receiver_art_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_ReceiverRightRoundCup", (-394, -558, 159), 26, 10, materials["black"], receiver_art_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_sphere("PROP_FrontDesk_Phone_CordRoundLoopA", (-354, -553, 140), (15, 9, 7), materials["black"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_Phone_CordRoundLoopB", (-336, -560, 140), (15, 9, 7), materials["black"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_Phone_CordRoundLoopC", (-318, -553, 140), (15, 9, 7), materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_ServiceBell_Dome", (-525, -505, 133), 40, 18, materials["dull_metal"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_ServiceBell_Button", (-525, -505, 149), (14, 14, 10), materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_DeskLamp_RoundFoot", (-332, -552, 132), 44, 8, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_DeskLamp_ThinStem", (-332, -552, 158), 8, 48, materials["brass"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_DeskLamp_ShadeCurvedSilhouette", (-320, -548, 176), (74, 34, 22), materials["desk_lamp"], front_desk_art_tags, no_collision=True)
    add_cube("LIGHTMESH_FrontDesk_PhoneCallLamp", (-395, -555, 158), (18, 8, 10), materials["warn_glow"], ("Hotel.Feedback.PhoneRingLamp", "Hotel.Capture.Readability"))
    add_cube("PROP_Surveillance_Monitor_PlayerChecksHall", (-620, -525, 160), (130, 16, 72), materials["screen_glow"], ("Hotel.Interact.Monitor",))
    monitor_mismatch_tags = ("Hotel.Capture.Readability", "Hotel.Capture.PostReportMonitorMismatch", "Hotel.Feedback.PostReportMonitorMismatchVisual")
    add_cube("PROP_Surveillance_Monitor_PostReportFeedFrame", (-620, -536, 160), (112, 5, 58), materials["screen"], monitor_mismatch_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportStaticBarA", (-646, -540, 178), (58, 4, 4), materials["screen_glow"], monitor_mismatch_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportStaticBarB", (-602, -540, 143), (76, 4, 4), materials["screen_glow"], monitor_mismatch_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportOpenDoorGlyph", (-585, -542, 159), (13, 5, 34), materials["warn_glow"], monitor_mismatch_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportRoom203Dot", (-608, -543, 174), (12, 5, 12), materials["warn"], monitor_mismatch_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportTimestampSmear", (-656, -542, 132), (40, 5, 4), materials["paper"], monitor_mismatch_tags, no_collision=True)
    add_cube("PROP_ReportLog_ReturnAndRecordPoint", (-255, -522, 128), (96, 62, 10), materials["warn_glow"], ("Hotel.Interact.ReportLog",))
    add_cube("PROP_FrontDesk_NightLog_OpenPage_Readable", (-255, -522, 137), (88, 54, 4), materials["paper"], ("Hotel.Capture.Readability",), no_collision=True)
    if "SM_FrontDesk_CurledLedgerPages_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_ReportLog_AuthoredCurledPages",
            meshes["SM_FrontDesk_CurledLedgerPages_v0"],
            (-255, -522, 141),
            (0.88, 0.78, 0.7),
            materials["paper"],
            authored_mesh_tags,
            no_collision=True,
        )
    report_log_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.ReportLogVisual")
    report_log_filed_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.ReportLogVisual", "Hotel.Feedback.ReportLogFiled")
    add_cube("PROP_FrontDesk_ReportLog_ClipboardClip_Readable", (-255, -550, 144), (44, 8, 5), materials["trim"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_IncidentHeaderCue", (-255, -540, 142), (58, 3, 3), materials["black"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_Room203EntryLine", (-262, -528, 142), (64, 3, 2), materials["black"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_TimeBoxCue", (-221, -516, 142), (30, 10, 2), materials["trim"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_RefusedCheckbox", (-292, -513, 142), (8, 8, 2), materials["black"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_RefusedCheckmarkShort", (-295, -511, 144), (3, 9, 2), materials["warn"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_RefusedCheckmarkLong", (-288, -509, 144), (16, 3, 2), materials["warn"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_FiledStampCue", (-236, -504, 143), (38, 16, 3), materials["warn"], report_log_filed_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_PenRest", (-207, -536, 144), (42, 5, 6), materials["black"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_PenTip", (-184, -536, 144), (8, 5, 5), materials["warn"], report_log_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_ReportLog_BinderRingTop", (-296, -548, 146), 9, 12, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_ReportLog_BinderRingBottom", (-296, -509, 146), 9, 12, materials["brass"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_ReportLog_RedInkSmear", (-238, -517, 145), (30, 8, 3), materials["deep_red"], front_desk_art_tags, no_collision=True)
    log_self_correction_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportLogSelfCorrection",
        "Hotel.Feedback.PostReportLogSelfCorrection",
    )
    log_self_correction_visual_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportLogSelfCorrection",
        "Hotel.Feedback.PostReportLogSelfCorrectionVisual",
    )
    add_cube("PROP_FrontDesk_ReportLog_SelfCorrectedRoom203OpenLine", (-205, -510, 146), (66, 4, 3), materials["warn_glow"], log_self_correction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_SelfCorrectedNoGuestLine", (-202, -500, 146), (58, 4, 3), materials["screen_glow"], log_self_correction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_SelfCorrectedTimestampSlash", (-226, -490, 146), (34, 4, 3), materials["warn"], log_self_correction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("LIGHTMESH_FrontDesk_ReportLog_SelfCorrectionCue", (-190, -520, 166), (42, 8, 10), materials["warn_glow"], log_self_correction_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_CallSlip_Room203_CameraMismatchCue", (-315, -565, 131), (76, 38, 4), materials["paper"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_CallSlip_Underline203", (-315, -565, 135), (42, 4, 3), materials["warn"], phone_visual_tags, no_collision=True)
    add_cube("LIGHTMESH_FrontDesk_DeskLampPractical", (-320, -548, 176), (72, 18, 18), materials["desk_lamp"], ("Hotel.Capture.Readability",))
    add_cylinder("PROP_FrontDesk_BackShelf_KeyHookA", (-858, -560, 176), 6, 28, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_BackShelf_KeyHookB", (-858, -495, 176), 6, 28, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_BackShelf_KeyHookC", (-858, -430, 176), 6, 28, materials["brass"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_BackShelf_KeyTag203", (-858, -495, 148), (22, 10, 26), materials["paper"], front_desk_art_tags, no_collision=True)
    add_cube("AREA_Lobby_GuestAdmissionThreshold", (780, 0, -8), (620, 1280, 16), materials["floor"])
    add_cube("PROP_Lobby_MainGlassDoor_Silhouette", (1080, -250, 110), (28, 270, 220), materials["screen_glow"])
    add_cube("PROP_Lobby_MainGlassDoor_RefuseLine", (1080, 250, 110), (28, 270, 220), materials["screen_glow"])
    post_report_desk_wait_tags = ("Hotel.Capture.Readability", "Hotel.Capture.PostReportDeskWait", "Hotel.Feedback.PostReportDeskWaitVisual")
    add_cube("PROP_FrontDesk_FloorWaitMarker_PostReport", (-260, -620, 4), (220, 80, 4), materials["route_mark"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_FrontDesk_CounterHoldLine_PostReport", (-210, -475, 122), (180, 6, 5), materials["warn"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportHoldClosedTape", (1062, -250, 172), (8, 210, 12), materials["warn"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportOutsidePalmSmear", (1060, -312, 132), (7, 46, 54), materials["paper"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportNoGuestReflection", (1058, -188, 112), (7, 54, 82), materials["black"], post_report_desk_wait_tags, no_collision=True)
    add_cube("LIGHTMESH_LobbyDoor_PostReportRattleCue", (1035, -250, 170), (10, 170, 18), materials["screen_glow"], post_report_desk_wait_tags, no_collision=True)
    desk_wait_rattle_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportDeskWait",
        "Hotel.Feedback.PostReportDeskWaitRattle",
        "Hotel.ArtDensity.FrontDesk",
    )
    add_cylinder("PROP_Lobby_GlassDoor_PostReportHandleRattleBar", (1055, -250, 134), 12, 132, materials["dull_metal"], desk_wait_rattle_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cylinder("PROP_Lobby_GlassDoor_PostReportLatchRattlePin", (1048, -250, 158), 10, 28, materials["brass"], desk_wait_rattle_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportTapeLooseEnd", (1053, -355, 178), (7, 36, 12), materials["warn"], desk_wait_rattle_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)

    # Controlled transition from work hub to guest-floor response.
    add_cube("AREA_Transition_CarpetRun_ToGuestHall_NoVoid", (1625, 0, -9), (750, 560, 18), materials["floor"])
    add_cube("AREA_Transition_LeftSightlineWall_ToGuestHall", (1625, -290, 140), (750, 24, 280), materials["wall"])
    add_cube("AREA_Transition_RightSightlineWall_ToGuestHall", (1625, 290, 140), (750, 24, 280), materials["wall"])
    transition_tags = ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear")
    add_cube("TRANSITION_Elevator_Door_AudibleBeforeSeen", (1160, 565, 120), (34, 280, 240), materials["door"], transition_tags)
    add_cube("TRANSITION_Elevator_CallPanel_SoundCueAnchor", (1125, 385, 120), (12, 30, 80), materials["warn_glow"], transition_tags, no_collision=True)
    add_cube("TRANSITION_Elevator_FloorIndicator_WrongFloorCue", (1124, 565, 214), (10, 92, 24), materials["warn_glow"], transition_tags, no_collision=True)
    add_cube("TRANSITION_Elevator_ClosedSeam_ShadowCue", (1142, 565, 121), (6, 10, 214), materials["black"], transition_tags, no_collision=True)
    add_cube("TRANSITION_EmergencyStair_Door_AlternateRoute", (1160, -565, 120), (34, 280, 240), materials["door"], transition_tags)
    add_cube("TRANSITION_EmergencyStair_ExitSign_ColdCue", (1125, -565, 230), (10, 120, 26), materials["screen_glow"], transition_tags, no_collision=True)
    add_cube("TRANSITION_EmergencyStair_DoorHandle_ShadowCue", (1135, -450, 126), (12, 30, 16), materials["black"], transition_tags, no_collision=True)
    add_cube("TRANSITION_ServiceBackHall_LockedShortcut", (430, 770, 110), (330, 26, 220), materials["trim"], transition_tags)
    add_cube("TRANSITION_ServiceBackHall_ChainLockedShortcutCue", (430, 745, 142), (210, 8, 10), materials["warn"], transition_tags, no_collision=True)
    patrol_decision_tags = ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear", "Hotel.Capture.PatrolDecision")
    add_cube("PATROL_Route_DecisionStopLine_ListenBeforeMoving", (930, 0, 3), (260, 10, 4), materials["route_mark"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_DecisionStopLine_CenterBreak", (930, 0, 8), (24, 24, 5), materials["warn"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_ElevatorTrack_FootstepA", (980, 210, 5), (42, 18, 4), materials["trim"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_ElevatorTrack_FootstepB", (1040, 320, 5), (42, 18, 4), materials["trim"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_ElevatorTrack_FootstepStopped", (1085, 440, 5), (44, 20, 4), materials["trim"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairReturn_FootstepA", (980, -185, 5), (42, 18, 4), materials["black"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairReturn_FootstepB", (1035, -310, 5), (42, 18, 4), materials["black"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairReturn_ScrapeMark", (1090, -438, 5), (76, 8, 4), materials["route_mark"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_DroppedKeyTag_ReturnCue", (955, -70, 9), (44, 24, 5), materials["warn"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_NightAuditClipboard_ElevatorOrStairChoice", (1015, 0, 16), (92, 64, 5), materials["paper"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_Clipboard_ElevatorMark", (1015, 22, 20), (56, 5, 3), materials["warn"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_Clipboard_StairMark", (1015, -22, 20), (56, 5, 3), materials["screen_glow"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_WallArrow_ElevatorNoiseCue", (1110, 205, 112), (8, 86, 12), materials["warn_glow"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_WallArrow_StairAirCue", (1110, -210, 112), (8, 86, 12), materials["screen_glow"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairDoor_ColdLightLeak", (1136, -565, 30), (8, 206, 14), materials["screen_glow"], patrol_decision_tags, no_collision=True)

    # Guest hallway response line.
    add_cube("AREA_GuestHall_Floor_OneDoorSlice", (3250, 0, -10), (2500, 560, 20), materials["floor"])
    add_cube("AREA_GuestHall_LeftWall_CameraMismatchSide", (3250, -290, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_GuestHall_RightWall_DoorDecisionSide", (3250, 290, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_GuestHall_Ceiling_LowPressure", (3250, 0, 286), (2500, 560, 20), materials["trim"])
    add_cube("PROP_GuestHall_Camera_MonitorMismatchAnchor", (2600, -282, 220), (36, 20, 28), materials["black"])
    return_route_tags = ("Hotel.Capture.Readability", "Hotel.Capture.ReturnRouteAnomaly")
    add_cube("RETURN_Route_FloorColdPatch_AfterRefusal", (2860, 0, 4), (310, 420, 5), materials["screen_glow"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_BackKnockDirectionStripe", (2860, -84, 10), (220, 8, 5), materials["warn"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_BackKnockDirectionStripe_Return", (2860, 84, 10), (220, 8, 5), materials["warn"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_WallStatusSlip_ReportAfterHall", (2840, -278, 124), (82, 7, 48), materials["paper"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_WallStatusSlip_Underline", (2840, -282, 104), (56, 5, 4), materials["warn"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_FootprintBacktrackA", (3040, -90, 6), (44, 18, 4), materials["black"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_FootprintBacktrackB", (2920, -32, 6), (44, 18, 4), materials["black"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_FootprintBacktrackC", (2785, 48, 6), (44, 18, 4), materials["black"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_CeilingLightmesh_ColdPulseCue", (2860, -90, 273), (280, 34, 9), materials["fluorescent_panel"], return_route_tags, no_collision=True)
    door_decision_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.Room203DoorDecisionVisual")
    door_refusal_tags = ("Hotel.Feedback.Room203Refusal", "Hotel.Capture.Readability")
    add_cube("PROP_GuestHall_RoomDoor203_OpenRefuseDecision", (3920, 302, 120), (260, 28, 240), materials["door"], ("Hotel.Interact.Room203Door",))
    add_cube("PROP_GuestHall_Room203_LeftDoorJamb", (3784, 272, 122), (14, 12, 244), materials["trim"])
    add_cube("PROP_GuestHall_Room203_RightDoorJamb", (4056, 272, 122), (14, 12, 244), materials["trim"])
    add_cube("PROP_GuestHall_Room203_TopDoorJamb", (3920, 272, 245), (286, 12, 14), materials["trim"])
    add_cube("PROP_GuestHall_Room203_DarkLatchGap", (4042, 266, 122), (8, 8, 188), materials["black"])
    add_cube("PROP_GuestHall_Room203_NumberPlate", (3840, 272, 178), (55, 8, 28), materials["warn_glow"])
    add_cube("PROP_GuestHall_Room203_HandleBackplate_Readable", (4028, 264, 132), (22, 8, 70), materials["black"], door_decision_tags, no_collision=True)
    add_cube(
        "PROP_GuestHall_Room203_LatchJoltCue",
        (4046, 257, 143),
        (54, 10, 10),
        materials["warn"],
        door_refusal_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    add_cube(
        "PROP_GuestHall_Room203_ChainJoltCue",
        (3992, 258, 166),
        (72, 8, 8),
        materials["trim"],
        door_refusal_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    add_cube("PROP_GuestHall_Room203_PeepholeBlackCue", (3920, 262, 186), (22, 7, 22), materials["black"], door_decision_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_DoNotOpenNotice", (3880, 260, 112), (62, 5, 42), materials["paper"], door_decision_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_NoticeUnderline", (3880, 256, 101), (46, 5, 4), materials["warn"], door_decision_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_ThresholdShadow", (3920, 257, 2), (230, 18, 6), materials["black"], door_decision_tags, no_collision=True)
    add_cube("LIGHTMESH_GuestHall_Room203DoorPractical", (3775, 268, 212), (96, 8, 24), materials["warn_glow"], ("Hotel.Capture.Readability",))
    add_cube("PROP_GuestHall_ServiceCart_BlockingSightline", (3380, -205, 58), (150, 82, 116), materials["trim"])
    add_cube("PROP_GuestHall_EndShadow_NoSmallRoomExtension", (4450, 0, 125), (44, 520, 250), materials["black"])
    add_cube("LIGHTMESH_GuestHall_FluorescentPanelA", (2820, 0, 274), (360, 44, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))
    add_cube("LIGHTMESH_GuestHall_FluorescentPanelB", (3920, 0, 274), (360, 44, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))
    add_cube("LIGHTMESH_FrontDesk_OverheadFluorescent", (-260, -330, 276), (460, 54, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))

    # Lighting and atmosphere: final-intent mood direction, still placeholder geometry.
    add_light("LIGHT_FrontDesk_TiredWarmCounter", unreal.RectLight, (-250, -440, 232), (-68, 0, 0), 6500.0, unreal.Color(255, 184, 116, 255), attenuation_radius=1250.0, source_width=360.0, source_height=90.0)
    add_light("LIGHT_FrontDesk_WorkSurfacePracticalFill", unreal.PointLight, (-330, -535, 178), (0, 0, 0), 950.0, unreal.Color(255, 190, 112, 255), ("Hotel.Capture.Readability",), attenuation_radius=520.0)
    add_light("LIGHT_FrontDesk_PhoneCallLampPulse", unreal.PointLight, (-395, -555, 158), (0, 0, 0), 280.0, unreal.Color(255, 168, 72, 255), ("Hotel.Feedback.PhoneRingLamp", "Hotel.Capture.Readability"), attenuation_radius=220.0)
    add_light("LIGHT_FrontDesk_CaptureEvidenceSoftFill", unreal.PointLight, (-110, -565, 210), (0, 0, 0), 1800.0, unreal.Color(255, 205, 145, 255), ("Hotel.Capture.Readability",), attenuation_radius=860.0)
    add_light("LIGHT_Lobby_ColdExteriorSpill", unreal.RectLight, (1000, 0, 230), (-75, 0, 180), 2200.0, unreal.Color(120, 165, 255, 255), attenuation_radius=950.0, source_width=280.0, source_height=240.0)
    add_light("LIGHT_Elevator_SickAmberTransition", unreal.PointLight, (1120, 565, 210), (0, 0, 0), 1400.0, unreal.Color(255, 198, 90, 255), attenuation_radius=780.0)
    add_light("LIGHT_Transition_ElevatorCallPanelDread", unreal.PointLight, (1122, 398, 150), (0, 0, 0), 980.0, unreal.Color(255, 155, 58, 255), ("Hotel.Capture.TransitionFear",), attenuation_radius=360.0)
    add_light("LIGHT_Transition_StairExitCold", unreal.PointLight, (1122, -560, 230), (0, 0, 0), 720.0, unreal.Color(92, 210, 170, 255), ("Hotel.Capture.TransitionFear",), attenuation_radius=420.0)
    add_light("LIGHT_Transition_CaptureEvidenceSoftFill", unreal.PointLight, (925, 0, 190), (0, 0, 0), 1850.0, unreal.Color(178, 218, 205, 255), ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear"), attenuation_radius=760.0)
    add_light("LIGHT_PatrolRoute_DecisionCueFloorFill", unreal.PointLight, (955, 0, 115), (0, 0, 0), 1100.0, unreal.Color(190, 218, 194, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PatrolDecision", "Hotel.Feedback.PatrolListenLight"), attenuation_radius=520.0)
    add_light("LIGHT_GuestHall_WeakFluorescentA", unreal.RectLight, (2820, 0, 262), (-90, 0, 0), 4800.0, unreal.Color(205, 225, 255, 255), attenuation_radius=1120.0, source_width=380.0, source_height=55.0)
    add_light("LIGHT_ReturnRoute_ColdPulseAfterRefusal", unreal.PointLight, (2860, -90, 188), (0, 0, 0), 620.0, unreal.Color(120, 225, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.ReturnRouteAnomaly", "Hotel.Feedback.ReturnRouteLight"), attenuation_radius=680.0)
    add_light("LIGHT_GuestHall_WeakFluorescentB_TargetDoor", unreal.RectLight, (3920, 0, 262), (-90, 0, 0), 3600.0, unreal.Color(178, 206, 255, 255), ("Hotel.Feedback.Room203Light",), attenuation_radius=1120.0, source_width=380.0, source_height=55.0)
    add_light("LIGHT_GuestHall_Room203PlatePractical", unreal.PointLight, (3785, 252, 205), (0, 0, 0), 620.0, unreal.Color(255, 178, 82, 255), ("Hotel.Capture.Readability",), attenuation_radius=430.0)
    add_light("LIGHT_GuestHall_CaptureEvidenceDoorFill", unreal.PointLight, (3590, 105, 215), (0, 0, 0), 2200.0, unreal.Color(210, 230, 255, 255), ("Hotel.Capture.Readability",), attenuation_radius=920.0)
    add_light("LIGHT_MonitorToHall_CaptureEvidenceGreenFill", unreal.PointLight, (-575, -555, 188), (0, 0, 0), 1250.0, unreal.Color(120, 255, 190, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportMonitorMismatch", "Hotel.Feedback.PostReportMonitorMismatchLight"), attenuation_radius=560.0)
    add_light("LIGHT_LobbyDoor_PostReportRattleColdPulse", unreal.PointLight, (1035, -250, 170), (0, 0, 0), 360.0, unreal.Color(120, 190, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportDeskWait", "Hotel.Feedback.PostReportDeskWaitLight"), attenuation_radius=650.0)
    add_light("LIGHT_FrontDesk_ReportLog_SelfCorrectionAmberPulse", unreal.PointLight, (-190, -520, 166), (0, 0, 0), 520.0, unreal.Color(255, 190, 120, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportLogSelfCorrection", "Hotel.Feedback.PostReportLogSelfCorrectionLight"), attenuation_radius=420.0)

    fog = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.ExponentialHeightFog,
        unreal.Vector(2100, 0, 0),
        make_rotator(0, 0, 0),
    )
    fog.set_actor_label("ATMOS_SubtleHotelDustFog")
    add_post_process_volume("PPV_HotelNightShift_ReadableHorrorExposure")

    player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(-260, -635, 92),
        make_rotator(0.0, 54.0, 0.0),
    )
    player_start.set_actor_label("PLAYERSTART_FrontDesk_FacingPhoneAndMonitor")

    add_camera("CAPTURE_FrontDesk_FirstSteamShotCandidate", (-130, -690, 178), (2, 151, 0), 60.0)
    add_camera("CAPTURE_ReportLog_ReadabilityCandidate", (-255, -660, 218), (-28, 90, 0), 48.0)
    add_camera("CAPTURE_PhoneResponse_LiftReceiverCandidate", (-255, -704, 168), (3, 136, 0), 54.0)
    add_camera("CAPTURE_Transition_ElevatorStair_AudioFearCandidate", (760, -18, 168), (1, 0, 0), 76.0)
    add_camera("CAPTURE_PatrolRoute_DecisionCueCandidate", (780, -430, 214), (-20, 58, 0), 78.0)
    add_camera("CAPTURE_GuestDoor_15SecondBeatCandidate", (2820, -210, 168), (2, 25, 0), 70.0)
    add_camera("CAPTURE_ReturnRoute_BackKnockCandidate", (2475, -220, 168), (2, 28, 0), 72.0)
    add_camera("CAPTURE_PostReportMonitorMismatchCandidate", (-780, -620, 180), (2, 28, 0), 72.0)
    add_camera("CAPTURE_PostReportDeskWait_DoNotAnswerCandidate", (-350, -720, 174), (1, 22, 0), 72.0)
    add_camera("CAPTURE_PostReportLogSelfCorrectionCandidate", (-265, -755, 232), (-31, 90, 0), 62.0)

    if "AMB_LobbyFluorescentHum_v0" in sounds:
        add_audio("AMB_Lobby_FluorescentHum_Source_v0", sounds["AMB_LobbyFluorescentHum_v0"], (-180, -450, 210), True)
    if "AMB_GuestHallDrone_v0" in sounds:
        add_audio("AMB_GuestHall_Drone_Source_v0", sounds["AMB_GuestHallDrone_v0"], (3380, 0, 210), True)
    if "AMB_ElevatorShaftGroan_v0" in sounds:
        add_audio("AMB_Elevator_ShaftGroan_Source_v0", sounds["AMB_ElevatorShaftGroan_v0"], (1120, 565, 180), True, ("Hotel.Audio.ElevatorShaftGroan",))
        add_audio("AMB_PatrolRoute_ElevatorGroanBleed_Source_v0", sounds["AMB_ElevatorShaftGroan_v0"], (960, 250, 164), True, ("Hotel.Audio.ElevatorShaftGroan", "Hotel.Audio.PatrolDecision"))
    if "AMB_StairwellAir_v0" in sounds:
        add_audio("AMB_Stairwell_Air_Source_v0", sounds["AMB_StairwellAir_v0"], (1120, -565, 180), True, ("Hotel.Audio.StairwellAir",))
        add_audio("AMB_PatrolRoute_StairAirBleed_Source_v0", sounds["AMB_StairwellAir_v0"], (960, -250, 164), True, ("Hotel.Audio.StairwellAir", "Hotel.Audio.PatrolDecision"))
    if "SFX_PatrolListenDrop_v0" in sounds:
        add_audio("SFX_PatrolListen_StopLine_ManualTrigger_v0", sounds["SFX_PatrolListenDrop_v0"], (930, 0, 72), False, ("Hotel.Audio.PatrolListen",))
    if "SFX_ReturnRouteKnockback_v0" in sounds:
        add_audio("SFX_ReturnRoute_BackKnock_ManualTrigger_v0", sounds["SFX_ReturnRouteKnockback_v0"], (3420, 270, 150), False, ("Hotel.Audio.ReturnRoute",))
    if "SFX_PostReportMonitorMismatch_v0" in sounds:
        add_audio("SFX_PostReportMonitorMismatch_ManualTrigger_v0", sounds["SFX_PostReportMonitorMismatch_v0"], (-620, -542, 172), False, ("Hotel.Audio.PostReportMonitorMismatch",))
    if "SFX_PostReportDeskWaitRattle_v0" in sounds:
        add_audio("SFX_PostReportDeskWait_Rattle_ManualTrigger_v0", sounds["SFX_PostReportDeskWaitRattle_v0"], (1080, -250, 150), False, ("Hotel.Audio.PostReportDeskWait",))
    if "SFX_PostReportLogSelfCorrection_v0" in sounds:
        add_audio("SFX_PostReportLogSelfCorrection_ManualTrigger_v0", sounds["SFX_PostReportLogSelfCorrection_v0"], (-214, -494, 154), False, ("Hotel.Audio.PostReportLogSelfCorrection",))
    if "SFX_PhoneRing_v0" in sounds:
        add_audio("SFX_PhoneRing_FrontDesk_ManualTrigger_v0", sounds["SFX_PhoneRing_v0"], (-430, -525, 150), False, ("Hotel.Audio.PhoneRing",))
    if "SFX_PhonePickup_v0" in sounds:
        add_audio("SFX_PhonePickup_FrontDesk_ManualTrigger_v0", sounds["SFX_PhonePickup_v0"], (-430, -548, 150), False, ("Hotel.Audio.PhonePickup",))
    if "SFX_PhoneLineStatic_v0" in sounds:
        add_audio("SFX_PhoneLineStatic_FrontDesk_ConnectedCue_v0", sounds["SFX_PhoneLineStatic_v0"], (-438, -552, 154), False, ("Hotel.Audio.PhoneLineStatic",))
    if "SFX_DoorKnock203_v0" in sounds:
        add_audio("SFX_DoorKnock203_ManualTrigger_v0", sounds["SFX_DoorKnock203_v0"], (3920, 285, 150), False, ("Hotel.Audio.Room203Knock",))
    if "SFX_ReportLogFiled_v0" in sounds:
        add_audio("SFX_ReportLogFiled_FrontDesk_ManualTrigger_v0", sounds["SFX_ReportLogFiled_v0"], (-242, -500, 152), False, ("Hotel.Audio.ReportLogFiled",))

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)


def main() -> None:
    log("Preparing directories.")
    ensure_dirs()
    log("Generating project-authored placeholder WAV sources.")
    source_audio = generate_source_audio()
    log("Generating project-authored procedural OBJ meshes.")
    source_meshes = generate_source_meshes()
    log("Importing audio into /Game/Hotel/Audio.")
    sounds = import_audio(source_audio)
    log("Importing authored meshes into /Game/Hotel/Meshes.")
    meshes = import_static_meshes(source_meshes)
    log("Building production-intent hotel spine level.")
    build_level(sounds, meshes)
    log("Done.")


main()
