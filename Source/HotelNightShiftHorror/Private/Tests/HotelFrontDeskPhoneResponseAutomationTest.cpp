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
const FName ReportLogTag(TEXT("Hotel.Interact.ReportLog"));
const FName ReportLogFiledFeedbackTag(TEXT("Hotel.Feedback.ReportLogFiled"));
const FName PatrolListenAudioTag(TEXT("Hotel.Audio.PatrolListen"));
const FName ReturnRouteAudioTag(TEXT("Hotel.Audio.ReturnRoute"));

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
		AActor* ReportLog = FindActorByTag(World, ReportLogTag);
		AActor* ReportLogFiledFeedback = FindActorByTag(World, ReportLogFiledFeedbackTag);
		AActor* PatrolListenSound = FindActorByTag(World, PatrolListenAudioTag);
		AActor* ReturnRouteSound = FindActorByTag(World, ReturnRouteAudioTag);

		TestNotNull(TEXT("Phone interaction actor exists"), Phone);
		TestNotNull(TEXT("Monitor interaction actor exists"), Monitor);
		TestNotNull(TEXT("Room 203 door interaction actor exists"), Room203Door);
		TestNotNull(TEXT("Room 203 door refusal feedback actor exists"), Room203DoorFeedback);
		TestNotNull(TEXT("Report log interaction actor exists"), ReportLog);
		TestNotNull(TEXT("Report log filed feedback actor exists"), ReportLogFiledFeedback);
		TestNotNull(TEXT("Patrol listen sound actor exists"), PatrolListenSound);
		TestNotNull(TEXT("Return route anomaly sound actor exists"), ReturnRouteSound);
		if (!Phone || !Monitor || !Room203Door || !Room203DoorFeedback || !ReportLog || !ReportLogFiledFeedback || !PatrolListenSound || !ReturnRouteSound)
		{
			return true;
		}

		TestEqual(TEXT("Initial loop stage is PhoneRinging"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::PhoneRinging);
		TestTrue(TEXT("Phone ring timer starts active"), Pawn->AutomationIsPhoneRingTimerActive());
		TestTrue(TEXT("Phone line static source is cached"), Pawn->AutomationHasPhoneLineSound());

		const FVector ReceiverRestLocation = Pawn->AutomationGetPhoneReceiverLocation();
		TestTrue(TEXT("Answering the phone succeeds"), Pawn->AutomationInteractWithActor(Phone));
		TestEqual(TEXT("Phone answer advances to RequestKnown"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::RequestKnown);
		TestFalse(TEXT("Phone ring timer stops after answer"), Pawn->AutomationIsPhoneRingTimerActive());
		TestTrue(TEXT("Phone line is connected after answer"), Pawn->AutomationIsPhoneLineConnected());

		Pawn->AutomationAdvancePhoneReceiver(0.50f);
		TestTrue(TEXT("Receiver lift animation reaches the held pose"), Pawn->AutomationGetPhoneReceiverLiftAlpha() >= 1.0f);
		TestTrue(TEXT("Receiver moves visibly after answer"), FVector::DistSquared(ReceiverRestLocation, Pawn->AutomationGetPhoneReceiverLocation()) > FMath::Square(18.0f));

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

		const FVector DoorFeedbackRestLocation = Pawn->AutomationGetDoorRefusalFeedbackLocation();
		TestTrue(TEXT("Refusing Room 203 succeeds"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Door refusal advances to DoorRefused"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::DoorRefused);
		Pawn->AutomationAdvanceDoorRefusalFeedback(0.12f);
		TestTrue(TEXT("Room 203 refusal feedback starts"), Pawn->AutomationGetDoorRefusalFeedbackAlpha() > 0.0f);
		TestTrue(TEXT("Room 203 latch feedback moves visibly"), FVector::DistSquared(DoorFeedbackRestLocation, Pawn->AutomationGetDoorRefusalFeedbackLocation()) > FMath::Square(2.0f));

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

		TestFalse(TEXT("Monitor cannot regress after report"), Pawn->AutomationInteractWithActor(Monitor));
		TestEqual(TEXT("Stage remains ReportFiled after monitor retry"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);
		TestFalse(TEXT("Door cannot regress after report"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Stage remains ReportFiled after door retry"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);

		return true;
	}));

	return true;
}

#endif
