# Animation Quick Start Guide

This guide will help you run and showcase the procedural locomotion animation system in this project.

## What's Been Set Up

The project now includes:
- **ProceduralLocomotionAnimInstance** - C++ AnimInstance with:
  - Locomotion calculation (speed, direction, acceleration)
  - Procedural leaning based on movement
  - Procedural bone rotation (head/spine oscillation demo)
  
- **ProceduralCharacter** - C++ Character class ready to use with the AnimInstance

## Quick Test (Minimal Setup)

### Option 1: Simple Cube Test (No External Assets Needed)

1. **Compile the Project**
   - The Editor should be compiling now (you opened the .uproject)
   - Wait for compilation to complete
   
2. **Create a Blueprint Character**
   - In Content Browser, right-click → Blueprint Class → ProceduralCharacter
   - Name it `BP_ProceduralCharacter`
   - Open it
   
3. **Test in Editor**
   - Drag `BP_ProceduralCharacter` into your level
   - Set it as the Default Pawn (in World Settings → GameMode → Default Pawn Class)
   - Press **Play (Alt+P)** to see the procedural bone animation running

### Option 2: With UE5 Mannequin (Better Visual Result)

1. **Add Mannequin Content**
   - Go to Content Browser → Add/Import → Add Feature or Content Pack
   - Select "Third Person" template content
   - This gives you the UE5 Mannequin skeletal mesh
   
2. **Create Blueprint Character**
   - Content Browser → Right-click → Blueprint Class → ProceduralCharacter
   - Name it `BP_ProceduralCharacter`
   - Open it
   
3. **Assign Mannequin Mesh**
   - In the Blueprint editor, select the `Mesh (Inherited)` component
   - In Details panel → Mesh → Skeletal Mesh → Select `SKM_Manny` or `SKM_Quinn`
   - The AnimInstance should already be set to `ProceduralLocomotionAnimInstance`
   
4. **Configure Bone Name**
   - In the Blueprint, find the `ProceduralLocomotionAnimInstance` settings
   - Set `Procedural Bone Name` to `head` (for Mannequin)
   - Adjust amplitudes if needed (default: 10 degrees pitch/yaw)
   
5. **Test**
   - Drag `BP_ProceduralCharacter` into level
   - Press **Play**
   - Use WASD to move - watch the head oscillate and body lean during movement

## Creating Animation for Your Portfolio

### Method 1: Record Gameplay to Video

1. **Set Up a Nice Scene**
   - Create or open a level with good lighting
   - Place your character with the Mannequin mesh
   
2. **Record in Editor**
   - Window → Cinematics → Take Recorder
   - Add → Player (or your character actor)
   - Click "Record" and move your character around
   - Stop recording
   
3. **Render to Video**
   - Open the recorded Level Sequence
   - Click "Render Movie" icon (clapboard)
   - Choose format (MP4 or image sequence)
   - Set resolution (1920x1080 recommended)
   - Render and share the video

### Method 2: Use Sequencer for Cinematic Shot

1. **Create a Sequencer**
   - Cinematics → Add Level Sequence
   - Name it `AnimationShowcase`
   
2. **Add Character and Camera**
   - In Sequencer, click "+ Track" → Actor to Sequencer → Select your character
   - Add a Cine Camera Actor to the level
   - Add camera to Sequencer
   - Create camera movement (keyframe transforms)
   
3. **Animate Properties**
   - On character track, add the AnimInstance properties
   - Keyframe changes to `LeanAngle`, `GroundSpeed`, etc.
   - Or use the Simulation Mode to record movement
   
4. **Render**
   - Same as Method 1 - click "Render Movie"
   - Export as MP4 or image sequence

### Method 3: Create a Standalone Animation Sequence (Advanced)

1. **Record Animation Data**
   - Use the Animation Recording tools (Window → Animation → Animation Recording)
   - Record your character's movement
   - This creates a reusable Animation Sequence asset
   
2. **Polish in Persona**
   - Open the recorded Animation Sequence
   - Use Persona editor to clean up, add additive layers
   - Can blend with the procedural effects
   
3. **Create a Demo Reel**
   - Combine multiple animations
   - Show walk, run, turn, lean behaviors
   - Highlight the procedural leaning and bone rotation features

## What Makes This Portfolio-Ready

Your animation showcases:

✅ **C++ Programming** - Custom AnimInstance with locomotion logic  
✅ **Procedural Animation** - Code-driven bone manipulation (not just keyframes)  
✅ **Character Movement Integration** - Reads velocity, acceleration from Character  
✅ **Real-time IK Setup** - Footer IK properties ready for implementation  
✅ **Blendspace-Ready** - Direction and speed variables for 8-way locomotion  

## Pro Tips for Portfolio Presentation

1. **Show the Code** - Include a split-screen: gameplay + the C++ code
2. **Before/After** - Show character with vs without procedural effects
3. **Explain the Math** - Briefly note the physics (acceleration → lean angle)
4. **Multiple Scenarios** - Tight turns, sprinting, walking in circles
5. **Add Polish** - Good lighting, camera work, and a simple environment

## Next Steps

- Import mocap data (see [MoCap_Workflow.md](MoCap_Workflow.md))
- Implement the FootIK traces (extend `UpdateProceduralBone`)
- Create blend spaces for directional locomotion
- Add animation state machine (Idle, Walk, Run, Jump)

## Troubleshooting

**"Bone not found" warning:**
- Check the skeletal mesh's skeleton in Persona
- Update `ProceduralBoneName` to match an actual bone (e.g., `head`, `spine_03`)

**Character doesn't move:**
- Ensure you've set up input bindings (Project Settings → Input)
- Or use the Third Person template's input setup

**Animation doesn't play:**
- Verify the AnimInstance is assigned to the Skeletal Mesh Component
- Check the Output Log for compilation errors
- Make sure the skeletal mesh has a valid skeleton

---

**Ready to impress?** Record a quick 30-second clip showing smooth movement with procedural leaning and head motion, then send it to the team! 🎬
