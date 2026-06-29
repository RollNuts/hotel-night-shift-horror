#include "HotelNightShiftPawn.h"

#include "Camera/CameraComponent.h"
#include "Components/AudioComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/LightComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/AmbientSound.h"

namespace
{
const FVector PhoneAnchor(-430.0f, -525.0f, 128.0f);
const FVector MonitorAnchor(-620.0f, -525.0f, 160.0f);
const FVector Door203Anchor(3920.0f, 302.0f, 120.0f);
const FVector ReportLogAnchor(-255.0f, -522.0f, 128.0f);
const FVector PhoneSoundAnchor(-430.0f, -525.0f, 150.0f);
const FVector PhonePickupSoundAnchor(-430.0f, -548.0f, 150.0f);
const FVector PhoneLineSoundAnchor(-438.0f, -552.0f, 154.0f);
const FVector PhoneReceiverAnchor(-430.0f, -558.0f, 150.0f);
const FVector PhoneIndicatorLightAnchor(-395.0f, -555.0f, 158.0f);
const FVector DoorKnockSoundAnchor(3920.0f, 285.0f, 150.0f);
const FVector DoorRefusalFeedbackAnchor(4020.0f, 258.0f, 150.0f);
const FVector ReportFiledSoundAnchor(-242.0f, -500.0f, 152.0f);
const FVector ReportLogFiledFeedbackAnchor(-232.0f, -503.0f, 145.0f);
const FVector PatrolListenAnchor(930.0f, 0.0f, 92.0f);
const FVector PatrolListenSoundAnchor(930.0f, 0.0f, 72.0f);
const FVector PatrolListenLightAnchor(955.0f, 0.0f, 115.0f);
const FVector ReturnRouteAnchor(2860.0f, 0.0f, 92.0f);
const FVector ReturnRouteSoundAnchor(3420.0f, 270.0f, 150.0f);
const FVector ReturnRouteLightAnchor(2860.0f, -90.0f, 188.0f);
const FVector PostReportMonitorMismatchSoundAnchor(-620.0f, -542.0f, 172.0f);
const FVector PostReportMonitorMismatchLightAnchor(-575.0f, -555.0f, 188.0f);
const FVector PostReportDeskWaitAnchor(-260.0f, -635.0f, 92.0f);
const FVector PostReportDeskWaitSoundAnchor(1080.0f, -250.0f, 150.0f);
const FVector PostReportDeskWaitLightAnchor(1035.0f, -250.0f, 170.0f);
const FVector PostReportDeskWaitRattleAnchor(1055.0f, -250.0f, 150.0f);
const FVector PostReportLogSelfCorrectionSoundAnchor(-214.0f, -494.0f, 154.0f);
const FVector PostReportLogSelfCorrectionFeedbackAnchor(-202.0f, -510.0f, 146.0f);
const FVector PostReportLogSelfCorrectionLightAnchor(-190.0f, -520.0f, 166.0f);
const FVector HallTargetLightAnchor(3920.0f, 0.0f, 260.0f);
const FName PhoneInteractTag(TEXT("Hotel.Interact.Phone"));
const FName PhoneReceiverTag(TEXT("Hotel.Feedback.PhoneReceiver"));
const FName PhoneLineAudioTag(TEXT("Hotel.Audio.PhoneLineStatic"));
const FName MonitorInteractTag(TEXT("Hotel.Interact.Monitor"));
const FName Room203DoorInteractTag(TEXT("Hotel.Interact.Room203Door"));
const FName Room203DoorRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203Refusal"));
const FName ReportLogInteractTag(TEXT("Hotel.Interact.ReportLog"));
const FName ReportLogFiledFeedbackTag(TEXT("Hotel.Feedback.ReportLogFiled"));
const FName ReportLogFiledAudioTag(TEXT("Hotel.Audio.ReportLogFiled"));
const FName PatrolListenAudioTag(TEXT("Hotel.Audio.PatrolListen"));
const FName PatrolListenLightTag(TEXT("Hotel.Feedback.PatrolListenLight"));
const FName ReturnRouteAudioTag(TEXT("Hotel.Audio.ReturnRoute"));
const FName ReturnRouteLightTag(TEXT("Hotel.Feedback.ReturnRouteLight"));
const FName PostReportMonitorMismatchAudioTag(TEXT("Hotel.Audio.PostReportMonitorMismatch"));
const FName PostReportMonitorMismatchLightTag(TEXT("Hotel.Feedback.PostReportMonitorMismatchLight"));
const FName PostReportDeskWaitAudioTag(TEXT("Hotel.Audio.PostReportDeskWait"));
const FName PostReportDeskWaitLightTag(TEXT("Hotel.Feedback.PostReportDeskWaitLight"));
const FName PostReportDeskWaitRattleTag(TEXT("Hotel.Feedback.PostReportDeskWaitRattle"));
const FName PostReportLogSelfCorrectionAudioTag(TEXT("Hotel.Audio.PostReportLogSelfCorrection"));
const FName PostReportLogSelfCorrectionFeedbackTag(TEXT("Hotel.Feedback.PostReportLogSelfCorrection"));
const FName PostReportLogSelfCorrectionLightTag(TEXT("Hotel.Feedback.PostReportLogSelfCorrectionLight"));
}

AHotelNightShiftPawn::AHotelNightShiftPawn()
{
	PrimaryActorTick.bCanEverTick = true;

	GetCapsuleComponent()->InitCapsuleSize(34.0f, 88.0f);
	GetCharacterMovement()->MaxWalkSpeed = 255.0f;
	GetCharacterMovement()->BrakingDecelerationWalking = 900.0f;

	FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
	FirstPersonCamera->SetupAttachment(GetCapsuleComponent());
	FirstPersonCamera->SetRelativeLocation(FVector(0.0f, 0.0f, 68.0f));
	FirstPersonCamera->bUsePawnControlRotation = true;

	bUseControllerRotationYaw = true;
}

void AHotelNightShiftPawn::BeginPlay()
{
	Super::BeginPlay();

	CacheHotelActors();
	SetWorkState(
		EHotelLoopStage::PhoneRinging,
		TEXT("Answer the front-desk phone before leaving the counter."),
		TEXT("The call lamp is the only warm thing in the lobby."),
		TEXT("DESK LINE: RINGING / NO CALLER ID"),
		0.12f);
	StartPhoneRing();
}

void AHotelNightShiftPawn::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	UpdateLookTarget();
	UpdatePatrolListenAnomaly(DeltaSeconds);
	UpdateReturnRouteAnomaly(DeltaSeconds);
	UpdatePostReportMonitorMismatch(DeltaSeconds);
	UpdatePostReportDeskWaitAnomaly(DeltaSeconds);
	UpdatePostReportLogSelfCorrection(DeltaSeconds);
	UpdatePhoneRingVisual(DeltaSeconds);
	UpdatePhoneReceiverAnimation(DeltaSeconds);
	UpdateDoorRefusalFeedback(DeltaSeconds);
	UpdateReportLogFiledFeedback(DeltaSeconds);
}

void AHotelNightShiftPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &AHotelNightShiftPawn::MoveForward);
	PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &AHotelNightShiftPawn::MoveRight);
	PlayerInputComponent->BindAxis(TEXT("Turn"), this, &AHotelNightShiftPawn::Turn);
	PlayerInputComponent->BindAxis(TEXT("LookUp"), this, &AHotelNightShiftPawn::LookUp);
	PlayerInputComponent->BindAction(TEXT("Interact"), IE_Pressed, this, &AHotelNightShiftPawn::Interact);
}

FText AHotelNightShiftPawn::GetObjectiveText() const
{
	return FText::FromString(ObjectiveText);
}

FText AHotelNightShiftPawn::GetWorkMessageText() const
{
	return FText::FromString(WorkMessageText);
}

FText AHotelNightShiftPawn::GetDeskStatusText() const
{
	return FText::FromString(DeskStatusText);
}

FText AHotelNightShiftPawn::GetInteractionPromptText() const
{
	return FText::FromString(InteractionPromptText);
}

float AHotelNightShiftPawn::GetFearPressure() const
{
	return FearPressure;
}

#if WITH_DEV_AUTOMATION_TESTS
EHotelLoopStage AHotelNightShiftPawn::AutomationGetLoopStage() const
{
	return LoopStage;
}

bool AHotelNightShiftPawn::AutomationInteractWithActor(AActor* TargetActor)
{
	return TryInteractWithActor(TargetActor);
}

bool AHotelNightShiftPawn::AutomationIsPhoneRingTimerActive() const
{
	return GetWorldTimerManager().IsTimerActive(PhoneRingTimerHandle);
}

bool AHotelNightShiftPawn::AutomationIsPhoneLineConnected() const
{
	return bPhoneLineConnected;
}

bool AHotelNightShiftPawn::AutomationHasPhoneLineSound() const
{
	const AAmbientSound* PhoneLineSound = Cast<AAmbientSound>(PhoneLineSoundActor);
	const UAudioComponent* AudioComponent = PhoneLineSound ? PhoneLineSound->GetAudioComponent() : nullptr;
	return AudioComponent && AudioComponent->Sound;
}

bool AHotelNightShiftPawn::AutomationIsPatrolListenActive() const
{
	return bPatrolListenActive;
}

bool AHotelNightShiftPawn::AutomationIsPatrolListenResolved() const
{
	return bPatrolListenResolved;
}

void AHotelNightShiftPawn::AutomationAdvancePatrolListen(float DeltaSeconds)
{
	UpdatePatrolListenAnomaly(DeltaSeconds);
}

bool AHotelNightShiftPawn::AutomationIsReturnRouteAnomalyActive() const
{
	return bReturnRouteAnomalyActive;
}

bool AHotelNightShiftPawn::AutomationIsReturnRouteAnomalyResolved() const
{
	return bReturnRouteAnomalyResolved;
}

void AHotelNightShiftPawn::AutomationAdvanceReturnRouteAnomaly(float DeltaSeconds)
{
	UpdateReturnRouteAnomaly(DeltaSeconds);
}

bool AHotelNightShiftPawn::AutomationIsPostReportMonitorMismatchActive() const
{
	return bPostReportMonitorMismatchActive;
}

void AHotelNightShiftPawn::AutomationAdvancePostReportMonitorMismatch(float DeltaSeconds)
{
	UpdatePostReportMonitorMismatch(DeltaSeconds);
}

bool AHotelNightShiftPawn::AutomationIsPostReportDeskWaitActive() const
{
	return bPostReportDeskWaitActive;
}

bool AHotelNightShiftPawn::AutomationIsPostReportDeskWaitResolved() const
{
	return bPostReportDeskWaitResolved;
}

void AHotelNightShiftPawn::AutomationAdvancePostReportDeskWait(float DeltaSeconds)
{
	UpdatePostReportDeskWaitAnomaly(DeltaSeconds);
}

FVector AHotelNightShiftPawn::AutomationGetPostReportDeskWaitRattleLocation() const
{
	return PostReportDeskWaitRattleActor ? PostReportDeskWaitRattleActor->GetActorLocation() : FVector::ZeroVector;
}

bool AHotelNightShiftPawn::AutomationIsPostReportLogSelfCorrectionActive() const
{
	return bPostReportLogSelfCorrectionActive;
}

bool AHotelNightShiftPawn::AutomationHasPostReportLogSelfCorrection() const
{
	return bPostReportLogSelfCorrectionObserved;
}

void AHotelNightShiftPawn::AutomationAdvancePostReportLogSelfCorrection(float DeltaSeconds)
{
	UpdatePostReportLogSelfCorrection(DeltaSeconds);
}

float AHotelNightShiftPawn::AutomationGetPostReportLogSelfCorrectionAlpha() const
{
	return PostReportLogSelfCorrectionAlpha;
}

FVector AHotelNightShiftPawn::AutomationGetPostReportLogSelfCorrectionLocation() const
{
	return PostReportLogSelfCorrectionFeedbackActor ? PostReportLogSelfCorrectionFeedbackActor->GetActorLocation() : FVector::ZeroVector;
}

void AHotelNightShiftPawn::AutomationAdvancePhoneReceiver(float DeltaSeconds)
{
	UpdatePhoneReceiverAnimation(DeltaSeconds);
}

float AHotelNightShiftPawn::AutomationGetPhoneReceiverLiftAlpha() const
{
	return PhoneReceiverLiftAlpha;
}

FVector AHotelNightShiftPawn::AutomationGetPhoneReceiverLocation() const
{
	return PhoneReceiverActor ? PhoneReceiverActor->GetActorLocation() : FVector::ZeroVector;
}

void AHotelNightShiftPawn::AutomationAdvanceDoorRefusalFeedback(float DeltaSeconds)
{
	UpdateDoorRefusalFeedback(DeltaSeconds);
}

