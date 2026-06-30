using UnrealBuildTool;

public class HotelNightShiftHorror : ModuleRules
{
	public HotelNightShiftHorror(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
			"EnhancedInput",
			"InputCore"
		});
	}
}
