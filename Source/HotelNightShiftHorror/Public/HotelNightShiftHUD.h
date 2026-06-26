#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "HotelNightShiftHUD.generated.h"

UCLASS()
class HOTELNIGHTSHIFTHORROR_API AHotelNightShiftHUD : public AHUD
{
	GENERATED_BODY()

public:
	virtual void DrawHUD() override;
};
