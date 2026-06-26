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
const FVector PhoneIndicatorLightAnchor(-395.0f, -555.0f, 158.0f);
const FVector DoorKnockSoundAnchor(3920.0f, 285.0f, 150.0f);
const FVector HallTargetLightAnchor(3920.0f, 0.0f, 260.0f);
const FName PhoneInteractTag(TEXT("Hotel.Interact.Phone"));
const FName MonitorInteractTag(TEXT("Hotel.Interact.Monitor"));
const FName Room203DoorInteractTag(TEXT("Hotel.Interact.Room203Door"));
const FName ReportLogInteractTag(TEXT("Hotel.Interact.ReportLog"));
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
	UpdatePhoneRingVisual(DeltaSeconds);
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
	if (!CurrentLookActor)
	{
		return;
	}

	if (ActorMatches(CurrentLookActor, PhoneAnchor, 90.0f, PhoneInteractTag) && LoopStage == EHotelLoopStage::PhoneRinging)
	{
		StopPhoneRing();
		PlayActorSound(PhonePickupSoundActor);
		SetPhoneIndicatorIntensity(96.0f);

		SetWorkState(
			EHotelLoopStage::RequestKnown,
			TEXT("Room 203 request: check the monitor before you leave the desk."),
			TEXT("Caller: 'Room 203. Do not open unless the hallway camera agrees.'"),
			TEXT("DESK LINE: CONNECTED / ROOM 203"),
			0.34f);
		return;
	}

	if (ActorMatches(CurrentLookActor, MonitorAnchor, 130.0f, MonitorInteractTag) && LoopStage == EHotelLoopStage::RequestKnown)
	{
		bMonitorChecked = true;
		PulseHallLight(85.0f);
		SetWorkState(
			EHotelLoopStage::MonitorChecked,
			TEXT("Go to Room 203 and keep the door closed."),
			TEXT("Monitor feed: empty hallway. The call says that should be impossible."),
			TEXT("DESK LINE: HOLDING / CAMERA MISMATCH"),
			0.54f);
		return;
	}

	if (
		ActorMatches(CurrentLookActor, Door203Anchor, 190.0f, Room203DoorInteractTag)
		&& (LoopStage == EHotelLoopStage::RequestKnown || LoopStage == EHotelLoopStage::MonitorChecked))
	{
		PlayActorSound(DoorKnockSoundActor);
		PulseHallLight(24.0f);
		SetWorkState(
			EHotelLoopStage::DoorRefused,
			TEXT("Return to the front desk and record the refusal."),
			bMonitorChecked
				? TEXT("Room 203 knocks after you refuse. The monitor still showed nobody.")
				: TEXT("Room 203 knocks before you checked the camera. That mistake now matters."),
			TEXT("DESK LINE: SILENT / REFUSAL PENDING"),
			0.76f);
		return;
	}

	if (ActorMatches(CurrentLookActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::DoorRefused)
	{
		SetWorkState(
			EHotelLoopStage::ReportFiled,
			TEXT("Entry filed. Stay at the desk and wait for the next call."),
			TEXT("Night log: 203 refused, hallway camera mismatch, knock confirmed."),
			TEXT("DESK LINE: CLOSED / INCIDENT LOGGED"),
			0.63f);
	}
}

void AHotelNightShiftPawn::CacheHotelActors()
{
	PhoneRingSoundActor = FindAudioActorNear(PhoneSoundAnchor, 90.0f);
	PhonePickupSoundActor = FindAudioActorNear(PhonePickupSoundAnchor, 80.0f);
	DoorKnockSoundActor = FindAudioActorNear(DoorKnockSoundAnchor, 140.0f);
	HallTargetLightActor = FindLightActorNear(HallTargetLightAnchor, 260.0f);
	PhoneIndicatorLightActor = FindLightActorNear(PhoneIndicatorLightAnchor, 90.0f);
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
	else if (
		ActorMatches(HitActor, Door203Anchor, 190.0f, Room203DoorInteractTag)
		&& (LoopStage == EHotelLoopStage::RequestKnown || LoopStage == EHotelLoopStage::MonitorChecked))
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Refuse and keep closed");
	}
	else if (ActorMatches(HitActor, ReportLogAnchor, 120.0f, ReportLogInteractTag) && LoopStage == EHotelLoopStage::DoorRefused)
	{
		CurrentLookActor = HitActor;
		InteractionPromptText = TEXT("E  Record incident");
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
