"""
Landmark Extractor Module

Extracts hand landmarks from images using MediaPipe Hands.
Converts landmarks to feature vectors for ML classification.
"""

import mediapipe as mp
import numpy as np
import cv2
from typing import List, Optional, Tuple


class LandmarkExtractor:
    """
    Extracts hand landmarks from images using MediaPipe Hands.
    
    MediaPipe Hands provides 21 3D landmarks per hand:
    - Wrist (0)
    - Thumb (1-4)
    - Index finger (5-8)
    - Middle finger (9-12)
    - Ring finger (13-16)
    - Pinky (17-20)
    """
    
    def __init__(self):
        """Initialize MediaPipe Hands model."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,  # Focus on single hand for ASL
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    def extract_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand landmarks from an image.
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            Feature vector of shape (63,) if hand detected, None otherwise
            Feature vector contains normalized x, y, z coordinates of 21 landmarks
        """
        # Convert BGR to RGB (MediaPipe expects RGB)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.hands.process(rgb_image)
        
        if not results.multi_hand_landmarks:
            return None
        
        # Get first hand landmarks
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Extract coordinates
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        
        return np.array(landmarks, dtype=np.float32)
    
    def draw_landmarks(self, image: np.ndarray, landmarks: Optional[np.ndarray]) -> np.ndarray:
        """
        Draw hand landmarks and connections on image.
        
        Args:
            image: Input image
            landmarks: Landmark data (not used directly, but kept for API consistency)
            
        Returns:
            Image with landmarks drawn
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)
        
        annotated_image = image.copy()
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
        
        return annotated_image
    
    def extract_features_for_training(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract normalized feature vector for training.
        Normalizes coordinates relative to wrist position.
        
        Args:
            image: Input image
            
        Returns:
            Normalized feature vector of shape (60,) or None
        """
        landmarks = self.extract_landmarks(image)
        
        if landmarks is None:
            return None
        
        # Reshape to (21, 3) for easier manipulation
        landmarks_3d = landmarks.reshape(21, 3)
        
        # Normalize relative to wrist (landmark 0)
        wrist = landmarks_3d[0]
        normalized = landmarks_3d - wrist
        
        # Flatten back to 1D (excluding z-coordinate for 2D features)
        # Using only x, y for better generalization
        features = normalized[:, :2].flatten()  # Shape: (42,)
        
        return features.astype(np.float32)
    
    def close(self):
        """Release MediaPipe resources."""
        self.hands.close()