float AHotelNightShiftPawn::AutomationGetDoorRefusalFeedbackAlpha() const
{
	return DoorRefusalFeedbackAlpha;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalFeedbackLocation() const
{
	return DoorRefusalFeedbackActor ? DoorRefusalFeedbackActor->GetActorLocation() : FVector::ZeroVector;
}

void AHotelNightShiftPawn::AutomationAdvanceReportLogFiledFeedback(float DeltaSeconds)
{
	UpdateReportLogFiledFeedback(DeltaSeconds);
}

float AHotelNightShiftPawn::AutomationGetReportLogFiledFeedbackAlpha() const
{
	return ReportLogFiledFeedbackAlpha;
}

FVector AHotelNightShiftPawn::AutomationGetReportLogFiledFeedbackLocation() const
{
	return ReportLogFiledFeedbackActor ? ReportLogFiledFeedbackActor->GetActorLocation() : FVector::ZeroVector;
}
#endif

void AHotelNightShiftPawn::MoveForward(float Value)
{
	if (!FMath::IsNearlyZero(Value))
	{
		const FRotator ControlRotation(0.0f, GetControlRotation().Yaw, 0.0f);
		AddMovementInput(ControlRotation.Vector(), Value);
	}
}

void AHotelNightShiftPawn::MoveRight(float Value)
{
	if (!FMath::IsNearlyZero(Value))
	{
		const FRotator ControlRotation(0.0f, GetControlRotation().Yaw, 0.0f);
		const FVector Right = FRotationMatrix(ControlRotation).GetScaledAxis(EAxis::Y);
		AddMovementInput(Right, Value);
	}
}

void AHotelNightShiftPawn::Turn(float Value)
{
	AddControllerYawInput(Value);
}

void AHotelNightShiftPawn::LookUp(float Value)
{
	AddControllerPitchInput(Value);
}

void AHotelNightShiftPawn::Interact()
{
	TryInteractWithActor(CurrentLookActor);
}

bool AHotelNightShiftPawn::TryInteractWithActor(AActor* TargetActor)
{
	if (!TargetActor)
	{
		return false;
	}

	if (ActorMatches(TargetActor, PhoneAnchor, 90.0f, PhoneInteractTag) && LoopStage == EHotelLoopStage::PhoneRinging)
	{
		StopPhoneRing();
		LiftPhoneReceiver();
		PlayActorSound(PhonePickupSoundActor);
		StartPhoneLineAudio();
		SetPhoneIndicatorIntensity(96.0f);

		SetWorkState(
			EHotelLoopStage::RequestKnown,
			TEXT("Room 203 request: check the monitor before you leave the desk."),
			TEXT("The receiver clicks open. A thin voice says: 'Room 203. Do not open unless the hallway camera agrees.'"),
			TEXT("DESK LINE: CONNECTED / ROOM 203"),
			0.34f);
		return true;
	}

	if (ActorMatches(TargetActor, MonitorAnchor, 130.0f, MonitorInteractTag) && LoopStage == EHotelLoopStage::RequestKnown)
	{
		bMonitorChecked = true;
		StopPhoneLineAudio();
		PulseHallLight(85.0f);
		SetWorkState(
			EHotelLoopStage::MonitorChecked,
			TEXT("Cross the taped line, listen, then go to Room 203."),
			TEXT("Monitor feed: empty hallway. The call says that should be impossible."),
			TEXT("DESK LINE: HOLDING / CAMERA MISMATCH"),
			0.54f);
		return true;
	}

	if (
		ActorMatches(TargetActor, Door203Anchor, 190.0f, Room203DoorInteractTag)
		&& (LoopStage == EHotelLoopStage::RequestKnown || LoopStage == EHotelLoopStage::MonitorChecked))
	{
		if (LoopStage == EHotelLoopStage::MonitorChecked && !bPatrolListenResolved)
		{
			if (!bPatrolListenActive)
			{
				PlayActorSound(PatrolListenSoundActor);
			}
			SetWorkState(
				EHotelLoopStage::MonitorChecked,
				TEXT("Return to the taped line and listen before Room 203."),
				TEXT("The elevator clicks behind you. You moved through the split too fast."),
				TEXT("PATROL: LISTEN REQUIRED / DO NOT RUSH"),
				0.68f);
			SetPatrolListenLightIntensity(1450.0f);
			return false;
		}

		PlayActorSound(DoorKnockSoundActor);
		PulseHallLight(24.0f);
		TriggerDoorRefusalFeedback();
		SetWorkState(
			EHotelLoopStage::DoorRefused,
			TEXT("Return through the guest hall. Do not write the report until the hall quiets."),
			bMonitorChecked
				? TEXT("Room 203 knocks after you refuse. The monitor still showed nobody.")
				: TEXT("Room 203 knocks before you checked the camera. That mistake now matters."),
			TEXT("DESK LINE: SILENT / RETURN UNCONFIRMED"),
			0.76f);
		return true;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::DoorRefused && !bReturnRouteAnomalyResolved)
	{
		SetWorkState(
			EHotelLoopStage::DoorRefused,
			TEXT("Do the return walk first. Record it only after the hall answers."),
			TEXT("Your pen stops above the log. The hallway has not finished with the refusal."),
			TEXT("DESK LINE: REPORT LOCKED / RETURN PENDING"),
			0.81f);
		return false;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReturnRouteCleared)
	{
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Entry filed. Check the monitor once before waiting."),
			TEXT("Night log: 203 refused, hallway camera mismatch, knock confirmed."),
			TEXT("DESK LINE: CLOSED / CAMERA CHECK REQUIRED"),
			0.63f);
		StopPhoneLineAudio();
		PlayActorSound(ReportFiledSoundActor);
		TriggerReportLogFiledFeedback();
		return true;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportMonitorMismatchObserved)
	{
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Check the monitor once before touching the filed entry again."),
			TEXT("The log is filed. The camera is the part that has not answered yet."),
			TEXT("NIGHT LOG: FILED / CAMERA CHECK REQUIRED"),
			0.70f);
		return false;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportDeskWaitResolved)
	{
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Stay at the desk. Recheck the log only after the lobby quiets."),
			TEXT("The filed page will not lie still while the glass is still moving."),
			TEXT("NIGHT LOG: HOLD / LOBBY UNRESOLVED"),
			0.90f);
		return false;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && bPostReportDeskWaitActive)
	{
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Keep your hands off the log until the glass is still."),
			TEXT("The page edge lifts as if the lobby rattle moved through the counter."),
			TEXT("NIGHT LOG: WAIT / DOOR STILL ACTIVE"),
			0.92f);
		return false;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && bPostReportDeskWaitResolved && !bPostReportLogSelfCorrectionObserved)
	{
		TriggerPostReportLogSelfCorrection();
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Do not correct the new line. Wait for the next call."),
			TEXT("The filed entry adds a line you did not write: ROOM 203 OPEN / NO GUEST AT LOBBY."),
			TEXT("NIGHT LOG: SELF-CORRECTED / DO NOT ALTER"),
			0.96f);
		return true;
	}

	if (ActorMatches(TargetActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && bPostReportLogSelfCorrectionObserved)
	{
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Keep the desk. Wait for the next call."),
			TEXT("The added line stays in the log no matter how long you look at it."),
			TEXT("NIGHT LOG: LOCKED / NEXT CALL PENDING"),
			0.82f);
		return false;
	}

	if (ActorMatches(TargetActor, MonitorAnchor, 130.0f, MonitorInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportMonitorMismatchObserved)
	{
		TriggerPostReportMonitorMismatch();
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Stay at the desk. Do not answer the hallway."),
			TEXT("The camera feed updates late: Room 203 is open in the monitor, but the hallway stayed closed behind you."),
			TEXT("CAMERA FEED: DELAYED / ROOM 203 OPEN"),
			0.88f);
		return true;
	}

	return false;
}

