"""
Model Training Script

Collects training data and trains the ASL gesture recognizer.
This script helps create a small dataset for the 5 basic ASL gestures.

Usage:
    python train_model.py --collect  # Collect training data
    python train_model.py --train    # Train model from collected data
"""

import cv2
import numpy as np
import argparse
import os
import json
from landmark_extractor import LandmarkExtractor
from gesture_recognizer import GestureRecognizer


class DataCollector:
    """Helper class to collect training data interactively."""
    
    def __init__(self, data_dir: str = "training_data"):
        self.data_dir = data_dir
        self.extractor = LandmarkExtractor()
        self.gestures = ["hello", "thank_you", "yes", "no", "i_love_you"]
        os.makedirs(data_dir, exist_ok=True)
    
    def collect_data(self, samples_per_gesture: int = 20):
        """
        Collect training data using webcam.
        
        Args:
            samples_per_gesture: Number of samples to collect per gesture
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("\n=== ASL Gesture Data Collection ===")
        print("Instructions:")
        print("1. Press number keys 1-5 to select gesture:")
        print("   1: hello, 2: thank_you, 3: yes, 4: no, 5: i_love_you")
        print("2. Press SPACE to capture a sample")
        print("3. Press 'q' to quit")
        print(f"4. Collect {samples_per_gesture} samples per gesture\n")
        
        gesture_data = {i: [] for i in range(len(self.gestures))}
        current_gesture = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Extract landmarks
            landmarks = self.extractor.extract_landmarks(frame)
            
            # Draw landmarks
            if landmarks is not None:
                annotated = self.extractor.draw_landmarks(frame, landmarks)
            else:
                annotated = frame.copy()
            
            # Display current gesture
            if current_gesture is not None:
                gesture_name = self.gestures[current_gesture]
                count = len(gesture_data[current_gesture])
                cv2.putText(annotated, f"Gesture: {gesture_name} ({count}/{samples_per_gesture})",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(annotated, "Select gesture (1-5)", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.putText(annotated, "SPACE: Capture | Q: Quit", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("Data Collection", annotated)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key >= ord('1') and key <= ord('5'):
                current_gesture = key - ord('1')
                print(f"Selected gesture: {self.gestures[current_gesture]}")
            elif key == ord(' ') and current_gesture is not None:
                if landmarks is not None:
                    # Extract features for training
                    features = self.extractor.extract_features_for_training(frame)
                    if features is not None:
                        gesture_data[current_gesture].append(features)
                        count = len(gesture_data[current_gesture])
                        print(f"Captured sample {count}/{samples_per_gesture} for {self.gestures[current_gesture]}")
                        
                        if count >= samples_per_gesture:
                            print(f"✓ Completed {self.gestures[current_gesture]}")
                            current_gesture = None
                else:
                    print("No hand detected. Try again.")
        
        cap.release()
        cv2.destroyAllWindows()
        self.extractor.close()
        
        # Save collected data
        self.save_data(gesture_data)
    
    def save_data(self, gesture_data: dict):
        """Save collected training data to files."""
        all_features = []
        all_labels = []
        
        for gesture_id, features_list in gesture_data.items():
            for features in features_list:
                all_features.append(features)
                all_labels.append(gesture_id)
        
        if len(all_features) == 0:
            print("No data collected!")
            return
        
        # Convert to numpy arrays
        X = np.array(all_features)
        y = np.array(all_labels)
        
        # Save to file
        data_file = os.path.join(self.data_dir, "training_data.npz")
        np.savez(data_file, X=X, y=y)
        
        print(f"\n✓ Saved {len(X)} samples to {data_file}")
        print(f"  Gesture distribution:")
        for i, gesture in enumerate(self.gestures):
            count = np.sum(y == i)
            print(f"    {gesture}: {count} samples")


def train_model(data_dir: str = "training_data", model_path: str = "trained_model.pkl"):
    """
    Train the gesture recognizer from collected data.
    
    Args:
        data_dir: Directory containing training data
        model_path: Path to save trained model
    """
    data_file = os.path.join(data_dir, "training_data.npz")
    
    if not os.path.exists(data_file):
        print(f"Error: Training data not found at {data_file}")
        print("Please collect data first using: python train_model.py --collect")
        return
    
    # Load data
    data = np.load(data_file)
    X = data['X']
    y = data['y']
    
    print(f"\n=== Training Model ===")
    print(f"Training samples: {len(X)}")
    print(f"Features per sample: {X.shape[1]}")
    print(f"Number of classes: {len(np.unique(y))}")
    
    # Initialize recognizer
    recognizer = GestureRecognizer(model_type="knn")
    
    # Train
    recognizer.train(X, y)
    
    # Save model
    recognizer.save_model(model_path)
    
    # Test accuracy (simple validation)
    predictions = recognizer.model.predict(recognizer.scaler.transform(X))
    accuracy = np.mean(predictions == y)
    print(f"\n✓ Training accuracy: {accuracy * 100:.2f}%")
    print(f"✓ Model saved to {model_path}")


def main():
    parser = argparse.ArgumentParser(description="Train ASL gesture recognizer")
    parser.add_argument("--collect", action="store_true", help="Collect training data")
    parser.add_argument("--train", action="store_true", help="Train model from data")
    parser.add_argument("--samples", type=int, default=20, help="Samples per gesture (default: 20)")
    parser.add_argument("--data-dir", type=str, default="training_data", help="Data directory")
    parser.add_argument("--model", type=str, default="trained_model.pkl", help="Model output path")
    
    args = parser.parse_args()
    
    if args.collect:
        collector = DataCollector(data_dir=args.data_dir)
        collector.collect_data(samples_per_gesture=args.samples)
    elif args.train:
        train_model(data_dir=args.data_dir, model_path=args.model)
    else:
        print("Please specify --collect or --train")
        print("Example: python train_model.py --collect")
        print("         python train_model.py --train")


if __name__ == "__main__":
    main()

