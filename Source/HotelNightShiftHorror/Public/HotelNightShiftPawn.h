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
	ReturnRouteCleared,
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
	FText GetDeskStatusText() const;

	UFUNCTION(BlueprintPure, Category = "Hotel Loop")
	FText GetInteractionPromptText() const;

	UFUNCTION(BlueprintPure, Category = "Hotel Loop")
	float GetFearPressure() const;

#if WITH_DEV_AUTOMATION_TESTS
	EHotelLoopStage AutomationGetLoopStage() const;
	bool AutomationInteractWithActor(AActor* TargetActor);
	bool AutomationIsPhoneRingTimerActive() const;
	bool AutomationIsPhoneLineConnected() const;
	bool AutomationHasPhoneLineSound() const;
	bool AutomationIsPatrolListenActive() const;
	bool AutomationIsPatrolListenResolved() const;
	void AutomationAdvancePatrolListen(float DeltaSeconds);
	bool AutomationIsReturnRouteAnomalyActive() const;
	bool AutomationIsReturnRouteAnomalyResolved() const;
	void AutomationAdvanceReturnRouteAnomaly(float DeltaSeconds);
	FVector AutomationGetReturnRouteBackKnockLocation() const;
	FVector AutomationGetReturnRouteCameraRelativeLocation() const;
	float AutomationGetReturnRouteCameraFieldOfView() const;
	bool AutomationHasReturnRouteTailSound() const;
	float AutomationGetReturnRouteLightIntensity() const;
	float AutomationGetReturnRouteTailLightIntensity() const;
	int32 AutomationCountMovedReturnRouteBackKnockActors(float MinDistance) const;
	bool AutomationIsPostReportMonitorMismatchActive() const;
	void AutomationAdvancePostReportMonitorMismatch(float DeltaSeconds);
	bool AutomationIsPostReportDeskWaitActive() const;
	bool AutomationIsPostReportDeskWaitResolved() const;
	void AutomationAdvancePostReportDeskWait(float DeltaSeconds);
	FVector AutomationGetPostReportDeskWaitRattleLocation() const;
	bool AutomationIsPostReportLogSelfCorrectionActive() const;
	bool AutomationHasPostReportLogSelfCorrection() const;
	void AutomationAdvancePostReportLogSelfCorrection(float DeltaSeconds);
	float AutomationGetPostReportLogSelfCorrectionAlpha() const;
	FVector AutomationGetPostReportLogSelfCorrectionLocation() const;
	void AutomationAdvancePhoneReceiver(float DeltaSeconds);
	float AutomationGetPhoneReceiverLiftAlpha() const;
	FVector AutomationGetPhoneReceiverLocation() const;
	FRotator AutomationGetPhoneReceiverRotation() const;
	bool AutomationIsPhoneReceiverLiftActive() const;
	FVector AutomationGetPhoneCordTugLocation() const;
	void AutomationAdvanceDoorRefusalFeedback(float DeltaSeconds);
	float AutomationGetDoorRefusalFeedbackAlpha() const;
	bool AutomationIsDoorRefusalFeedbackActive() const;
	FVector AutomationGetDoorRefusalFeedbackLocation() const;
	FVector AutomationGetDoorRefusalLatchLocation() const;
	FVector AutomationGetDoorRefusalChainLocation() const;
	FVector AutomationGetDoorRefusalSurfaceLocation() const;
	FVector AutomationGetDoorRefusalWallpaperFlutterLocation() const;
	void AutomationAdvanceReportLogFiledFeedback(float DeltaSeconds);
	float AutomationGetReportLogFiledFeedbackAlpha() const;
	FVector AutomationGetReportLogFiledFeedbackLocation() const;
#endif

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
	TObjectPtr<UCameraComponent> FirstPersonCamera;