void AHotelNightShiftPawn::CacheHotelActors()
{
	PhoneRingSoundActor = FindAudioActorNear(PhoneSoundAnchor, 90.0f);
	PhonePickupSoundActor = FindAudioActorNear(PhonePickupSoundAnchor, 80.0f);
	PhoneLineSoundActor = FindActorWithTagNear(PhoneLineAudioTag, PhoneLineSoundAnchor, 90.0f);
	PhoneReceiverActors.Reset();
	for (AActor* ReceiverPart : FindActorsWithTagNear(PhoneReceiverTag, PhoneReceiverAnchor, 120.0f))
	{
		PhoneReceiverActors.Add(ReceiverPart);
	}
	PhoneReceiverActor = FindActorWithTagNear(PhoneReceiverTag, PhoneReceiverAnchor, 120.0f);
	DoorKnockSoundActor = FindAudioActorNear(DoorKnockSoundAnchor, 140.0f);
	DoorRefusalFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203DoorRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f))
	{
		DoorRefusalFeedbackActors.Add(FeedbackPart);
	}
	DoorRefusalFeedbackActor = FindActorWithTagNear(Room203DoorRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f);
	ReportFiledSoundActor = FindActorWithTagNear(ReportLogFiledAudioTag, ReportFiledSoundAnchor, 120.0f);
	ReportLogFiledFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(ReportLogFiledFeedbackTag, ReportLogFiledFeedbackAnchor, 150.0f))
	{
		ReportLogFiledFeedbackActors.Add(FeedbackPart);
	}
	ReportLogFiledFeedbackActor = FindActorWithTagNear(ReportLogFiledFeedbackTag, ReportLogFiledFeedbackAnchor, 150.0f);
	PatrolListenSoundActor = FindActorWithTagNear(PatrolListenAudioTag, PatrolListenSoundAnchor, 120.0f);
	PatrolListenLightActor = FindActorWithTagNear(PatrolListenLightTag, PatrolListenLightAnchor, 120.0f);
	ReturnRouteSoundActor = FindActorWithTagNear(ReturnRouteAudioTag, ReturnRouteSoundAnchor, 220.0f);
	ReturnRouteLightActor = FindActorWithTagNear(ReturnRouteLightTag, ReturnRouteLightAnchor, 180.0f);
	PostReportMonitorMismatchSoundActor = FindActorWithTagNear(PostReportMonitorMismatchAudioTag, PostReportMonitorMismatchSoundAnchor, 120.0f);
	PostReportMonitorMismatchLightActor = FindActorWithTagNear(PostReportMonitorMismatchLightTag, PostReportMonitorMismatchLightAnchor, 160.0f);
	PostReportDeskWaitSoundActor = FindActorWithTagNear(PostReportDeskWaitAudioTag, PostReportDeskWaitSoundAnchor, 180.0f);
	PostReportDeskWaitLightActor = FindActorWithTagNear(PostReportDeskWaitLightTag, PostReportDeskWaitLightAnchor, 220.0f);
	PostReportDeskWaitRattleActors.Reset();
	for (AActor* RattlePart : FindActorsWithTagNear(PostReportDeskWaitRattleTag, PostReportDeskWaitRattleAnchor, 240.0f))
	{
		PostReportDeskWaitRattleActors.Add(RattlePart);
	}
	PostReportDeskWaitRattleActor = FindActorWithTagNear(PostReportDeskWaitRattleTag, PostReportDeskWaitRattleAnchor, 240.0f);
	PostReportLogSelfCorrectionSoundActor = FindActorWithTagNear(PostReportLogSelfCorrectionAudioTag, PostReportLogSelfCorrectionSoundAnchor, 140.0f);
	PostReportLogSelfCorrectionFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(PostReportLogSelfCorrectionFeedbackTag, PostReportLogSelfCorrectionFeedbackAnchor, 160.0f))
	{
		PostReportLogSelfCorrectionFeedbackActors.Add(FeedbackPart);
	}
	PostReportLogSelfCorrectionFeedbackActor = FindActorWithTagNear(PostReportLogSelfCorrectionFeedbackTag, PostReportLogSelfCorrectionFeedbackAnchor, 160.0f);
	PostReportLogSelfCorrectionLightActor = FindActorWithTagNear(PostReportLogSelfCorrectionLightTag, PostReportLogSelfCorrectionLightAnchor, 170.0f);
	HallTargetLightActor = FindLightActorNear(HallTargetLightAnchor, 260.0f);
	PhoneIndicatorLightActor = FindLightActorNear(PhoneIndicatorLightAnchor, 90.0f);

	if (PhoneReceiverActor)
	{
		PhoneReceiverRestLocation = PhoneReceiverActor->GetActorLocation();
		PhoneReceiverRestRotation = PhoneReceiverActor->GetActorRotation();
		PhoneReceiverLiftLocation = PhoneReceiverRestLocation + FVector(48.0f, -20.0f, 28.0f);
		PhoneReceiverLiftRotation = PhoneReceiverRestRotation + FRotator(-18.0f, 6.0f, -24.0f);
	}

	PhoneReceiverPartRestLocations.Reset();
	PhoneReceiverPartRestRotations.Reset();
	for (AActor* ReceiverPart : PhoneReceiverActors)
	{
		PhoneReceiverPartRestLocations.Add(ReceiverPart->GetActorLocation());
		PhoneReceiverPartRestRotations.Add(ReceiverPart->GetActorRotation());
	}

	DoorRefusalFeedbackRestLocations.Reset();
	DoorRefusalFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalFeedbackActors)
	{
		DoorRefusalFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	ReportLogFiledFeedbackRestLocations.Reset();
	ReportLogFiledFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : ReportLogFiledFeedbackActors)
	{
		ReportLogFiledFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		ReportLogFiledFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	PostReportDeskWaitRattleRestLocations.Reset();
	PostReportDeskWaitRattleRestRotations.Reset();
	for (AActor* RattlePart : PostReportDeskWaitRattleActors)
	{
		PostReportDeskWaitRattleRestLocations.Add(RattlePart->GetActorLocation());
		PostReportDeskWaitRattleRestRotations.Add(RattlePart->GetActorRotation());
	}

	PostReportLogSelfCorrectionFeedbackRestLocations.Reset();
	PostReportLogSelfCorrectionFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : PostReportLogSelfCorrectionFeedbackActors)
	{
		PostReportLogSelfCorrectionFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		PostReportLogSelfCorrectionFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
	}
}

