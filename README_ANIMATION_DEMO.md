# Procedural Locomotion Animation Demo

**Quick portfolio-ready animation showcase** - No Unreal Engine required!

## What This Demonstrates

This standalone Python animation showcases the same procedural animation techniques from the Unreal project:

✅ **Procedural Walking Animation** - Mathematically generated walk cycle  
✅ **Dynamic Body Leaning** - Character leans into turns based on velocity changes  
✅ **Head Oscillation** - Procedural bone rotation using sine/cosine waves  
✅ **IK Simulation** - Foot placement adjusts to stride  
✅ **Real-time Physics** - Velocity, rotation, and interpolation  

## Quick Start (2 Commands)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the animation
python3 standalone_animation_demo.py
```

The animation window will open showing a stick figure walking in a figure-8 pattern with:
- Body leaning during turns
- Procedural leg movement
- Head bobbing/rotation
- Real-time metrics display

## Record for Portfolio

### Option 1: Screen Recording (Easiest)
1. Run the animation
2. Use macOS screen recorder: `Cmd+Shift+5` → Record Selected Portion
3. Capture the animation window for 10-15 seconds
4. Save as MP4 and send to recruiters

### Option 2: Direct Video Export (Requires FFmpeg)
```bash
# Install FFmpeg (if not already installed)
brew install ffmpeg

# Save animation directly as MP4
python3 standalone_animation_demo.py --save portfolio_animation.mp4
```

This creates a ready-to-share video file.

## What to Tell Recruiters

> "This is a procedural locomotion system I developed that demonstrates:
> 
> - **Procedural animation generation** - No keyframe animation; entirely code-driven
> - **Real-time physics simulation** - Velocity-based leaning and movement
> - **Mathematical transforms** - Rotation matrices, interpolation, trigonometric oscillation
> - **Character state management** - Position, rotation, lean angle updated per frame
> 
> The system calculates body lean based on turning rate (like how a bike leans into turns), 
> generates walking cycles procedurally, and applies bone rotations in real-time.
> 
> I also have an Unreal Engine C++ implementation with the same algorithms that includes
> foot IK, blend spaces, and integration with UE's Character Movement Component."

## Technical Highlights for Portfolio

The code demonstrates:

1. **Object-Oriented Design**
   - `CharacterState` dataclass for clean state management
   - `ProceduralCharacter` encapsulates locomotion logic
   - `AnimationRenderer` separates rendering from simulation

2. **Animation Mathematics**
   - Rotation matrices for coordinate transforms
   - Trigonometric functions for oscillation (head bob)
   - Linear interpolation for smooth transitions
   - Vector math for velocity and direction

3. **Real-time Simulation**
   - Frame-based updates (delta time)
   - Physics-based movement (velocity → position)
   - Smooth rotation using angle normalization
   - Responsive state changes

4. **Production Patterns**
   - Configurable parameters (lean angle, speeds)
   - Modular update functions
   - Clean separation of concerns
   - Documentation and type hints

## File Structure

```
├── standalone_animation_demo.py   # Main animation program
├── requirements.txt               # Python dependencies
└── README_ANIMATION_DEMO.md       # This file
```

## Troubleshooting

**"No module named 'matplotlib'"**
```bash
pip3 install matplotlib numpy
```

**Animation is laggy**
- Normal on first run; matplotlib needs to initialize
- Reduce trail length or frame count in code if needed

**Can't save video**
```bash
# Install FFmpeg first
brew install ffmpeg
# Then retry save command
```

## Extending the Demo

Quick modifications to customize:

**Change movement path:**
```python
# In ProceduralCharacter.update() method:
target_x = 5.0 * math.cos(t * 0.5)  # Circular path
target_y = 5.0 * math.sin(t * 0.5)
```

**Adjust animation style:**
```python
# In __init__:
self.max_lean_angle = 30.0  # More dramatic leaning
self.walk_speed = 4.0       # Faster movement
```

**Add more bones:**
Extend `get_skeleton_points()` to add spine segments, fingers, etc.

---

**Ready to send!** Run the demo, record it, and share with recruiters showing your procedural animation skills. 🎬
