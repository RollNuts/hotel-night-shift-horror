#include "HotelNightShiftHUD.h"

#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "HotelNightShiftPawn.h"

void AHotelNightShiftHUD::DrawHUD()
{
	Super::DrawHUD();

	if (!Canvas)
	{
		return;
	}

	const AHotelNightShiftPawn* HotelPawn = Cast<AHotelNightShiftPawn>(GetOwningPawn());
	if (!HotelPawn)
	{
		return;
	}

	const FText Header = FText::FromString(TEXT("NIGHT LOG / FRONT DESK"));
	const FText Objective = HotelPawn->GetObjectiveText();
	const FText Message = HotelPawn->GetWorkMessageText();
	const FText DeskStatus = HotelPawn->GetDeskStatusText();
	const FText Prompt = HotelPawn->GetInteractionPromptText();

	const float Left = 38.0f;
	const float Top = 34.0f;
	const FLinearColor Paper = FLinearColor(0.84f, 0.80f, 0.68f, 1.0f);
	const FLinearColor Dim = FLinearColor(0.58f, 0.72f, 0.69f, 1.0f);
	const FLinearColor Warning = FLinearColor(1.0f, 0.64f, 0.29f, 1.0f);
	const FLinearColor LineGreen = FLinearColor(0.36f, 0.95f, 0.58f, 1.0f);

	Canvas->SetDrawColor(Paper.ToFColor(true));
	Canvas->DrawText(GEngine->GetSmallFont(), Header, Left, Top, 1.0f, 1.0f, FFontRenderInfo());
	Canvas->DrawText(GEngine->GetSmallFont(), Objective, Left, Top + 24.0f, 1.0f, 1.0f, FFontRenderInfo());
	if (!Message.IsEmpty())
	{
		Canvas->SetDrawColor(Dim.ToFColor(true));
		Canvas->DrawText(GEngine->GetSmallFont(), Message, Left, Top + 50.0f, 1.0f, 1.0f, FFontRenderInfo());
	}

	if (!DeskStatus.IsEmpty())
	{
		Canvas->SetDrawColor(LineGreen.ToFColor(true));
		Canvas->DrawText(GEngine->GetSmallFont(), DeskStatus, Left, Top + 78.0f, 1.0f, 1.0f, FFontRenderInfo());
	}

	const FString FearLine = FString::Printf(TEXT("Lobby pressure: %.0f%%"), HotelPawn->GetFearPressure() * 100.0f);
	Canvas->SetDrawColor(Warning.ToFColor(true));
	Canvas->DrawText(GEngine->GetSmallFont(), FText::FromString(FearLine), Left, Top + 104.0f, 1.0f, 1.0f, FFontRenderInfo());

	if (!Prompt.IsEmpty())
	{
		const float PromptX = Canvas->ClipX * 0.5f - 150.0f;
		const float PromptY = Canvas->ClipY * 0.68f;
		Canvas->SetDrawColor(Paper.ToFColor(true));
		Canvas->DrawText(GEngine->GetMediumFont(), Prompt, PromptX, PromptY, 1.0f, 1.0f, FFontRenderInfo());
	}
}
