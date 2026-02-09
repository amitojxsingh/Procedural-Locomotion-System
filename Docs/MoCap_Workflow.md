# MoCap Workflow (Maya → UE5 IK Retargeting → Footstep Markers)

This document describes a production-style pipeline for importing motion capture (**.FBX**) into **Maya**, retargeting it onto the **Unreal Engine 5 Mannequin** using **IK Rig / IK Retargeter**, and then using **Animation Data Modifiers** (C++) to automatically generate **footstep sync markers** from the animation data.

> Assumptions
> - Your MoCap FBX contains a skeleton (and optionally a mesh) with consistent naming and stable bone orientations.
> - You have a “high-fidelity” source rig (more joints / twist bones / facial, etc.) and a target gameplay rig (UE5 Manny/Quinn).
> - Your UE5 project uses standard animation assets: `USkeleton`, `UAnimSequence`, IK Rig assets, and an IK Retargeter asset.

---

## 1) Importing .FBX MoCap into Maya

### 1.1 Pre-import checks (before Maya)

- **Frame rate**: Confirm the MoCap capture FPS (commonly 30/60/120). Decide your pipeline FPS and keep it consistent end-to-end.
- **Units**: UE uses centimeters; Maya can use centimeters. Ensure conversion is intentional (don’t “accidentally” scale by 100).
- **Coordinate system**:
  - Maya is Y-up by default.
  - UE is Z-up.
  - Most FBX importers handle this, but you must verify the character’s forward axis and root orientation after import.
- **Root definition**:
  - Identify the intended *root motion* node (often `root` / `hips` / `pelvis` depending on provider).
  - Decide whether you want the animation authored **in-place** or with **root motion**.

### 1.2 Maya FBX import settings (recommended)

In Maya: **File → Import** (or **File → Open Scene** if it’s a full scene). In the FBX options:

- **File Type Specific Options**
  - **Animation**: enabled
  - **Bake Animation**: enabled (if the file has constraints; otherwise optional)
  - **Resample All**: enabled if the source is noisy or irregularly sampled
  - **Quaternion Interpolation**: `Resample As Euler` can help with editor stability, but keep an eye on gimbal issues
- **Axis conversion**: leave default unless the FBX is known to be wrong
- **Units conversion**: keep consistent with your scene units

### 1.3 Cleanup pass (Maya)

After import:

1. **Verify scale**
   - Measure a known distance (e.g., Manny’s height ~180 cm).
2. **Verify orientation**
   - Character faces expected forward in your rig space.
3. **Fix bone roll / joint orientation issues early**
   - Do not “patch over” major joint orientation mismatch with constraints later; it will haunt retargeting.
4. **Stabilize hips/root**
   - If the capture has jitter, apply filtering carefully (Butterworth / Euler filter) and inspect foot contact frames.
5. **Remove unnecessary transforms**
   - Avoid double transforms (group nodes above skeleton that introduce offsets).
6. **Set the correct playback range**
   - Trim dead frames at head/tail.

### 1.4 Export from Maya for Unreal

When exporting a cleaned MoCap clip as FBX for UE:

- Export **skeleton only** for anim clips (mesh optional).
- Ensure:
  - **Bake animation** on export
  - **Start/End** match your clip range
  - **Frame rate** matches the capture/pipeline
  - **Up axis** and **unit scale** are consistent
- Use a consistent naming convention (example):
  - `AN_Run_Fwd_01`, `AN_Stop_L_01`, `AN_Turn90_R_01`

---

## 2) Retargeting MoCap to UE5 Mannequin (IK Retargeting)

UE5’s **IK Rig / IK Retargeter** workflow is the modern approach (recommended over legacy Retarget Manager).

### 2.1 Importing source animation into UE5

1. **Import FBX** into your UE project.
2. In the import dialog:
   - **Import Animations**: enabled
   - **Import Mesh**: optional
   - **Skeleton**: select the correct *source* skeleton (high-fidelity) or create a new one
   - **Convert Scene** / **Force Front XAxis**: only if your orientation is wrong
   - **Preserve Local Transform**: consider enabling if the skeleton has complex offsets
3. Confirm the resulting `UAnimSequence` plays correctly on the source skeleton.

### 2.2 Create IK Rig assets

You need **two** IK Rig assets:

- **Source IK Rig** (for high-fidelity skeleton)
- **Target IK Rig** (for UE5 Mannequin Manny/Quinn)

In each IK Rig:

1. Define **Retarget Chains** (critical):
   - Spine: `Spine` chain (pelvis → spine_01 → spine_02 → spine_03 → neck → head)
   - Arms: `Arm_L`, `Arm_R` (clavicle → upperarm → lowerarm → hand)
   - Legs: `Leg_L`, `Leg_R` (thigh → calf → foot → ball)
   - Optional: fingers, twist bones, IK bones