private:
	void MoveForward(float Value);
	void MoveRight(float Value);
	void Turn(float Value);
	void LookUp(float Value);
	void Interact();
	bool TryInteractWithActor(AActor* TargetActor);
	void CacheHotelActors();
	void UpdateLookTarget();
	void StartPhoneRing();
	void PlayPhoneRing();
	void StopPhoneRing();
	void StartPhoneLineAudio();
	void StopPhoneLineAudio();
	void PlayActorSound(AActor* SoundActor) const;
	void UpdatePatrolListenAnomaly(float DeltaSeconds);
	void StartPatrolListenAnomaly();
	void ResolvePatrolListenAnomaly();
	void UpdateReturnRouteAnomaly(float DeltaSeconds);
	void StartReturnRouteAnomaly();
	void ResolveReturnRouteAnomaly();
	void UpdateReturnRouteBackKnockFeedback(float NormalizedTime);
	void ResetReturnRouteBackKnockFeedback();
	void CaptureReturnRouteCameraRestState();
	void ApplyReturnRouteCameraPressure(float NormalizedTime, float Pulse);
	void ResetReturnRouteCameraPressure();
	void TriggerPostReportMonitorMismatch();
	void UpdatePostReportMonitorMismatch(float DeltaSeconds);
	void TriggerPostReportDeskWaitAnomaly();
	void UpdatePostReportDeskWaitAnomaly(float DeltaSeconds);
	void TriggerPostReportLogSelfCorrection();
	void UpdatePostReportLogSelfCorrection(float DeltaSeconds);
	void UpdatePhoneRingVisual(float DeltaSeconds);
	void LiftPhoneReceiver();
	void UpdatePhoneReceiverAnimation(float DeltaSeconds);
	void TriggerDoorRefusalFeedback();
	void UpdateDoorRefusalFeedback(float DeltaSeconds);
	void TriggerReportLogFiledFeedback();
	void UpdateReportLogFiledFeedback(float DeltaSeconds);
	void SetPhoneIndicatorIntensity(float NewIntensity);
	void SetPatrolListenLightIntensity(float NewIntensity);
	void SetReturnRouteLightIntensity(float NewIntensity);
	void SetReturnRouteTailLightIntensity(float NewIntensity);
	void SetPostReportMonitorMismatchLightIntensity(float NewIntensity);
	void SetPostReportDeskWaitLightIntensity(float NewIntensity);
	void SetPostReportLogSelfCorrectionLightIntensity(float NewIntensity);
	void PulseHallLight(float NewIntensity);
	void SetWorkState(
		EHotelLoopStage NewStage,
		const FString& NewObjective,
		const FString& NewMessage,
		const FString& NewDeskStatus,
		float NewFearPressure);
	bool ActorMatches(const AActor* Actor, const FVector& Anchor, float Radius, FName RequiredTag) const;
	bool IsActorNear(const AActor* Actor, const FVector& Anchor, float Radius) const;
	AActor* FindAudioActorNear(const FVector& Anchor, float Radius) const;
	AActor* FindActorWithTagNear(FName RequiredTag, const FVector& Anchor, float Radius) const;
	TArray<AActor*> FindActorsWithTagNear(FName RequiredTag, const FVector& Anchor, float Radius) const;
	AActor* FindLightActorNear(const FVector& Anchor, float Radius) const;
	AActor* FindLightActorWithTagNear(FName RequiredTag, const FVector& Anchor, float Radius) const;
	float GetLightIntensity(const AActor* LightActor) const;

	UPROPERTY()
	TObjectPtr<AActor> PhoneRingSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PhonePickupSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PhoneLineSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PhoneReceiverActor;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> PhoneReceiverActors;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> PhoneCordTugActors;

	UPROPERTY()
	TObjectPtr<AActor> DoorKnockSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> DoorRefusalFeedbackActor;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> DoorRefusalFeedbackActors;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> DoorRefusalLatchActors;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> DoorRefusalChainActors;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> DoorRefusalSurfaceActors;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> DoorRefusalWallpaperFlutterActors;

	UPROPERTY()
	TObjectPtr<AActor> Room203AftershockSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> ReportFiledSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> ReportLogFiledFeedbackActor;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> ReportLogFiledFeedbackActors;

	UPROPERTY()
	TObjectPtr<AActor> PatrolListenSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PatrolListenLightActor;

	UPROPERTY()
	TObjectPtr<AActor> ReturnRouteSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> ReturnRouteTailSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> ReturnRouteLightActor;

	UPROPERTY()
	TObjectPtr<AActor> ReturnRouteTailLightActor;

	UPROPERTY()
	TObjectPtr<AActor> ReturnRouteBackKnockActor;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> ReturnRouteBackKnockActors;

	UPROPERTY()
	TObjectPtr<AActor> PostReportMonitorMismatchSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PostReportMonitorMismatchLightActor;

	UPROPERTY()
	TObjectPtr<AActor> PostReportDeskWaitSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PostReportDeskWaitLightActor;

	UPROPERTY()
	TObjectPtr<AActor> PostReportDeskWaitRattleActor;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> PostReportDeskWaitRattleActors;

	UPROPERTY()
	TObjectPtr<AActor> PostReportLogSelfCorrectionSoundActor;

	UPROPERTY()
	TObjectPtr<AActor> PostReportLogSelfCorrectionFeedbackActor;

	UPROPERTY()
	TArray<TObjectPtr<AActor>> PostReportLogSelfCorrectionFeedbackActors;

	UPROPERTY()
	TObjectPtr<AActor> PostReportLogSelfCorrectionLightActor;

	UPROPERTY()
	TObjectPtr<AActor> HallTargetLightActor;

	UPROPERTY()
	TObjectPtr<AActor> PhoneIndicatorLightActor;

	UPROPERTY()
	TObjectPtr<AActor> CurrentLookActor;

	FTimerHandle PhoneRingTimerHandle;

	EHotelLoopStage LoopStage = EHotelLoopStage::PhoneRinging;
	FString ObjectiveText;
	FString WorkMessageText;
	FString DeskStatusText;
	FString InteractionPromptText;
	float FearPressure = 0.0f;
	float PhoneRingVisualClock = 0.0f;
	float PhoneReceiverLiftSeconds = 0.0f;
	float PhoneReceiverLiftAlpha = 0.0f;
	FVector PhoneReceiverRestLocation = FVector::ZeroVector;
	FVector PhoneReceiverLiftLocation = FVector::ZeroVector;
	FRotator PhoneReceiverRestRotation = FRotator::ZeroRotator;
	FRotator PhoneReceiverLiftRotation = FRotator::ZeroRotator;
	TArray<FVector> PhoneReceiverPartRestLocations;
	TArray<FRotator> PhoneReceiverPartRestRotations;
	TArray<FVector> PhoneCordTugRestLocations;
	TArray<FRotator> PhoneCordTugRestRotations;
	TArray<FVector> DoorRefusalFeedbackRestLocations;
	TArray<FRotator> DoorRefusalFeedbackRestRotations;
	TArray<FVector> DoorRefusalLatchRestLocations;
	TArray<FRotator> DoorRefusalLatchRestRotations;
	TArray<FVector> DoorRefusalChainRestLocations;
	TArray<FRotator> DoorRefusalChainRestRotations;
	TArray<FVector> DoorRefusalSurfaceRestLocations;
	TArray<FRotator> DoorRefusalSurfaceRestRotations;
	TArray<FVector> DoorRefusalWallpaperFlutterRestLocations;
	TArray<FRotator> DoorRefusalWallpaperFlutterRestRotations;
	TArray<FVector> ReportLogFiledFeedbackRestLocations;
	TArray<FRotator> ReportLogFiledFeedbackRestRotations;
	TArray<FVector> ReturnRouteBackKnockRestLocations;
	TArray<FRotator> ReturnRouteBackKnockRestRotations;
	FVector ReturnRouteCameraRestRelativeLocation = FVector::ZeroVector;
	float ReturnRouteCameraRestFieldOfView = 90.0f;
	TArray<FVector> PostReportDeskWaitRattleRestLocations;
	TArray<FRotator> PostReportDeskWaitRattleRestRotations;
	TArray<FVector> PostReportLogSelfCorrectionFeedbackRestLocations;
	TArray<FRotator> PostReportLogSelfCorrectionFeedbackRestRotations;
	int32 PhoneRingCount = 0;
	bool bMonitorChecked = false;
	bool bPhoneReceiverLiftActive = false;
	bool bPhoneLineConnected = false;
	float PatrolListenHoldSeconds = 0.0f;
	float PatrolListenPulseClock = 0.0f;
	bool bPatrolListenActive = false;
	bool bPatrolListenResolved = false;
	float ReturnRouteAnomalySeconds = 0.0f;
	float ReturnRoutePulseClock = 0.0f;
	bool bReturnRouteAnomalyActive = false;
	bool bReturnRouteAnomalyResolved = false;
	bool bReturnRouteTailSoundPlayed = false;
	bool bReturnRouteCameraRestCaptured = false;
	float PostReportMonitorMismatchSeconds = 0.0f;
	float PostReportMonitorMismatchPulseClock = 0.0f;
	bool bPostReportMonitorMismatchActive = false;
	bool bPostReportMonitorMismatchObserved = false;
	float PostReportDeskWaitHoldSeconds = 0.0f;
	float PostReportDeskWaitSeconds = 0.0f;
	float PostReportDeskWaitPulseClock = 0.0f;
	bool bPostReportDeskWaitActive = false;
	bool bPostReportDeskWaitResolved = false;
	float PostReportLogSelfCorrectionAlpha = 0.0f;
	float PostReportLogSelfCorrectionPulseClock = 0.0f;
	bool bPostReportLogSelfCorrectionActive = false;
	bool bPostReportLogSelfCorrectionObserved = false;
	float DoorRefusalFeedbackSeconds = 0.0f;
	float DoorRefusalFeedbackAlpha = 0.0f;
	bool bDoorRefusalFeedbackActive = false;
	bool bDoorRefusalAftershockSoundPlayed = false;
	float ReportLogFiledFeedbackAlpha = 0.0f;
	bool bReportLogFiledFeedbackActive = false;
};
