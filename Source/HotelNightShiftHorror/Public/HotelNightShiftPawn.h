#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "HotelNightShiftPawn.generated.h"

class UCameraComponent;

UENUM(BlueprintType)
enum class EHotelLoopStage : uint8
{
	PhoneRinging,
	RequestKnown,
	MonitorChecked,
	DoorRefused,
	ReportFiled
};

UCLASS(Blueprintable)
class HOTELNIGHTSHIFTHORROR_API AHotelNightShiftPawn : public ACharacter
{
	GENERATED_BODY()

public:
	AHotelNightShiftPawn();

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

	UFUNCTION(BlueprintPure, Category = "Hotel Loop")
	FText GetObjectiveText() const;

	UFUNCTION(BlueprintPure, Category = "Hotel Loop")
	FText GetWorkMessageText() const;

	UFUNCTION(BlueprintPure, Category = "Hotel Loop")
	FText GetInteractionPromptText() const;

	UFUNCTION(BlueprintPure, Category = "Hotel Loop")
	float GetFearPressure() const;

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
	TObjectPtr<UCameraComponent> FirstPersonCamera;

private:
	void MoveForward(float Value);
	void MoveRight(float Value);
	void Turn(float Value);
	void LookUp(float Value);
	void Interact();
	void CacheHotelActors();
	void UpdateLookTarget();
	void StartPhoneRing();
	void PlayPhoneRing();
	void PlayActorSound(AActor* SoundActor) const;
	void PulseHallLight(float NewIntensity);
	void SetWorkState(EHotelLoopStage NewStage, const FString& NewObjective, const FString& NewMessage, float NewFearPressure);
	bool IsActorNear(const AActor* Actor, const FVector& Anchor, float Radius) const;
	AActor* FindAudioActorNear(const FVector& Anchor, float Radius) const;
	AActor* FindLightActorNear(const FVector& Anchor, float Radius) const;

	UPROPERTY()
	TObjectPtr<AActor> PhoneRingSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> DoorKnockSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> HallTargetLightActor;

	UPROPERTY()
	TObjectPtr<AActor> CurrentLookActor;

	FTimerHandle PhoneRingTimerHandle;

	EHotelLoopStage LoopStage = EHotelLoopStage::PhoneRinging;
	FString ObjectiveText;
	FString WorkMessageText;
	FString InteractionPromptText;
	float FearPressure = 0.0f;
	bool bMonitorChecked = false;
};
