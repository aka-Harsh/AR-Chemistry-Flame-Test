"""
State management for AR Chemistry Flame Test Simulator
"""

import time
import numpy as np
from config.chemicals import CHEMICALS, BEAKER_POSITIONS, FLAME_AREA, CHEMICAL_MIXTURES, INTERACTION_RADIUS

class StateManager:
    def __init__(self):
        """Initialize state manager"""
        self.finger_states = {}
        self.recent_interactions = []
        self.educational_messages = []
        self.current_explanation = ""
        self.last_update_time = time.time()
        
        # Initialize finger states for both hands
        self.initialize_finger_states()
        
        print("🧠 State manager initialized")
    
    def initialize_finger_states(self):
        """Initialize finger states for both hands"""
        fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
        hands = ['Left', 'Right']
        
        for hand in hands:
            for finger in fingers:
                finger_id = f"{hand}_{finger}"
                self.finger_states[finger_id] = {
                    'chemical': None,
                    'has_flame': False,
                    'dip_time': 0,
                    'flame_intensity': 0,
                    'last_interaction': 0
                }
    
    def update_finger_states(self, hands_data, screen_width, screen_height):
        """Update finger states based on hand positions"""
        current_time = time.time()
        
        # Check interactions for each detected hand
        for hand_data in hands_data:
            hand_label = hand_data['label']
            finger_positions = hand_data['finger_positions']
            
            for finger_name, finger_pos in finger_positions.items():
                finger_id = f"{hand_label}_{finger_name}"
                
                # Check beaker interactions
                self.check_beaker_interactions(finger_id, finger_pos, screen_width, screen_height)
                
                # Check flame area interactions
                self.check_flame_interactions(finger_id, finger_pos, screen_width, screen_height)
        
        # Check for finger-to-finger interactions (mixing)
        self.check_mixing_interactions(hands_data)
        
        # Update flame intensities
        self.update_flame_intensities()
    
    def check_beaker_interactions(self, finger_id, finger_pos, screen_width, screen_height):
        """Check if finger is interacting with beakers - OPTIMIZED"""
        # Check bottom beakers
        beaker_y = screen_height - 130  # Beakers at bottom
        
        for chemical, x_ratio in BEAKER_POSITIONS.items():
            beaker_x = int(x_ratio * screen_width)
            beaker_center = (beaker_x, beaker_y)
            
            # Check if finger is near beaker
            if self.is_point_in_circle(finger_pos, beaker_center, INTERACTION_RADIUS):
                # Dip in chemical
                self.dip_finger_in_chemical(finger_id, chemical)
                self.add_educational_message(f"🧪 {finger_id} dipped in {CHEMICALS[chemical]['name']} ({chemical})")
        
        # Check water beaker (top-right corner)
        from config.chemicals import WATER_POSITION
        water_x = int(WATER_POSITION['x_ratio'] * screen_width)
        water_y = int(WATER_POSITION['y_ratio'] * screen_height)
        water_center = (water_x, water_y)
        
        if self.is_point_in_circle(finger_pos, water_center, INTERACTION_RADIUS):
            # Reset finger
            self.reset_finger(finger_id)
            self.add_educational_message(f"🚿 {finger_id} cleaned with water")
    
    def check_flame_interactions(self, finger_id, finger_pos, screen_width, screen_height):
        """Check if finger is interacting with flame area"""
        flame_x = int(FLAME_AREA['x'] * screen_width)
        flame_y = int(FLAME_AREA['y'] * screen_height)
        flame_width = int(FLAME_AREA['width'] * screen_width)
        flame_height = int(FLAME_AREA['height'] * screen_height)
        
        # Check if finger is in flame area
        if (flame_x <= finger_pos[0] <= flame_x + flame_width and
            flame_y <= finger_pos[1] <= flame_y + flame_height):
            
            finger_state = self.finger_states[finger_id]
            if finger_state['chemical'] and not finger_state['has_flame']:
                # Ignite chemical
                self.ignite_finger(finger_id)
                chemical = finger_state['chemical']
                self.add_educational_message(f"🔥 {finger_id} ignited with {CHEMICALS[chemical]['name']}!")
                self.set_current_explanation(self.get_chemical_explanation(chemical))
    
    def check_mixing_interactions(self, hands_data):
        """Check for flame mixing and flame transfer between fingers - ENHANCED"""
        flaming_fingers = []
        chemical_fingers = []
        
        # Collect all fingers with flames and chemicals
        for hand_data in hands_data:
            hand_label = hand_data['label']
            finger_positions = hand_data['finger_positions']
            
            for finger_name, finger_pos in finger_positions.items():
                finger_id = f"{hand_label}_{finger_name}"
                finger_state = self.finger_states[finger_id]
                
                if finger_state['has_flame']:
                    flaming_fingers.append((finger_id, finger_pos))
                elif finger_state['chemical']:  # Has chemical but no flame
                    chemical_fingers.append((finger_id, finger_pos))
        
        # Check flame to flame mixing (original functionality)
        for i in range(len(flaming_fingers)):
            for j in range(i + 1, len(flaming_fingers)):
                finger1_id, pos1 = flaming_fingers[i]
                finger2_id, pos2 = flaming_fingers[j]
                
                distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                
                if distance <= 60:  # Close enough to mix
                    self.mix_chemicals(finger1_id, finger2_id)
        
        # NEW: Check flame to chemical transfer (ignite chemical fingers)
        for flaming_finger_id, flame_pos in flaming_fingers:
            for chemical_finger_id, chemical_pos in chemical_fingers:
                distance = np.sqrt((flame_pos[0] - chemical_pos[0])**2 + (flame_pos[1] - chemical_pos[1])**2)
                
                if distance <= 50:  # Close enough to transfer flame
                    # Ignite the chemical finger
                    self.ignite_finger(chemical_finger_id)
                    chemical = self.finger_states[chemical_finger_id]['chemical']
                    self.add_educational_message(f"🔥 {chemical_finger_id} ignited by flame transfer with {CHEMICALS[chemical]['name']}!")
                    self.set_current_explanation(f"Flame Transfer: {chemical_finger_id} was ignited by touching another flame. {self.get_chemical_explanation(chemical)}")
    
    def dip_finger_in_chemical(self, finger_id, chemical):
        """Dip finger in chemical"""
        self.finger_states[finger_id]['chemical'] = chemical
        self.finger_states[finger_id]['dip_time'] = time.time()
        self.finger_states[finger_id]['has_flame'] = False
        
        # Add safety warning
        safety_warning = CHEMICALS[chemical]['safety_warning']
        self.add_educational_message(f"⚠️ Safety: {safety_warning}")
    
    def ignite_finger(self, finger_id):
        """Ignite chemical on finger"""
        self.finger_states[finger_id]['has_flame'] = True
        self.finger_states[finger_id]['flame_intensity'] = 1.0
        self.finger_states[finger_id]['last_interaction'] = time.time()
    
    def reset_finger(self, finger_id):
        """Reset finger state"""
        self.finger_states[finger_id]['chemical'] = None
        self.finger_states[finger_id]['has_flame'] = False
        self.finger_states[finger_id]['flame_intensity'] = 0
        self.finger_states[finger_id]['dip_time'] = 0
    
    def reset_all_fingers(self):
        """Reset all finger states"""
        for finger_id in self.finger_states:
            self.reset_finger(finger_id)
        self.educational_messages.clear()
        self.current_explanation = ""
    
    def mix_chemicals(self, finger1_id, finger2_id):
        """Mix chemicals from two fingers"""
        chemical1 = self.finger_states[finger1_id]['chemical']
        chemical2 = self.finger_states[finger2_id]['chemical']
        
        if chemical1 and chemical2 and chemical1 != chemical2:
            # Create mixture key (sorted for consistency)
            mixture_key = tuple(sorted([chemical1, chemical2]))
            
            if mixture_key in CHEMICAL_MIXTURES:
                mixture_data = CHEMICAL_MIXTURES[mixture_key]
                self.add_educational_message(f"🔬 Mixing {chemical1} + {chemical2}: {mixture_data['description']}")
                self.set_current_explanation(f"Chemical Reaction: {mixture_data['explanation']}\n\nRealistic Note: {mixture_data['realistic_note']}")
            else:
                self.add_educational_message(f"🔬 Mixing {chemical1} + {chemical2}: No significant color change observed")
                self.set_current_explanation("These chemicals don't produce a notable flame color change when mixed.")
    
    def update_flame_intensities(self):
        """Update flame intensities over time"""
        current_time = time.time()
        
        for finger_id, state in self.finger_states.items():
            if state['has_flame']:
                # Flame intensity varies slightly over time for realism
                time_since_ignition = current_time - state['last_interaction']
                base_intensity = max(0.5, 1.0 - time_since_ignition * 0.1)
                variation = 0.1 * np.sin(current_time * 10)  # Flickering effect
                state['flame_intensity'] = min(1.0, base_intensity + variation)
    
    def add_educational_message(self, message):
        """Add educational message with timestamp"""
        timestamp = time.time()
        self.educational_messages.append({
            'message': message,
            'timestamp': timestamp
        })
        
        # Keep only recent messages (last 10)
        if len(self.educational_messages) > 10:
            self.educational_messages = self.educational_messages[-10:]
    
    def set_current_explanation(self, explanation):
        """Set current detailed explanation"""
        self.current_explanation = explanation
    
    def get_chemical_explanation(self, chemical):
        """Get detailed explanation for chemical"""
        if chemical not in CHEMICALS:
            return ""
        
        chem_data = CHEMICALS[chemical]
        explanation = f"""
Chemical: {chem_data['name']} ({chem_data['formula']})

Description: {chem_data['description']}

Wavelength: {chem_data['temperature']} nm

Scientific Background: When {chem_data['name']} atoms are heated in a flame, electrons absorb energy and jump to higher energy levels. When they return to ground state, they emit light at characteristic wavelengths, producing the distinctive {chem_data['name']} flame color.

Safety: {chem_data['safety_warning']}
        """.strip()
        
        return explanation
    
    def get_finger_position(self, finger_id, hands_data):
        """Get current position of specific finger"""
        hand_label, finger_name = finger_id.split('_', 1)
        
        for hand_data in hands_data:
            if hand_data['label'] == hand_label:
                return hand_data['finger_positions'].get(finger_name)
        return None
    
    def is_point_in_circle(self, point, center, radius):
        """Check if point is within circular area"""
        if point is None:
            return False
        
        distance = np.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)
        return distance <= radius
    
    def get_active_chemicals(self):
        """Get list of currently active chemicals"""
        active = set()
        for state in self.finger_states.values():
            if state['chemical']:
                active.add(state['chemical'])
        return list(active)
    
    def get_flaming_fingers(self):
        """Get list of fingers currently on fire"""
        flaming = []
        for finger_id, state in self.finger_states.items():
            if state['has_flame']:
                flaming.append(finger_id)
        return flaming