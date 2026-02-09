using UnrealBuildTool;
using System.Collections.Generic;

public class ProceduralLocomotionSystemEditorTarget : TargetRules
{
	public ProceduralLocomotionSystemEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V5;
		IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_0;
		ExtraModuleNames.AddRange(new string[] { "ProceduralLocomotionSystem" });
	}
}
