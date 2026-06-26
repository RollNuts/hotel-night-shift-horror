"""Verify the first hotel spine slice contains the intended product areas."""

from __future__ import annotations

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"

REQUIRED_ASSETS = [
    MAP_PATH,
    "/Game/Hotel/Audio/SFX_PhoneRing_v0",
    "/Game/Hotel/Audio/SFX_PhonePickup_v0",
    "/Game/Hotel/Audio/SFX_PhoneLineStatic_v0",
    "/Game/Hotel/Audio/SFX_DoorKnock203_v0",
    "/Game/Hotel/Audio/AMB_LobbyFluorescentHum_v0",
    "/Game/Hotel/Audio/AMB_GuestHallDrone_v0",
    "/Game/Hotel/Materials/M_Hotel_WornFloor_v0",
    "/Game/Hotel/Materials/M_Hotel_AgedWall_v0",
    "/Game/Hotel/Materials/M_Hotel_RoomDoorPaint_v0",
    "/Game/Hotel/Materials/M_Hotel_FluorescentPanelGlow_v0",
    "/Game/Hotel/Materials/M_Hotel_MonitorGreenGlow_v0",
    "/Game/Hotel/Cinematics/LS_HotelSpine_Stills",
    "/Game/Hotel/Cinematics/MRQ_HotelEvidencePng",
]

REQUIRED_ACTOR_LABELS = [
    "PLAYERSTART_FrontDesk_FacingPhoneAndMonitor",
    "PROP_FrontDesk_Phone_AnswerLoopPlaceholder",
    "PROP_FrontDesk_Phone_ReceiverCue",
    "PROP_FrontDesk_Phone_CradleShadow",
    "PROP_FrontDesk_Phone_CoiledCordCue",
    "LIGHTMESH_FrontDesk_PhoneCallLamp",
    "PROP_Surveillance_Monitor_PlayerChecksHall",
    "PROP_ReportLog_ReturnAndRecordPoint",
    "AREA_FrontDesk_Ceiling_LowPressure",
    "AREA_Transition_CarpetRun_ToGuestHall_NoVoid",
    "AREA_Transition_LeftSightlineWall_ToGuestHall",
    "AREA_Transition_RightSightlineWall_ToGuestHall",
    "TRANSITION_Elevator_Door_AudibleBeforeSeen",
    "TRANSITION_EmergencyStair_Door_AlternateRoute",
    "AREA_GuestHall_Floor_OneDoorSlice",
    "PROP_GuestHall_RoomDoor203_OpenRefuseDecision",
    "PROP_GuestHall_Room203_LeftDoorJamb",
    "PROP_GuestHall_Room203_RightDoorJamb",
    "PROP_GuestHall_Room203_TopDoorJamb",
    "PROP_GuestHall_Room203_DarkLatchGap",
    "SFX_PhoneRing_FrontDesk_ManualTrigger_v0",
    "SFX_PhonePickup_FrontDesk_ManualTrigger_v0",
    "SFX_PhoneLineStatic_FrontDesk_ConnectedCue_v0",
    "SFX_DoorKnock203_ManualTrigger_v0",
    "AMB_Lobby_FluorescentHum_Source_v0",
    "AMB_GuestHall_Drone_Source_v0",
    "CAPTURE_FrontDesk_FirstSteamShotCandidate",
    "CAPTURE_PhoneResponse_LiftReceiverCandidate",
    "CAPTURE_GuestDoor_15SecondBeatCandidate",
    "CAPTURE_MonitorToHall_MismatchCandidate",
    "LIGHTMESH_FrontDesk_OverheadFluorescent",
    "LIGHTMESH_GuestHall_FluorescentPanelA",
    "LIGHTMESH_GuestHall_FluorescentPanelB",
    "LIGHT_FrontDesk_WorkSurfacePracticalFill",
    "LIGHT_FrontDesk_PhoneCallLampPulse",
    "LIGHT_FrontDesk_CaptureEvidenceSoftFill",
    "LIGHT_GuestHall_Room203PlatePractical",
    "LIGHT_GuestHall_CaptureEvidenceDoorFill",
    "LIGHT_MonitorToHall_CaptureEvidenceGreenFill",
    "PPV_HotelNightShift_ReadableHorrorExposure",
]

