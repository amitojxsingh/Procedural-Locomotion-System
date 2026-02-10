# Animation Demo Instructions

Complete guide to running and recording the procedural locomotion animation for your portfolio.

## 🎯 Quick Summary

**Fastest Option:** Python interactive demo (ready in 30 seconds)  
**Professional Option:** Unreal Engine recording (requires UE5 installation)

---

## Option 1: Python Interactive Demo (RECOMMENDED for Quick Portfolio Submission)

### Prerequisites
```bash
pip3 install numpy matplotlib
```

### Starting the Demo

```bash
cd /path/to/Procedural-Locomotion-System
python3 interactive_animation_demo.py
```

A window will open with the animated character.

### Controls

| Key | Action |
|-----|--------|
| **W** or **↑** | Move Forward |
| **S** or **↓** | Move Backward |
| **A** or **←** | Turn Left |
| **D** or **→** | Turn Right |
| **SPACE** | Stop Movement |
| **ESC** | Close Demo |

### Recording the Demo

**macOS Screen Recording:**
1. Press **Cmd + Shift + 5**
2. Select "Record Selected Portion"
3. Draw a box around the animation window
4. Click "Record"
5. Run the demo and control the character:
   - Walk forward in a circle (shows walking cycle)
   - Make tight figure-8 patterns (shows body leaning)
   - Quick turns (shows maximum lean angle)
   - Vary speed (shows procedural head oscillation)
6. Click the stop button in menu bar when done
7. Video saves to Desktop

**Recommended Recording Length:** 30-60 seconds

