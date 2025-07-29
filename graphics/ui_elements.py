"""
UI elements and educational interface for AR Chemistry Flame Test Simulator
"""

import cv2
import numpy as np
import time
import textwrap
from config.chemicals import CHEMICALS, INTERACTION_RADIUS

class UIRenderer:
    def __init__(self):
        """Initialize UI renderer - OPTIMIZED FOR NO OVERLAP"""
        self.sidebar_width = 320  # Reduced from 350 for better layout
        self.message_history = []
        self.last_message_time = 0
        print("🖥️ Optimized UI renderer initialized")
    
    def render_sidebar(self, frame, state_manager, screen_width, screen_height):
        """Render educational sidebar"""
        # Create sidebar background
        sidebar_start = screen_width - self.sidebar_width
        sidebar_overlay = np.zeros((screen_height, self.sidebar_width, 3), dtype=np.uint8)
        sidebar_overlay[:] = (30, 30, 30)  # Dark background
        
        # Add transparency
        alpha = 0.85
        frame[:, sidebar_start:] = (
            frame[:, sidebar_start:] * (1 - alpha) + 
            sidebar_overlay * alpha
        ).astype(np.uint8)
        
        # Add border
        cv2.line(frame, (sidebar_start, 0), (sidebar_start, screen_height), (100, 100, 100), 2)
        
        # Render sidebar content
        self.render_sidebar_header(frame, sidebar_start, screen_width)
        self.render_active_chemicals(frame, state_manager, sidebar_start, screen_width)
        self.render_current_explanation(frame, state_manager, sidebar_start, screen_width)
        self.render_recent_messages(frame, state_manager, sidebar_start, screen_width)
        self.render_instructions(frame, sidebar_start, screen_width, screen_height)
    
    def render_sidebar_header(self, frame, sidebar_start, screen_width):
        """Render sidebar header"""
        header_y = 30
        
        # Title
        cv2.putText(frame, "AR CHEMISTRY LAB", (sidebar_start + 10, header_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Subtitle
        cv2.putText(frame, "Flame Test Simulator", (sidebar_start + 10, header_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Separator line
        cv2.line(frame, (sidebar_start + 10, header_y + 35), 
                (screen_width - 10, header_y + 35), (100, 100, 100), 1)
    
    def render_active_chemicals(self, frame, state_manager, sidebar_start, screen_width):
        """Render currently active chemicals"""
        start_y = 80
        y_offset = start_y
        
        # Section title
        cv2.putText(frame, "ACTIVE CHEMICALS", (sidebar_start + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)
        y_offset += 25
        
        # List active chemicals on fingers
        active_found = False
        for finger_id, state in state_manager.finger_states.items():
            if state['chemical']:
                active_found = True
                chemical = state['chemical']
                chemical_data = CHEMICALS[chemical]
                
                # Finger name
                finger_display = finger_id.replace('_', ' ').title()
                status = "🔥" if state['has_flame'] else "💧"
                
                text = f"{status} {finger_display}: {chemical}"
                cv2.putText(frame, text, (sidebar_start + 15, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                y_offset += 18
                
                # Chemical formula
                cv2.putText(frame, f"   {chemical_data['formula']}", 
                           (sidebar_start + 15, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
                y_offset += 20
        
        if not active_found:
            cv2.putText(frame, "No chemicals active", (sidebar_start + 15, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
            y_offset += 20
        
        # Separator
        y_offset += 10
        cv2.line(frame, (sidebar_start + 10, y_offset), 
                (screen_width - 10, y_offset), (100, 100, 100), 1)
        
        return y_offset + 15
    
    def render_current_explanation(self, frame, state_manager, sidebar_start, screen_width):
        """Render current detailed explanation"""
        start_y = self.render_active_chemicals(frame, state_manager, sidebar_start, screen_width)
        y_offset = start_y
        
        # Section title
        cv2.putText(frame, "EXPLANATION", (sidebar_start + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 150, 255), 2)
        y_offset += 25
        
        # Current explanation
        explanation = state_manager.current_explanation
        if explanation:
            # Wrap text to fit sidebar
            wrapped_lines = self.wrap_text(explanation, 40)
            
            for line in wrapped_lines[:8]:  # Limit lines
                cv2.putText(frame, line, (sidebar_start + 15, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)
                y_offset += 15
        else:
            cv2.putText(frame, "Dip finger in chemical", (sidebar_start + 15, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
            y_offset += 15
            cv2.putText(frame, "then touch flame area", (sidebar_start + 15, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
            y_offset += 15
        
        # Separator
        y_offset += 10
        cv2.line(frame, (sidebar_start + 10, y_offset), 
                (screen_width - 10, y_offset), (100, 100, 100), 1)
        
        return y_offset + 15
    
    def render_recent_messages(self, frame, state_manager, sidebar_start, screen_width):
        """Render recent activity messages"""
        start_y = self.render_current_explanation(frame, state_manager, sidebar_start, screen_width)
        y_offset = start_y
        
        # Section title
        cv2.putText(frame, "RECENT ACTIVITY", (sidebar_start + 10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 100), 2)
        y_offset += 25
        
        # Recent messages
        messages = state_manager.educational_messages[-5:]  # Last 5 messages
        
        for message_data in reversed(messages):
            message = message_data['message']
            timestamp = message_data['timestamp']
            
            # Time since message
            time_diff = time.time() - timestamp
            if time_diff < 60:
                time_str = f"{int(time_diff)}s"
            else:
                time_str = f"{int(time_diff/60)}m"
            
            # Message color based on age
            age_factor = min(1.0, time_diff / 30)  # Fade over 30 seconds
            color_intensity = int(255 * (1 - age_factor * 0.5))
            message_color = (color_intensity, color_intensity, color_intensity)
            
            # Wrap message
            wrapped_lines = self.wrap_text(message, 35)
            
            for line in wrapped_lines[:2]:  # Limit to 2 lines per message
                cv2.putText(frame, line, (sidebar_start + 15, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, message_color, 1)
                y_offset += 12
            
            y_offset += 5  # Space between messages
        
        return y_offset
    
    def render_instructions(self, frame, sidebar_start, screen_width, screen_height):
        """Render control instructions at bottom"""
        y_start = screen_height - 120
        
        # Instructions title
        cv2.putText(frame, "CONTROLS", (sidebar_start + 10, y_start), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 100), 2)
        
        instructions = [
            "• Hover over beakers to dip",
            "• Touch flame area to ignite",
            "• Touch water to clean",
            "• Bring flames together to mix",
            "• Press 'r' to reset",
            "• Press 'q' to quit"
        ]
        
        y_offset = y_start + 20
        for instruction in instructions:
            cv2.putText(frame, instruction, (sidebar_start + 15, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, (200, 200, 200), 1)
            y_offset += 15
    
    def render_finger_labels(self, frame, state_manager, hands_data):
        """Render chemical labels on fingers"""
        for hand_data in hands_data:
            hand_label = hand_data['label']
            finger_positions = hand_data['finger_positions']
            
            for finger_name, finger_pos in finger_positions.items():
                finger_id = f"{hand_label}_{finger_name}"
                finger_state = state_manager.finger_states[finger_id]
                
                if finger_state['chemical']:
                    # Draw chemical label near finger
                    label = finger_state['chemical']
                    label_pos = (finger_pos[0] + 20, finger_pos[1] - 20)
                    
                    # Background for label
                    cv2.rectangle(frame, (label_pos[0] - 5, label_pos[1] - 15), 
                                 (label_pos[0] + len(label) * 8, label_pos[1] + 5), 
                                 (0, 0, 0), -1)
                    
                    # Label text
                    cv2.putText(frame, label, label_pos, 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    # Flame indicator
                    if finger_state['has_flame']:
                        cv2.putText(frame, "🔥", (label_pos[0] + len(label) * 8 + 5, label_pos[1]), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 150, 255), 1)
    
    def render_interactions(self, frame, state_manager, hands_data):
        """Render interaction feedback - NO OVERLAP WITH SIDEBAR"""
        from config.chemicals import BEAKER_POSITIONS, WATER_POSITION
        
        h, w = frame.shape[:2]
        
        for hand_data in hands_data:
            finger_positions = hand_data['finger_positions']
            
            for finger_pos in finger_positions.values():
                # Check proximity to bottom beakers
                for chemical, x_ratio in BEAKER_POSITIONS.items():
                    beaker_x = int(x_ratio * w)
                    beaker_y = h - 140  # Updated position
                    beaker_center = (beaker_x, beaker_y)
                    
                    distance = np.sqrt((finger_pos[0] - beaker_center[0])**2 + 
                                     (finger_pos[1] - beaker_center[1])**2)
                    
                    if distance <= INTERACTION_RADIUS:
                        # Draw interaction circle
                        cv2.circle(frame, beaker_center, INTERACTION_RADIUS, (0, 255, 0), 2)
                        # Draw connection line
                        cv2.line(frame, finger_pos, beaker_center, (0, 255, 0), 1)
                
                # Check proximity to water beaker (top-center)
                water_x = int(WATER_POSITION['x_ratio'] * w)
                water_y = int(WATER_POSITION['y_ratio'] * h)
                water_center = (water_x, water_y)
                
                distance = np.sqrt((finger_pos[0] - water_center[0])**2 + 
                                 (finger_pos[1] - water_center[1])**2)
                
                if distance <= INTERACTION_RADIUS:
                    # Draw interaction circle
                    cv2.circle(frame, water_center, INTERACTION_RADIUS, (100, 255, 255), 2)
                    # Draw connection line  
                    cv2.line(frame, finger_pos, water_center, (100, 255, 255), 1)
    
    def wrap_text(self, text, width):
        """Wrap text to specified width"""
        return textwrap.wrap(text, width=width)
    
    def render_safety_warning(self, frame, chemical):
        """Render safety warning popup"""
        if chemical not in CHEMICALS:
            return
        
        warning = CHEMICALS[chemical]['safety_warning']
        h, w = frame.shape[:2]
        
        # Warning box dimensions
        box_width = min(400, w - 100)
        box_height = 100
        box_x = (w - box_width) // 2
        box_y = (h - box_height) // 2
        
        # Draw warning box
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), 
                     (0, 0, 200), -1)
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), 
                     (255, 255, 255), 2)
        
        # Warning title
        cv2.putText(frame, "⚠️ SAFETY WARNING", (box_x + 10, box_y + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Warning text
        wrapped_warning = self.wrap_text(warning, 50)
        y_offset = box_y + 50
        
        for line in wrapped_warning[:3]:  # Max 3 lines
            cv2.putText(frame, line, (box_x + 10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            y_offset += 15