void AHotelNightShiftPawn::UpdateLookTarget()
{
	InteractionPromptText.Empty();
	CurrentLookActor = nullptr;

	FHitResult Hit;
	const FVector Start = FirstPersonCamera->GetComponentLocation();
	const FVector End = Start + FirstPersonCamera->GetForwardVector() * 240.0f;
	FCollisionQueryParams Params(SCENE_QUERY_STAT(HotelInteractTrace), false, this);

	if (!GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		return;
	}

	AActor* HitActor = Hit.GetActor();
	if (!HitActor)
	{
		return;
	}

	if (ActorMatches(HitActor, PhoneAnchor, 90.0f, PhoneInteractTag) && LoopStage == EHotelLoopStage::PhoneRinging)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Lift receiver");
	}
	else if (ActorMatches(HitActor, MonitorAnchor, 130.0f, MonitorInteractTag) && LoopStage == EHotelLoopStage::RequestKnown)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Check camera feed");
	}
	else if (ActorMatches(HitActor, MonitorAnchor, 130.0f, MonitorInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportMonitorMismatchObserved)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Recheck camera feed");
	}
	else if (
		ActorMatches(HitActor, Door203Anchor, 190.0f, Room203DoorInteractTag)
		&& (LoopStage == EHotelLoopStage::RequestKnown || LoopStage == EHotelLoopStage::MonitorChecked))
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Refuse and keep closed");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::DoorRefused && !bReturnRouteAnomalyResolved)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Return walk incomplete");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReturnRouteCleared)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Record incident");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportMonitorMismatchObserved)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Check monitor first");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportDeskWaitResolved)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Wait before reviewing log");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && !bPostReportLogSelfCorrectionObserved)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Recheck filed entry");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::ReportFiled && bPostReportLogSelfCorrectionObserved)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Review corrected entry");
	}
}

void AHotelNightShiftPawn::StartPhoneRing()
{
	PhoneRingCount = 0;
	PhoneRingVisualClock = 0.0f;
	PlayPhoneRing();
	GetWorldTimerManager().SetTimer(PhoneRingTimerHandle, this, &AHotelNightShiftPawn::PlayPhoneRing, 3.2f, true);
}

void AHotelNightShiftPawn::PlayPhoneRing()
{
	if (LoopStage == EHotelLoopStage::PhoneRinging)
	{
		++PhoneRingCount;
		FearPressure = FMath::Clamp(0.12f + (PhoneRingCount - 1) * 0.04f, 0.12f, 0.28f);
		if (PhoneRingCount >= 3)
		{
			WorkMessageText = TEXT("The third ring makes the empty lobby feel occupied.");
			DeskStatusText = TEXT("DESK LINE: RINGING / URGENT");
		}
		if (AAmbientSound* PhoneSound = Cast<AAmbientSound>(PhoneRingSoundActor))
		{
			if (UAudioComponent* AudioComponent = PhoneSound->GetAudioComponent())
			{
				AudioComponent->Stop();
				AudioComponent->Play();
			}
		}
	}
}

void AHotelNightShiftPawn::StopPhoneRing()
{
	GetWorldTimerManager().ClearTimer(PhoneRingTimerHandle);
	if (AAmbientSound* PhoneSound = Cast<AAmbientSound>(PhoneRingSoundActor))
	{
		if (UAudioComponent* AudioComponent = PhoneSound->GetAudioComponent())
		{
			AudioComponent->Stop();
		}
	}
}

void AHotelNightShiftPawn::StartPhoneLineAudio()
{
	bPhoneLineConnected = true;
	if (AAmbientSound* PhoneLineSound = Cast<AAmbientSound>(PhoneLineSoundActor))
	{
		if (UAudioComponent* AudioComponent = PhoneLineSound->GetAudioComponent())
		{
			AudioComponent->Stop();
			AudioComponent->Play();
		}
	}
}

void AHotelNightShiftPawn::StopPhoneLineAudio()
{
	bPhoneLineConnected = false;
	if (AAmbientSound* PhoneLineSound = Cast<AAmbientSound>(PhoneLineSoundActor))
	{
		if (UAudioComponent* AudioComponent = PhoneLineSound->GetAudioComponent())
		{
			AudioComponent->Stop();
		}
	}
}

void AHotelNightShiftPawn::PlayActorSound(AActor* SoundActor) const
{
	const AAmbientSound* AmbientSound = Cast<AAmbientSound>(SoundActor);
	if (!AmbientSound)
	{
		return;
	}

	const UAudioComponent* AudioComponent = AmbientSound->GetAudioComponent();
	if (AudioComponent && AudioComponent->Sound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, AudioComponent->Sound, AmbientSound->GetActorLocation());
	}
}

void AHotelNightShiftPawn::UpdatePatrolListenAnomaly(float DeltaSeconds)
{
	if (LoopStage != EHotelLoopStage::MonitorChecked || bPatrolListenResolved)
	{
		return;
	}

	const bool bNearListenLine = IsActorNear(this, PatrolListenAnchor, 235.0f);
	if (bNearListenLine && !bPatrolListenActive)
	{
		StartPatrolListenAnomaly();
	}

	if (!bPatrolListenActive)
	{
		return;
	}

	PatrolListenPulseClock += DeltaSeconds;
	const float Pulse = 0.5f + 0.5f * FMath::Sin(PatrolListenPulseClock * 8.0f);
	SetPatrolListenLightIntensity(520.0f + Pulse * 1250.0f);

	if (!bNearListenLine)
	{
		PatrolListenHoldSeconds = 0.0f;
		ObjectiveText = TEXT("Return to the taped line and listen before Room 203.");
		WorkMessageText = TEXT("The sound thins out when you leave the mark.");
		DeskStatusText = TEXT("PATROL: LISTEN LOST / RETURN");
		return;
	}

	if (GetVelocity().SizeSquared2D() <= FMath::Square(12.0f))
	{
		PatrolListenHoldSeconds += DeltaSeconds;
	}
	else
	{
		PatrolListenHoldSeconds = FMath::Max(0.0f, PatrolListenHoldSeconds - DeltaSeconds * 1.5f);
	}

	if (PatrolListenHoldSeconds >= 1.25f)
	{
		ResolvePatrolListenAnomaly();
	}
}

void AHotelNightShiftPawn::StartPatrolListenAnomaly()
{
	bPatrolListenActive = true;
	PatrolListenHoldSeconds = 0.0f;
	PatrolListenPulseClock = 0.0f;
	PlayActorSound(PatrolListenSoundActor);
	SetWorkState(
		EHotelLoopStage::MonitorChecked,
		TEXT("Hold at the taped line and listen."),
		TEXT("The elevator groans, then the stairwell answers from the wrong side."),
		TEXT("PATROL: HOLD POSITION / LISTEN"),
		0.70f);
	SetPatrolListenLightIntensity(1600.0f);
}

void AHotelNightShiftPawn::ResolvePatrolListenAnomaly()
{
	bPatrolListenActive = false;
	bPatrolListenResolved = true;
	PatrolListenHoldSeconds = 0.0f;
	PlayActorSound(PatrolListenSoundActor);
	SetWorkState(
		EHotelLoopStage::MonitorChecked,
		TEXT("Go to Room 203 and keep the door closed."),
		TEXT("The stairwell breathes twice. The right move is to continue, not hurry."),
		TEXT("PATROL: LISTENED / ROUTE CLEARED"),
		0.66f);
	SetPatrolListenLightIntensity(820.0f);
}

