"""Capture PNG evidence from the hotel spine slice camera anchors.

Run with UnrealEditor-Cmd and -AllowCommandletRendering so PRs can attach
fresh visual evidence without relying on an interactive editor viewport.
"""

from __future__ import annotations

import os

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"
CAPTURE_DIR = os.path.join(unreal.Paths.project_saved_dir(), "Captures", "HotelSpineSlice")
WIDTH = 1280
HEIGHT = 720

CAPTURE_CAMERAS = [
    ("CAPTURE_FrontDesk_FirstSteamShotCandidate", "front_desk_first_steam_shot.png"),
    ("CAPTURE_GuestDoor_15SecondBeatCandidate", "guest_door_15_second_beat.png"),
    ("CAPTURE_MonitorToHall_MismatchCandidate", "monitor_to_hall_mismatch.png"),
]


def fail(message: str) -> None:
    raise RuntimeError(f"[HotelSpineCapture] {message}")


def get_world():
    if hasattr(unreal.EditorLevelLibrary, "get_editor_world"):
        world = unreal.EditorLevelLibrary.get_editor_world()
        if world:
            return world
    return unreal.EditorLevelLibrary.get_all_level_actors()[0].get_world()


def set_property(obj, name: str, value) -> bool:
    try:
        obj.set_editor_property(name, value)
        return True
    except Exception:
        try:
            setattr(obj, name, value)
            return True
        except Exception:
            return False


def get_camera_component(actor):
    if hasattr(actor, "get_camera_component"):
        return actor.get_camera_component()
    try:
        return actor.get_editor_property("camera_component")
    except Exception:
        return None


def get_capture_component(actor):
    if hasattr(actor, "get_capture_component2d"):
        return actor.get_capture_component2d()
    try:
        return actor.get_editor_property("capture_component2d")
    except Exception:
        return None


def find_actor_by_label(label: str):
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() == label:
            return actor
    return None


def color_energy(color) -> int:
    return int(getattr(color, "r", 0)) + int(getattr(color, "g", 0)) + int(getattr(color, "b", 0))


def capture_camera(world, camera_actor, filename: str) -> str:
    render_target = unreal.KismetRenderingLibrary.create_render_target2d(
        world,
        WIDTH,
        HEIGHT,
        unreal.TextureRenderTargetFormat.RTF_RGBA8_SRGB,
        unreal.LinearColor(0.0, 0.0, 0.0, 1.0),
        False,
        False,
    )
    if not render_target:
        fail("Unable to create render target.")

    capture_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SceneCapture2D,
        camera_actor.get_actor_location(),
        camera_actor.get_actor_rotation(),
    )
    capture_actor.set_actor_label(f"TEMP_EvidenceCapture_{camera_actor.get_actor_label()}")

    capture_component = get_capture_component(capture_actor)
    if not capture_component:
        fail("Unable to access SceneCapture2D component.")

    camera_component = get_camera_component(camera_actor)
    if camera_component:
        try:
            set_property(capture_component, "fov_angle", camera_component.get_editor_property("field_of_view"))
        except Exception:
            pass

    set_property(capture_component, "texture_target", render_target)
    set_property(capture_component, "capture_every_frame", False)
    set_property(capture_component, "capture_on_movement", False)
    set_property(capture_component, "capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
    set_property(capture_component, "primitive_render_mode", unreal.SceneCapturePrimitiveRenderMode.PRM_RENDER_SCENE_PRIMITIVES)

    unreal.KismetRenderingLibrary.clear_render_target2d(
        world,
        render_target,
        unreal.LinearColor(0.0, 0.0, 0.0, 1.0),
    )
    capture_component.capture_scene()

    samples = [
        unreal.KismetRenderingLibrary.read_render_target_pixel(world, render_target, WIDTH // 2, HEIGHT // 2),
        unreal.KismetRenderingLibrary.read_render_target_pixel(world, render_target, WIDTH // 3, HEIGHT // 3),
        unreal.KismetRenderingLibrary.read_render_target_pixel(world, render_target, (WIDTH * 2) // 3, HEIGHT // 3),
        unreal.KismetRenderingLibrary.read_render_target_pixel(world, render_target, WIDTH // 3, (HEIGHT * 2) // 3),
        unreal.KismetRenderingLibrary.read_render_target_pixel(world, render_target, (WIDTH * 2) // 3, (HEIGHT * 2) // 3),
    ]
    if max(color_energy(color) for color in samples) <= 8:
        fail(f"Capture from {camera_actor.get_actor_label()} appears black.")

    unreal.KismetRenderingLibrary.export_render_target(world, render_target, CAPTURE_DIR, filename)
    output_path = os.path.join(CAPTURE_DIR, filename)
    if not os.path.exists(output_path):
        fail(f"Missing exported PNG: {output_path}")
    if os.path.getsize(output_path) < 4096:
        fail(f"Exported PNG is unexpectedly small: {output_path}")

    unreal.EditorLevelLibrary.destroy_actor(capture_actor)
    unreal.log(f"[HotelSpineCapture] Wrote {output_path}")
    return output_path


unreal.EditorLevelLibrary.load_level(MAP_PATH)
os.makedirs(CAPTURE_DIR, exist_ok=True)
world = get_world()

outputs = []
for camera_label, output_filename in CAPTURE_CAMERAS:
    camera = find_actor_by_label(camera_label)
    if not camera:
        fail(f"Missing capture camera actor: {camera_label}")
    outputs.append(capture_camera(world, camera, output_filename))

unreal.log(f"[HotelSpineCapture] Captured {len(outputs)} PNG evidence files.")
