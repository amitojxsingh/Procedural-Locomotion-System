#!/usr/bin/env python3
"""
Procedural Locomotion Animation Demo
Showcases procedural animation techniques without requiring Unreal Engine:
- Procedural walking cycle
- Dynamic body leaning based on movement
- Head rotation/oscillation
- Footstep IK simulation
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Polygon
from dataclasses import dataclass
import math

@dataclass
class CharacterState:
    """Represents the character's current state"""
    position: np.ndarray
    velocity: np.ndarray
    rotation: float
    lean_angle: float
    ground_speed: float
    direction: float
    time: float
    
class ProceduralCharacter:
    """Character with procedural locomotion animation"""
    
    def __init__(self):
        self.state = CharacterState(
            position=np.array([0.0, 0.0]),
            velocity=np.array([0.0, 0.0]),
            rotation=0.0,
            lean_angle=0.0,
            ground_speed=0.0,
            direction=0.0,
            time=0.0
        )
        
        # Animation parameters (matching Unreal implementation)
        self.max_lean_angle = 20.0  # degrees
        self.lean_interp_speed = 6.0
        self.head_pitch_amplitude = 10.0
        self.head_yaw_amplitude = 10.0
        self.head_oscillation_speed = 1.5
        
        # Locomotion parameters
        self.walk_speed = 2.0
        self.turn_rate = 90.0  # degrees per second
        
        # Skeleton proportions (relative units)
        self.body_height = 1.8
        self.head_size = 0.2
        self.leg_length = 0.9
        self.arm_length = 0.6
        
        # Movement path (creates a figure-8 pattern to show leaning)
        self.path_index = 0
        
    def update(self, dt):
        """Update character state (called each frame)"""
        self.state.time += dt
        
        # Create a figure-8 movement path to showcase leaning
        t = self.state.time * 0.3
        target_x = 3.0 * math.sin(t)
        target_y = 1.5 * math.sin(2 * t)
        
        # Calculate velocity toward target
        target_pos = np.array([target_x, target_y])
        direction_to_target = target_pos - self.state.position
        distance = np.linalg.norm(direction_to_target)
        
        if distance > 0.1:
            direction_to_target /= distance
            self.state.velocity = direction_to_target * self.walk_speed
        else:
            self.state.velocity *= 0.9
            
        # Update position
        self.state.position += self.state.velocity * dt
        
        # Calculate ground speed and direction
        self.state.ground_speed = np.linalg.norm(self.state.velocity)
        
        # Update rotation to face movement direction
        angle_diff = 0.0
        if self.state.ground_speed > 0.1:
            target_rotation = math.atan2(self.state.velocity[1], self.state.velocity[0])
            # Smooth rotation
            angle_diff = target_rotation - self.state.rotation
            # Normalize to [-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            self.state.rotation += angle_diff * 5.0 * dt
            
        # Calculate lean angle based on turning rate (like Unreal implementation)
        yaw_rate = angle_diff / max(dt, 0.001)  # degrees per second
        target_lean = yaw_rate * 0.3  # Convert to lean degrees
        target_lean = np.clip(target_lean, -self.max_lean_angle, self.max_lean_angle)
        
        # Interpolate lean angle
        self.state.lean_angle += (target_lean - self.state.lean_angle) * self.lean_interp_speed * dt
        
    def get_skeleton_points(self):
        """Calculate skeleton joint positions for rendering"""
        # Base position
        x, y = self.state.position
        rot = self.state.rotation
        
        # Apply lean (tilt the whole body)
        lean_rad = math.radians(self.state.lean_angle)
        
        # Rotation matrix
        cos_r = math.cos(rot)
        sin_r = math.sin(rot)
        
        def rotate_point(px, py):
            """Rotate point around character facing direction"""
            # Apply lean
            px_lean = px * math.cos(lean_rad)
            # Apply rotation
            return (x + px_lean * cos_r - py * sin_r,
                    y + px_lean * sin_r + py * cos_r)
        
        # Hip
        hip = (x, y)
        
        # Spine top
        spine_top = rotate_point(0, self.body_height * 0.6)
        
        # Head with procedural oscillation
        head_time = self.state.time * self.head_oscillation_speed
        head_pitch = math.sin(head_time) * math.radians(self.head_pitch_amplitude)
        head_yaw = math.cos(head_time) * math.radians(self.head_yaw_amplitude)
        
        head_offset_x = self.head_size * math.sin(head_yaw)
        head_offset_y = self.head_size * math.cos(head_pitch)
        
        head_x = spine_top[0] + head_offset_x * cos_r
        head_y = spine_top[1] + head_offset_y + 0.3
        head = (head_x, head_y)
        
        # Legs - procedural walk cycle
        stride_time = self.state.time * self.state.ground_speed * 2.0
        
        # Left leg
        left_phase = math.sin(stride_time)
        left_foot = rotate_point(
            -0.2 + left_phase * 0.3,
            -self.leg_length + abs(left_phase) * 0.2
        )
        
        # Right leg
        right_phase = math.sin(stride_time + math.pi)
        right_foot = rotate_point(
            0.2 + right_phase * 0.3,
            -self.leg_length + abs(right_phase) * 0.2
        )
        
        # Arms - swing opposite to legs
        left_hand = rotate_point(
            -0.4 - right_phase * 0.2,
            self.body_height * 0.3 - abs(right_phase) * 0.1
        )
        
        right_hand = rotate_point(
            0.4 - left_phase * 0.2,
            self.body_height * 0.3 - abs(left_phase) * 0.1
        )
        
        return {
            'hip': hip,
            'spine_top': spine_top,
            'head': head,
            'left_foot': left_foot,
            'right_foot': right_foot,
            'left_hand': left_hand,
            'right_hand': right_hand,
        }

