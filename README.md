# Procedural Locomotion System

A technical animation system showcasing procedural locomotion, dynamic body leaning, and real-time character animation - implemented in both Unreal Engine C++ and standalone Python.

![Animation Demo](https://img.shields.io/badge/Animation-Procedural-blue)
![Platform](https://img.shields.io/badge/Platform-Unreal%20Engine%205-orange)
![Language](https://img.shields.io/badge/Language-C%2B%2B%20%7C%20Python-green)

## 🎯 Project Overview

This project demonstrates advanced procedural animation techniques for character locomotion, featuring:

- **Procedural Walking Cycle** - Dynamically generated leg/arm movement based on velocity
- **Dynamic Body Leaning** - Physics-based leaning during acceleration and turns
- **Procedural Bone Rotation** - Head oscillation using sine/cosine waves
- **Foot IK Setup** - Infrastructure for inverse kinematics foot placement
- **Real-time Animation Response** - Animation driven by character movement data

## 🚀 Quick Start (Interactive Demo - No Unreal Required!)

Want to see the animation immediately? Run the standalone Python demo:

```bash
# Install dependencies
pip3 install numpy matplotlib

# Run interactive demo with keyboard controls
python3 interactive_animation_demo.py

# Controls: WASD or Arrow Keys to move, SPACE to stop, ESC to quit
```

## 🎮 Features

### Unreal Engine Implementation (C++)

- **ProceduralLocomotionAnimInstance** - Custom AnimInstance class with:
  - Ground speed and direction calculation
  - Acceleration-based body leaning
  - Turn-rate based leaning
  - Procedural bone manipulation (head rotation)
  - Blueprint-exposed variables for runtime tuning

- **ProceduralCharacter** - Character class ready to use the AnimInstance

### Standalone Python Demo

- **Interactive Controls** - WASD/Arrow keys to control character movement
- **Real-time Visualization** - See the animation respond to your input
- **Technical Metrics** - Live display of speed, lean angle, rotation
- **Perfect for Portfolio** - Record and share immediately

## 📋 Technical Implementation

### Core Animation Variables

```cpp
// Locomotion (calculated per frame)
float GroundSpeed;        // Horizontal velocity magnitude
float Direction;          // Movement direction relative to facing
bool bIsAccelerating;     // Whether character is accelerating

// Procedural Leaning
float LeanAngle;          // Current body lean angle (degrees)
float MaxLeanAngle;       // Maximum lean (default: 20°)
float AccelerationLeanMultiplier;  // Accel → lean conversion
float YawRateLeanMultiplier;       // Turn rate → lean conversion

// Procedural Bone Animation
FName ProceduralBoneName;          // Bone to animate (e.g., "head")
float ProceduralBonePitchAmplitude; // Oscillation amount
float ProceduralBoneSpeed;          // Oscillation frequency
```

### Animation Flow

1. **Character Movement** → Velocity & Acceleration
2. **AnimInstance Update** → Calculate ground speed, direction
3. **Procedural Leaning** → Apply physics-based lean angle
4. **Bone Manipulation** → Oscillate head/spine bones
5. **Render** → Display animated character

## 🛠️ Unreal Engine Setup

### Prerequisites
- Unreal Engine 5.x
- Visual Studio Code or Visual Studio (for C++ editing)
- C++17 compatible compiler

### Build & Run

1. **Open Project**
   ```bash
   # Double-click or use command line
   open ProceduralLocomotionSystem.uproject
   ```

2. **Compile** (if prompted, let Unreal rebuild C++ modules)

3. **Create Character Blueprint**
   - Content Browser → New Blueprint → Select `ProceduralCharacter` parent class
   - Assign skeletal mesh (UE5 Mannequin recommended)
   - AnimInstance is auto-assigned to `ProceduralLocomotionAnimInstance`

4. **Test in Editor**
   - Place character in level
   - Press Play (Alt+P)
   - Move character to see procedural animation

See [Docs/Animation_QuickStart.md](Docs/Animation_QuickStart.md) for detailed setup.

## 📁 Project Structure

```
Procedural-Locomotion-System/
├── Source/
│   └── ProceduralLocomotionSystem/
│       ├── Public/
│       │   ├── ProceduralLocomotionAnimInstance.h  # Main AnimInstance
│       │   └── ProceduralCharacter.h               # Character class
│       └── Private/
│           ├── ProceduralLocomotionAnimInstance.cpp
│           └── ProceduralCharacter.cpp
├── Content/                    # Unreal assets (blueprints, meshes, etc.)
├── Config/                     # Engine configuration
├── Docs/
│   ├── Animation_QuickStart.md # Detailed Unreal setup guide
│   ├── MoCap_Workflow.md       # Motion capture workflow
│   └── DEMO_INSTRUCTIONS.md    # How to run & record demos
├── interactive_animation_demo.py  # Standalone interactive demo
├── standalone_animation_demo.py   # Auto-play demo
└── README.md                   # This file

## 🎬 Recording Animation for Portfolio

### Option 1: Python Demo (Fastest)

```bash
# Run interactive demo
python3 interactive_animation_demo.py

# Screen record on macOS: Cmd+Shift+5
# Move character in figure-8 patterns to show leaning
# Save and share the video
```

### Option 2: Unreal Engine (Professional)

1. Open Unreal Editor
2. Window → Cinematics → Take Recorder
3. Record character movement
4. Render to video (MP4, 1920x1080, 30fps)

See [Docs/DEMO_INSTRUCTIONS.md](Docs/DEMO_INSTRUCTIONS.md) for detailed recording steps.

## 🎓 Educational Value

This project demonstrates:

✅ **C++ Programming** - Custom Unreal Engine classes, inheritance, virtual functions  
✅ **Animation Programming** - AnimInstance, procedural animation, IK concepts  
✅ **Game Math** - Vector math, rotation matrices, interpolation, trigonometry  
✅ **Physics Simulation** - Acceleration, velocity, smooth damping  
✅ **Software Architecture** - Clean separation of concerns, reusable components  
✅ **Cross-Platform Development** - Unreal C++ + Python implementation  

## 🔧 Customization

Adjust these properties in Blueprint or C++ defaults:

```cpp
MaxLeanAngle = 20.0f;              // More lean = more dramatic turns
AccelerationLeanMultiplier = 0.02f; // How much to lean when accelerating
YawRateLeanMultiplier = 0.02f;     // How much to lean when turning
LeanInterpSpeed = 6.0f;            // How fast lean responds (higher = snappier)

ProceduralBonePitchAmplitude = 10.0f;  // Head nod amount
ProceduralBoneYawAmplitude = 10.0f;    // Head turn amount  
ProceduralBoneSpeed = 1.5f;            // Head oscillation speed
```

## 📝 TODO / Future Enhancements

- [ ] Implement full foot IK with ground tracing
- [ ] Add animation state machine (Idle, Walk, Run, Jump)
- [ ] Create 8-way locomotion blendspace
- [ ] Add motion matching integration
- [ ] Implement slope adaptation
- [ ] Add procedural hand IK for object interaction

## 🤝 Contributing

This is a portfolio/demonstration project. Feel free to fork and extend!

## 📄 License

See [LICENSE](LICENSE) file for details.

## 👤 Author

**Amitoj Gill**  
Technical Animator | Game Developer  

Showcasing procedural animation techniques and real-time character systems.

---

**Built with** ❤️ **and a lot of math** 🧮

## Project Overview

Procedural-Locomotion-System is a gameplay animation project focused on high-quality, responsive character locomotion in Unreal Engine 5. It blends motion capture (MoCap) driven animation with procedural techniques to improve responsiveness, grounding, and physicality in real time.

The goal is a Battlefield-style movement feel: stable weapon platform, weighty turning, believable body lean, and reliable foot placement on varied terrain.

## Tech Stack

- C++
- Unreal Engine 5
- Autodesk Maya

## Features

- **MoCap Retargeting**
  - Retarget MoCap onto in-game skeletons for consistent motion across characters.

- **Procedural Leaning**
  - Runtime lean driven by acceleration and yaw rotation rate, smoothed for animation-friendly results.

- **Foot IK**
  - Traces and offsets to keep feet grounded on slopes, stairs, and uneven terrain.

## Repository Structure

- `Source/` – C++ code (UE modules, components, animation instance logic)
- `Content/` – Unreal assets (animations, blueprints, meshes, maps)
- `Docs/` – Technical workflows and implementation notes
