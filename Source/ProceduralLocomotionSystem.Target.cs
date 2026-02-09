using UnrealBuildTool;
using System.Collections.Generic;

public class ProceduralLocomotionSystemTarget : TargetRules
{
	public ProceduralLocomotionSystemTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_0;
		ExtraModuleNames.AddRange(new string[] { "ProceduralLocomotionSystem" });
	}
}
