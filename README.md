# Procedural-Locomotion-System

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
