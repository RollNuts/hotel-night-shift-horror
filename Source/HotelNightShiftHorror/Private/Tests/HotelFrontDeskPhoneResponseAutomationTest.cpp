#include "HotelNightShiftPawn.h"

#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/InputSettings.h"
#include "InputCoreTypes.h"
#include "Misc/AutomationTest.h"
#include "Tests/AutomationCommon.h"

#if WITH_DEV_AUTOMATION_TESTS

namespace
{
const TCHAR* HotelMapPath = TEXT("/Game/Hotel/Maps/L_HotelNightShift_Slice");
const FName PhoneTag(TEXT("Hotel.Interact.Phone"));
const FName MonitorTag(TEXT("Hotel.Interact.Monitor"));
const FName Room203DoorTag(TEXT("Hotel.Interact.Room203Door"));
const FName Room203DoorRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203Refusal"));
const FName Room203WallpaperFlutterTag(TEXT("Hotel.Feedback.Room203WallpaperFlutter"));
const FName ReportLogTag(TEXT("Hotel.Interact.ReportLog"));
const FName ReportLogFiledFeedbackTag(TEXT("Hotel.Feedback.ReportLogFiled"));
const FName PatrolListenAudioTag(TEXT("Hotel.Audio.PatrolListen"));
const FName ReturnRouteAudioTag(TEXT("Hotel.Audio.ReturnRoute"));
const FName PostReportMonitorMismatchAudioTag(TEXT("Hotel.Audio.PostReportMonitorMismatch"));
const FName PostReportDeskWaitAudioTag(TEXT("Hotel.Audio.PostReportDeskWait"));
const FName PostReportDeskWaitRattleTag(TEXT("Hotel.Feedback.PostReportDeskWaitRattle"));
const FName PostReportLogSelfCorrectionAudioTag(TEXT("Hotel.Audio.PostReportLogSelfCorrection"));
const FName PostReportLogSelfCorrectionFeedbackTag(TEXT("Hotel.Feedback.PostReportLogSelfCorrection"));
const TCHAR* AuthoredPhoneBodyLabel = TEXT("PROP_FrontDesk_Phone_AuthoredCurvedBody");
const TCHAR* AuthoredPhoneReceiverLabel = TEXT("PROP_FrontDesk_Phone_ReceiverAuthoredSilhouette");
const TCHAR* AuthoredPhoneCordLabel = TEXT("PROP_FrontDesk_Phone_AuthoredCoiledCord");
const TCHAR* AuthoredLedgerPagesLabel = TEXT("PROP_FrontDesk_ReportLog_AuthoredCurledPages");
const TCHAR* Room203DoorEdgeSlamShadowLabel = TEXT("PROP_GuestHall_Room203_DoorEdgeSlamShadowCue");
const TCHAR* Room203NoticeCornerJoltLabel = TEXT("PROP_GuestHall_Room203_NoticeCornerJoltCue");
const TCHAR* Room203AftershockLoosePaperLabel = TEXT("PROP_GuestHall_RightWall_Room203AftershockLoosePaper");
const TCHAR* Room203AftershockHighCurlLabel = TEXT("PROP_GuestHall_RightWall_Room203AftershockHighCurl");

AActor* FindActorByTag(UWorld* World, FName RequiredTag)
{
	if (!World)
	{
		return nullptr;
	}

	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (Actor && Actor->ActorHasTag(RequiredTag))
		{
			return Actor;
		}
	}
	return nullptr;
}

AActor* FindActorByLabel(UWorld* World, const TCHAR* RequiredLabel)
{
	if (!World)
	{
		return nullptr;
	}

	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (Actor && Actor->GetActorLabel() == RequiredLabel)
		{
			return Actor;
		}
	}
	return nullptr;
}

AHotelNightShiftPawn* FindHotelPawn(UWorld* World)
{
	if (!World)
	{
		return nullptr;
	}

	for (TActorIterator<AHotelNightShiftPawn> It(World); It; ++It)
	{
		AHotelNightShiftPawn* Pawn = *It;
		if (Pawn)
		{
			return Pawn;
		}
	}
	return nullptr;
}

