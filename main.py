#!/usr/bin/env python3
"""
AR Chemistry Flame Test Simulator
Main application entry point
"""

import cv2
import numpy as np
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.camera import CameraManager
from core.hand_tracker import HandTracker
from core.state_manager import StateManager
from graphics.flame_renderer import FlameRenderer
from graphics.beaker_renderer import BeakerRenderer
from graphics.particle_system import ParticleSystem
from graphics.ui_elements import UIRenderer
from config.chemicals import CHEMICALS

class FlameTestSimulator:
    def __init__(self):
        """Initialize the AR Chemistry Flame Test Simulator"""
        print("🔥 Initializing AR Chemistry Flame Test Simulator...")
        
        # Initialize core components
        self.camera = CameraManager()
        self.hand_tracker = HandTracker()
        self.state_manager = StateManager()
        
        # Initialize graphics components
        self.flame_renderer = FlameRenderer()
        self.beaker_renderer = BeakerRenderer()
        self.particle_system = ParticleSystem()
        self.ui_renderer = UIRenderer()
        
        # Application state
        self.running = True
        self.frame_count = 0
        self.fps_counter = 0
        self.last_fps_time = time.time()
        
        print("✅ Initialization complete! Starting simulation...")
    
    def process_frame(self, frame):
        """Process a single frame - OPTIMIZED FOR 120+ FPS"""
        self.frame_count += 1
        h, w = frame.shape[:2]
        
        # Create working copy
        output_frame = frame.copy()
        
        # Detect hands with optimized settings
        hands = self.hand_tracker.detect_hands(frame)
        
        # Update state based on hand positions
        self.state_manager.update_finger_states(hands, w, h)
        
        # Render beakers (optimized layout)
        self.beaker_renderer.render(output_frame, w, h)
        
        # Render BIG flames on fingers
        for finger_id, finger_state in self.state_manager.finger_states.items():
            if finger_state['has_flame']:
                # Get finger position
                finger_pos = self.state_manager.get_finger_position(finger_id, hands)
                if finger_pos:
                    # Render BIGGER flame
                    self.flame_renderer.render_flame(
                        output_frame, 
                        finger_pos, 
                        finger_state['chemical'],
                        self.frame_count
                    )
                    
                    # Add particles for bigger flames
                    self.particle_system.add_flame_particles(
                        finger_pos, 
                        finger_state['chemical']
                    )
        
        # Update and render particle system (optimized)
        self.particle_system.update()
        self.particle_system.render(output_frame)
        
        # Render UI elements (no overlap)
        self.ui_renderer.render_sidebar(output_frame, self.state_manager, w, h)
        self.ui_renderer.render_finger_labels(output_frame, self.state_manager, hands)
        self.ui_renderer.render_interactions(output_frame, self.state_manager, hands)
        
        # Render FPS
        self.render_fps(output_frame)
        
        return output_frame
    
    def render_fps(self, frame):
        """Render FPS counter"""
        current_time = time.time()
        if current_time - self.last_fps_time >= 1.0:
            self.fps_counter = self.frame_count
            self.frame_count = 0
            self.last_fps_time = current_time
        
        cv2.putText(frame, f"FPS: {self.fps_counter}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    def handle_key_events(self, key):
        """Handle keyboard input"""
        if key == ord('q') or key == 27:  # 'q' or ESC
            self.running = False
        elif key == ord('r'):  # Reset
            self.state_manager.reset_all_fingers()
            print("🔄 All fingers reset!")
        elif key == ord('h'):  # Help
            self.show_help()
    
    def show_help(self):
        """Show help information"""
        help_text = """
        🔥 AR Chemistry Flame Test Simulator - HIGH FPS Controls:
        
        • Hover finger over beakers to dip in chemicals
        • Touch flame area to ignite chemical on finger
        • Touch H2O beaker (top-center) to reset finger state
        • Bring two flames together to mix chemicals
        • Touch flame with chemical finger to transfer flame ⭐NEW⭐
        • Press 'q' to quit
        • Press 'r' to reset all fingers
        • Press 'h' to show this help
        
        🧪 Available Chemicals: Na, K, Li, Cu, Ca (Ba removed)
        💧 Water beaker moved to top-center
        🔥 Flames are now BIGGER and more impressive!
        """
        print(help_text)
    
    def run(self):
        """Main application loop - OPTIMIZED FOR 120+ FPS"""
        print("🚀 Starting HIGH-PERFORMANCE AR Chemistry Flame Test Simulator!")
        print("🎯 Target FPS: 120+")
        print("📚 Educational mode: ON")
        print("🔬 Available chemicals:", ', '.join(CHEMICALS.keys()))
        
        self.show_help()
        
        try:
            while self.running:
                # Capture frame
                frame = self.camera.get_frame()
                if frame is None:
                    print("❌ Failed to capture frame")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Display frame
                cv2.imshow('AR Chemistry Flame Test Simulator - HIGH FPS', processed_frame)
                
                # Minimal wait for maximum FPS (1ms)
                key = cv2.waitKey(1) & 0xFF
                if key != 255:  # Key pressed
                    self.handle_key_events(key)
                
        except KeyboardInterrupt:
            print("\n🛑 Simulation interrupted by user")
        except Exception as e:
            print(f"❌ Error during simulation: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("🧹 Cleaning up resources...")
        self.camera.release()
        cv2.destroyAllWindows()
        print("✅ Cleanup complete. Thank you for using AR Chemistry Simulator!")

def main():
    """Main entry point"""
    print("=" * 60)
    print("🔥 AR CHEMISTRY FLAME TEST SIMULATOR")
    print("🎓 Educational Chemistry Lab Experience")
    print("=" * 60)
    
    try:
        # Create and run simulator
        simulator = FlameTestSimulator()
        simulator.run()
    except Exception as e:
        print(f"❌ Failed to start simulator: {e}")
        print("💡 Make sure your webcam is connected and accessible")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())