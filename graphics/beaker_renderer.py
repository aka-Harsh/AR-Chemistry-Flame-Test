"""
Beaker and chemical container rendering for AR Chemistry Flame Test Simulator
"""

import cv2
import numpy as np
import math
from config.chemicals import CHEMICALS, BEAKER_POSITIONS, BEAKER_SIZE

class BeakerRenderer:
    def __init__(self):
        """Initialize beaker renderer"""
        self.animation_frame = 0
        print("🧪 Beaker renderer initialized")
    
    def render(self, frame, screen_width, screen_height):
        """Render all beakers and chemicals - OPTIMIZED LAYOUT"""
        self.animation_frame += 1
        
        # Render ignition area first
        self.render_ignition_area(frame, screen_width, screen_height)
        
        # Render chemical beakers (bottom row, no overlap with sidebar)
        for chemical, x_ratio in BEAKER_POSITIONS.items():
            x = int(x_ratio * screen_width)
            y = screen_height - 140  # Moved down slightly
            self.render_chemical_beaker(frame, x, y, chemical)
        
        # Render water beaker (top-center)
        self.render_water_beaker_top_center(frame, screen_width, screen_height)
    
    def render_chemical_beaker(self, frame, x, y, chemical):
        """Render individual chemical beaker"""
        if chemical not in CHEMICALS:
            return
        
        chemical_data = CHEMICALS[chemical]
        chemical_color = chemical_data['color']
        
        # Draw beaker glass
        self.draw_beaker_glass(frame, x, y)
        
        # Draw chemical liquid
        self.draw_chemical_liquid(frame, x, y, chemical_color, chemical)
        
        # Draw beaker label
        self.draw_beaker_label(frame, x, y, chemical, chemical_data)
        
        # Add interaction highlight
        self.add_interaction_glow(frame, x, y, chemical_color)
    
    def render_water_beaker_top_center(self, frame, screen_width, screen_height):
        """Render water beaker in top-center position"""
        from config.chemicals import WATER_POSITION
        
        x = int(WATER_POSITION['x_ratio'] * screen_width)
        y = int(WATER_POSITION['y_ratio'] * screen_height)
        
        # Draw beaker glass (medium size for top center)
        size = int(BEAKER_SIZE * 0.7)  # 70% size for top placement
        self.draw_beaker_glass_small(frame, x, y, size)
        
        # Draw water with ripple effect
        self.draw_water_with_ripples_small(frame, x, y, size)
        
        # Draw centered label
        cv2.putText(frame, "H2O", (x - 20, y + size + 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "CLEAN", (x - 25, y + size + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 255), 2)
    
    def draw_beaker_glass_small(self, frame, x, y, size):
        """Draw smaller glass beaker for top-right"""
        # Beaker outline (dark gray)
        cv2.ellipse(frame, (x, y + size - 8), (size//2, 6), 0, 0, 360, (80, 80, 80), 2)
        cv2.rectangle(frame, (x - size//2, y), (x + size//2, y + size - 8), (80, 80, 80), 2)
        cv2.ellipse(frame, (x, y), (size//2, 6), 0, 0, 360, (80, 80, 80), 2)
        
        # Glass reflection effect
        cv2.ellipse(frame, (x - size//4, y + size//4), (size//8, size//4), 45, 0, 180, (200, 200, 200), 1)
    
    def draw_water_with_ripples_small(self, frame, x, y, size):
        """Draw water with animated ripples - smaller version"""
        liquid_height = size - 15
        
        # Base water color
        water_color = (255, 200, 150)  # Light blue
        
        # Draw base water
        liquid_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.ellipse(liquid_mask, (x, y + liquid_height - 4), (size//2 - 4, 4), 0, 0, 360, 255, -1)
        cv2.rectangle(liquid_mask, (x - size//2 + 4, y + 12), (x + size//2 - 4, y + liquid_height - 4), 255, -1)
        
        frame[liquid_mask > 0] = water_color
        
        # Add smaller animated ripples
        ripple_phase = self.animation_frame * 0.1
        ripple_radius = int(8 + 10 * math.sin(ripple_phase))
        ripple_alpha = max(0, math.sin(ripple_phase))
        
        if ripple_alpha > 0:
            cv2.circle(frame, (x, y + liquid_height - 8), ripple_radius, 
                      (255, 255, 255), max(1, int(2 * ripple_alpha)))
    
    def draw_beaker_glass(self, frame, x, y):
        """Draw realistic glass beaker"""
        size = BEAKER_SIZE
        
        # Beaker outline (dark gray)
        cv2.ellipse(frame, (x, y + size - 10), (size//2, 8), 0, 0, 360, (80, 80, 80), 2)
        cv2.rectangle(frame, (x - size//2, y), (x + size//2, y + size - 10), (80, 80, 80), 2)
        cv2.ellipse(frame, (x, y), (size//2, 8), 0, 0, 360, (80, 80, 80), 2)
        
        # Glass reflection effect
        cv2.ellipse(frame, (x - size//4, y + size//4), (size//8, size//4), 45, 0, 180, (200, 200, 200), 2)
        
        # Beaker spout
        cv2.ellipse(frame, (x + size//2 - 5, y + size//4), (8, 4), 0, 0, 180, (80, 80, 80), 2)
    
    def draw_chemical_liquid(self, frame, x, y, color, chemical):
        """Draw chemical liquid inside beaker"""
        size = BEAKER_SIZE
        liquid_height = size - 20
        
        # Create liquid mask
        liquid_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        # Draw liquid shape (slightly smaller than beaker)
        cv2.ellipse(liquid_mask, (x, y + liquid_height - 5), (size//2 - 5, 6), 0, 0, 360, 255, -1)
        cv2.rectangle(liquid_mask, (x - size//2 + 5, y + 15), (x + size//2 - 5, y + liquid_height - 5), 255, -1)
        
        # Add slight animation to liquid surface
        wave_offset = math.sin(self.animation_frame * 0.1) * 2
        cv2.ellipse(liquid_mask, (x, y + 15 + int(wave_offset)), (size//2 - 5, 6), 0, 0, 360, 255, -1)
        
        # Apply liquid color
        liquid_color = self.adjust_liquid_color(color)
        frame[liquid_mask > 0] = liquid_color
        
        # Add surface highlights
        cv2.ellipse(frame, (x, y + 15 + int(wave_offset)), (size//2 - 5, 6), 0, 0, 360, (255, 255, 255), 1)
    
    def draw_water_with_ripples(self, frame, x, y):
        """Draw water with animated ripples"""
        size = BEAKER_SIZE
        liquid_height = size - 20
        
        # Base water color
        water_color = (255, 200, 150)  # Light blue
        
        # Draw base water
        liquid_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.ellipse(liquid_mask, (x, y + liquid_height - 5), (size//2 - 5, 6), 0, 0, 360, 255, -1)
        cv2.rectangle(liquid_mask, (x - size//2 + 5, y + 15), (x + size//2 - 5, y + liquid_height - 5), 255, -1)
        
        frame[liquid_mask > 0] = water_color
        
        # Add animated ripples
        for i in range(3):
            ripple_phase = (self.animation_frame + i * 20) * 0.1
            ripple_radius = int(10 + 15 * math.sin(ripple_phase))
            ripple_alpha = max(0, math.sin(ripple_phase))
            
            if ripple_alpha > 0:
                cv2.circle(frame, (x, y + liquid_height - 10), ripple_radius, 
                          (255, 255, 255), max(1, int(3 * ripple_alpha)))
    
    def draw_beaker_label(self, frame, x, y, chemical, chemical_data):
        """Draw chemical label and formula"""
        size = BEAKER_SIZE
        
        # Chemical symbol (large)
        cv2.putText(frame, chemical, (x - 15, y + size + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Chemical name
        cv2.putText(frame, chemical_data['name'], (x - len(chemical_data['name']) * 4, y + size + 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Chemical formula
        cv2.putText(frame, chemical_data['formula'], (x - len(chemical_data['formula']) * 4, y + size + 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
    
    def add_interaction_glow(self, frame, x, y, color):
        """Add subtle glow effect for interaction feedback"""
        glow_intensity = 0.3 + 0.2 * math.sin(self.animation_frame * 0.1)
        
        # Create glow overlay
        glow_overlay = np.zeros(frame.shape, dtype=np.float32)
        cv2.circle(glow_overlay, (x, y + BEAKER_SIZE//2), BEAKER_SIZE, color, -1)
        
        # Apply Gaussian blur
        glow_overlay = cv2.GaussianBlur(glow_overlay, (31, 31), 10)
        
        # Blend with frame
        alpha = 0.1 * glow_intensity
        frame[:] = (frame * (1 - alpha) + glow_overlay * alpha).astype(np.uint8)
    
    def adjust_liquid_color(self, base_color):
        """Adjust color for liquid appearance"""
        # Make liquid slightly darker and more saturated
        b, g, r = base_color
        factor = 0.8
        return (int(b * factor), int(g * factor), int(r * factor))
    
    def render_ignition_area(self, frame, screen_width, screen_height):
        """Render the flame ignition area"""
        from config.chemicals import FLAME_AREA
        
        x = int(FLAME_AREA['x'] * screen_width)
        y = int(FLAME_AREA['y'] * screen_height)
        width = int(FLAME_AREA['width'] * screen_width)
        height = int(FLAME_AREA['height'] * screen_height)
        
        # Animated border
        border_intensity = 0.5 + 0.3 * math.sin(self.animation_frame * 0.2)
        border_color = (0, int(100 * border_intensity), int(255 * border_intensity))
        
        cv2.rectangle(frame, (x, y), (x + width, y + height), border_color, 3)
        
        # Add gradient background
        gradient_overlay = np.zeros(frame.shape, dtype=np.float32)
        cv2.rectangle(gradient_overlay, (x, y), (x + width, y + height), (50, 25, 0), -1)
        cv2.GaussianBlur(gradient_overlay, (21, 21), 5, gradient_overlay)
        
        alpha = 0.2 * border_intensity
        frame[y:y+height, x:x+width] = (
            frame[y:y+height, x:x+width] * (1 - alpha) + 
            gradient_overlay[y:y+height, x:x+width] * alpha
        ).astype(np.uint8)
        
        # Add label with glow
        cv2.putText(frame, "IGNITION", (x + 5, y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 3)
        cv2.putText(frame, "IGNITION", (x + 5, y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, border_color, 2)
        
        # Draw animated Bunsen burner
        self.draw_animated_bunsen_burner(frame, x + width // 2, y + height // 2 + 10)
    
    def draw_animated_bunsen_burner(self, frame, x, y):
        """Draw animated Bunsen burner icon"""
        # Burner base
        cv2.rectangle(frame, (x - 15, y + 10), (x + 15, y + 25), (100, 100, 100), -1)
        cv2.rectangle(frame, (x - 12, y + 12), (x + 12, y + 23), (150, 150, 150), -1)
        
        # Burner tube
        cv2.rectangle(frame, (x - 6, y - 15), (x + 6, y + 10), (120, 120, 120), -1)
        cv2.rectangle(frame, (x - 4, y - 13), (x + 4, y + 8), (180, 180, 180), -1)
        
        # Animated pilot flame
        flame_height = 8 + 3 * math.sin(self.animation_frame * 0.3)
        flame_color = (0, int(100 + 50 * math.sin(self.animation_frame * 0.4)), 255)
        
        flame_points = [
            (x, int(y - 15 - flame_height)),
            (x - 4, y - 15),
            (x + 4, y - 15)
        ]
        cv2.fillPoly(frame, [np.array(flame_points)], flame_color)
        
        # Control knobs
        cv2.circle(frame, (x - 10, y + 5), 3, (80, 80, 80), -1)
        cv2.circle(frame, (x + 10, y + 5), 3, (80, 80, 80), -1)