void AHotelNightShiftPawn::UpdateReturnRouteAnomaly(float DeltaSeconds)
{
	if (LoopStage != EHotelLoopStage::DoorRefused || bReturnRouteAnomalyResolved)
	{
		return;
	}

	const bool bNearReturnRoute = IsActorNear(this, ReturnRouteAnchor, 260.0f);
	if (bNearReturnRoute && !bReturnRouteAnomalyActive)
	{
		StartReturnRouteAnomaly();
	}

	if (!bReturnRouteAnomalyActive)
	{
		return;
	}

	ReturnRoutePulseClock += DeltaSeconds;
	ReturnRouteAnomalySeconds += DeltaSeconds;
	const float Pulse = 0.5f + 0.5f * FMath::Sin(ReturnRoutePulseClock * 9.5f);
	SetReturnRouteLightIntensity(280.0f + Pulse * 1550.0f);

	if (ReturnRouteAnomalySeconds >= 0.95f)
	{
		ResolveReturnRouteAnomaly();
	}
}

void AHotelNightShiftPawn::StartReturnRouteAnomaly()
{
	bReturnRouteAnomalyActive = true;
	ReturnRouteAnomalySeconds = 0.0f;
	ReturnRoutePulseClock = 0.0f;
	PlayActorSound(ReturnRouteSoundActor);
	SetWorkState(
		EHotelLoopStage::DoorRefused,
		TEXT("Keep moving. Write the report only after this hallway quiets."),
		TEXT("The knock returns from behind you, then arrives ahead of you."),
		TEXT("RETURN ROUTE: LISTEN / DO NOT RUN"),
		0.84f);
	SetReturnRouteLightIntensity(1600.0f);
}

void AHotelNightShiftPawn::ResolveReturnRouteAnomaly()
{
	bReturnRouteAnomalyActive = false;
	bReturnRouteAnomalyResolved = true;
	ReturnRouteAnomalySeconds = 0.0f;
	SetWorkState(
		EHotelLoopStage::ReturnRouteCleared,
		TEXT("Return to the front desk and record the refusal."),
		TEXT("The hallway goes still. The report can be written now."),
		TEXT("DESK LINE: SILENT / REFUSAL READY TO LOG"),
		0.72f);
	SetReturnRouteLightIntensity(640.0f);
}

void AHotelNightShiftPawn::TriggerPostReportMonitorMismatch()
{
	bPostReportMonitorMismatchActive = true;
	bPostReportMonitorMismatchObserved = true;
	PostReportMonitorMismatchSeconds = 0.0f;
	PostReportMonitorMismatchPulseClock = 0.0f;
	PlayActorSound(PostReportMonitorMismatchSoundActor);
	SetPostReportMonitorMismatchLightIntensity(1900.0f);
}

void AHotelNightShiftPawn::UpdatePostReportMonitorMismatch(float DeltaSeconds)
{
	if (!bPostReportMonitorMismatchActive)
	{
		return;
	}

	PostReportMonitorMismatchSeconds += DeltaSeconds;
	PostReportMonitorMismatchPulseClock += DeltaSeconds;
	const float Pulse = 0.5f + 0.5f * FMath::Sin(PostReportMonitorMismatchPulseClock * 13.0f);
	SetPostReportMonitorMismatchLightIntensity(360.0f + Pulse * 1650.0f);

	if (PostReportMonitorMismatchSeconds >= 1.10f)
	{
		bPostReportMonitorMismatchActive = false;
		PostReportMonitorMismatchSeconds = 0.0f;
		SetPostReportMonitorMismatchLightIntensity(780.0f);
	}
}

void AHotelNightShiftPawn::TriggerPostReportDeskWaitAnomaly()
{
	bPostReportDeskWaitActive = true;
	bPostReportDeskWaitResolved = true;
	PostReportDeskWaitHoldSeconds = 0.0f;
	PostReportDeskWaitSeconds = 0.0f;
	PostReportDeskWaitPulseClock = 0.0f;
	PlayActorSound(PostReportDeskWaitSoundActor);
	SetWorkState(
		EHotelLoopStage::ReportFiled,
		TEXT("Remain behind the counter. Do not open the lobby door."),
		TEXT("The lobby glass rattles once from the outside. No guest appears in the monitor."),
		TEXT("LOBBY DOOR: HOLD CLOSED / NO GUEST"),
		0.93f);
	SetPostReportDeskWaitLightIntensity(2100.0f);
}

void AHotelNightShiftPawn::UpdatePostReportDeskWaitAnomaly(float DeltaSeconds)
{
	if (LoopStage != EHotelLoopStage::ReportFiled || !bPostReportMonitorMismatchObserved)
	{
		return;
	}

	if (bPostReportDeskWaitActive)
	{
		PostReportDeskWaitSeconds += DeltaSeconds;
		PostReportDeskWaitPulseClock += DeltaSeconds;
		const float Pulse = 0.5f + 0.5f * FMath::Sin(PostReportDeskWaitPulseClock * 11.5f);
		SetPostReportDeskWaitLightIntensity(220.0f + Pulse * 1880.0f);
		const float RattleAlpha = FMath::Clamp(PostReportDeskWaitSeconds / 1.25f, 0.0f, 1.0f);
		const float RattleKick = FMath::Sin(RattleAlpha * UE_PI * 8.0f) * (1.0f - RattleAlpha);
		const FVector RattleOffset(0.0f, RattleKick * 14.0f, FMath::Abs(RattleKick) * 3.0f);
		const FRotator RattleRotation(RattleKick * 8.0f, 0.0f, RattleKick * 5.0f);

		for (int32 Index = 0; Index < PostReportDeskWaitRattleActors.Num(); ++Index)
		{
			AActor* RattlePart = PostReportDeskWaitRattleActors[Index];
			if (!RattlePart || !PostReportDeskWaitRattleRestLocations.IsValidIndex(Index) || !PostReportDeskWaitRattleRestRotations.IsValidIndex(Index))
			{
				continue;
			}

			RattlePart->SetActorLocationAndRotation(
				PostReportDeskWaitRattleRestLocations[Index] + RattleOffset,
				PostReportDeskWaitRattleRestRotations[Index] + RattleRotation);
		}

		if (PostReportDeskWaitSeconds >= 1.25f)
		{
			bPostReportDeskWaitActive = false;
			PostReportDeskWaitSeconds = 0.0f;
			SetPostReportDeskWaitLightIntensity(360.0f);
			for (int32 Index = 0; Index < PostReportDeskWaitRattleActors.Num(); ++Index)
			{
				AActor* RattlePart = PostReportDeskWaitRattleActors[Index];
				if (!RattlePart || !PostReportDeskWaitRattleRestLocations.IsValidIndex(Index) || !PostReportDeskWaitRattleRestRotations.IsValidIndex(Index))
				{
					continue;
				}

				RattlePart->SetActorLocationAndRotation(
					PostReportDeskWaitRattleRestLocations[Index],
					PostReportDeskWaitRattleRestRotations[Index]);
			}
		}
		return;
	}

	if (bPostReportDeskWaitResolved || bPostReportMonitorMismatchActive)
	{
		return;
	}

	const bool bWaitingAtDesk = IsActorNear(this, PostReportDeskWaitAnchor, 300.0f);
	if (bWaitingAtDesk && GetVelocity().SizeSquared2D() <= FMath::Square(16.0f))
	{
		PostReportDeskWaitHoldSeconds += DeltaSeconds;
	}
	else
	{
		PostReportDeskWaitHoldSeconds = 0.0f;
	}

	if (PostReportDeskWaitHoldSeconds >= 1.35f)
	{
		TriggerPostReportDeskWaitAnomaly();
	}
}

