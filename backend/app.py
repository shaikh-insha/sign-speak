"""
FastAPI Server for SignSpeak AI

Receives camera frames from Flutter app, processes them with MediaPipe,
and returns gesture predictions with confidence scores.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
from PIL import Image
import io
from typing import Optional
import os

from landmark_extractor import LandmarkExtractor
from gesture_recognizer import GestureRecognizer

# Initialize FastAPI app
app = FastAPI(
    title="SignSpeak AI API",
    description="Real-time ASL gesture recognition API",
    version="1.0.0"
)

# Enable CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
extractor = LandmarkExtractor()
recognizer = None

# Load model if available
MODEL_PATH = "trained_model.pkl"
if os.path.exists(MODEL_PATH):
    recognizer = GestureRecognizer(model_path=MODEL_PATH)
    print(f"✓ Loaded model from {MODEL_PATH}")
else:
    print(f"⚠ Warning: Model not found at {MODEL_PATH}")
    print("  Please train a model first using: python train_model.py --train")


class PredictionResponse(BaseModel):
    """Response model for gesture prediction."""
    gesture: str
    confidence: float
    hand_detected: bool
    message: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": recognizer is not None and recognizer.is_trained
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": recognizer is not None and recognizer.is_trained
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_gesture(file: UploadFile = File(...)):
    """
    Predict ASL gesture from uploaded image.
    
    Args:
        file: Image file (JPEG/PNG) from Flutter camera
        
    Returns:
        PredictionResponse with gesture label, confidence, and feedback
    """
    if recognizer is None or not recognizer.is_trained:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train a model first."
        )
    
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL Image to OpenCV format (BGR)
        image_np = np.array(image)
        if len(image_np.shape) == 3:
            if image_np.shape[2] == 4:  # RGBA
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
            elif image_np.shape[2] == 3:  # RGB
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        else:
            # Grayscale
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        
        # Extract features
        features = extractor.extract_features_for_training(image_np)
        
        if features is None:
            return PredictionResponse(
                gesture="none",
                confidence=0.0,
                hand_detected=False,
                message="No hand detected. Please show your hand to the camera."
            )
        
        # Predict gesture
        gesture_label, confidence = recognizer.predict(features)
        
        # Generate feedback message
        confidence_threshold = 0.6  # Minimum confidence for "correct"
        if confidence >= confidence_threshold:
            gesture_info = recognizer.get_gesture_info(gesture_label)
            message = f"✓ Correct sign! ({gesture_info['name']})"
        else:
            message = "❌ Try again. Make sure your hand is clearly visible."
        
        return PredictionResponse(
            gesture=gesture_label,
            confidence=confidence,
            hand_detected=True,
            message=message
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.get("/gestures")
async def get_gestures():
    """Get list of supported gestures with descriptions."""
    # Return gesture info even if model is not loaded
    # Gesture info is static and doesn't require a trained model
    gesture_labels = ["hello", "thank_you", "yes", "no", "i_love_you"]
    
    # Static gesture information (same as in GestureRecognizer)
    gesture_info_map = {
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
    
    gestures_info = []
    for gesture_label in gesture_labels:
        info = gesture_info_map.get(gesture_label, {"name": gesture_label, "description": "Unknown gesture"})
        gestures_info.append({
            "label": gesture_label,
            "name": info["name"],
            "description": info["description"]
        })
    
    return {"gestures": gestures_info}


@app.get("/gesture/{gesture_label}")
async def get_gesture_info(gesture_label: str):
    """Get detailed information about a specific gesture."""
    # Return gesture info even if model is not loaded
    gesture_info_map = {
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
    
    if gesture_label not in gesture_info_map:
        raise HTTPException(status_code=404, detail="Gesture not found")
    
    info = gesture_info_map[gesture_label]
    return {
        "label": gesture_label,
        "name": info["name"],
        "description": info["description"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

