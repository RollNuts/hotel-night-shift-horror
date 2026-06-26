#include "HotelNightShiftPawn.h"

#include "Engine/World.h"
#include "EngineUtils.h"
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
const FName ReportLogTag(TEXT("Hotel.Interact.ReportLog"));

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
		AActor* ReportLog = FindActorByTag(World, ReportLogTag);

		TestNotNull(TEXT("Phone interaction actor exists"), Phone);
		TestNotNull(TEXT("Monitor interaction actor exists"), Monitor);
		TestNotNull(TEXT("Room 203 door interaction actor exists"), Room203Door);
		TestNotNull(TEXT("Report log interaction actor exists"), ReportLog);
		if (!Phone || !Monitor || !Room203Door || !ReportLog)
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

		TestTrue(TEXT("Refusing Room 203 succeeds"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Door refusal advances to DoorRefused"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::DoorRefused);

		TestTrue(TEXT("Filing report succeeds"), Pawn->AutomationInteractWithActor(ReportLog));
		TestEqual(TEXT("Report advances to ReportFiled"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);

		TestFalse(TEXT("Monitor cannot regress after report"), Pawn->AutomationInteractWithActor(Monitor));
		TestEqual(TEXT("Stage remains ReportFiled after monitor retry"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);
		TestFalse(TEXT("Door cannot regress after report"), Pawn->AutomationInteractWithActor(Room203Door));
		TestEqual(TEXT("Stage remains ReportFiled after door retry"), Pawn->AutomationGetLoopStage(), EHotelLoopStage::ReportFiled);

		return true;
	}));

	return true;
}

#endif
