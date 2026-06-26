"""Verify the first hotel spine slice contains the intended product areas."""

from __future__ import annotations

import unreal


MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"

REQUIRED_ASSETS = [
    MAP_PATH,
    "/Game/Hotel/Audio/SFX_PhoneRing_v0",
    "/Game/Hotel/Audio/SFX_PhonePickup_v0",
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


def fail(message: str) -> None:
    raise RuntimeError(f"[HotelSpineVerify] {message}")


for asset_path in REQUIRED_ASSETS:
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        fail(f"Missing asset: {asset_path}")

unreal.EditorLevelLibrary.load_level(MAP_PATH)
labels = {actor.get_actor_label() for actor in unreal.EditorLevelLibrary.get_all_level_actors()}
missing_labels = [label for label in REQUIRED_ACTOR_LABELS if label not in labels]
if missing_labels:
    fail("Missing actors: " + ", ".join(missing_labels))

unreal.log(f"[HotelSpineVerify] Verified {len(REQUIRED_ASSETS)} assets and {len(REQUIRED_ACTOR_LABELS)} required actors.")
