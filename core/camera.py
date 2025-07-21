"""
Camera management for AR Chemistry Flame Test Simulator
"""

import cv2
import numpy as np

class CameraManager:
    def __init__(self, camera_id=0, width=1280, height=720):
        """Initialize camera manager - OPTIMIZED FOR HIGH FPS"""
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        self.initialize_camera()
    
    def initialize_camera(self):
        """Initialize camera capture with high performance settings"""
        print(f"📹 Initializing high-performance camera {self.camera_id}...")
        
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {self.camera_id}")
        
        # HIGH PERFORMANCE CAMERA SETTINGS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 120)  # Request 120 FPS
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer lag
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # Fast codec
        
        # Disable auto-adjustments for consistent performance
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual exposure
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Disable autofocus
        
        # Get actual camera properties
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        print(f"✅ High-performance camera initialized: {actual_width}x{actual_height} @ {actual_fps}fps")
    
    def get_frame(self):
        """Get current frame from camera"""
        if self.cap is None:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        return frame
    
    def release(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            print("📹 Camera released")
    
    def get_camera_info(self):
        """Get camera information"""
        if self.cap is None:
            return None
        
        return {
            'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': self.cap.get(cv2.CAP_PROP_FPS)
        }