class AnimationRenderer:
    """Renders and animates the procedural character"""
    
    def __init__(self):
        self.character = ProceduralCharacter()
        
        # Set up the figure
        self.fig, (self.ax_main, self.ax_info) = plt.subplots(1, 2, figsize=(14, 7))
        self.fig.suptitle('Procedural Locomotion System - Animation Demo', fontsize=16, fontweight='bold')
        
        # Main animation view
        self.ax_main.set_xlim(-5, 5)
        self.ax_main.set_ylim(-3, 3)
        self.ax_main.set_aspect('equal')
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_title('Character Animation (Figure-8 Path)')
        
        # Info panel
        self.ax_info.set_xlim(0, 10)
        self.ax_info.set_ylim(0, 10)
        self.ax_info.axis('off')
        
        # Initialize plot elements
        self.body_line, = self.ax_main.plot([], [], 'b-', linewidth=3, label='Body')
        self.left_leg_line, = self.ax_main.plot([], [], 'r-', linewidth=2.5, label='Left Leg')
        self.right_leg_line, = self.ax_main.plot([], [], 'g-', linewidth=2.5, label='Right Leg')
        self.left_arm_line, = self.ax_main.plot([], [], 'c-', linewidth=2)
        self.right_arm_line, = self.ax_main.plot([], [], 'm-', linewidth=2)
        self.head_circle = Circle((0, 0), 0.2, color='yellow', ec='black', linewidth=2)
        self.ax_main.add_patch(self.head_circle)
        
        # Trail showing path
        self.trail_line, = self.ax_main.plot([], [], 'k--', alpha=0.3, linewidth=1)
        self.trail_x = []
        self.trail_y = []
        
        # Info text
        self.info_text = self.ax_info.text(0.5, 9, '', fontsize=11, verticalalignment='top',
                                           family='monospace')
        
        # Add legend and technical info
        self.ax_main.legend(loc='upper right')
        
        tech_info = (
            "Technical Features:\n\n"
            "• Procedural walk cycle\n"
            "• Dynamic body leaning\n"
            "• Head oscillation (sine/cosine)\n"
            "• Inverse kinematics simulation\n"
            "• Real-time velocity calculation\n"
            "• Smooth rotation interpolation\n\n"
            "Implementation:\n"
            "• Character state management\n"
            "• Frame-by-frame updates\n"
            "• Mathematical transforms\n"
            "• Animation blending"
        )
        self.ax_info.text(0.5, 7.5, tech_info, fontsize=10, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Footer
        self.ax_info.text(5, 0.5, 'Portfolio Demo - Amitoj Gill\nProcedural Animation System',
                         fontsize=9, ha='center', style='italic')
        
    def update_frame(self, frame):
        """Update animation frame"""
        dt = 1.0 / 30.0  # 30 FPS
        self.character.update(dt)
        
        # Get skeleton points
        skeleton = self.character.get_skeleton_points()
        
        # Update body (hip to spine to head)
        body_x = [skeleton['hip'][0], skeleton['spine_top'][0]]
        body_y = [skeleton['hip'][1], skeleton['spine_top'][1]]
        self.body_line.set_data(body_x, body_y)
        
        # Update head
        self.head_circle.center = skeleton['head']
        
        # Update legs
        self.left_leg_line.set_data(
            [skeleton['hip'][0], skeleton['left_foot'][0]],
            [skeleton['hip'][1], skeleton['left_foot'][1]]
        )
        self.right_leg_line.set_data(
            [skeleton['hip'][0], skeleton['right_foot'][0]],
            [skeleton['hip'][1], skeleton['right_foot'][1]]
        )
        
        # Update arms
        self.left_arm_line.set_data(
            [skeleton['spine_top'][0], skeleton['left_hand'][0]],
            [skeleton['spine_top'][1], skeleton['left_hand'][1]]
        )
        self.right_arm_line.set_data(
            [skeleton['spine_top'][0], skeleton['right_hand'][0]],
            [skeleton['spine_top'][1], skeleton['right_hand'][1]]
        )
        
        # Update trail
        self.trail_x.append(skeleton['hip'][0])
        self.trail_y.append(skeleton['hip'][1])
        if len(self.trail_x) > 100:
            self.trail_x.pop(0)
            self.trail_y.pop(0)
        self.trail_line.set_data(self.trail_x, self.trail_y)
        
        # Update info text
        state = self.character.state
        info = (
            f"Time: {state.time:.2f}s\n\n"
            f"Position: ({state.position[0]:.2f}, {state.position[1]:.2f})\n"
            f"Ground Speed: {state.ground_speed:.2f} m/s\n"
            f"Rotation: {math.degrees(state.rotation):.1f}°\n"
            f"Lean Angle: {state.lean_angle:.1f}°\n\n"
            f"Velocity: ({state.velocity[0]:.2f}, {state.velocity[1]:.2f})\n"
        )
        self.info_text.set_text(info)
        
        return (self.body_line, self.left_leg_line, self.right_leg_line,
                self.left_arm_line, self.right_arm_line, self.head_circle,
                self.trail_line, self.info_text)
    
    def run(self, save_path=None):
        """Run the animation"""
        anim = animation.FuncAnimation(
            self.fig, self.update_frame,
            frames=600,  # 20 seconds at 30fps
            interval=33,  # ~30 FPS
            blit=True,
            repeat=True
        )
        
        if save_path:
            print(f"Saving animation to {save_path}...")
            writer = animation.FFMpegWriter(fps=30, bitrate=1800)
            anim.save(save_path, writer=writer)
            print("Animation saved!")
        
        plt.tight_layout()
        plt.show()
        
        return anim

def main():
    """Main entry point"""
    print("=" * 60)
    print("Procedural Locomotion Animation Demo")
    print("=" * 60)
    print("\nThis demo showcases procedural animation techniques:")
    print("  • Real-time character animation")
    print("  • Procedural walking cycle")
    print("  • Dynamic body leaning during turns")
    print("  • Head oscillation and rotation")
    print("  • Inverse kinematics simulation")
    print("\nTechnical implementation:")
    print("  • Character state management")
    print("  • Frame-by-frame physics updates")
    print("  • Mathematical transforms (rotation matrices)")
    print("  • Smooth interpolation")
    print("\n" + "=" * 60)
    print("\nStarting animation... (Close window to exit)")
    print("To save as video, use: --save animation.mp4")
    print("=" * 60 + "\n")
    
    renderer = AnimationRenderer()
    
    # Check if save argument provided
    import sys
    save_path = None
    if len(sys.argv) > 2 and sys.argv[1] == '--save':
        save_path = sys.argv[2]
    
    renderer.run(save_path)

if __name__ == '__main__':
    main()
