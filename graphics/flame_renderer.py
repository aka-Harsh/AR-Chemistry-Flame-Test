"""
Procedural flame rendering for AR Chemistry Flame Test Simulator
"""

import cv2
import numpy as np
import math
from config.chemicals import CHEMICALS

class FlameRenderer:
    def __init__(self):
        """Initialize flame renderer"""
        self.flame_cache = {}
        self.time_offset = 0
        print("🔥 Flame renderer initialized")
    
    def render_flame(self, frame, position, chemical, frame_count):
        """Render BIG procedural flame at position - OPTIMIZED FOR HIGH FPS"""
        if chemical not in CHEMICALS:
            return
        
        chemical_data = CHEMICALS[chemical]
        color = chemical_data['color']
        intensity = chemical_data['intensity']
        
        # Create BIGGER flame shape using optimized noise
        flame_points = self.generate_flame_shape(position, frame_count, intensity)
        
        # Render flame with gradient and effects
        self.draw_flame_gradient(frame, flame_points, color, intensity, frame_count)
        
        # Add stronger glow effect for bigger flames
        self.add_glow_effect(frame, position, color, intensity)
        
        # Add larger flame core
        self.draw_flame_core(frame, position, color, intensity)
    
    def simple_noise(self, x, y, scale=1.0):
        """OPTIMIZED simple noise function for high FPS"""
        x *= scale
        y *= scale
        # Faster math operations
        return (math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1.0 - 0.5
    
    def generate_flame_shape(self, position, frame_count, intensity):
        """Generate BIGGER flame shape - PERFORMANCE OPTIMIZED"""
        x, y = position
        flame_points = []
        
        # BIGGER flame parameters
        flame_height = int(100 * intensity)  # Increased from 60
        flame_width = int(50 * intensity)    # Increased from 30
        noise_scale = 0.08  # Optimized scale
        time_factor = frame_count * 0.08  # Slightly slower for stability
        
        # Reduced points for better performance but still good quality
        for i in range(16):  # Reduced from 20 to 16 for performance
            angle = (i / 16.0) * 2 * math.pi
            
            # Base radius varies with height
            height_factor = i / 16.0
            base_radius = flame_width * (1 - height_factor * 0.6)
            
            # Add optimized noise for organic flame movement
            noise_x = self.simple_noise(angle * 3, time_factor) * 15 * intensity  # Increased noise
            noise_y = self.simple_noise(angle * 3 + 100, time_factor) * 8 * intensity
            
            # Calculate point position
            radius = base_radius + noise_x
            point_x = x + radius * math.cos(angle)
            point_y = y - (height_factor * flame_height) + noise_y
            
            flame_points.append((int(point_x), int(point_y)))
        
        return flame_points
    
    def draw_flame_gradient(self, frame, flame_points, color, intensity, frame_count):
        """Draw flame with color gradient"""
        if len(flame_points) < 3:
            return
        
        # Create flame mask
        h, w = frame.shape[:2]
        flame_mask = np.zeros((h, w), dtype=np.uint8)
        
        # Fill flame shape
        points_array = np.array(flame_points, dtype=np.int32)
        cv2.fillPoly(flame_mask, [points_array], 255)
        
        # Create gradient effect
        self.apply_flame_gradient(frame, flame_mask, color, intensity, frame_count)
    
    def apply_flame_gradient(self, frame, mask, color, intensity, frame_count):
        """Apply gradient coloring to flame"""
        h, w = frame.shape[:2]
        
        # Find flame bounds
        y_coords, x_coords = np.where(mask > 0)
        if len(y_coords) == 0:
            return
        
        min_y, max_y = np.min(y_coords), np.max(y_coords)
        
        # Create gradient from bottom (hot) to top (cool)
        for y in range(min_y, max_y + 1):
            # Calculate gradient factor (0 = top, 1 = bottom)
            gradient_factor = (max_y - y) / max(1, max_y - min_y)
            
            # Color intensity based on gradient
            flame_intensity = intensity * (0.3 + 0.7 * gradient_factor)
            
            # Add flickering effect
            flicker = 0.8 + 0.2 * math.sin(frame_count * 0.3 + y * 0.1)
            flame_intensity *= flicker
            
            # Calculate flame color
            flame_color = self.calculate_flame_color(color, flame_intensity, gradient_factor)
            
            # Apply color to row
            row_mask = (mask[y, :] > 0)
            if np.any(row_mask):
                # Blend with original frame
                alpha = 0.7 * flame_intensity
                frame[y, row_mask] = (
                    frame[y, row_mask] * (1 - alpha) + 
                    np.array(flame_color) * alpha
                ).astype(np.uint8)
    
    def calculate_flame_color(self, base_color, intensity, gradient_factor):
        """Calculate flame color with temperature gradient"""
        # Base chemical color
        b, g, r = base_color
        
        # Add temperature gradient (hotter = more white/yellow)
        if gradient_factor > 0.7:  # Bottom of flame (hottest)
            # Add white/yellow for heat
            heat_factor = (gradient_factor - 0.7) / 0.3
            r = min(255, r + heat_factor * (255 - r) * 0.8)
            g = min(255, g + heat_factor * (255 - g) * 0.6)
            b = min(255, b + heat_factor * 50)
        
        # Apply intensity
        r = int(r * intensity)
        g = int(g * intensity)
        b = int(b * intensity)
        
        return (b, g, r)
    
    def add_glow_effect(self, frame, position, color, intensity):
        """Add BIGGER glow effect around flame - OPTIMIZED"""
        x, y = position
        glow_radius = int(60 * intensity)  # Increased from 40
        
        # Create glow overlay
        h, w = frame.shape[:2]
        glow_overlay = np.zeros((h, w, 3), dtype=np.float32)
        
        # Draw glow circle
        cv2.circle(glow_overlay, (x, y), glow_radius, color, -1)
        
        # Apply Gaussian blur for soft glow - optimized kernel size
        glow_overlay = cv2.GaussianBlur(glow_overlay, (31, 31), 12)  # Smaller kernel for performance
        
        # Blend with frame
        alpha = 0.4 * intensity  # Increased alpha for more visible glow
        frame[:] = (frame * (1 - alpha) + glow_overlay * alpha).astype(np.uint8)
    
    def draw_flame_core(self, frame, position, color, intensity):
        """Draw BIGGER bright flame core"""
        x, y = position
        core_radius = int(15 * intensity)  # Increased from 8
        
        # Core color (brighter version of chemical color)
        core_color = tuple(min(255, int(c * 1.5)) for c in color)
        
        # Draw core with soft edges
        cv2.circle(frame, (x, y), core_radius, core_color, -1)
        cv2.circle(frame, (x, y), core_radius // 2, (255, 255, 255), -1)
    
    def render_ignition_area(self, frame, screen_width, screen_height):
        """Render the flame ignition area"""
        from config.chemicals import FLAME_AREA
        
        x = int(FLAME_AREA['x'] * screen_width)
        y = int(FLAME_AREA['y'] * screen_height)
        width = int(FLAME_AREA['width'] * screen_width)
        height = int(FLAME_AREA['height'] * screen_height)
        
        # Draw ignition area border
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 100, 255), 2)
        
        # Add label
        cv2.putText(frame, "IGNITION", (x + 5, y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 255), 2)
        
        # Draw flame icon
        self.draw_bunsen_burner(frame, x + width // 2, y + height // 2)
    
    def draw_bunsen_burner(self, frame, x, y):
        """Draw simple Bunsen burner icon"""
        # Burner base
        cv2.rectangle(frame, (x - 15, y + 10), (x + 15, y + 30), (100, 100, 100), -1)
        
        # Burner tube
        cv2.rectangle(frame, (x - 5, y - 20), (x + 5, y + 10), (150, 150, 150), -1)
        
        # Small flame
        flame_points = [
            (x, y - 20),
            (x - 8, y - 5),
            (x + 8, y - 5)
        ]
        cv2.fillPoly(frame, [np.array(flame_points)], (0, 150, 255))