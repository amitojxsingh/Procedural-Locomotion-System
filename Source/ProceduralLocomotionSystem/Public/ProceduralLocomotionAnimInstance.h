#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "ProceduralLocomotionAnimInstance.generated.h"

UCLASS(Blueprintable, BlueprintType)
class UProceduralLocomotionAnimInstance : public UAnimInstance
{
	GENERATED_BODY()

public:
	UProceduralLocomotionAnimInstance();

	virtual void NativeInitializeAnimation() override;
	virtual void NativeUpdateAnimation(float DeltaSeconds) override;

protected:
	// --- Locomotion ---
	UPROPERTY(BlueprintReadOnly, Category = "Locomotion")
	float GroundSpeed = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Locomotion")
	float Direction = 0.0f;

	UPROPERTY(BlueprintReadOnly, Category = "Locomotion")
	bool bIsAccelerating = false;

	// --- Procedural Leaning ---
	UPROPERTY(BlueprintReadOnly, Category = "Locomotion|Leaning")
	float LeanAngle = 0.0f;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|Leaning")
	float MaxLeanAngle = 20.0f;

	// Acceleration is in cm/s^2; multipliers are tuned to produce degrees.
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|Leaning")
	float AccelerationLeanMultiplier = 0.02f;

	// Yaw rate is degrees/sec; multiplier converts to degrees of lean.
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|Leaning")
	float YawRateLeanMultiplier = 0.02f;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|Leaning")
	float LeanInterpSpeed = 6.0f;

	// --- Foot IK (header definitions; traces/offsets are commonly implemented in ABP or a component) ---
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|FootIK")
	float LeftFootTraceDistance = 55.0f;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|FootIK")
	float RightFootTraceDistance = 55.0f;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|FootIK")
	float FootTraceStartHeight = 25.0f;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|FootIK")
	float FootTraceEndHeight = 65.0f;

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|FootIK")
	FName LeftFootBoneName = TEXT("foot_l");

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Locomotion|FootIK")
	FName RightFootBoneName = TEXT("foot_r");

private:
	void UpdateProceduralLeaning(float DeltaSeconds);

	TWeakObjectPtr<class ACharacter> CachedCharacter;
	float LastYawDegrees = 0.0f;
};
