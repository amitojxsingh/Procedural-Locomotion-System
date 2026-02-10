#include "ProceduralCharacter.h"
#include "ProceduralLocomotionAnimInstance.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

AProceduralCharacter::AProceduralCharacter()
{
	PrimaryActorTick.bCanEverTick = true;

	// Set up capsule
	GetCapsuleComponent()->InitCapsuleSize(42.f, 96.0f);

	// Configure character movement
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.0f, 540.0f, 0.0f);
	GetCharacterMovement()->JumpZVelocity = 600.f;
	GetCharacterMovement()->AirControl = 0.2f;

	// Configure mesh
	USkeletalMeshComponent* MeshComp = GetMesh();
	if (MeshComp)
	{
		MeshComp->SetRelativeLocation(FVector(0.0f, 0.0f, -96.0f));
		MeshComp->SetRelativeRotation(FRotator(0.0f, -90.0f, 0.0f));
		
		// Set anim instance class
		MeshComp->SetAnimInstanceClass(UProceduralLocomotionAnimInstance::StaticClass());
	}
}

void AProceduralCharacter::BeginPlay()
{
	Super::BeginPlay();
	
	SetupDefaultMeshAndAnimation();
}

void AProceduralCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}

void AProceduralCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
}

void AProceduralCharacter::SetupDefaultMeshAndAnimation()
{
	USkeletalMeshComponent* MeshComp = GetMesh();
	if (!MeshComp)
	{
		return;
	}

	// Note: In the Editor, you can assign a skeletal mesh (e.g., UE5 Mannequin)
	// via the Blueprint derived from this class or directly on instances.
	// The AnimInstance is already set in the constructor.
	
	// If no mesh is assigned, try to load a default (UE5 Mannequin)
	if (!MeshComp->GetSkeletalMeshAsset())
	{
		static ConstructorHelpers::FObjectFinder<USkeletalMesh> MeshFinder(
			TEXT("/Engine/EngineMeshes/SkeletalCube")
		);
		if (MeshFinder.Succeeded())
		{
			MeshComp->SetSkeletalMesh(MeshFinder.Object);
		}
	}
}