2. Set the **Retarget Root**
   - Typically the pelvis/hips/root depending on skeleton.
   - For Manny: pelvis is often a good root for chains; root bone may be used for root motion.

### 2.3 Create an IK Retargeter asset

Create: **IK Retargeter**

- **Source IK Rig**: your high-fidelity IK Rig
- **Target IK Rig**: UE5 Mannequin IK Rig

In the retargeter:

1. **Chain mapping**: map each source chain → target chain.
2. **Retarget pose** (very important):
   - Align source and target into a similar base pose.
   - If the source is A-pose and target is T-pose (or vice versa), create a custom retarget pose to reduce shoulder/arm artifacts.
3. **Root / pelvis translation settings**:
   - Decide if you want:
     - **In-place** gameplay clips (root translation removed / stabilized), or
     - **Root motion** clips (root translation preserved).
   - Configure root translation retarget mode accordingly.
4. Preview multiple clips:
   - Focus on:
     - foot contact (sliding/penetration)
     - knee pop
     - pelvis height
     - shoulder deformation

### 2.4 Common retargeting pitfalls (and fixes)

- **Feet drift / sliding**
  - Ensure leg chain includes foot and ball.
  - Ensure the retarget pose aligns hip height and leg length as well as possible.
  - Check scale mismatch and unit conversion.

- **Knee collapse or popping**
  - Check chain definitions and bone orientations.
  - Consider adding IK goals / solvers in IK Rig if required (depending on your setup).

- **Arms crossing / shoulders exploding**
  - Retarget pose mismatch is the #1 cause.
  - Verify clavicle is included correctly.

---

## 3) Auto-generating Footstep Sync Markers with Animation Data Modifiers (C++)

### 3.1 What “Animation Data Modifiers” are

An **Animation Modifier** is an editor-time data processing step that can be applied to animation assets (typically `UAnimSequence`) to add/adjust:

- **Notifies** (footsteps, weapon events)
- **Curves** (foot IK weights, stride warping weights)
- **Sync markers** (for animation syncing and matching)

This is ideal for MoCap because you can batch-process large libraries and keep results consistent.

### 3.2 Footstep detection strategy (robust, production-friendly)

You need a signal that correlates with foot contact.

Common approaches:

1. **Foot bone vertical velocity**
   - When the foot’s vertical velocity crosses below a threshold and the foot is near the ground plane → “contact”.
2. **Foot height relative to root/pelvis**
   - Track foot bone Z relative to root. Contact occurs near local minima.
3. **Foot speed near zero while planted**
   - During stance phase, foot speed is low. Combined with height, this is robust.
4. **Optional: use existing curves from DCC**
   - If your Maya cleanup outputs a curve like `FootPlant_L` and `FootPlant_R`, your modifier can just convert those into markers.

Recommended hybrid heuristic:

- Compute per-frame:
  - Foot height (relative to root) and foot speed
- Detect local minima where:
  - height is within a tolerance
  - speed is below a threshold
  - enforce a minimum time between steps

### 3.3 What to generate

Two typical outputs:

- **Sync markers**: `Foot_L`, `Foot_R` at contact frames (useful for sync groups)
- **Anim notifies**: `Footstep_L`, `Footstep_R` (useful for gameplay/audio)

You can generate either or both.

### 3.4 C++ structure: a custom Animation Modifier

Create a class derived from `UAnimationModifier`. In the editor, you apply it to selected animations.

Skeleton code (editor-only concept):

```cpp
// Pseudocode / pattern — exact API calls vary slightly by UE version.
// Put this into an Editor module or guard with WITH_EDITOR.

#include "Animation/AnimationModifier.h"
#include "AnimationBlueprintLibrary.h"

UCLASS()
class UGenerateFootstepMarkersModifier : public UAnimationModifier
{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere, Category="Footsteps")
	FName LeftFootBone = TEXT("foot_l");

	UPROPERTY(EditAnywhere, Category="Footsteps")
	FName RightFootBone = TEXT("foot_r");

	UPROPERTY(EditAnywhere, Category="Footsteps")
	float MaxFootSpeedForPlant = 3.0f; // cm/s, tune per library

	UPROPERTY(EditAnywhere, Category="Footsteps")
	float MinTimeBetweenSteps = 0.18f; // seconds

protected:
	virtual void OnApply_Implementation(UAnimSequence* AnimationSequence) override
	{
		// 1) Sample foot bone transforms over time
		// 2) Compute height + speed
		// 3) Detect contact frames
		// 4) Write Sync Markers or Notifies

		// Typical helper surface lives in UAnimationBlueprintLibrary.
		// Example operations you may need:
		// - Evaluate bone transforms at time
		// - Add or remove notifies / markers
		// - Add curves for debug (optional)
	}
};
```

### 3.5 Sampling animation data (practical guidance)

In editor code you typically:

- Iterate frames (or time steps) from `0 → SequenceLength`.
- For each time sample:
  - Evaluate foot bone transform in component or local space.
  - Compute height signal (e.g., relative to root/pelvis).
  - Compute speed signal using finite differences:
    - $v \approx \|p(t) - p(t-\Delta t)\| / \Delta t$

Notes:

- Use consistent sample rate (the animation’s frame rate if available).
- Be careful with compression; use evaluation functions that return the *evaluated pose*, not raw keys.

### 3.6 Writing sync markers / notifies

In many pipelines:

- **Sync markers** drive animation syncing inside a Sync Group.
- **Notifies** drive gameplay/audio.

Implementation details vary by UE version and project setup, but the overall flow is:

1. Remove existing autogenerated markers (idempotency).
2. Add markers at detected contact times.
3. Optionally add metadata:
   - marker names: `Foot_L`, `Foot_R`
   - notify payload: surface type (resolved at runtime), foot index, etc.

### 3.7 Validation checklist

After applying the modifier to a batch of MoCap clips:

- Scrub the animation sequence and verify:
  - markers land exactly on the *first planted* frame (not mid-stance)
  - no duplicate markers within a single step
  - left/right alternation looks correct
- In gameplay:
  - footstep sounds line up with perceived impacts
  - VFX spawn at correct times
  - network prediction doesn’t cause repeated footsteps (prefer animation-driven events but gate gameplay if needed)

---

## 4) Best Practices: Root Motion + Foot Sliding Cleanup

### 4.1 Decide early: In-place vs Root Motion

- **In-place locomotion** (common for shooters):
  - Movement is driven by character movement component; animation is visual.
  - Pros: responsive; easy to network; easy to blend.
  - Cons: foot sliding must be handled via tuning/IK/warping.

- **Root motion locomotion**:
  - Animation drives movement.
  - Pros: high fidelity; foot planting is easier.
  - Cons: gameplay responsiveness and networking are harder; requires careful authoring.

Many Battlefield-style systems are predominantly **in-place**, with targeted use of root motion for specials (vaults, takedowns, certain turns).

### 4.2 Root motion cleanup (Maya)

- Ensure there is a clean **root node**:
  - Root has world translation/rotation.
  - Pelvis/hips contains body motion relative to root.
- Remove unwanted drift:
  - If you want in-place: constrain root translation to zero (keep rotation if desired), then re-bake.
- Separate vertical motion:
  - Keep vertical bounce on pelvis/spine, not on root (unless you intentionally want root Z motion).

### 4.3 Root motion configuration (Unreal)

- For each `UAnimSequence`:
  - Verify root bone track exists (if using root motion).
  - Check root lock options (root lock to ref pose / first frame) based on your project standard.

### 4.4 Foot sliding: the real causes

Foot sliding usually comes from one (or more) of these:

- Speed mismatch between animation and gameplay velocity
- Retargeting pose mismatch causing foot arc changes
- Compression artifacts / noisy capture
- Poorly defined contact frames (the “plant” phase isn’t stable)

### 4.5 Practical fixes for foot sliding

**In DCC (best ROI):**

- Fix the plant phase first:
  - Pin planted foot in an animation layer, then adjust hips/pelvis.
- Remove jitter with care:
  - Over-filtering can cause “floaty” feet.
- Align stride length:
  - If your gameplay speed is fixed (e.g., 600 cm/s), tune the clip or scale time so the stride matches.

**In Unreal (runtime fixes):**

- Add **Foot IK** to reduce penetration and stabilize contact.
- Use animation curves:
  - `FootPlant_L/R` to drive IK alpha and lock.
- Consider **stride warping / speed warping**:
  - Adjust stride length dynamically to match gameplay speed.
- For slopes/stairs:
  - Ensure pelvis offset logic is stable and filtered (avoid oscillation).

### 4.6 Retargeting-specific best practices

- Always create a clean, agreed-upon **retarget pose** for each skeleton.
- Verify bone naming and chain coverage (especially feet and ball).
- Test with a diagnostic clip:
  - straight walk, straight run, strafe, and a turn-in-place.

---

## 5) Recommended conventions

- Marker names:
  - Sync markers: `Foot_L`, `Foot_R`
  - Notifies: `Footstep_L`, `Footstep_R`
- Curves:
  - `FootPlant_L`, `FootPlant_R` (0–1)
  - `StrideScale` (optional)
- File naming:
  - `AN_<Verb>_<Direction>_<Variant>`

---

## 6) Next steps (optional additions)

If you want this pipeline to be fully “hands-off” at scale:

- Add a “MoCap Import Checklist” script in Maya (Python) to standardize:
  - FPS, units, time range trimming, root cleaning, naming
- Implement a full editor module in UE that:
  - Applies the `UAnimationModifier` to a folder
  - Writes per-clip diagnostics (CSV) for step counts and contact timing
- Integrate gameplay by consuming markers in animation state machines / sync groups.