bool HasInteractEKeyBinding()
{
	const UInputSettings* InputSettings = GetDefault<UInputSettings>();
	TArray<FInputActionKeyMapping> Mappings;
	InputSettings->GetActionMappingByName(TEXT("Interact"), Mappings);
	for (const FInputActionKeyMapping& Mapping : Mappings)
	{
		if (Mapping.Key == EKeys::E)
		{
			return true;
		}
	}
	return false;
}

float MaxRotationDeltaDegrees(const FRotator& From, const FRotator& To)
{
	const float PitchDelta = FMath::Abs(FRotator::NormalizeAxis(To.Pitch - From.Pitch));
	const float YawDelta = FMath::Abs(FRotator::NormalizeAxis(To.Yaw - From.Yaw));
	const float RollDelta = FMath::Abs(FRotator::NormalizeAxis(To.Roll - From.Roll));
	return FMath::Max(FMath::Max(PitchDelta, YawDelta), RollDelta);
}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHotelFrontDeskPhoneResponseLiveMapTest,
	"Hotel.FrontDesk.PhoneResponse.LiveMap",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FHotelFrontDeskPhoneResponseLiveMapTest::RunTest(const FString& Parameters)
{
	if (!TestTrue(TEXT("Interact is bound to E"), HasInteractEKeyBinding()))
	{
		return false;
	}

	if (!TestTrue(TEXT("Production hotel map opened"), AutomationOpenMap(HotelMapPath, true)))
	{
		return false;
	}

	ADD_LATENT_AUTOMATION_COMMAND(FWaitLatentCommand(0.25f));
	ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([this]()
	{
		UWorld* World = AutomationCommon::GetAnyGameWorld();
		if (!TestNotNull(TEXT("Game world is available"), World))
		{
			return true;
		}

		AHotelNightShiftPawn* Pawn = FindHotelPawn(World);
		if (!TestNotNull(TEXT("Hotel pawn spawned in production map"), Pawn))
		{
			return true;
		}

		AActor* Phone = FindActorByTag(World, PhoneTag);
		AActor* Monitor = FindActorByTag(World, MonitorTag);
		AActor* Room203Door = FindActorByTag(World, Room203DoorTag);
		AActor* Room203DoorFeedback = FindActorByTag(World, Room203DoorRefusalFeedbackTag);
		AActor* Room203WallpaperFlutter = FindActorByTag(World, Room203WallpaperFlutterTag);
		AActor* ReportLog = FindActorByTag(World, ReportLogTag);
		AActor* ReportLogFiledFeedback = FindActorByTag(World, ReportLogFiledFeedbackTag);
		AActor* PatrolListenSound = FindActorByTag(World, PatrolListenAudioTag);
		AActor* ReturnRouteSound = FindActorByTag(World, ReturnRouteAudioTag);
		AActor* PostReportMonitorMismatchSound = FindActorByTag(World, PostReportMonitorMismatchAudioTag);
		AActor* PostReportDeskWaitSound = FindActorByTag(World, PostReportDeskWaitAudioTag);
		AActor* PostReportDeskWaitRattle = FindActorByTag(World, PostReportDeskWaitRattleTag);
		AActor* PostReportLogSelfCorrectionSound = FindActorByTag(World, PostReportLogSelfCorrectionAudioTag);
		AActor* PostReportLogSelfCorrectionFeedback = FindActorByTag(World, PostReportLogSelfCorrectionFeedbackTag);
		AActor* AuthoredPhoneBody = FindActorByLabel(World, AuthoredPhoneBodyLabel);
		AActor* AuthoredPhoneReceiver = FindActorByLabel(World, AuthoredPhoneReceiverLabel);
		AActor* AuthoredPhoneCord = FindActorByLabel(World, AuthoredPhoneCordLabel);
		AActor* AuthoredLedgerPages = FindActorByLabel(World, AuthoredLedgerPagesLabel);
		AActor* Room203DoorEdgeSlamShadow = FindActorByLabel(World, Room203DoorEdgeSlamShadowLabel);
		AActor* Room203NoticeCornerJolt = FindActorByLabel(World, Room203NoticeCornerJoltLabel);
		AActor* Room203AftershockLoosePaper = FindActorByLabel(World, Room203AftershockLoosePaperLabel);
		AActor* Room203AftershockHighCurl = FindActorByLabel(World, Room203AftershockHighCurlLabel);

		TestNotNull(TEXT("Phone interaction actor exists"), Phone);
		TestNotNull(TEXT("Monitor interaction actor exists"), Monitor);
		TestNotNull(TEXT("Room 203 door interaction actor exists"), Room203Door);
		TestNotNull(TEXT("Room 203 door refusal feedback actor exists"), Room203DoorFeedback);
		TestNotNull(TEXT("Room 203 wallpaper aftershock feedback actor exists"), Room203WallpaperFlutter);
		TestNotNull(TEXT("Report log interaction actor exists"), ReportLog);
		TestNotNull(TEXT("Report log filed feedback actor exists"), ReportLogFiledFeedback);
		TestNotNull(TEXT("Patrol listen sound actor exists"), PatrolListenSound);
		TestNotNull(TEXT("Return route anomaly sound actor exists"), ReturnRouteSound);
		TestNotNull(TEXT("Post-report monitor mismatch sound actor exists"), PostReportMonitorMismatchSound);
		TestNotNull(TEXT("Post-report desk wait sound actor exists"), PostReportDeskWaitSound);
		TestNotNull(TEXT("Post-report desk wait rattle actor exists"), PostReportDeskWaitRattle);
		TestNotNull(TEXT("Post-report log self-correction sound actor exists"), PostReportLogSelfCorrectionSound);
		TestNotNull(TEXT("Post-report log self-correction feedback actor exists"), PostReportLogSelfCorrectionFeedback);
		TestNotNull(TEXT("Authored phone body mesh exists in production map"), AuthoredPhoneBody);
		TestNotNull(TEXT("Authored phone receiver mesh exists in production map"), AuthoredPhoneReceiver);
		TestNotNull(TEXT("Authored phone cord mesh exists in production map"), AuthoredPhoneCord);
		TestNotNull(TEXT("Authored curled ledger page mesh exists in production map"), AuthoredLedgerPages);
		TestNotNull(TEXT("Room 203 door-edge slam shadow exists in production map"), Room203DoorEdgeSlamShadow);
		TestNotNull(TEXT("Room 203 notice-corner jolt cue exists in production map"), Room203NoticeCornerJolt);
		TestNotNull(TEXT("Room 203 aftershock loose-paper mesh exists in production map"), Room203AftershockLoosePaper);
		TestNotNull(TEXT("Room 203 aftershock high-curl mesh exists in production map"), Room203AftershockHighCurl);
		if (!Phone || !Monitor || !Room203Door || !Room203DoorFeedback || !Room203WallpaperFlutter || !ReportLog || !ReportLogFiledFeedback || !PatrolListenSound || !ReturnRouteSound || !PostReportMonitorMismatchSound || !PostReportDeskWaitSound || !PostReportDeskWaitRattle || !PostReportLogSelfCorrectionSound || !PostReportLogSelfCorrectionFeedback || !AuthoredPhoneBody || !AuthoredPhoneReceiver || !AuthoredPhoneCord || !AuthoredLedgerPages || !Room203DoorEdgeSlamShadow || !Room203NoticeCornerJolt || !Room203AftershockLoosePaper || !Room203AftershockHighCurl)
		{
			return true;
		}

		TestEqual(TEXT("Initial loop stage is PhoneRinging"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::PhoneRinging);
		TestTrue(TEXT("Phone ring timer starts active"), Pawn->AutomationIsPhoneRingTimerActive());
		TestTrue(TEXT("Phone line static source is cached"), Pawn->AutomationHasPhoneLineSound());

		const FVector ReceiverRestLocation = Pawn->AutomationGetPhoneReceiverLocation();
		const FRotator ReceiverRestRotation = Pawn->AutomationGetPhoneReceiverRotation();
		const FVector AuthoredReceiverRestLocation = AuthoredPhoneReceiver->GetActorLocation();
		const FVector CordRestLocation = Pawn->AutomationGetPhoneCordTugLocation();
		TestTrue(TEXT("Authored coiled cord is cached for the phone pickup tug"), FVector::DistSquared(CordRestLocation, AuthoredPhoneCord->GetActorLocation()) < FMath::Square(2.0f));
		TestTrue(TEXT("Answering the phone succeeds"), Pawn->AutomationInteractWithActor(Phone));
		TestEqual(TEXT("Phone answer advances to RequestKnown"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::RequestKnown);
		TestFalse(TEXT("Phone ring timer stops after answer"), Pawn->AutomationIsPhoneRingTimerActive());
		TestTrue(TEXT("Phone line is connected after answer"), Pawn->AutomationIsPhoneLineConnected());

		Pawn->AutomationAdvancePhoneReceiver(0.06f);
		const FVector ReceiverAnticipationDelta = Pawn->AutomationGetPhoneReceiverLocation() - ReceiverRestLocation;
		TestTrue(TEXT("Receiver pickup has a visible contact anticipation"), ReceiverAnticipationDelta.SizeSquared() > FMath::Square(2.0f) && ReceiverAnticipationDelta.SizeSquared() < FMath::Square(10.0f));
		TestTrue(TEXT("Receiver anticipation moves against the final pickup direction"), ReceiverAnticipationDelta.X < 0.0f && ReceiverAnticipationDelta.Y > 0.0f && ReceiverAnticipationDelta.Z < 0.0f);
		TestTrue(TEXT("Receiver remains in active pickup after anticipation"), Pawn->AutomationIsPhoneReceiverLiftActive());

		Pawn->AutomationAdvancePhoneReceiver(0.18f);
		TestTrue(TEXT("Receiver active lift moves substantially from the cradle"), FVector::DistSquared(ReceiverRestLocation, Pawn->AutomationGetPhoneReceiverLocation()) > FMath::Square(18.0f));
		TestTrue(TEXT("Receiver active lift has readable rotation"), MaxRotationDeltaDegrees(ReceiverRestRotation, Pawn->AutomationGetPhoneReceiverRotation()) > 8.0f);
		TestTrue(TEXT("Receiver remains active during lift before settle"), Pawn->AutomationIsPhoneReceiverLiftActive());

		Pawn->AutomationAdvancePhoneReceiver(0.34f);
		TestTrue(TEXT("Receiver lift animation reaches the held pose"), Pawn->AutomationGetPhoneReceiverLiftAlpha() >= 1.0f);
		TestFalse(TEXT("Receiver pickup settles after the held pose"), Pawn->AutomationIsPhoneReceiverLiftActive());
		TestTrue(TEXT("Receiver moves visibly after answer"), FVector::DistSquared(ReceiverRestLocation, Pawn->AutomationGetPhoneReceiverLocation()) > FMath::Square(18.0f));
		TestTrue(TEXT("Authored receiver silhouette moves with the phone lift"), FVector::DistSquared(AuthoredReceiverRestLocation, AuthoredPhoneReceiver->GetActorLocation()) > FMath::Square(18.0f));
		TestTrue(TEXT("Authored coiled cord tugs with the lifted receiver"), FVector::DistSquared(CordRestLocation, Pawn->AutomationGetPhoneCordTugLocation()) > FMath::Square(5.0f));

		TestTrue(TEXT("Checking monitor succeeds"), Pawn->AutomationInteractWithActor(Monitor));
		TestEqual(TEXT("Monitor advances to MonitorChecked"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::MonitorChecked);
		TestFalse(TEXT("Phone line disconnects after monitor check"), Pawn->AutomationIsPhoneLineConnected());
		TestFalse(TEXT("Patrol listen is not already resolved"), Pawn->AutomationIsPatrolListenResolved());

		TestFalse(TEXT("Room 203 refusal is blocked before listening at the patrol line"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Early Room 203 attempt stays in MonitorChecked"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::MonitorChecked);

		Pawn->SetActorLocation(FVector(930.0f, 0.0f, 92.0f));
		Pawn->GetCharacterMovement()->Velocity = FVector(80.0f, 0.0f, 0.0f);
		Pawn->AutomationAdvancePatrolListen(1.30f);
		TestTrue(TEXT("Patrol listen anomaly starts even while moving through the taped line"), Pawn->AutomationIsPatrolListenActive());
		TestFalse(TEXT("Moving through the taped line does not resolve patrol listen"), Pawn->AutomationIsPatrolListenResolved());

		Pawn->SetActorLocation(FVector(1250.0f, 0.0f, 92.0f));
		Pawn->GetCharacterMovement()->Velocity = FVector::ZeroVector;
		Pawn->AutomationAdvancePatrolListen(1.30f);
		TestTrue(TEXT("Patrol listen anomaly remains active after leaving the taped line"), Pawn->AutomationIsPatrolListenActive());
		TestFalse(TEXT("Leaving the taped line prevents patrol listen resolution"), Pawn->AutomationIsPatrolListenResolved());

		Pawn->SetActorLocation(FVector(930.0f, 0.0f, 92.0f));
		Pawn->GetCharacterMovement()->Velocity = FVector::ZeroVector;
		Pawn->AutomationAdvancePatrolListen(0.05f);
		TestTrue(TEXT("Patrol listen anomaly continues at the taped line"), Pawn->AutomationIsPatrolListenActive());
		TestFalse(TEXT("Patrol listen does not resolve instantly"), Pawn->AutomationIsPatrolListenResolved());
		Pawn->AutomationAdvancePatrolListen(1.30f);
		TestTrue(TEXT("Holding still at the taped line resolves patrol listen"), Pawn->AutomationIsPatrolListenResolved());
		TestFalse(TEXT("Patrol listen anomaly stops after resolution"), Pawn->AutomationIsPatrolListenActive());

		const FVector DoorLatchRestLocation = Pawn->AutomationGetDoorRefusalLatchLocation();
		const FVector DoorChainRestLocation = Pawn->AutomationGetDoorRefusalChainLocation();
		const FVector DoorSurfaceRestLocation = Pawn->AutomationGetDoorRefusalSurfaceLocation();
		const FVector DoorWallpaperRestLocation = Pawn->AutomationGetDoorRefusalWallpaperFlutterLocation();
		TestTrue(TEXT("Room 203 loose wallpaper is cached for aftershock motion"), DoorWallpaperRestLocation.SizeSquared() > 0.0f);
		TestTrue(TEXT("Refusing Room 203 succeeds"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Door refusal advances to DoorRefused"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::DoorRefused);
		Pawn->AutomationAdvanceDoorRefusalFeedback(0.09f);
		TestTrue(TEXT("Room 203 refusal feedback starts"), Pawn->AutomationGetDoorRefusalFeedbackAlpha() > 0.0f);
		const float EarlyLatchMove = FVector::Dist(DoorLatchRestLocation, Pawn->AutomationGetDoorRefusalLatchLocation());
		const float EarlyChainMove = FVector::Dist(DoorChainRestLocation, Pawn->AutomationGetDoorRefusalChainLocation());
		TestTrue(TEXT("Room 203 latch jolts before the chain catches"), EarlyLatchMove > 8.0f && EarlyLatchMove > EarlyChainMove + 4.0f);
		TestTrue(TEXT("Room 203 refusal remains active after latch contact"), Pawn->AutomationIsDoorRefusalFeedbackActive());
		Pawn->AutomationAdvanceDoorRefusalFeedback(0.16f);
		TestTrue(TEXT("Room 203 chain catches after the latch"), FVector::DistSquared(DoorChainRestLocation, Pawn->AutomationGetDoorRefusalChainLocation()) > FMath::Square(5.0f));
		TestTrue(TEXT("Room 203 door-surface cue reacts without opening the door"), FVector::DistSquared(DoorSurfaceRestLocation, Pawn->AutomationGetDoorRefusalSurfaceLocation()) > FMath::Square(2.0f));
		Pawn->AutomationAdvanceDoorRefusalFeedback(0.28f);
		TestTrue(TEXT("Room 203 loose wallpaper reacts after the door impact"), FVector::DistSquared(DoorWallpaperRestLocation, Pawn->AutomationGetDoorRefusalWallpaperFlutterLocation()) > FMath::Square(2.0f));
		TestTrue(TEXT("Room 203 refusal remains active through the wallpaper aftershock"), Pawn->AutomationIsDoorRefusalFeedbackActive());
		Pawn->AutomationAdvanceDoorRefusalFeedback(0.96f);
		TestTrue(TEXT("Room 203 refusal feedback reaches completion"), Pawn->AutomationGetDoorRefusalFeedbackAlpha() >= 1.0f);
		TestFalse(TEXT("Room 203 refusal feedback settles after the non-human aftershock"), Pawn->AutomationIsDoorRefusalFeedbackActive());
		TestTrue(TEXT("Room 203 latch returns to rest"), FVector::DistSquared(DoorLatchRestLocation, Pawn->AutomationGetDoorRefusalLatchLocation()) < FMath::Square(1.5f));
		TestTrue(TEXT("Room 203 chain returns to rest"), FVector::DistSquared(DoorChainRestLocation, Pawn->AutomationGetDoorRefusalChainLocation()) < FMath::Square(1.5f));
		TestTrue(TEXT("Room 203 door-surface cue returns to rest"), FVector::DistSquared(DoorSurfaceRestLocation, Pawn->AutomationGetDoorRefusalSurfaceLocation()) < FMath::Square(1.5f));
		TestTrue(TEXT("Room 203 loose wallpaper returns to rest"), FVector::DistSquared(DoorWallpaperRestLocation, Pawn->AutomationGetDoorRefusalWallpaperFlutterLocation()) < FMath::Square(1.5f));

		TestFalse(TEXT("Report filing is blocked before the return route anomaly resolves"), Pawn->AutomationInteractWithActor(ReportLog));
		TestEqual(TEXT("Early report attempt remains DoorRefused"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::DoorRefused);
		TestFalse(TEXT("Return route anomaly is not already resolved"), Pawn->AutomationIsReturnRouteAnomalyResolved());

		Pawn->SetActorLocation(FVector(2860.0f, 0.0f, 92.0f));
		Pawn->AutomationAdvanceReturnRouteAnomaly(0.10f);
		TestTrue(TEXT("Return route anomaly starts in the guest hall"), Pawn->AutomationIsReturnRouteAnomalyActive());
		TestFalse(TEXT("Return route anomaly does not resolve instantly"), Pawn->AutomationIsReturnRouteAnomalyResolved());
		Pawn->AutomationAdvanceReturnRouteAnomaly(1.00f);
		TestTrue(TEXT("Return route anomaly resolves after the hallway answer"), Pawn->AutomationIsReturnRouteAnomalyResolved());
		TestFalse(TEXT("Return route anomaly stops after resolution"), Pawn->AutomationIsReturnRouteAnomalyActive());
		TestEqual(TEXT("Return route clear stage enables report filing"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReturnRouteCleared);

		const FVector ReportFiledRestLocation = Pawn->AutomationGetReportLogFiledFeedbackLocation();
		TestTrue(TEXT("Filing report succeeds"), Pawn->AutomationInteractWithActor(ReportLog));
		TestEqual(TEXT("Report advances to ReportFiled"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);
		Pawn->AutomationAdvanceReportLogFiledFeedback(0.12f);
		TestTrue(TEXT("Report filed feedback starts"), Pawn->AutomationGetReportLogFiledFeedbackAlpha() > 0.0f);
		TestTrue(TEXT("Report filed stamp feedback moves visibly"), FVector::DistSquared(ReportFiledRestLocation, Pawn->AutomationGetReportLogFiledFeedbackLocation()) > FMath::Square(2.0f));

		TestTrue(TEXT("Monitor recheck after report succeeds"), Pawn->AutomationInteractWithActor(Monitor));
		TestEqual(TEXT("Monitor recheck keeps ReportFiled as the terminal loop stage"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);
		TestTrue(TEXT("Post-report monitor mismatch feedback starts"), Pawn->AutomationIsPostReportMonitorMismatchActive());
		Pawn->AutomationAdvancePostReportMonitorMismatch(1.20f);
		TestFalse(TEXT("Post-report monitor mismatch feedback settles"), Pawn->AutomationIsPostReportMonitorMismatchActive());
		TestFalse(TEXT("Post-report log self-correction is blocked before desk wait resolves"), Pawn->AutomationInteractWithActor(ReportLog));
		TestFalse(TEXT("Post-report log has not self-corrected before desk wait"), Pawn->AutomationHasPostReportLogSelfCorrection());
		TestFalse(TEXT("Post-report desk wait has not fired before waiting"), Pawn->AutomationIsPostReportDeskWaitResolved());
		Pawn->SetActorLocation(FVector(780.0f, 0.0f, 92.0f));
		Pawn->GetCharacterMovement()->Velocity = FVector::ZeroVector;
		Pawn->AutomationAdvancePostReportDeskWait(1.40f);
		TestFalse(TEXT("Post-report desk wait does not fire away from the counter"), Pawn->AutomationIsPostReportDeskWaitResolved());
		Pawn->SetActorLocation(FVector(-260.0f, -635.0f, 92.0f));
		Pawn->GetCharacterMovement()->Velocity = FVector::ZeroVector;
		Pawn->AutomationAdvancePostReportDeskWait(1.40f);
		TestTrue(TEXT("Post-report desk wait anomaly starts after holding at the counter"), Pawn->AutomationIsPostReportDeskWaitActive());
		TestTrue(TEXT("Post-report desk wait anomaly is one-shot resolved"), Pawn->AutomationIsPostReportDeskWaitResolved());
		TestEqual(TEXT("Desk wait anomaly keeps ReportFiled as the terminal loop stage"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);
		TestFalse(TEXT("Post-report log self-correction waits while lobby glass feedback is active"), Pawn->AutomationInteractWithActor(ReportLog));
		const FVector PostReportDeskWaitRattleRestLocation = Pawn->AutomationGetPostReportDeskWaitRattleLocation();
		Pawn->AutomationAdvancePostReportDeskWait(0.10f);
		TestTrue(TEXT("Post-report lobby door rattle moves visibly"), FVector::DistSquared(PostReportDeskWaitRattleRestLocation, Pawn->AutomationGetPostReportDeskWaitRattleLocation()) > FMath::Square(2.0f));
		Pawn->AutomationAdvancePostReportDeskWait(1.20f);
		TestFalse(TEXT("Post-report desk wait feedback settles"), Pawn->AutomationIsPostReportDeskWaitActive());
		TestTrue(TEXT("Post-report lobby door rattle returns to rest"), FVector::DistSquared(PostReportDeskWaitRattleRestLocation, Pawn->AutomationGetPostReportDeskWaitRattleLocation()) < FMath::Square(0.5f));
		const FVector PostReportLogCorrectionRestLocation = Pawn->AutomationGetPostReportLogSelfCorrectionLocation();
		TestTrue(TEXT("Post-report log self-correction succeeds after the lobby wait settles"), Pawn->AutomationInteractWithActor(ReportLog));
		TestTrue(TEXT("Post-report log self-correction feedback starts"), Pawn->AutomationIsPostReportLogSelfCorrectionActive());
		TestTrue(TEXT("Post-report log has self-corrected once"), Pawn->AutomationHasPostReportLogSelfCorrection());
		TestEqual(TEXT("Post-report log self-correction keeps ReportFiled terminal"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);
		Pawn->AutomationAdvancePostReportLogSelfCorrection(0.22f);
		TestTrue(TEXT("Post-report log self-correction alpha advances"), Pawn->AutomationGetPostReportLogSelfCorrectionAlpha() > 0.0f);
		TestTrue(TEXT("Post-report self-correction line moves visibly"), FVector::DistSquared(PostReportLogCorrectionRestLocation, Pawn->AutomationGetPostReportLogSelfCorrectionLocation()) > FMath::Square(2.0f));
		Pawn->AutomationAdvancePostReportLogSelfCorrection(0.30f);
		TestFalse(TEXT("Post-report log self-correction feedback settles"), Pawn->AutomationIsPostReportLogSelfCorrectionActive());
		TestFalse(TEXT("Post-report log self-correction is one-shot"), Pawn->AutomationInteractWithActor(ReportLog));
		TestFalse(TEXT("Door cannot regress after post-report mismatch"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Stage remains ReportFiled after door retry"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);

		return true;
	}));

	return true;
}

#endif
