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
const FVector MonitorCheckSoundAnchor(-620.0f, -542.0f, 172.0f);
const FVector MonitorCheckFeedbackAnchor(-620.0f, -548.0f, 160.0f);
const FVector MonitorCheckLightAnchor(-620.0f, -552.0f, 178.0f);
const FVector PhoneReceiverAnchor(-430.0f, -558.0f, 150.0f);
const FVector PhoneCordTugAnchor(-356.0f, -558.0f, 140.0f);
const FVector PhoneIndicatorLightAnchor(-395.0f, -555.0f, 158.0f);
const FVector DoorKnockSoundAnchor(3920.0f, 285.0f, 150.0f);
const FVector DoorRefusalFeedbackAnchor(4020.0f, 258.0f, 150.0f);
const FVector Room203PracticalLightAnchor(3785.0f, 252.0f, 205.0f);
const FVector Room203WallpaperFlutterAnchor(3635.0f, 276.0f, 166.0f);
const FVector Room203AftershockSoundAnchor(3725.0f, 276.0f, 168.0f);
const FVector ReportFiledSoundAnchor(-242.0f, -500.0f, 152.0f);
const FVector ReportLogFiledFeedbackAnchor(-232.0f, -503.0f, 145.0f);
const FVector ReportLogFiledLightAnchor(-318.0f, -548.0f, 176.0f);
const FVector PatrolListenAnchor(930.0f, 0.0f, 92.0f);
const FVector PatrolListenSoundAnchor(930.0f, 0.0f, 72.0f);
const FVector PatrolListenLightAnchor(955.0f, 0.0f, 115.0f);
const FVector ReturnRouteAnchor(2860.0f, 0.0f, 92.0f);
const FVector ReturnRouteSoundAnchor(3420.0f, 270.0f, 150.0f);
const FVector ReturnRouteTailSoundAnchor(3020.0f, -70.0f, 155.0f);
const FVector ReturnRouteLightAnchor(2860.0f, -90.0f, 188.0f);
const FVector ReturnRouteTailLightAnchor(3020.0f, -30.0f, 174.0f);
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
const FName PhoneCordTugTag(TEXT("Hotel.Feedback.PhoneCordTug"));
const FName PhoneLineAudioTag(TEXT("Hotel.Audio.PhoneLineStatic"));
const FName MonitorInteractTag(TEXT("Hotel.Interact.Monitor"));
const FName MonitorCheckAudioTag(TEXT("Hotel.Audio.MonitorCheck"));
const FName MonitorCheckFeedbackTag(TEXT("Hotel.Feedback.MonitorCheckVisual"));
const FName MonitorCheckLightTag(TEXT("Hotel.Feedback.MonitorCheckLight"));
const FName Room203DoorInteractTag(TEXT("Hotel.Interact.Room203Door"));
const FName Room203DoorRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203Refusal"));
const FName Room203LatchRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203LatchJolt"));
const FName Room203ChainRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203ChainJolt"));
const FName Room203SurfaceRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203DoorSurfaceJolt"));
const FName Room203EvidenceRefusalFeedbackTag(TEXT("Hotel.Feedback.Room203EvidenceReaction"));
const FName Room203WallpaperFlutterTag(TEXT("Hotel.Feedback.Room203WallpaperFlutter"));
const FName Room203PracticalLightTag(TEXT("Hotel.Feedback.Room203DoorPracticalLight"));
const FName Room203AftershockAudioTag(TEXT("Hotel.Audio.Room203Aftershock"));
const FName ReportLogInteractTag(TEXT("Hotel.Interact.ReportLog"));
const FName ReportLogFiledFeedbackTag(TEXT("Hotel.Feedback.ReportLogFiled"));
const FName ReportLogFiledReactionTag(TEXT("Hotel.Feedback.ReportLogFiledReaction"));
const FName ReportLogFiledLightTag(TEXT("Hotel.Feedback.ReportLogFiledLight"));
const FName ReportLogFiledAudioTag(TEXT("Hotel.Audio.ReportLogFiled"));
const FName PatrolListenAudioTag(TEXT("Hotel.Audio.PatrolListen"));
const FName PatrolListenLightTag(TEXT("Hotel.Feedback.PatrolListenLight"));
const FName ReturnRouteAudioTag(TEXT("Hotel.Audio.ReturnRoute"));
const FName ReturnRouteTailAudioTag(TEXT("Hotel.Audio.ReturnRouteTail"));
const FName ReturnRouteLightTag(TEXT("Hotel.Feedback.ReturnRouteLight"));
const FName ReturnRouteTailLightTag(TEXT("Hotel.Feedback.ReturnRouteTailLight"));
const FName ReturnRouteBackKnockTag(TEXT("Hotel.Feedback.ReturnRouteBackKnock"));
const FName PostReportMonitorMismatchAudioTag(TEXT("Hotel.Audio.PostReportMonitorMismatch"));
const FName PostReportMonitorMismatchLightTag(TEXT("Hotel.Feedback.PostReportMonitorMismatchLight"));
const FName PostReportMonitorMismatchFeedbackTag(TEXT("Hotel.Feedback.PostReportMonitorMismatchVisual"));
const FName PostReportDeskWaitAudioTag(TEXT("Hotel.Audio.PostReportDeskWait"));
const FName PostReportDeskWaitLightTag(TEXT("Hotel.Feedback.PostReportDeskWaitLight"));
const FName PostReportDeskWaitRattleTag(TEXT("Hotel.Feedback.PostReportDeskWaitRattle"));
const FName PostReportDeskWaitCrackTag(TEXT("Hotel.Feedback.PostReportDeskWaitCrack"));
const FName PostReportDeskWaitTapeTag(TEXT("Hotel.Feedback.PostReportDeskWaitTape"));
const FName PostReportDeskWaitLatchTag(TEXT("Hotel.Feedback.PostReportDeskWaitLatch"));
const FName PostReportLogSelfCorrectionAudioTag(TEXT("Hotel.Audio.PostReportLogSelfCorrection"));
const FName PostReportLogSelfCorrectionFeedbackTag(TEXT("Hotel.Feedback.PostReportLogSelfCorrection"));
const FName PostReportLogSelfCorrectionLightTag(TEXT("Hotel.Feedback.PostReportLogSelfCorrectionLight"));
constexpr float ReturnRouteAnomalyTotalSeconds = 2.35f;
constexpr float ReturnRouteTailSoundDelaySeconds = 0.48f;
constexpr float ReturnRouteCameraMaxFovKick = 4.2f;
const FVector ReturnRouteCameraImpactOffset(-8.0f, 0.0f, -2.4f);
const FVector ReturnRouteCameraTailOffset(2.4f, 0.0f, 0.8f);
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
	CaptureReturnRouteCameraRestState();
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
	UpdateMonitorCheckFeedback(DeltaSeconds);
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

bool AHotelNightShiftPawn::AutomationHasMonitorCheckSound() const
{
	const AAmbientSound* MonitorCheckSound = Cast<AAmbientSound>(MonitorCheckSoundActor);
	const UAudioComponent* AudioComponent = MonitorCheckSound ? MonitorCheckSound->GetAudioComponent() : nullptr;
	return AudioComponent && AudioComponent->Sound;
}

bool AHotelNightShiftPawn::AutomationIsMonitorCheckFeedbackActive() const
{
	return bMonitorCheckFeedbackActive;
}

void AHotelNightShiftPawn::AutomationAdvanceMonitorCheckFeedback(float DeltaSeconds)
{
	UpdateMonitorCheckFeedback(DeltaSeconds);
}

