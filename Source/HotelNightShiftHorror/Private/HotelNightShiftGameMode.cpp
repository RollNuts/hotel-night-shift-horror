#include "HotelNightShiftGameMode.h"

#include "HotelNightShiftHUD.h"
#include "HotelNightShiftPawn.h"

AHotelNightShiftGameMode::AHotelNightShiftGameMode()
{
	DefaultPawnClass = AHotelNightShiftPawn::StaticClass();
	HUDClass = AHotelNightShiftHUD::StaticClass();
}
