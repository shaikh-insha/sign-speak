"""
Gesture Recognizer Module

Trains and uses ML models (KNN/SVM) to classify ASL gestures.
Supports 5 basic ASL phrases: Hello, Thank You, Yes, No, I Love You
"""

import numpy as np
import pickle
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from typing import Optional, Tuple, Dict
import joblib


class GestureRecognizer:
    """
    ML-based ASL gesture recognizer.
    
    Uses KNN classifier by default (fast, interpretable, good for small datasets).
    Can also use SVM for comparison.
    """
    
    # Supported ASL gestures
    GESTURES = {
        0: "hello",
        1: "thank_you",
        2: "yes",
        3: "no",
        4: "i_love_you"
    }
    
    GESTURE_LABELS = ["hello", "thank_you", "yes", "no", "i_love_you"]
    
    def __init__(self, model_type: str = "knn", model_path: Optional[str] = None):
        """
        Initialize gesture recognizer.
        
        Args:
            model_type: "knn" or "svm"
            model_path: Path to saved model file (optional)
        """
        self.model_type = model_type
        self.scaler = StandardScaler()
        self.model = None
        self.is_trained = False
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the ML model based on type."""
        if self.model_type == "knn":
            # KNN with k=5 neighbors, good for small datasets
            self.model = KNeighborsClassifier(n_neighbors=5, weights='distance')
        elif self.model_type == "svm":
            # SVM with RBF kernel
            self.model = SVC(kernel='rbf', probability=True, C=1.0, gamma='scale')
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        Train the gesture recognizer.
        
        Args:
            X: Feature vectors (n_samples, n_features)
            y: Labels (n_samples,) - integer labels corresponding to GESTURES
        """
        if len(X) == 0:
            raise ValueError("Training data is empty")
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        print(f"Model trained on {len(X)} samples")
        print(f"Classes: {np.unique(y)}")
    
    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Predict gesture from feature vector.
        
        Args:
            features: Feature vector of shape (n_features,)
            
        Returns:
            Tuple of (gesture_label, confidence_score)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Please train or load a model first.")
        
        # Reshape if needed
        if features.ndim == 1:
            features = features.reshape(1, -1)
        
        # Normalize
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get confidence (probability of predicted class)
        confidence = float(probabilities[prediction])
        
        # Get gesture label
        gesture_label = self.GESTURES.get(prediction, "unknown")
        
        return gesture_label, confidence
    
    def predict_batch(self, features_list: np.ndarray) -> list:
        """
        Predict gestures for multiple feature vectors.
        
        Args:
            features_list: Array of feature vectors (n_samples, n_features)
            
        Returns:
            List of (gesture_label, confidence) tuples
        """
        if not self.is_trained:
            raise ValueError("Model not trained.")
        
        features_scaled = self.scaler.transform(features_list)
        predictions = self.model.predict(features_scaled)
        probabilities = self.model.predict_proba(features_scaled)
        
        results = []
        for i, pred in enumerate(predictions):
            confidence = float(probabilities[i][pred])
            gesture_label = self.GESTURES.get(pred, "unknown")
            results.append((gesture_label, confidence))
        
        return results
    
    def save_model(self, filepath: str):
        """
        Save trained model to file.
        
        Args:
            filepath: Path to save model
        """
        if not self.is_trained:
            raise ValueError("No trained model to save")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_type': self.model_type,
            'gestures': self.GESTURES
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """
        Load trained model from file.
        
        Args:
            filepath: Path to model file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.model_type = model_data.get('model_type', 'knn')
        self.is_trained = True
        
        print(f"Model loaded from {filepath}")
    
    def get_gesture_info(self, gesture_label: str) -> Dict[str, str]:
        """
        Get information about a gesture.
        
        Args:
            gesture_label: Gesture label (e.g., "hello")
            
        Returns:
            Dictionary with gesture information
        """
        info = {
            "hello": {
                "name": "Hello",
                "description": "Wave your hand from side to side, or raise your hand with palm facing forward."
            },
            "thank_you": {
                "name": "Thank You",
                "description": "Touch your chin with your fingertips, then move your hand forward and down."
            },
            "yes": {
                "name": "Yes",
                "description": "Make a fist and move it up and down, like nodding."
            },
            "no": {
                "name": "No",
                "description": "Touch your thumb and middle finger together, then snap them apart."
            },
            "i_love_you": {
                "name": "I Love You",
                "description": "Raise your hand with thumb, index finger, and pinky extended, middle and ring fingers down."
            }
        }
        
        return info.get(gesture_label, {"name": "Unknown", "description": "Unknown gesture"})