float AHotelNightShiftPawn::AutomationGetMonitorCheckFeedbackAlpha() const
{
	return MonitorCheckFeedbackAlpha;
}

FVector AHotelNightShiftPawn::AutomationGetMonitorCheckFeedbackLocation() const
{
	return MonitorCheckFeedbackActor ? MonitorCheckFeedbackActor->GetActorLocation() : FVector::ZeroVector;
}

float AHotelNightShiftPawn::AutomationGetMonitorCheckLightIntensity() const
{
	return GetLightIntensity(MonitorCheckLightActor);
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

FVector AHotelNightShiftPawn::AutomationGetReturnRouteBackKnockLocation() const
{
	return ReturnRouteBackKnockActor ? ReturnRouteBackKnockActor->GetActorLocation() : FVector::ZeroVector;
}

FVector AHotelNightShiftPawn::AutomationGetReturnRouteCameraRelativeLocation() const
{
	return FirstPersonCamera ? FirstPersonCamera->GetRelativeLocation() : FVector::ZeroVector;
}

float AHotelNightShiftPawn::AutomationGetReturnRouteCameraFieldOfView() const
{
	return FirstPersonCamera ? FirstPersonCamera->FieldOfView : 0.0f;
}

bool AHotelNightShiftPawn::AutomationHasReturnRouteTailSound() const
{
	const AAmbientSound* TailSound = Cast<AAmbientSound>(ReturnRouteTailSoundActor);
	const UAudioComponent* AudioComponent = TailSound ? TailSound->GetAudioComponent() : nullptr;
	return AudioComponent && AudioComponent->Sound;
}

float AHotelNightShiftPawn::AutomationGetReturnRouteLightIntensity() const
{
	return GetLightIntensity(ReturnRouteLightActor);
}

float AHotelNightShiftPawn::AutomationGetReturnRouteTailLightIntensity() const
{
	return GetLightIntensity(ReturnRouteTailLightActor);
}

int32 AHotelNightShiftPawn::AutomationCountMovedReturnRouteBackKnockActors(float MinDistance) const
{
	const float MinDistanceSquared = FMath::Square(MinDistance);
	int32 MovedCount = 0;
	for (int32 Index = 0; Index < ReturnRouteBackKnockActors.Num(); ++Index)
	{
		const AActor* FeedbackPart = ReturnRouteBackKnockActors[Index];
		if (!FeedbackPart || !ReturnRouteBackKnockRestLocations.IsValidIndex(Index))
		{
			continue;
		}

		if (FVector::DistSquared(FeedbackPart->GetActorLocation(), ReturnRouteBackKnockRestLocations[Index]) >= MinDistanceSquared)
		{
			++MovedCount;
		}
	}
	return MovedCount;
}

bool AHotelNightShiftPawn::AutomationIsPostReportMonitorMismatchActive() const
{
	return bPostReportMonitorMismatchActive;
}

void AHotelNightShiftPawn::AutomationAdvancePostReportMonitorMismatch(float DeltaSeconds)
{
	UpdatePostReportMonitorMismatch(DeltaSeconds);
}

FVector AHotelNightShiftPawn::AutomationGetPostReportMonitorMismatchFeedbackLocation() const
{
	return PostReportMonitorMismatchFeedbackActor ? PostReportMonitorMismatchFeedbackActor->GetActorLocation() : FVector::ZeroVector;
}

int32 AHotelNightShiftPawn::AutomationCountMovedPostReportMonitorMismatchActors(float MinDistance) const
{
	const float MinDistanceSquared = FMath::Square(MinDistance);
	int32 MovedCount = 0;
	for (int32 Index = 0; Index < PostReportMonitorMismatchFeedbackActors.Num(); ++Index)
	{
		const AActor* FeedbackPart = PostReportMonitorMismatchFeedbackActors[Index];
		if (!FeedbackPart || !PostReportMonitorMismatchFeedbackRestLocations.IsValidIndex(Index))
		{
			continue;
		}

		if (FVector::DistSquared(FeedbackPart->GetActorLocation(), PostReportMonitorMismatchFeedbackRestLocations[Index]) >= MinDistanceSquared)
		{
			++MovedCount;
		}
	}
	return MovedCount;
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

FRotator AHotelNightShiftPawn::AutomationGetPhoneReceiverRotation() const
{
	return PhoneReceiverActor ? PhoneReceiverActor->GetActorRotation() : FRotator::ZeroRotator;
}

bool AHotelNightShiftPawn::AutomationIsPhoneReceiverLiftActive() const
{
	return bPhoneReceiverLiftActive;
}

FVector AHotelNightShiftPawn::AutomationGetPhoneCordTugLocation() const
{
	return PhoneCordTugActors.IsValidIndex(0) && PhoneCordTugActors[0]
		? PhoneCordTugActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

void AHotelNightShiftPawn::AutomationAdvanceDoorRefusalFeedback(float DeltaSeconds)
{
	UpdateDoorRefusalFeedback(DeltaSeconds);
}

float AHotelNightShiftPawn::AutomationGetDoorRefusalFeedbackAlpha() const
{
	return DoorRefusalFeedbackAlpha;
}

bool AHotelNightShiftPawn::AutomationIsDoorRefusalFeedbackActive() const
{
	return bDoorRefusalFeedbackActive;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalFeedbackLocation() const
{
	return DoorRefusalFeedbackActor ? DoorRefusalFeedbackActor->GetActorLocation() : FVector::ZeroVector;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalLatchLocation() const
{
	return DoorRefusalLatchActors.IsValidIndex(0) && DoorRefusalLatchActors[0]
		? DoorRefusalLatchActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalChainLocation() const
{
	return DoorRefusalChainActors.IsValidIndex(0) && DoorRefusalChainActors[0]
		? DoorRefusalChainActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalSurfaceLocation() const
{
	return DoorRefusalSurfaceActors.IsValidIndex(0) && DoorRefusalSurfaceActors[0]
		? DoorRefusalSurfaceActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalEvidenceLocation() const
{
	return DoorRefusalEvidenceActors.IsValidIndex(0) && DoorRefusalEvidenceActors[0]
		? DoorRefusalEvidenceActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

FVector AHotelNightShiftPawn::AutomationGetDoorRefusalWallpaperFlutterLocation() const
{
	return DoorRefusalWallpaperFlutterActors.IsValidIndex(0) && DoorRefusalWallpaperFlutterActors[0]
		? DoorRefusalWallpaperFlutterActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

float AHotelNightShiftPawn::AutomationGetRoom203PracticalLightIntensity() const
{
	return GetLightIntensity(Room203PracticalLightActor);
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

FVector AHotelNightShiftPawn::AutomationGetReportLogFiledReactionLocation() const
{
	return ReportLogFiledReactionActors.IsValidIndex(0) && ReportLogFiledReactionActors[0]
		? ReportLogFiledReactionActors[0]->GetActorLocation()
		: FVector::ZeroVector;
}

float AHotelNightShiftPawn::AutomationGetReportLogFiledLightIntensity() const
{
	return GetLightIntensity(ReportLogFiledLightActor);
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
		TriggerMonitorCheckFeedback();
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
	MonitorCheckSoundActor = FindActorWithTagNear(MonitorCheckAudioTag, MonitorCheckSoundAnchor, 120.0f);
	MonitorCheckFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(MonitorCheckFeedbackTag, MonitorCheckFeedbackAnchor, 150.0f))
	{
		MonitorCheckFeedbackActors.Add(FeedbackPart);
	}
	MonitorCheckFeedbackActor = FindActorWithTagNear(MonitorCheckFeedbackTag, MonitorCheckFeedbackAnchor, 150.0f);
	MonitorCheckLightActor = FindLightActorWithTagNear(MonitorCheckLightTag, MonitorCheckLightAnchor, 140.0f);
	PhoneReceiverActors.Reset();
	for (AActor* ReceiverPart : FindActorsWithTagNear(PhoneReceiverTag, PhoneReceiverAnchor, 120.0f))
	{
		PhoneReceiverActors.Add(ReceiverPart);
	}
	PhoneReceiverActor = FindActorWithTagNear(PhoneReceiverTag, PhoneReceiverAnchor, 120.0f);
	PhoneCordTugActors.Reset();
	for (AActor* CordPart : FindActorsWithTagNear(PhoneCordTugTag, PhoneCordTugAnchor, 90.0f))
	{
		PhoneCordTugActors.Add(CordPart);
	}
	DoorKnockSoundActor = FindAudioActorNear(DoorKnockSoundAnchor, 140.0f);
	DoorRefusalFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203DoorRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f))
	{
		DoorRefusalFeedbackActors.Add(FeedbackPart);
	}
	DoorRefusalFeedbackActor = FindActorWithTagNear(Room203DoorRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f);
	DoorRefusalLatchActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203LatchRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f))
	{
		DoorRefusalLatchActors.Add(FeedbackPart);
	}
	DoorRefusalChainActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203ChainRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f))
	{
		DoorRefusalChainActors.Add(FeedbackPart);
	}
	DoorRefusalSurfaceActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203SurfaceRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 190.0f))
	{
		DoorRefusalSurfaceActors.Add(FeedbackPart);
	}
	DoorRefusalEvidenceActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203EvidenceRefusalFeedbackTag, DoorRefusalFeedbackAnchor, 330.0f))
	{
		DoorRefusalEvidenceActors.Add(FeedbackPart);
	}
	DoorRefusalWallpaperFlutterActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(Room203WallpaperFlutterTag, Room203WallpaperFlutterAnchor, 360.0f))
	{
		DoorRefusalWallpaperFlutterActors.Add(FeedbackPart);
	}
	Room203PracticalLightActor = FindLightActorWithTagNear(Room203PracticalLightTag, Room203PracticalLightAnchor, 180.0f);
	Room203PracticalLightRestIntensity = Room203PracticalLightActor ? GetLightIntensity(Room203PracticalLightActor) : 460.0f;
	Room203AftershockSoundActor = FindActorWithTagNear(Room203AftershockAudioTag, Room203AftershockSoundAnchor, 260.0f);
	ReportFiledSoundActor = FindActorWithTagNear(ReportLogFiledAudioTag, ReportFiledSoundAnchor, 120.0f);
	ReportLogFiledFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(ReportLogFiledFeedbackTag, ReportLogFiledFeedbackAnchor, 150.0f))
	{
		ReportLogFiledFeedbackActors.Add(FeedbackPart);
	}
	ReportLogFiledFeedbackActor = FindActorWithTagNear(ReportLogFiledFeedbackTag, ReportLogFiledFeedbackAnchor, 150.0f);
	ReportLogFiledReactionActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(ReportLogFiledReactionTag, ReportLogFiledFeedbackAnchor, 180.0f))
	{
		ReportLogFiledReactionActors.Add(FeedbackPart);
	}
	ReportLogFiledLightActor = FindLightActorWithTagNear(ReportLogFiledLightTag, ReportLogFiledLightAnchor, 180.0f);
	ReportLogFiledLightRestIntensity = ReportLogFiledLightActor ? GetLightIntensity(ReportLogFiledLightActor) : 620.0f;
	PatrolListenSoundActor = FindActorWithTagNear(PatrolListenAudioTag, PatrolListenSoundAnchor, 120.0f);
	PatrolListenLightActor = FindActorWithTagNear(PatrolListenLightTag, PatrolListenLightAnchor, 120.0f);
	ReturnRouteSoundActor = FindActorWithTagNear(ReturnRouteAudioTag, ReturnRouteSoundAnchor, 220.0f);
	ReturnRouteTailSoundActor = FindActorWithTagNear(ReturnRouteTailAudioTag, ReturnRouteTailSoundAnchor, 260.0f);
	ReturnRouteLightActor = FindLightActorWithTagNear(ReturnRouteLightTag, ReturnRouteLightAnchor, 180.0f);
	ReturnRouteTailLightActor = FindLightActorWithTagNear(ReturnRouteTailLightTag, ReturnRouteTailLightAnchor, 260.0f);
	ReturnRouteBackKnockActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(ReturnRouteBackKnockTag, ReturnRouteAnchor, 660.0f))
	{
		ReturnRouteBackKnockActors.Add(FeedbackPart);
	}
	ReturnRouteBackKnockActor = FindActorWithTagNear(ReturnRouteBackKnockTag, ReturnRouteAnchor, 660.0f);
	PostReportMonitorMismatchSoundActor = FindActorWithTagNear(PostReportMonitorMismatchAudioTag, PostReportMonitorMismatchSoundAnchor, 120.0f);
	PostReportMonitorMismatchLightActor = FindActorWithTagNear(PostReportMonitorMismatchLightTag, PostReportMonitorMismatchLightAnchor, 160.0f);
	PostReportMonitorMismatchFeedbackActors.Reset();
	for (AActor* FeedbackPart : FindActorsWithTagNear(PostReportMonitorMismatchFeedbackTag, MonitorCheckFeedbackAnchor, 180.0f))
	{
		PostReportMonitorMismatchFeedbackActors.Add(FeedbackPart);
	}
	PostReportMonitorMismatchFeedbackActor = FindActorWithTagNear(PostReportMonitorMismatchFeedbackTag, MonitorCheckFeedbackAnchor, 180.0f);
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

	PhoneCordTugRestLocations.Reset();
	PhoneCordTugRestRotations.Reset();
	for (AActor* CordPart : PhoneCordTugActors)
	{
		PhoneCordTugRestLocations.Add(CordPart->GetActorLocation());
		PhoneCordTugRestRotations.Add(CordPart->GetActorRotation());
	}

	MonitorCheckFeedbackRestLocations.Reset();
	MonitorCheckFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : MonitorCheckFeedbackActors)
	{
		MonitorCheckFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		MonitorCheckFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	DoorRefusalFeedbackRestLocations.Reset();
	DoorRefusalFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalFeedbackActors)
	{
		DoorRefusalFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	DoorRefusalLatchRestLocations.Reset();
	DoorRefusalLatchRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalLatchActors)
	{
		DoorRefusalLatchRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalLatchRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	DoorRefusalChainRestLocations.Reset();
	DoorRefusalChainRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalChainActors)
	{
		DoorRefusalChainRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalChainRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	DoorRefusalSurfaceRestLocations.Reset();
	DoorRefusalSurfaceRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalSurfaceActors)
	{
		DoorRefusalSurfaceRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalSurfaceRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	DoorRefusalEvidenceRestLocations.Reset();
	DoorRefusalEvidenceRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalEvidenceActors)
	{
		DoorRefusalEvidenceRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalEvidenceRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	DoorRefusalWallpaperFlutterRestLocations.Reset();
	DoorRefusalWallpaperFlutterRestRotations.Reset();
	for (AActor* FeedbackPart : DoorRefusalWallpaperFlutterActors)
	{
		DoorRefusalWallpaperFlutterRestLocations.Add(FeedbackPart->GetActorLocation());
		DoorRefusalWallpaperFlutterRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	ReportLogFiledFeedbackRestLocations.Reset();
	ReportLogFiledFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : ReportLogFiledFeedbackActors)
	{
		ReportLogFiledFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		ReportLogFiledFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	ReportLogFiledReactionRestLocations.Reset();
	ReportLogFiledReactionRestRotations.Reset();
	for (AActor* FeedbackPart : ReportLogFiledReactionActors)
	{
		ReportLogFiledReactionRestLocations.Add(FeedbackPart->GetActorLocation());
		ReportLogFiledReactionRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	ReturnRouteBackKnockRestLocations.Reset();
	ReturnRouteBackKnockRestRotations.Reset();
	for (AActor* FeedbackPart : ReturnRouteBackKnockActors)
	{
		ReturnRouteBackKnockRestLocations.Add(FeedbackPart->GetActorLocation());
		ReturnRouteBackKnockRestRotations.Add(FeedbackPart->GetActorRotation());
	}

	PostReportMonitorMismatchFeedbackRestLocations.Reset();
	PostReportMonitorMismatchFeedbackRestRotations.Reset();
	for (AActor* FeedbackPart : PostReportMonitorMismatchFeedbackActors)
	{
		PostReportMonitorMismatchFeedbackRestLocations.Add(FeedbackPart->GetActorLocation());
		PostReportMonitorMismatchFeedbackRestRotations.Add(FeedbackPart->GetActorRotation());
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

void AHotelNightShiftPawn::TriggerMonitorCheckFeedback()
{
	bMonitorCheckFeedbackActive = true;
	MonitorCheckFeedbackAlpha = 0.0f;
	MonitorCheckFeedbackPulseClock = 0.0f;
	PlayActorSound(MonitorCheckSoundActor);
	SetMonitorCheckLightIntensity(1700.0f);
}

void AHotelNightShiftPawn::UpdateMonitorCheckFeedback(float DeltaSeconds)
{
	if (!bMonitorCheckFeedbackActive)
	{
		return;
	}

	MonitorCheckFeedbackPulseClock += DeltaSeconds;
	MonitorCheckFeedbackAlpha = FMath::Min(1.0f, MonitorCheckFeedbackAlpha + DeltaSeconds / 0.68f);
	const float Settle = 1.0f - MonitorCheckFeedbackAlpha;
	const float Pulse = 0.5f + 0.5f * FMath::Sin(MonitorCheckFeedbackPulseClock * 18.0f);
	SetMonitorCheckLightIntensity(420.0f + Pulse * 1180.0f * Settle);

	for (int32 Index = 0; Index < MonitorCheckFeedbackActors.Num(); ++Index)
	{
		AActor* FeedbackPart = MonitorCheckFeedbackActors[Index];
		if (!FeedbackPart || !MonitorCheckFeedbackRestLocations.IsValidIndex(Index) || !MonitorCheckFeedbackRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const float Phase = MonitorCheckFeedbackPulseClock * (16.0f + Index * 1.7f) + Index * 0.61f;
		const FVector Jitter(
			FMath::Sin(Phase) * (2.2f + Index * 0.12f) * Settle,
			-FMath::Abs(FMath::Sin(Phase * 0.73f)) * 0.9f * Settle,
			FMath::Cos(Phase * 0.83f) * (1.2f + Index * 0.08f) * Settle);
		const FRotator Tilt(0.0f, 0.0f, FMath::Sin(Phase * 0.51f) * 0.8f * Settle);
		FeedbackPart->SetActorLocationAndRotation(
			MonitorCheckFeedbackRestLocations[Index] + Jitter,
			MonitorCheckFeedbackRestRotations[Index] + Tilt);
	}

	if (MonitorCheckFeedbackAlpha >= 1.0f)
	{
		bMonitorCheckFeedbackActive = false;
		for (int32 Index = 0; Index < MonitorCheckFeedbackActors.Num(); ++Index)
		{
			AActor* FeedbackPart = MonitorCheckFeedbackActors[Index];
			if (!FeedbackPart || !MonitorCheckFeedbackRestLocations.IsValidIndex(Index) || !MonitorCheckFeedbackRestRotations.IsValidIndex(Index))
			{
				continue;
			}
			FeedbackPart->SetActorLocationAndRotation(
				MonitorCheckFeedbackRestLocations[Index],
				MonitorCheckFeedbackRestRotations[Index]);
		}
		SetMonitorCheckLightIntensity(420.0f);
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
	const float Phase = FMath::Clamp(ReturnRouteAnomalySeconds / ReturnRouteAnomalyTotalSeconds, 0.0f, 1.0f);
	const float Pulse = 0.5f + 0.5f * FMath::Sin(ReturnRoutePulseClock * 9.5f);
	const float ImpactEnvelope = FMath::Pow(1.0f - Phase, 1.15f);
	SetReturnRouteLightIntensity(260.0f + Pulse * (920.0f + 720.0f * ImpactEnvelope));

	const float TailPhase = FMath::Clamp((ReturnRouteAnomalySeconds - 0.36f) / 1.48f, 0.0f, 1.0f);
	const float TailEnvelope = FMath::Sin(TailPhase * UE_PI);
	SetReturnRouteTailLightIntensity(90.0f + TailEnvelope * (1180.0f + Pulse * 260.0f));
	UpdateReturnRouteBackKnockFeedback(Phase);
	ApplyReturnRouteCameraPressure(Phase, Pulse);

	if (!bReturnRouteTailSoundPlayed && ReturnRouteAnomalySeconds >= ReturnRouteTailSoundDelaySeconds)
	{
		bReturnRouteTailSoundPlayed = true;
		PlayActorSound(ReturnRouteTailSoundActor);
		WorkMessageText = TEXT("The first knock was behind you. The paper answers from the wall ahead.");
		DeskStatusText = TEXT("RETURN ROUTE: BACK KNOCK / FOLLOWING");
	}

	if (ReturnRouteAnomalySeconds >= ReturnRouteAnomalyTotalSeconds)
	{
		ResolveReturnRouteAnomaly();
	}
}

void AHotelNightShiftPawn::StartReturnRouteAnomaly()
{
	bReturnRouteAnomalyActive = true;
	ReturnRouteAnomalySeconds = 0.0f;
	ReturnRoutePulseClock = 0.0f;
	bReturnRouteTailSoundPlayed = false;
	ResetReturnRouteBackKnockFeedback();
	ResetReturnRouteCameraPressure();
	PlayActorSound(ReturnRouteSoundActor);
	SetWorkState(
		EHotelLoopStage::DoorRefused,
		TEXT("Keep moving. Write the report only after this hallway quiets."),
		TEXT("The knock returns from behind you, then arrives ahead of you."),
		TEXT("RETURN ROUTE: LISTEN / DO NOT RUN"),
		0.84f);
	SetReturnRouteLightIntensity(1600.0f);
	SetReturnRouteTailLightIntensity(90.0f);
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
	SetReturnRouteTailLightIntensity(120.0f);
	ResetReturnRouteBackKnockFeedback();
	ResetReturnRouteCameraPressure();
}

void AHotelNightShiftPawn::UpdateReturnRouteBackKnockFeedback(float NormalizedTime)
{
	const float Phase = FMath::Clamp(NormalizedTime, 0.0f, 1.0f);

	for (int32 Index = 0; Index < ReturnRouteBackKnockActors.Num(); ++Index)
	{
		AActor* FeedbackPart = ReturnRouteBackKnockActors[Index];
		if (!FeedbackPart || !ReturnRouteBackKnockRestLocations.IsValidIndex(Index) || !ReturnRouteBackKnockRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const float LocalDelay = FMath::Clamp(static_cast<float>(Index) * 0.055f, 0.0f, 0.34f);
		const float LocalSpan = 1.0f - LocalDelay;
		const float LocalPhase = LocalSpan > KINDA_SMALL_NUMBER
			? FMath::Clamp((Phase - LocalDelay) / LocalSpan, 0.0f, 1.0f)
			: Phase;
		const float Envelope = FMath::Sin(LocalPhase * UE_PI);
		const float ReverseSlide = FMath::InterpEaseOut(0.0f, 1.0f, LocalPhase, 2.0f) * (1.0f - LocalPhase * 0.22f);
		const float Bias = static_cast<float>(Index) * 0.17f;
		const float Beat = FMath::Sin((LocalPhase * 4.6f + Bias) * UE_PI) * FMath::Pow(1.0f - LocalPhase * 0.72f, 0.58f);
		const float Direction = (Index % 2 == 0) ? -1.0f : 1.0f;
		const bool bWallCue = ReturnRouteBackKnockRestLocations[Index].Z > 35.0f;
		const FVector Offset = bWallCue
			? FVector(-7.5f * Envelope, -10.5f * ReverseSlide, FMath::Abs(Beat) * 3.4f)
			: FVector(-20.0f * ReverseSlide, Direction * Beat * 5.8f, FMath::Abs(Beat) * 1.8f);
		const FRotator Rotation = bWallCue
			? FRotator(0.0f, Direction * Envelope * 2.5f, Beat * 7.8f)
			: FRotator(Beat * 1.4f, Direction * Envelope * 2.3f, Direction * Beat * 4.4f);

		FeedbackPart->SetActorLocationAndRotation(
			ReturnRouteBackKnockRestLocations[Index] + Offset,
			ReturnRouteBackKnockRestRotations[Index] + Rotation);
	}
}

void AHotelNightShiftPawn::CaptureReturnRouteCameraRestState()
{
	if (!FirstPersonCamera)
	{
		return;
	}

	ReturnRouteCameraRestRelativeLocation = FirstPersonCamera->GetRelativeLocation();
	ReturnRouteCameraRestFieldOfView = FirstPersonCamera->FieldOfView;
	bReturnRouteCameraRestCaptured = true;
}

void AHotelNightShiftPawn::ApplyReturnRouteCameraPressure(float NormalizedTime, float Pulse)
{
	if (!FirstPersonCamera)
	{
		return;
	}

	if (!bReturnRouteCameraRestCaptured)
	{
		CaptureReturnRouteCameraRestState();
	}

	const float Phase = FMath::Clamp(NormalizedTime, 0.0f, 1.0f);
	const float ImpactIn = FMath::Sin(FMath::Clamp(Phase / 0.20f, 0.0f, 1.0f) * (UE_PI * 0.5f));
	const float ImpactOut = FMath::Pow(1.0f - Phase, 1.65f);
	const float Impact = ImpactIn * ImpactOut;
	const float TailPhase = FMath::Clamp((Phase - 0.18f) / 0.66f, 0.0f, 1.0f);
	const float Tail = FMath::Sin(TailPhase * UE_PI);
	const float Sway = FMath::Sin(ReturnRoutePulseClock * 14.0f) * (Impact * 1.6f + Tail * 0.75f);

	const FVector PressureOffset =
		(ReturnRouteCameraImpactOffset * Impact)
		+ (ReturnRouteCameraTailOffset * Tail)
		+ FVector(0.0f, Sway, 0.0f);
	FirstPersonCamera->SetRelativeLocation(ReturnRouteCameraRestRelativeLocation + PressureOffset);

	const float FovKick = (Impact * ReturnRouteCameraMaxFovKick) + (Tail * 1.25f) + (Pulse * 0.35f * (Impact + Tail));
	FirstPersonCamera->SetFieldOfView(ReturnRouteCameraRestFieldOfView + FovKick);
}

void AHotelNightShiftPawn::ResetReturnRouteCameraPressure()
{
	if (!FirstPersonCamera)
	{
		return;
	}

	if (!bReturnRouteCameraRestCaptured)
	{
		CaptureReturnRouteCameraRestState();
	}

	FirstPersonCamera->SetRelativeLocation(ReturnRouteCameraRestRelativeLocation);
	FirstPersonCamera->SetFieldOfView(ReturnRouteCameraRestFieldOfView);
}

void AHotelNightShiftPawn::ResetReturnRouteBackKnockFeedback()
{
	for (int32 Index = 0; Index < ReturnRouteBackKnockActors.Num(); ++Index)
	{
		AActor* FeedbackPart = ReturnRouteBackKnockActors[Index];
		if (!FeedbackPart || !ReturnRouteBackKnockRestLocations.IsValidIndex(Index) || !ReturnRouteBackKnockRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		FeedbackPart->SetActorLocationAndRotation(
			ReturnRouteBackKnockRestLocations[Index],
			ReturnRouteBackKnockRestRotations[Index]);
	}
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
	const float MismatchAlpha = FMath::Clamp(PostReportMonitorMismatchSeconds / 1.10f, 0.0f, 1.0f);
	const float Settle = 1.0f - MismatchAlpha;
	const float Pulse = 0.5f + 0.5f * FMath::Sin(PostReportMonitorMismatchPulseClock * 13.0f);
	SetPostReportMonitorMismatchLightIntensity(360.0f + Pulse * 1650.0f);

	for (int32 Index = 0; Index < PostReportMonitorMismatchFeedbackActors.Num(); ++Index)
	{
		AActor* FeedbackPart = PostReportMonitorMismatchFeedbackActors[Index];
		if (!FeedbackPart || !PostReportMonitorMismatchFeedbackRestLocations.IsValidIndex(Index) || !PostReportMonitorMismatchFeedbackRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const float Phase = PostReportMonitorMismatchPulseClock * (21.0f + Index * 1.35f) + Index * 0.52f;
		const float Hit = FMath::Sin(MismatchAlpha * UE_PI * (5.5f + Index * 0.35f)) * Settle;
		const FVector FlickerOffset(
			FMath::Sin(Phase) * (1.2f + Index * 0.18f) * Settle,
			-FMath::Abs(FMath::Sin(Phase * 0.71f)) * 1.4f * Settle,
			Hit * (3.2f + Index * 0.22f));
		const FRotator FlickerRotation(
			0.0f,
			FMath::Sin(Phase * 0.29f) * 0.35f * Settle,
			FMath::Sin(Phase * 0.53f) * (0.9f + Index * 0.05f) * Settle);
		FeedbackPart->SetActorLocationAndRotation(
			PostReportMonitorMismatchFeedbackRestLocations[Index] + FlickerOffset,
			PostReportMonitorMismatchFeedbackRestRotations[Index] + FlickerRotation);
	}

	if (PostReportMonitorMismatchSeconds >= 1.10f)
	{
		bPostReportMonitorMismatchActive = false;
		PostReportMonitorMismatchSeconds = 0.0f;
		for (int32 Index = 0; Index < PostReportMonitorMismatchFeedbackActors.Num(); ++Index)
		{
			AActor* FeedbackPart = PostReportMonitorMismatchFeedbackActors[Index];
			if (!FeedbackPart || !PostReportMonitorMismatchFeedbackRestLocations.IsValidIndex(Index) || !PostReportMonitorMismatchFeedbackRestRotations.IsValidIndex(Index))
			{
				continue;
			}

			FeedbackPart->SetActorLocationAndRotation(
				PostReportMonitorMismatchFeedbackRestLocations[Index],
				PostReportMonitorMismatchFeedbackRestRotations[Index]);
		}
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

		for (int32 Index = 0; Index < PostReportDeskWaitRattleActors.Num(); ++Index)
		{
			AActor* RattlePart = PostReportDeskWaitRattleActors[Index];
			if (!RattlePart || !PostReportDeskWaitRattleRestLocations.IsValidIndex(Index) || !PostReportDeskWaitRattleRestRotations.IsValidIndex(Index))
			{
				continue;
			}

			const bool bCrackWeb = RattlePart->ActorHasTag(PostReportDeskWaitCrackTag);
			const bool bTape = RattlePart->ActorHasTag(PostReportDeskWaitTapeTag);
			const bool bLatch = RattlePart->ActorHasTag(PostReportDeskWaitLatchTag);
			const float Flutter = FMath::Sin((RattleAlpha * UE_PI * 13.0f) + Index * 0.47f) * (1.0f - RattleAlpha);
			const float SideTravel = bLatch ? 16.0f : (bTape ? 10.0f : (bCrackWeb ? 7.0f : 3.0f));
			const float LiftTravel = bLatch ? 3.6f : (bTape ? 2.8f : (bCrackWeb ? 1.6f : 0.6f));
			const float PitchTravel = bLatch ? 9.0f : (bTape ? 4.0f : (bCrackWeb ? 1.4f : 0.8f));
			const float RollTravel = bLatch ? 5.5f : (bTape ? 11.0f : (bCrackWeb ? 1.2f : 0.6f));
			const FVector RattleOffset(
				0.0f,
				RattleKick * SideTravel,
				FMath::Abs(RattleKick) * LiftTravel + (bTape ? Flutter * 2.2f : 0.0f));
			const FRotator RattleRotation(
				RattleKick * PitchTravel,
				bCrackWeb ? Flutter * 0.7f : 0.0f,
				RattleKick * RollTravel + (bTape ? Flutter * 6.0f : 0.0f));
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
	PhoneReceiverLiftSeconds = 0.0f;
}

void AHotelNightShiftPawn::UpdatePhoneReceiverAnimation(float DeltaSeconds)
{
	if (!bPhoneReceiverLiftActive || !PhoneReceiverActor)
	{
		return;
	}

	constexpr float AnticipationSeconds = 0.10f;
	constexpr float LiftSeconds = 0.30f;
	constexpr float SettleSeconds = 0.18f;
	constexpr float TotalSeconds = AnticipationSeconds + LiftSeconds + SettleSeconds;
	const auto LerpRotator = [](const FRotator& From, const FRotator& To, float Alpha)
	{
		return FRotator(
			FMath::Lerp(From.Pitch, To.Pitch, Alpha),
			FMath::Lerp(From.Yaw, To.Yaw, Alpha),
			FMath::Lerp(From.Roll, To.Roll, Alpha));
	};

	PhoneReceiverLiftSeconds = FMath::Min(PhoneReceiverLiftSeconds + DeltaSeconds, TotalSeconds);
	PhoneReceiverLiftAlpha = FMath::Clamp(PhoneReceiverLiftSeconds / TotalSeconds, 0.0f, 1.0f);
	const FVector LiftOffset = PhoneReceiverLiftLocation - PhoneReceiverRestLocation;
	const FRotator LiftRotationDelta = PhoneReceiverLiftRotation - PhoneReceiverRestRotation;
	const FVector AnticipationOffset(-5.0f, 5.0f, -3.5f);
	const FRotator AnticipationRotation(3.0f, -2.0f, 5.0f);
	const FVector OvershootOffset = LiftOffset + FVector(5.0f, -3.0f, 4.0f);
	const FRotator OvershootRotation = LiftRotationDelta + FRotator(-3.0f, 1.0f, -5.0f);
	FVector MotionOffset = LiftOffset;
	FRotator MotionRotationDelta = LiftRotationDelta;

	if (PhoneReceiverLiftSeconds < AnticipationSeconds)
	{
		const float PhaseAlpha = PhoneReceiverLiftSeconds / AnticipationSeconds;
		const float Ease = FMath::InterpEaseOut(0.0f, 1.0f, PhaseAlpha, 2.0f);
		MotionOffset = AnticipationOffset * Ease;
		MotionRotationDelta = AnticipationRotation * Ease;
	}
	else if (PhoneReceiverLiftSeconds < AnticipationSeconds + LiftSeconds)
	{
		const float PhaseAlpha = (PhoneReceiverLiftSeconds - AnticipationSeconds) / LiftSeconds;
		const float Ease = FMath::InterpEaseOut(0.0f, 1.0f, PhaseAlpha, 2.4f);
		MotionOffset = FMath::Lerp(AnticipationOffset, OvershootOffset, Ease);
		MotionRotationDelta = LerpRotator(AnticipationRotation, OvershootRotation, Ease);
	}
	else
	{
		const float PhaseAlpha = (PhoneReceiverLiftSeconds - AnticipationSeconds - LiftSeconds) / SettleSeconds;
		const float Ease = FMath::InterpEaseOut(0.0f, 1.0f, PhaseAlpha, 3.0f);
		const float Wobble = FMath::Sin(PhaseAlpha * UE_PI * 2.0f) * (1.0f - PhaseAlpha);
		MotionOffset = FMath::Lerp(OvershootOffset, LiftOffset, Ease) + FVector(0.0f, Wobble * 2.4f, Wobble * 1.6f);
		MotionRotationDelta = LerpRotator(OvershootRotation, LiftRotationDelta, Ease) + FRotator(Wobble * 3.0f, 0.0f, Wobble * 4.0f);
	}

	for (int32 Index = 0; Index < PhoneReceiverActors.Num(); ++Index)
	{
		AActor* ReceiverPart = PhoneReceiverActors[Index];
		if (!ReceiverPart || !PhoneReceiverPartRestLocations.IsValidIndex(Index) || !PhoneReceiverPartRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		ReceiverPart->SetActorLocationAndRotation(
			PhoneReceiverPartRestLocations[Index] + MotionOffset,
			PhoneReceiverPartRestRotations[Index] + MotionRotationDelta);
	}

	const float CordAlpha = FMath::Clamp((PhoneReceiverLiftSeconds - AnticipationSeconds) / (LiftSeconds + SettleSeconds), 0.0f, 1.0f);
	const float CordEase = FMath::InterpEaseOut(0.0f, 1.0f, CordAlpha, 2.0f);
	const float CordWobble = FMath::Sin(CordAlpha * UE_PI * 3.0f) * (1.0f - CordAlpha);
	const FVector CordOffset(18.0f * CordEase, -7.0f * CordEase + CordWobble * 1.5f, 4.0f * CordEase + FMath::Abs(CordWobble) * 1.4f);
	const FRotator CordRotation(0.0f, 0.0f, 9.0f * CordEase + CordWobble * 3.0f);
	for (int32 Index = 0; Index < PhoneCordTugActors.Num(); ++Index)
	{
		AActor* CordPart = PhoneCordTugActors[Index];
		if (!CordPart || !PhoneCordTugRestLocations.IsValidIndex(Index) || !PhoneCordTugRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		CordPart->SetActorLocationAndRotation(
			PhoneCordTugRestLocations[Index] + CordOffset,
			PhoneCordTugRestRotations[Index] + CordRotation);
	}

	if (PhoneReceiverLiftAlpha >= 1.0f)
	{
		bPhoneReceiverLiftActive = false;
	}
}

void AHotelNightShiftPawn::TriggerDoorRefusalFeedback()
{
	const bool bHasRefusalParts =
		!DoorRefusalLatchActors.IsEmpty()
		|| !DoorRefusalChainActors.IsEmpty()
		|| !DoorRefusalSurfaceActors.IsEmpty()
		|| !DoorRefusalEvidenceActors.IsEmpty()
		|| !DoorRefusalWallpaperFlutterActors.IsEmpty();
	if (!DoorRefusalFeedbackActor || !bHasRefusalParts)
	{
		return;
	}

	bDoorRefusalFeedbackActive = true;
	DoorRefusalFeedbackSeconds = 0.0f;
	DoorRefusalFeedbackAlpha = 0.0f;
	bDoorRefusalAftershockSoundPlayed = false;
}

void AHotelNightShiftPawn::UpdateDoorRefusalFeedback(float DeltaSeconds)
{
	if (!bDoorRefusalFeedbackActive || !DoorRefusalFeedbackActor)
	{
		return;
	}

	constexpr float TotalSeconds = 1.48f;
	DoorRefusalFeedbackSeconds = FMath::Min(DoorRefusalFeedbackSeconds + DeltaSeconds, TotalSeconds);
	DoorRefusalFeedbackAlpha = FMath::Clamp(DoorRefusalFeedbackSeconds / TotalSeconds, 0.0f, 1.0f);
	const auto ApplyDoorMotion = [](
		const TArray<TObjectPtr<AActor>>& Actors,
		const TArray<FVector>& RestLocations,
		const TArray<FRotator>& RestRotations,
		const FVector& Offset,
		const FRotator& Rotation)
	{
		for (int32 Index = 0; Index < Actors.Num(); ++Index)
		{
			AActor* FeedbackPart = Actors[Index];
			if (!FeedbackPart || !RestLocations.IsValidIndex(Index) || !RestRotations.IsValidIndex(Index))
			{
				continue;
			}

			FeedbackPart->SetActorLocationAndRotation(
				RestLocations[Index] + Offset,
				RestRotations[Index] + Rotation);
		}
	};

	const float LatchPhase = FMath::Clamp(DoorRefusalFeedbackSeconds / 0.20f, 0.0f, 1.0f);
	const float ChainPhase = FMath::Clamp((DoorRefusalFeedbackSeconds - 0.10f) / 0.30f, 0.0f, 1.0f);
	const float SurfacePhase = FMath::Clamp((DoorRefusalFeedbackSeconds - 0.06f) / 0.52f, 0.0f, 1.0f);
	const float EvidencePhase = FMath::Clamp((DoorRefusalFeedbackSeconds - 0.14f) / 0.84f, 0.0f, 1.0f);
	const float WallpaperPhase = FMath::Clamp((DoorRefusalFeedbackSeconds - 0.32f) / 1.10f, 0.0f, 1.0f);
	const float LatchKick = FMath::Sin(LatchPhase * UE_PI) * (1.0f - 0.10f * LatchPhase);
	const float ChainKick = FMath::Sin(ChainPhase * UE_PI) * (1.0f - 0.18f * ChainPhase);
	const float SurfaceKick = FMath::Sin(SurfacePhase * UE_PI * 2.0f) * (1.0f - SurfacePhase);
	const float EvidenceKick = FMath::Sin(EvidencePhase * UE_PI * 3.0f) * FMath::Pow(1.0f - EvidencePhase, 0.80f);
	const float EvidenceLift = FMath::Sin(EvidencePhase * UE_PI);
	const float WallpaperHold = FMath::Sin(FMath::Min(WallpaperPhase * 1.25f, 1.0f) * UE_PI);
	const float LightPulse = FMath::Sin(WallpaperPhase * UE_PI * 5.0f) * FMath::Pow(1.0f - WallpaperPhase, 1.35f);

	if (!bDoorRefusalAftershockSoundPlayed && DoorRefusalFeedbackSeconds >= 0.34f)
	{
		PlayActorSound(Room203AftershockSoundActor);
		bDoorRefusalAftershockSoundPlayed = true;
	}

	ApplyDoorMotion(
		DoorRefusalLatchActors,
		DoorRefusalLatchRestLocations,
		DoorRefusalLatchRestRotations,
		FVector(0.0f, -18.0f * LatchKick, 5.0f * FMath::Abs(LatchKick)),
		FRotator(0.0f, 0.0f, 10.0f * LatchKick));
	ApplyDoorMotion(
		DoorRefusalChainActors,
		DoorRefusalChainRestLocations,
		DoorRefusalChainRestRotations,
		FVector(0.0f, -12.0f * ChainKick, 3.0f * FMath::Abs(ChainKick)),
		FRotator(0.0f, 5.0f * ChainKick, -7.0f * ChainKick));
	ApplyDoorMotion(
		DoorRefusalSurfaceActors,
		DoorRefusalSurfaceRestLocations,
		DoorRefusalSurfaceRestRotations,
		FVector(0.0f, -6.0f * SurfaceKick, 1.5f * FMath::Abs(SurfaceKick)),
		FRotator(0.0f, 0.0f, 3.0f * SurfaceKick));

	for (int32 Index = 0; Index < DoorRefusalEvidenceActors.Num(); ++Index)
	{
		AActor* FeedbackPart = DoorRefusalEvidenceActors[Index];
		if (!FeedbackPart || !DoorRefusalEvidenceRestLocations.IsValidIndex(Index) || !DoorRefusalEvidenceRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const float Direction = (Index % 2 == 0) ? 1.0f : -1.0f;
		const float Weight = FMath::Max(0.35f, 1.0f - static_cast<float>(Index) * 0.10f);
		const FVector Offset(0.0f, -4.5f * EvidenceKick * Weight, FMath::Abs(EvidenceKick) * 1.8f + EvidenceLift * 0.9f * Weight);
		const FRotator Rotation(EvidenceKick * 0.8f * Direction, Direction * EvidenceLift * 1.2f, EvidenceKick * 3.6f * Direction);
		FeedbackPart->SetActorLocationAndRotation(
			DoorRefusalEvidenceRestLocations[Index] + Offset,
			DoorRefusalEvidenceRestRotations[Index] + Rotation);
	}

	for (int32 Index = 0; Index < DoorRefusalWallpaperFlutterActors.Num(); ++Index)
	{
		AActor* FeedbackPart = DoorRefusalWallpaperFlutterActors[Index];
		if (!FeedbackPart || !DoorRefusalWallpaperFlutterRestLocations.IsValidIndex(Index) || !DoorRefusalWallpaperFlutterRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const float DelayBias = static_cast<float>(Index) * 0.37f;
		const float Flutter = FMath::Sin((WallpaperPhase * 6.0f + DelayBias) * UE_PI) * FMath::Pow(1.0f - WallpaperPhase, 0.72f);
		const float Lift = WallpaperHold * (1.0f - 0.16f * Index);
		FeedbackPart->SetActorLocationAndRotation(
			DoorRefusalWallpaperFlutterRestLocations[Index] + FVector(0.0f, -12.0f * Flutter, 5.0f * FMath::Max(0.0f, Lift)),
			DoorRefusalWallpaperFlutterRestRotations[Index] + FRotator(0.0f, 4.0f * Lift, 10.0f * Flutter));
	}

	if (WallpaperPhase > 0.0f && WallpaperPhase < 1.0f)
	{
		PulseHallLight(3600.0f + FMath::Abs(LightPulse) * 2250.0f + FMath::Max(0.0f, WallpaperHold) * 420.0f);
	}
	if (EvidencePhase > 0.0f && EvidencePhase < 1.0f)
	{
		const float PracticalPulse = FMath::Abs(EvidenceKick) * 1320.0f + EvidenceLift * 420.0f;
		if (ULightComponent* LightComponent = Room203PracticalLightActor ? Room203PracticalLightActor->FindComponentByClass<ULightComponent>() : nullptr)
		{
			LightComponent->SetIntensity(Room203PracticalLightRestIntensity + PracticalPulse);
		}
	}

	if (DoorRefusalFeedbackAlpha >= 1.0f)
	{
		ApplyDoorMotion(DoorRefusalLatchActors, DoorRefusalLatchRestLocations, DoorRefusalLatchRestRotations, FVector::ZeroVector, FRotator::ZeroRotator);
		ApplyDoorMotion(DoorRefusalChainActors, DoorRefusalChainRestLocations, DoorRefusalChainRestRotations, FVector::ZeroVector, FRotator::ZeroRotator);
		ApplyDoorMotion(DoorRefusalSurfaceActors, DoorRefusalSurfaceRestLocations, DoorRefusalSurfaceRestRotations, FVector::ZeroVector, FRotator::ZeroRotator);
		ApplyDoorMotion(DoorRefusalEvidenceActors, DoorRefusalEvidenceRestLocations, DoorRefusalEvidenceRestRotations, FVector::ZeroVector, FRotator::ZeroRotator);
		ApplyDoorMotion(DoorRefusalWallpaperFlutterActors, DoorRefusalWallpaperFlutterRestLocations, DoorRefusalWallpaperFlutterRestRotations, FVector::ZeroVector, FRotator::ZeroRotator);
		PulseHallLight(3600.0f);
		if (ULightComponent* LightComponent = Room203PracticalLightActor ? Room203PracticalLightActor->FindComponentByClass<ULightComponent>() : nullptr)
		{
			LightComponent->SetIntensity(Room203PracticalLightRestIntensity);
		}
		DoorRefusalFeedbackSeconds = 0.0f;
		bDoorRefusalFeedbackActive = false;
	}
}

void AHotelNightShiftPawn::TriggerReportLogFiledFeedback()
{
	if (!ReportLogFiledFeedbackActor && ReportLogFiledFeedbackActors.IsEmpty() && ReportLogFiledReactionActors.IsEmpty() && !ReportLogFiledLightActor)
	{
		return;
	}

	bReportLogFiledFeedbackActive = true;
	ReportLogFiledFeedbackAlpha = 0.0f;
	if (ULightComponent* LightComponent = ReportLogFiledLightActor ? ReportLogFiledLightActor->FindComponentByClass<ULightComponent>() : nullptr)
	{
		LightComponent->SetIntensity(ReportLogFiledLightRestIntensity + 980.0f);
	}
}

void AHotelNightShiftPawn::UpdateReportLogFiledFeedback(float DeltaSeconds)
{
	if (!bReportLogFiledFeedbackActive)
	{
		return;
	}

	ReportLogFiledFeedbackAlpha = FMath::Clamp(ReportLogFiledFeedbackAlpha + DeltaSeconds / 0.30f, 0.0f, 1.0f);
	const float Ease = FMath::InterpEaseOut(0.0f, 1.0f, ReportLogFiledFeedbackAlpha, 3.0f);
	const float Impact = FMath::Sin(ReportLogFiledFeedbackAlpha * UE_PI) * (1.0f - ReportLogFiledFeedbackAlpha);
	const float LightPulse = FMath::Sin(ReportLogFiledFeedbackAlpha * UE_PI);
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

	for (int32 Index = 0; Index < ReportLogFiledReactionActors.Num(); ++Index)
	{
		AActor* FeedbackPart = ReportLogFiledReactionActors[Index];
		if (!FeedbackPart || !ReportLogFiledReactionRestLocations.IsValidIndex(Index) || !ReportLogFiledReactionRestRotations.IsValidIndex(Index))
		{
			continue;
		}

		const float Direction = (Index % 2 == 0) ? 1.0f : -1.0f;
		const float DelayBias = FMath::Clamp(static_cast<float>(Index) * 0.09f, 0.0f, 0.28f);
		const float LocalAlpha = FMath::Clamp((ReportLogFiledFeedbackAlpha - DelayBias) / FMath::Max(0.1f, 1.0f - DelayBias), 0.0f, 1.0f);
		const float LocalEase = FMath::InterpEaseOut(0.0f, 1.0f, LocalAlpha, 2.2f);
		const float LocalImpact = FMath::Sin(LocalAlpha * UE_PI) * FMath::Pow(1.0f - LocalAlpha, 0.72f);
		const FVector ReactionOffset(
			Direction * 2.8f * LocalImpact,
			-5.0f * LocalEase - 2.5f * LocalImpact,
			3.8f * FMath::Abs(LocalImpact));
		const FRotator ReactionRotation(-3.8f * LocalImpact, Direction * 1.2f * LocalEase, Direction * 6.2f * LocalImpact);
		FeedbackPart->SetActorLocationAndRotation(
			ReportLogFiledReactionRestLocations[Index] + ReactionOffset,
			ReportLogFiledReactionRestRotations[Index] + ReactionRotation);
	}

	if (ULightComponent* LightComponent = ReportLogFiledLightActor ? ReportLogFiledLightActor->FindComponentByClass<ULightComponent>() : nullptr)
	{
		LightComponent->SetIntensity(ReportLogFiledLightRestIntensity + LightPulse * 1320.0f);
	}

	if (ReportLogFiledFeedbackAlpha >= 1.0f)
	{
		bReportLogFiledFeedbackActive = false;
		if (ULightComponent* LightComponent = ReportLogFiledLightActor ? ReportLogFiledLightActor->FindComponentByClass<ULightComponent>() : nullptr)
		{
			LightComponent->SetIntensity(ReportLogFiledLightRestIntensity);
		}
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

void AHotelNightShiftPawn::SetMonitorCheckLightIntensity(float NewIntensity)
{
	if (!MonitorCheckLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = MonitorCheckLightActor->FindComponentByClass<ULightComponent>())
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

void AHotelNightShiftPawn::SetReturnRouteTailLightIntensity(float NewIntensity)
{
	if (!ReturnRouteTailLightActor)
	{
		return;
	}

	if (ULightComponent* LightComponent = ReturnRouteTailLightActor->FindComponentByClass<ULightComponent>())
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

AActor* AHotelNightShiftPawn::FindLightActorWithTagNear(FName RequiredTag, const FVector& Anchor, float Radius) const
{
	TArray<AActor*> Actors;
	UGameplayStatics::GetAllActorsOfClass(this, AActor::StaticClass(), Actors);
	for (AActor* Actor : Actors)
	{
		if (
			Actor
			&& Actor->ActorHasTag(RequiredTag)
			&& IsActorNear(Actor, Anchor, Radius)
			&& Actor->FindComponentByClass<ULightComponent>())
		{
			return Actor;
		}
	}
	return nullptr;
}

float AHotelNightShiftPawn::GetLightIntensity(const AActor* LightActor) const
{
	if (!LightActor)
	{
		return 0.0f;
	}

	const ULightComponent* LightComponent = LightActor->FindComponentByClass<ULightComponent>();
	return LightComponent ? LightComponent->Intensity : 0.0f;
}