REQUIRED_ACTOR_TAGS = {
    "PROP_FrontDesk_Phone_AnswerLoopPlaceholder": ["Hotel.Interact.Phone"],
    "PROP_FrontDesk_Phone_ReceiverCue": ["Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"],
    "LIGHTMESH_FrontDesk_PhoneCallLamp": ["Hotel.Feedback.PhoneRingLamp", "Hotel.Capture.Readability"],
    "PROP_Surveillance_Monitor_PlayerChecksHall": ["Hotel.Interact.Monitor"],
    "PROP_GuestHall_RoomDoor203_OpenRefuseDecision": ["Hotel.Interact.Room203Door"],
    "PROP_ReportLog_ReturnAndRecordPoint": ["Hotel.Interact.ReportLog"],
    "LIGHT_FrontDesk_PhoneCallLampPulse": ["Hotel.Feedback.PhoneRingLamp", "Hotel.Capture.Readability"],
    "SFX_PhoneRing_FrontDesk_ManualTrigger_v0": ["Hotel.Audio.PhoneRing"],
    "SFX_PhonePickup_FrontDesk_ManualTrigger_v0": ["Hotel.Audio.PhonePickup"],
    "SFX_PhoneLineStatic_FrontDesk_ConnectedCue_v0": ["Hotel.Audio.PhoneLineStatic"],
}

REQUIRED_AUDIO_LABELS = [
    "SFX_PhoneRing_FrontDesk_ManualTrigger_v0",
    "SFX_PhonePickup_FrontDesk_ManualTrigger_v0",
    "SFX_PhoneLineStatic_FrontDesk_ConnectedCue_v0",
    "SFX_DoorKnock203_ManualTrigger_v0",
    "AMB_Lobby_FluorescentHum_Source_v0",
    "AMB_GuestHall_Drone_Source_v0",
]

MOVABLE_STATIC_MESH_LABELS = [
    "PROP_FrontDesk_Phone_ReceiverCue",
]


def fail(message: str) -> None:
    raise RuntimeError(f"[HotelSpineVerify] {message}")


for asset_path in REQUIRED_ASSETS:
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        fail(f"Missing asset: {asset_path}")

unreal.EditorLevelLibrary.load_level(MAP_PATH)
actors_by_label = {actor.get_actor_label(): actor for actor in unreal.EditorLevelLibrary.get_all_level_actors()}
labels = set(actors_by_label)
missing_labels = [label for label in REQUIRED_ACTOR_LABELS if label not in labels]
if missing_labels:
    fail("Missing actors: " + ", ".join(missing_labels))

for label, expected_tags in REQUIRED_ACTOR_TAGS.items():
    actor = actors_by_label.get(label)
    if actor is None:
        fail(f"Missing tagged actor: {label}")
    actual_tags = {str(tag) for tag in actor.tags}
    missing_tags = [tag for tag in expected_tags if tag not in actual_tags]
    if missing_tags:
        fail(f"Actor {label} is missing tags: {', '.join(missing_tags)}")

for label in REQUIRED_AUDIO_LABELS:
    actor = actors_by_label.get(label)
    if actor is None:
        fail(f"Missing audio actor: {label}")
    try:
        audio_component = actor.get_editor_property("audio_component")
    except Exception as exc:
        fail(f"Actor {label} has no audio_component: {exc}")
    if audio_component is None:
        fail(f"Actor {label} has no audio component")
    if not audio_component.get_editor_property("sound"):
        fail(f"Actor {label} has no sound assigned")
    if label.startswith("SFX_") and audio_component.get_editor_property("auto_activate"):
        fail(f"One-shot cue {label} must not auto activate")

for label in MOVABLE_STATIC_MESH_LABELS:
    actor = actors_by_label.get(label)
    component = actor.static_mesh_component if actor is not None and hasattr(actor, "static_mesh_component") else None
    if component is None:
        fail(f"Actor {label} must have a static mesh component")
    if component.get_editor_property("mobility") != unreal.ComponentMobility.MOVABLE:
        fail(f"Actor {label} must be movable for live receiver feedback")

unreal.log(
    f"[HotelSpineVerify] Verified {len(REQUIRED_ASSETS)} assets, "
    f"{len(REQUIRED_ACTOR_LABELS)} required actors, {len(REQUIRED_ACTOR_TAGS)} tagged actors, "
    f"{len(REQUIRED_AUDIO_LABELS)} audio actors, and {len(MOVABLE_STATIC_MESH_LABELS)} movable feedback meshes."
)
