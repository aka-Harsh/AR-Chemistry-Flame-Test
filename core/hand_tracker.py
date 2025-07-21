"""
Hand tracking using MediaPipe for AR Chemistry Flame Test Simulator
"""

import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, max_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """Initialize hand tracker"""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Finger tip landmark IDs
        self.finger_tips = {
            'thumb': 4,
            'index': 8,
            'middle': 12,
            'ring': 16,
            'pinky': 20
        }
        
        print("✋ Hand tracker initialized")
    
    def detect_hands(self, frame):
        """Detect hands in frame and return finger positions"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.hands.process(rgb_frame)
        
        hands_data = []
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Get hand information
                hand_info = results.multi_handedness[hand_idx]
                hand_label = hand_info.classification[0].label  # 'Left' or 'Right'
                
                # Extract finger tip positions
                finger_positions = {}
                h, w = frame.shape[:2]
                
                for finger_name, landmark_id in self.finger_tips.items():
                    landmark = hand_landmarks.landmark[landmark_id]
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    finger_positions[finger_name] = (x, y)
                
                hands_data.append({
                    'label': hand_label,
                    'landmarks': hand_landmarks,
                    'finger_positions': finger_positions
                })
        
        return hands_data
    
    def draw_landmarks(self, frame, hands_data):
        """Draw hand landmarks on frame"""
        for hand_data in hands_data:
            landmarks = hand_data['landmarks']
            
            # Draw hand landmarks
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
    
    def get_finger_position(self, finger_name, hand_label, hands_data):
        """Get position of specific finger"""
        for hand_data in hands_data:
            if hand_data['label'] == hand_label:
                return hand_data['finger_positions'].get(finger_name)
        return None
    
    def is_finger_in_area(self, finger_pos, area_center, radius):
        """Check if finger is within circular area"""
        if finger_pos is None:
            return False
        
        distance = np.sqrt(
            (finger_pos[0] - area_center[0])**2 + 
            (finger_pos[1] - area_center[1])**2
        )
        
        return distance <= radius
    
    def get_distance_between_fingers(self, finger1_pos, finger2_pos):
        """Get distance between two finger positions"""
        if finger1_pos is None or finger2_pos is None:
            return float('inf')
        
        return np.sqrt(
            (finger1_pos[0] - finger2_pos[0])**2 + 
            (finger1_pos[1] - finger2_pos[1])**2
        )
    
    def cleanup(self):
        """Clean up resources"""
        if self.hands:
            self.hands.close()