#pragma once

#include "Modules/ModuleManager.h"

class FProceduralLocomotionSystemModule final : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