**What to Showcase:**
- Forward movement (procedural walk cycle)
- Circular movement (body lean during turns)
- Speed changes (animation responds to velocity)
- Figure-8 patterns (maximum lean angles)
- The real-time stats panel (proves it's procedural, not pre-baked)

### Stopping the Demo

- Press **ESC** in the animation window, or
- Close the window, or
- Press **Ctrl+C** in terminal

---

## Option 2: Unreal Engine Demo (Professional Quality)

### Prerequisites
- Unreal Engine 5.x installed
- UE5 Mannequin (Third Person template content)

### Setup Steps

1. **Open Project**
   ```bash
   open ProceduralLocomotionSystem.uproject
   ```
   
2. **Wait for Compilation**
   - Unreal will compile the C++ code automatically
   - This may take 5-10 minutes on first open
   - Look for "Compiling C++ modules" in bottom-right

3. **Import Mannequin** (if not already in project)
   - Content Browser → Add/Import → Add Feature or Content Pack
   - Select "Third Person" template
   - Import

4. **Create Character Blueprint**
   - Content Browser → Right-click → Blueprint Class
   - Select `ProceduralCharacter` as parent
   - Name: `BP_ProceduralCharacter`
   - Open the blueprint

5. **Assign Skeletal Mesh**
   - Select `Mesh (Inherited)` component in blueprint
   - Details Panel → Mesh → Skeletal Mesh → Choose `SKM_Manny` or `SKM_Quinn`
   - The AnimInstance should already be `ProceduralLocomotionAnimInstance`
   - Compile and Save

6. **Test Character**
   - Drag `BP_ProceduralCharacter` into level
   - Press **Play (Alt+P)**
   - Use WASD to move and test

### Recording in Unreal

#### Method A: Take Recorder (Quick)

1. **Window → Cinematics → Take Recorder**
2. Click **+ Add** → **Player**
3. Click **Record** button
4. Move character around level
5. Press **Stop** when done
6. Sequencer opens with recorded animation

#### Method B: Level Sequence (Professional)

1. **Create Sequence**
   - Toolbar → Cinematics → Add Level Sequence
   - Name: `AnimationShowcase`

2. **Add Character**
   - In Sequencer, click **+ Track**
   - Actor to Sequencer → Select your character

3. **Add Camera**
   - Place a Cine Camera Actor in level
   - Add to Sequencer
   - Position camera to frame character nicely
   - Add a camera track binding

4. **Animate**
   - Use the Sequencer timeline to keyframe character movement
   - Or use Simulate mode to record live movement

### Rendering Video

1. **Click "Render Movie"** (clapboard icon in Sequencer)
2. Configure settings:
   - Output Format: **Video Sequence (.mp4)**
   - Resolution: **1920x1080** (Full HD)
   - Frame Rate: **30 fps**
   - Quality: **High**
3. Choose output location
4. Click **Render**
5. Wait for rendering (may take several minutes)

### Stopping Unreal Editor

- **File → Exit**, or
- Close the window (will prompt to save)

---

## 📊 What the Animation Demonstrates

Your video should showcase:

### Technical Features
✅ **Procedural Walk Cycle** - Legs/arms move based on velocity (not pre-animated)  
✅ **Dynamic Body Leaning** - Character leans into turns (physics-based)  
✅ **Head Oscillation** - Procedural bone rotation using sine/cosine  
✅ **Real-time Response** - Animation adjusts to movement instantly  
✅ **Smooth Interpolation** - Velocity, rotation, and lean blend smoothly  

### Implementation Skills
✅ **C++ Programming** - Custom AnimInstance class  
✅ **Animation Systems** - Understanding of animation graphs and state  
✅ **Game Mathematics** - Vectors, matrices, trigonometry  
✅ **Physics Integration** - Acceleration, velocity calculations  
✅ **Real-time Systems** - Frame-by-frame updates and interpolation  

---

## 🎬 Video Presentation Tips

### For Portfolio:

1. **Keep it Short** - 30-60 seconds is perfect
2. **Show Variety** - Different movements (walk, turn, circle, figure-8)
3. **Include UI** - Python demo shows real-time stats (proves procedural)
4. **Explain in Email** - Briefly describe what's procedural vs pre-baked

### Sample Video Script:

> "This demonstrates my procedural locomotion system. The character's walk cycle, 
> body lean, and head movement are all generated in real-time from C++ code - 
> no pre-baked animations. The lean angle responds to turn rate and acceleration, 
> while the walk cycle adjusts to velocity. Built in Unreal Engine with C++."

---

## 🐛 Troubleshooting

### Python Demo Won't Start

**Error: "No module named 'numpy'"**
```bash
pip3 install numpy matplotlib
```

**Error: "No module named 'tkinter'"**
```bash
# macOS (if using Homebrew Python)
brew install python-tk

# Or use system Python
/usr/bin/python3 interactive_animation_demo.py
```

**Window doesn't appear**
- Check if window opened behind other windows
- Try running from terminal (not background)
- Ensure matplotlib backend is working

### Unreal Engine Issues

**Compilation Errors**
- Close Unreal Editor
- Delete `Intermediate/` and `Binaries/` folders
- Reopen .uproject (will rebuild from scratch)

**Character doesn't move**
- Check that you've set up input bindings, or
- Use the Third Person template's default controls

**Animation doesn't play**
- Verify AnimInstance is assigned to Skeletal Mesh
- Check Output Log for errors
- Ensure skeletal mesh has a valid skeleton

**Red squiggles in VS Code but compiles fine**
- These are IntelliSense errors, not real compiler errors
- The code will compile successfully in Unreal
- To suppress: See `.vscode/settings.json` (already configured)

---

## 📤 Sharing Your Animation

### File Size Optimization

If video is too large (>10MB):
```bash
# Compress with ffmpeg (if installed)
ffmpeg -i original.mp4 -vcodec h264 -acodec aac -crf 28 compressed.mp4

# Or use online compressor: https://www.freeconvert.com/video-compressor
```

### Upload Methods

1. **Google Drive / Dropbox**
   - Upload video
   - Get shareable link
   - Include link in email

2. **YouTube (Unlisted)**
   - Upload as "Unlisted" video
   - Share link in email
   - Can add annotations/descriptions

3. **Vimeo**
   - Professional presentation
   - Password-protect if desired
   - Share link

4. **Email Attachment** (if <10MB)
   - Directly attach to reply email

---

## ✅ Pre-Submission Checklist

Before sending to the company:

- [ ] Video is 30-60 seconds long
- [ ] Shows variety of movement (forward, turns, circles)
- [ ] Quality is clear (720p minimum, 1080p preferred)
- [ ] File size is reasonable (<25MB for email, or use link)
- [ ] Audio is muted or has professional background music (optional)
- [ ] Your name/contact is in the email (not required in video)

---

## 🚀 You're Ready!

Choose your method:
- **Quick submission:** Python demo + screen record (10 minutes total)
- **Professional:** Unreal Engine + rendered video (1-2 hours)

Both demonstrate the same technical skills! The Python version is actually impressive 
because it shows you can implement the same logic in multiple languages/platforms.

Good luck with your submission! 🎯
