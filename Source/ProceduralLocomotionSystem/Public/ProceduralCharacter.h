#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ProceduralCharacter.generated.h"

UCLASS()
class PROCEDURALLOCOMOTIONSYSTEM_API AProceduralCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	AProceduralCharacter();

protected:
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

private:
	// Helper to set up a default skeletal mesh and anim instance if none set in editor
	void SetupDefaultMeshAndAnimation();
};
