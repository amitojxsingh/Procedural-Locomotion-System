#!/usr/bin/env python3
"""
Interactive Procedural Locomotion Animation Demo
Control the character with keyboard and see procedural animation respond in real-time.

Controls:
    W/↑ - Move Forward
    S/↓ - Move Backward  
    A/← - Turn Left
    D/→ - Turn Right
    SPACE - Stop
    ESC - Quit
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import math

class InteractiveCharacter:
    """Character with keyboard-controlled procedural locomotion"""
    
    def __init__(self):
        # State
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.rotation = 0.0  # radians
        self.lean_angle = 0.0
        self.ground_speed = 0.0
        self.time = 0.0
        self.last_rotation = 0.0
        
        # Input state
        self.input_forward = 0.0
        self.input_turn = 0.0
        
        # Movement parameters
        self.max_speed = 3.0  # units per second
        self.acceleration = 8.0
        self.turn_speed = 2.5  # radians per second
        self.friction = 0.85
        
        # Animation parameters (from Unreal C++ implementation)
        self.max_lean_angle = 20.0  # degrees
        self.lean_interp_speed = 6.0
        self.head_pitch_amplitude = 10.0
        self.head_yaw_amplitude = 10.0
        self.head_oscillation_speed = 1.5
        
        # Skeleton proportions
        self.body_height = 1.8
        self.head_size = 0.2
        self.leg_length = 0.9
        
    def update(self, dt):
        """Update character state based on input"""
        self.time += dt
        
        # Update rotation from input
        if self.input_turn != 0:
            rotation_change = self.input_turn * self.turn_speed * dt
            self.last_rotation = self.rotation
            self.rotation += rotation_change
        
        # Calculate target velocity from input
        cos_r = math.cos(self.rotation)
        sin_r = math.sin(self.rotation)
        
        target_velocity = np.array([
            self.input_forward * cos_r * self.max_speed,
            self.input_forward * sin_r * self.max_speed
        ])
        
        # Apply acceleration toward target velocity
        velocity_diff = target_velocity - self.velocity
        accel_magnitude = min(self.acceleration * dt, np.linalg.norm(velocity_diff))
        
        if np.linalg.norm(velocity_diff) > 0.001:
            velocity_diff = velocity_diff / np.linalg.norm(velocity_diff) * accel_magnitude
            self.velocity += velocity_diff
        
        # Apply friction
        self.velocity *= self.friction
        
        # Update position
        self.position += self.velocity * dt
        
        # Calculate ground speed
        self.ground_speed = np.linalg.norm(self.velocity)
        
        # Calculate lean angle based on turning (like Unreal implementation)
        yaw_rate = (self.rotation - self.last_rotation) / max(dt, 0.001)
        self.last_rotation = self.rotation
        
        # Convert yaw rate to lean angle (procedural leaning)
        target_lean = math.degrees(yaw_rate) * 0.5
        target_lean = np.clip(target_lean, -self.max_lean_angle, self.max_lean_angle)
        
        # Interpolate lean angle smoothly
        self.lean_angle += (target_lean - self.lean_angle) * self.lean_interp_speed * dt
        
    def get_skeleton_points(self):
        """Calculate skeleton joint positions for rendering"""
        x, y = self.position
        rot = self.rotation
        
        # Apply lean
        lean_rad = math.radians(self.lean_angle)
        
        cos_r = math.cos(rot)
        sin_r = math.sin(rot)
        
        def rotate_point(px, py):
            """Rotate and position point"""
            px_lean = px * math.cos(lean_rad)
            return (x + px_lean * cos_r - py * sin_r,
                    y + px_lean * sin_r + py * cos_r)
        
        # Hip (base)
        hip = (x, y)
        
        # Spine top
        spine_top = rotate_point(0, self.body_height * 0.6)
        
        # Head with procedural oscillation
        head_time = self.time * self.head_oscillation_speed
        head_pitch = math.sin(head_time) * math.radians(self.head_pitch_amplitude)
        head_yaw = math.cos(head_time) * math.radians(self.head_yaw_amplitude)
        
        head_offset_x = self.head_size * math.sin(head_yaw)
        head_offset_y = self.head_size * math.cos(head_pitch)
        
        head_x = spine_top[0] + head_offset_x * cos_r
        head_y = spine_top[1] + head_offset_y + 0.3
        head = (head_x, head_y)
        
        # Procedural walk cycle for legs
        stride_time = self.time * max(self.ground_speed, 0.5) * 2.0
        
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
        
        # Arms swing opposite to legs
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

class InteractiveRenderer:
    """Interactive animation renderer with keyboard controls"""
    
    def __init__(self):
        self.character = InteractiveCharacter()
        
        # Set up figure
        self.fig, (self.ax_main, self.ax_info) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.canvas.manager.set_window_title('Interactive Procedural Animation - Use WASD/Arrow Keys')
        self.fig.suptitle('Interactive Procedural Locomotion System', fontsize=16, fontweight='bold')
        
        # Main view
        self.ax_main.set_xlim(-8, 8)
        self.ax_main.set_ylim(-6, 6)
        self.ax_main.set_aspect('equal')
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_title('Character Animation (Use WASD or Arrow Keys to Control)')
        
        # Info panel
        self.ax_info.set_xlim(0, 10)
        self.ax_info.set_ylim(0, 10)
        self.ax_info.axis('off')
        
        # Plot elements
        self.body_line, = self.ax_main.plot([], [], 'b-', linewidth=4, label='Spine')
        self.left_leg_line, = self.ax_main.plot([], [], 'r-', linewidth=3, label='Left Leg')
        self.right_leg_line, = self.ax_main.plot([], [], 'g-', linewidth=3, label='Right Leg')
        self.left_arm_line, = self.ax_main.plot([], [], 'c-', linewidth=2.5, alpha=0.7)
        self.right_arm_line, = self.ax_main.plot([], [], 'm-', linewidth=2.5, alpha=0.7)
        
        self.head_circle = Circle((0, 0), 0.2, color='yellow', ec='black', linewidth=2, zorder=10)
        self.ax_main.add_patch(self.head_circle)
        
        # Direction indicator (nose)
        self.direction_line, = self.ax_main.plot([], [], 'k-', linewidth=2, zorder=11)
        
        # Trail
        self.trail_line, = self.ax_main.plot([], [], 'b--', alpha=0.2, linewidth=1)
        self.trail_x = []
        self.trail_y = []
        
        # Info text
        self.info_text = self.ax_info.text(0.5, 9.5, '', fontsize=10, verticalalignment='top',
                                           family='monospace')
        
        # Controls text
        controls_text = (
            "🎮 CONTROLS:\n\n"
            "W / ↑  - Move Forward\n"
            "S / ↓  - Move Backward\n"
            "A / ←  - Turn Left\n"
            "D / →  - Turn Right\n"
            "SPACE - Stop\n"
            "ESC    - Quit\n\n"
            "───────────────────\n\n"
            "✨ FEATURES:\n\n"
            "• Real-time input response\n"
            "• Procedural walk cycle\n"
            "• Dynamic body leaning\n"
            "• Head oscillation\n"
            "• Smooth interpolation\n"
            "• Physics-based movement"
        )
        self.ax_info.text(0.5, 7.5, controls_text, fontsize=9.5, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        # Footer
        self.ax_info.text(5, 0.3, 'Portfolio Demo\nProcedural Animation System\nAmitoj Gill',
                         fontsize=9, ha='center', style='italic',
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        self.ax_main.legend(loc='upper left', fontsize=10)
        
        # Connect keyboard events
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        
        # Recording state
        self.frame_count = 0
        
    def on_key_press(self, event):
        """Handle key press"""
        if event.key in ['w', 'up']:
            self.character.input_forward = 1.0
        elif event.key in ['s', 'down']:
            self.character.input_forward = -1.0
        elif event.key in ['a', 'left']:
            self.character.input_turn = 1.0
        elif event.key in ['d', 'right']:
            self.character.input_turn = -1.0
        elif event.key == ' ':
            self.character.input_forward = 0.0
            self.character.input_turn = 0.0
            self.character.velocity *= 0.0
        elif event.key == 'escape':
            plt.close(self.fig)
            
    def on_key_release(self, event):
        """Handle key release"""
        if event.key in ['w', 'up', 's', 'down']:
            self.character.input_forward = 0.0
        elif event.key in ['a', 'left', 'd', 'right']:
            self.character.input_turn = 0.0
            
    def update_frame(self, frame):
        """Update animation frame"""
        dt = 1.0 / 30.0  # 30 FPS
        self.character.update(dt)
        self.frame_count += 1
        
        # Get skeleton
        skeleton = self.character.get_skeleton_points()
        
        # Update body
        self.body_line.set_data(
            [skeleton['hip'][0], skeleton['spine_top'][0]],
            [skeleton['hip'][1], skeleton['spine_top'][1]]
        )
        
        # Update head
        self.head_circle.center = skeleton['head']
        
        # Direction indicator (nose)
        head_x, head_y = skeleton['head']
        nose_length = 0.25
        nose_x = head_x + nose_length * math.cos(self.character.rotation)
        nose_y = head_y + nose_length * math.sin(self.character.rotation)
        self.direction_line.set_data([head_x, nose_x], [head_y, nose_y])
        
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
        
        # Update trail (every 3 frames)
        if self.frame_count % 3 == 0:
            self.trail_x.append(skeleton['hip'][0])
            self.trail_y.append(skeleton['hip'][1])
            if len(self.trail_x) > 150:
                self.trail_x.pop(0)
                self.trail_y.pop(0)
        self.trail_line.set_data(self.trail_x, self.trail_y)
        
        # Update info
        info = (
            f"⏱️  Time: {self.character.time:.1f}s\n"
            f"📍 Position: ({self.character.position[0]:.2f}, {self.character.position[1]:.2f})\n"
            f"🏃 Speed: {self.character.ground_speed:.2f} m/s\n"
            f"🧭 Rotation: {math.degrees(self.character.rotation):.1f}°\n"
            f"↗️  Lean: {self.character.lean_angle:.1f}°\n"
            f"⌨️  Input: F={self.character.input_forward:.1f}, T={self.character.input_turn:.1f}\n"
        )
        self.info_text.set_text(info)
        
        return (self.body_line, self.left_leg_line, self.right_leg_line,
                self.left_arm_line, self.right_arm_line, self.head_circle,
                self.direction_line, self.trail_line, self.info_text)
    
    def run(self):
        """Run the interactive animation"""
        anim = animation.FuncAnimation(
            self.fig, self.update_frame,
            interval=33,  # ~30 FPS
            blit=True,
            cache_frame_data=False
        )
        
        plt.tight_layout()
        plt.show()
        
        return anim

def main():
    """Main entry point"""
    print("=" * 70)
    print("🎮 INTERACTIVE PROCEDURAL LOCOMOTION ANIMATION DEMO")
    print("=" * 70)
    print("\n📋 CONTROLS:")
    print("   W/↑ Arrow  - Move Forward")
    print("   S/↓ Arrow  - Move Backward")
    print("   A/← Arrow  - Turn Left")
    print("   D/→ Arrow  - Turn Right")
    print("   SPACE      - Stop")
    print("   ESC        - Quit")
    print("\n✨ FEATURES DEMONSTRATED:")
    print("   • Real-time keyboard input")
    print("   • Procedural walking animation")
    print("   • Dynamic body leaning during turns")
    print("   • Head oscillation (procedural bone rotation)")
    print("   • Smooth velocity/rotation interpolation")
    print("   • Physics-based movement")
    print("\n💡 TIP: Try making figure-8 patterns to showcase the leaning!")
    print("=" * 70)
    print("\n🎬 Starting interactive demo...\n")
    
    renderer = InteractiveRenderer()
    renderer.run()
    
    print("\n✅ Demo closed. Thanks for watching!")

if __name__ == '__main__':
    main()
