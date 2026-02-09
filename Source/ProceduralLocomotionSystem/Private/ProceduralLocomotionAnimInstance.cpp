                                #include "ProceduralLocomotionAnimInstance.h"

#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

UProceduralLocomotionAnimInstance::UProceduralLocomotionAnimInstance() = default;

void UProceduralLocomotionAnimInstance::NativeInitializeAnimation()
{
	Super::NativeInitializeAnimation();

	CachedCharacter = Cast<ACharacter>(TryGetPawnOwner());
	if (CachedCharacter.IsValid())
	{
		LastYawDegrees = CachedCharacter->GetActorRotation().Yaw;
	}
}

void UProceduralLocomotionAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);

	if (DeltaSeconds <= 0.0f)
	{
		return;
	}

	ACharacter* Character = CachedCharacter.Get();
	if (!Character)
	{
		Character = Cast<ACharacter>(TryGetPawnOwner());
		CachedCharacter = Character;
		if (!Character)
		{
			return;
		}
	}

	const UCharacterMovementComponent* MoveComp = Character->GetCharacterMovement();
	const FVector Velocity = MoveComp ? MoveComp->Velocity : Character->GetVelocity();
	const FVector HorizontalVelocity(Velocity.X, Velocity.Y, 0.0f);

	GroundSpeed = HorizontalVelocity.Size();

	// Direction relative to the actor's facing (commonly fed into BlendSpaces)
	Direction = CalculateDirection(HorizontalVelocity, Character->GetActorRotation());

	bIsAccelerating = MoveComp && (MoveComp->GetCurrentAcceleration().SizeSquared() > KINDA_SMALL_NUMBER);

	UpdateProceduralLeaning(DeltaSeconds);
}

void UProceduralLocomotionAnimInstance::UpdateProceduralLeaning(float DeltaSeconds)
{
	ACharacter* Character = CachedCharacter.Get();
	if (!Character)
	{
		return;
	}

	const UCharacterMovementComponent* MoveComp = Character->GetCharacterMovement();
	const FVector WorldAccel = MoveComp ? MoveComp->GetCurrentAcceleration() : FVector::ZeroVector;

	// Convert acceleration into local space so +Y means "accelerating to the right" relative to facing.
	const FTransform ActorTransform(Character->GetActorRotation(), Character->GetActorLocation());
	const FVector LocalAccel = ActorTransform.InverseTransformVectorNoScale(WorldAccel);

	const float CurrentYaw = Character->GetActorRotation().Yaw;
	const float YawDelta = FMath::FindDeltaAngleDegrees(LastYawDegrees, CurrentYaw);
	const float YawRateDegPerSec = YawDelta / FMath::Max(DeltaSeconds, KINDA_SMALL_NUMBER);
	LastYawDegrees = CurrentYaw;

	float TargetLeanAngle = (LocalAccel.Y * AccelerationLeanMultiplier) + (YawRateDegPerSec * YawRateLeanMultiplier);
	TargetLeanAngle = FMath::Clamp(TargetLeanAngle, -MaxLeanAngle, MaxLeanAngle);

	LeanAngle = FMath::FInterpTo(LeanAngle, TargetLeanAngle, DeltaSeconds, LeanInterpSpeed);
}
