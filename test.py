#!/usr/bin/env python3
"""
Minimal test to isolate the tuple concatenation issue
"""

import cv2
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.camera import CameraManager
from core.hand_tracker import HandTracker

def main():
    """Minimal test"""
    print("🔍 Testing minimal functionality...")
    
    try:
        # Initialize camera
        camera = CameraManager()
        hand_tracker = HandTracker()
        
        print("✅ Basic components initialized")
        
        frame_count = 0
        while True:
            # Get frame
            frame = camera.get_frame()
            if frame is None:
                break
            
            frame_count += 1
            
            # Detect hands (basic test)
            hands = hand_tracker.detect_hands(frame)
            
            # Draw hand landmarks
            hand_tracker.draw_landmarks(frame, hands)
            
            # Add simple text
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.putText(frame, f"Hands: {len(hands)}", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display
            cv2.imshow('Minimal Test', frame)
            
            # Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        camera.release()
        cv2.destroyAllWindows()
        print("✅ Minimal test completed successfully")
        
    except Exception as e:
        print(f"❌ Minimal test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()