void AHotelNightShiftPawn::TriggerPostReportLogSelfCorrection()
{
	bPostReportLogSelfCorrectionActive = true;
	bPostReportLogSelfCorrectionObserved = true;
	PostReportLogSelfCorrectionAlpha = 0.0f;
	PostReportLogSelfCorrectionPulseClock = 0.0f;
	PlayActorSound(PostReportLogSelfCorrectionSoundActor);
	SetPostReportLogSelfCorrectionLightIntensity(1450.0f);
}

void AHotelNightShiftPawn::UpdatePostReportLogSelfCorrection(float DeltaSeconds)
{
	if (!bPostReportLogSelfCorrectionActive)
	{
		return;
	}

	PostReportLogSelfCorrectionAlpha = FMath::Clamp(PostReportLogSelfCorrectionAlpha + DeltaSeconds / 0.44f, 0.0f, 1.0f);
	PostReportLogSelfCorrectionPulseClock += DeltaSeconds;
	const float Ease = FMath::InterpEaseOut(0.0f, 1.0f, PostReportLogSelfCorrectionAlpha, 3.0f);
	const float Impact = FMath::Sin(PostReportLogSelfCorrectionAlpha * UE_PI) * (1.0f - PostReportLogSelfCorrectionAlpha);
	const FVector CorrectionOffset(0.0f, -7.0f * Ease, 5.0f * Impact);
	const FRotator CorrectionRotation(-5.0f * Impact, 0.0f, 7.0f * Impact);
	const float Pulse = 0.5f + 0.5f * FMath::Sin(PostReportLogSelfCorrectionPulseClock * 10.0f);
	SetPostReportLogSelfCorrectionLightIntensity(520.0f + Pulse * 920.0f);

	for (int32 Index = 0; Index < PostReportLogSelfCorrectionFeedbackActors.Num(); ++Index)
	{
		AActor* FeedbackPart = PostReportLogSelfCorrectionFeedbackActors[Index];
		if (!FeedbackPart || !PostReportLogSelfCorrectionFeedbackRestLocations.IsValidIndex(Index) || !PostReportLogSelfCorrectionFeedbackRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		FeedbackPart->SetActorLocationAndRotation(
			PostReportLogSelfCorrectionFeedbackRestLocations[Index] + CorrectionOffset,
			PostReportLogSelfCorrectionFeedbackRestRotations[Index] + CorrectionRotation);
	}

	if (PostReportLogSelfCorrectionAlpha >= 1.0f)
	{
		bPostReportLogSelfCorrectionActive = false;
		SetPostReportLogSelfCorrectionLightIntensity(520.0f);
	}
}

void AHotelNightShiftPawn::UpdatePhoneRingVisual(float DeltaSeconds)
{
	if (LoopStage != EHotelLoopStage::PhoneRinging)
	{
		return;
	}

	PhoneRingVisualClock += DeltaSeconds;
	const float Pulse = 0.5f + 0.5f * FMath::Sin(PhoneRingVisualClock * 7.2f);
	SetPhoneIndicatorIntensity(120.0f + Pulse * 920.0f);
}

void AHotelNightShiftPawn::LiftPhoneReceiver()
{
	if (!PhoneReceiverActor || PhoneReceiverActors.IsEmpty())
	{
		return;
	}

	bPhoneReceiverLiftActive = true;
	PhoneReceiverLiftAlpha = 0.0f;
}

void AHotelNightShiftPawn::UpdatePhoneReceiverAnimation(float DeltaSeconds)
{
	if (!bPhoneReceiverLiftActive || !PhoneReceiverActor)
	{
		return;
	}

	PhoneReceiverLiftAlpha = FMath::Clamp(PhoneReceiverLiftAlpha + DeltaSeconds / 0.42f, 0.0f, 1.0f);
	const float Ease = FMath::InterpEaseInOut(0.0f, 1.0f, PhoneReceiverLiftAlpha, 2.0f);
	const FVector LiftOffset = PhoneReceiverLiftLocation - PhoneReceiverRestLocation;
	const FRotator LiftRotationDelta = PhoneReceiverLiftRotation - PhoneReceiverRestRotation;
	for (int32 Index = 0; Index < PhoneReceiverActors.Num(); ++Index)
	{
		AActor* ReceiverPart = PhoneReceiverActors[Index];
		if (!ReceiverPart || !PhoneReceiverPartRestLocations.IsValidIndex(Index) || !PhoneReceiverPartRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const FVector NewLocation = PhoneReceiverPartRestLocations[Index] + LiftOffset * Ease;
		const FRotator TargetRotation = PhoneReceiverPartRestRotations[Index] + LiftRotationDelta;
		const FQuat NewRotation = FQuat::Slerp(
			PhoneReceiverPartRestRotations[Index].Quaternion(),
			TargetRotation.Quaternion(),
			Ease);
		ReceiverPart->SetActorLocationAndRotation(NewLocation, NewRotation.Rotator());
	}

	if (PhoneReceiverLiftAlpha >= 1.0f)
	{
		bPhoneReceiverLiftActive = false;
	}
}

void AHotelNightShiftPawn::TriggerDoorRefusalFeedback()
{
	if (!DoorRefusalFeedbackActor || DoorRefusalFeedbackActors.IsEmpty())
	{
		return;
	}

	bDoorRefusalFeedbackActive = true;
	DoorRefusalFeedbackAlpha = 0.0f;
}

void AHotelNightShiftPawn::UpdateDoorRefusalFeedback(float DeltaSeconds)
{
	if (!bDoorRefusalFeedbackActive || !DoorRefusalFeedbackActor)
	{
		return;
	}

	DoorRefusalFeedbackAlpha = FMath::Clamp(DoorRefusalFeedbackAlpha + DeltaSeconds / 0.34f, 0.0f, 1.0f);
	const float Kick = FMath::Sin(DoorRefusalFeedbackAlpha * UE_PI * 4.0f) * (1.0f - DoorRefusalFeedbackAlpha);
	const FVector KnockOffset(0.0f, -10.0f * Kick, 2.0f * FMath::Abs(Kick));
	const FRotator KnockRotation(0.0f, 0.0f, 4.0f * Kick);

	for (int32 Index = 0; Index < DoorRefusalFeedbackActors.Num(); ++Index)
	{
		AActor* FeedbackPart = DoorRefusalFeedbackActors[Index];
		if (!FeedbackPart || !DoorRefusalFeedbackRestLocations.IsValidIndex(Index) || !DoorRefusalFeedbackRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		FeedbackPart->SetActorLocationAndRotation(
			DoorRefusalFeedbackRestLocations[Index] + KnockOffset,
			DoorRefusalFeedbackRestRotations[Index] + KnockRotation);
	}

	if (DoorRefusalFeedbackAlpha >= 1.0f)
	{
		for (int32 Index = 0; Index < DoorRefusalFeedbackActors.Num(); ++Index)
		{
			AActor* FeedbackPart = DoorRefusalFeedbackActors[Index];
			if (!FeedbackPart || !DoorRefusalFeedbackRestLocations.IsValidIndex(Index) || !DoorRefusalFeedbackRestRotations.IsValidIndex(Index))
			{
				continue;
			}

			FeedbackPart->SetActorLocationAndRotation(DoorRefusalFeedbackRestLocations[Index], DoorRefusalFeedbackRestRotations[Index]);
		}
		bDoorRefusalFeedbackActive = false;
	}
}

void AHotelNightShiftPawn::TriggerReportLogFiledFeedback()
{
	if (!ReportLogFiledFeedbackActor || ReportLogFiledFeedbackActors.IsEmpty())
	{
		return;
	}

	bReportLogFiledFeedbackActive = true;
	ReportLogFiledFeedbackAlpha = 0.0f;
}

void AHotelNightShiftPawn::UpdateReportLogFiledFeedback(float DeltaSeconds)
{
	if (!bReportLogFiledFeedbackActive || !ReportLogFiledFeedbackActor)
	{
		return;
	}

	ReportLogFiledFeedbackAlpha = FMath::Clamp(ReportLogFiledFeedbackAlpha + DeltaSeconds / 0.30f, 0.0f, 1.0f);
	const float Ease = FMath::InterpEaseOut(0.0f, 1.0f, ReportLogFiledFeedbackAlpha, 3.0f);
	const float Impact = FMath::Sin(ReportLogFiledFeedbackAlpha * UE_PI) * (1.0f - ReportLogFiledFeedbackAlpha);
	const FVector StampOffset(0.0f, 6.0f * Ease, 8.0f * Impact);
	const FRotator StampRotation(-4.0f * Impact, 0.0f, -9.0f * Impact);

	for (int32 Index = 0; Index < ReportLogFiledFeedbackActors.Num(); ++Index)
	{
		AActor* FeedbackPart = ReportLogFiledFeedbackActors[Index];
		if (!FeedbackPart || !ReportLogFiledFeedbackRestLocations.IsValidIndex(Index) || !ReportLogFiledFeedbackRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		FeedbackPart->SetActorLocationAndRotation(
			ReportLogFiledFeedbackRestLocations[Index] + StampOffset,
			ReportLogFiledFeedbackRestRotations[Index] + StampRotation);
	}

	if (ReportLogFiledFeedbackAlpha >= 1.0f)
	{
		bReportLogFiledFeedbackActive = false;
	}
}

void AHotelNightShiftPawn::SetPhoneIndicatorIntensity(float NewIntensity)
{
	if (!PhoneIndicatorLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = PhoneIndicatorLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::SetPatrolListenLightIntensity(float NewIntensity)
{
	if (!PatrolListenLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = PatrolListenLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::SetReturnRouteLightIntensity(float NewIntensity)
{
	if (!ReturnRouteLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = ReturnRouteLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::SetPostReportMonitorMismatchLightIntensity(float NewIntensity)
{
	if (!PostReportMonitorMismatchLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = PostReportMonitorMismatchLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::SetPostReportDeskWaitLightIntensity(float NewIntensity)
{
	if (!PostReportDeskWaitLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = PostReportDeskWaitLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::SetPostReportLogSelfCorrectionLightIntensity(float NewIntensity)
{
	if (!PostReportLogSelfCorrectionLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = PostReportLogSelfCorrectionLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::PulseHallLight(float NewIntensity)
{
	if (!HallTargetLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = HallTargetLightActor->FindComponentByClass<ULightComponent>())
	{
		LightComponent->SetIntensity(NewIntensity);
	}
}

void AHotelNightShiftPawn::SetWorkState(
	EHotelLoopStage NewStage,
	const FString& NewObjective,
	const FString& NewMessage,
	const FString& NewDeskStatus,
	float NewFearPressure)
{
	LoopStage = NewStage;
	ObjectiveText = NewObjective;
	WorkMessageText = NewMessage;
	DeskStatusText = NewDeskStatus;
	FearPressure = NewFearPressure;
}

bool AHotelNightShiftPawn::ActorMatches(const AActor* Actor, const FVector& Anchor, float Radius, FName RequiredTag) const
{
	return Actor && (Actor->ActorHasTag(RequiredTag) || IsActorNear(Actor, Anchor, Radius));
}

bool AHotelNightShiftPawn::IsActorNear(const AActor* Actor, const FVector& Anchor, float Radius) const
{
	return Actor && FVector::DistSquared(Actor->GetActorLocation(), Anchor) <= FMath::Square(Radius);
}

AActor* AHotelNightShiftPawn::FindAudioActorNear(const FVector& Anchor, float Radius) const
{
	TArray<AActor*> Actors;
	UGameplayStatics::GetAllActorsOfClass(this, AAmbientSound::StaticClass(), Actors);
	for (AActor* Actor : Actors)
	{
		if (IsActorNear(Actor, Anchor, Radius))
		{
			return Actor;
		}
	}
	return nullptr;
}

AActor* AHotelNightShiftPawn::FindActorWithTagNear(FName RequiredTag, const FVector& Anchor, float Radius) const
{
	TArray<AActor*> Actors;
	UGameplayStatics::GetAllActorsOfClass(this, AActor::StaticClass(), Actors);
	for (AActor* Actor : Actors)
	{
		if (Actor && Actor->ActorHasTag(RequiredTag) && IsActorNear(Actor, Anchor, Radius))
		{
			return Actor;
		}
	}
	return nullptr;
}

TArray<AActor*> AHotelNightShiftPawn::FindActorsWithTagNear(FName RequiredTag, const FVector& Anchor, float Radius) const
{
	TArray<AActor*> MatchingActors;
	TArray<AActor*> Actors;
	UGameplayStatics::GetAllActorsOfClass(this, AActor::StaticClass(), Actors);
	for (AActor* Actor : Actors)
	{
		if (Actor && Actor->ActorHasTag(RequiredTag) && IsActorNear(Actor, Anchor, Radius))
		{
			MatchingActors.Add(Actor);
		}
	}
	return MatchingActors;
}

AActor* AHotelNightShiftPawn::FindLightActorNear(const FVector& Anchor, float Radius) const
{
	TArray<AActor*> Actors;
	UGameplayStatics::GetAllActorsOfClass(this, AActor::StaticClass(), Actors);
	for (AActor* Actor : Actors)
	{
		if (IsActorNear(Actor, Anchor, Radius) && Actor->FindComponentByClass<ULightComponent>())
		{
			return Actor;
		}
	}
	return nullptr;
}
