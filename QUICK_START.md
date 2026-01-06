# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train_model.py --collect --samples 20  # Collect data
python train_model.py --train                  # Train model
python app.py                                  # Start server
```

### Flutter Setup

```bash
cd flutter_app
flutter pub get
# Edit lib/services/api_service.dart to set correct baseUrl
flutter run
```

## 📝 Key Files

### Backend
- `app.py` - FastAPI server (main entry point)
- `landmark_extractor.py` - MediaPipe Hands integration
- `gesture_recognizer.py` - ML classifier
- `train_model.py` - Data collection & training

### Flutter
- `lib/main.dart` - App entry point
- `lib/services/api_service.dart` - **IMPORTANT: Update baseUrl here**
- `lib/screens/practice_screen.dart` - Camera practice mode
- `lib/screens/learning_screen.dart` - Gesture learning mode

## 🔧 Common Issues

### "Model not found"
```bash
cd backend
python train_model.py --train
```

### "Camera permission denied"
- Android: Check `android/app/src/main/AndroidManifest.xml`
- iOS: Check `ios/Runner/Info.plist`

### "API connection failed"
1. Verify backend is running: `curl http://localhost:8000/health`
2. Update `baseUrl` in `lib/services/api_service.dart`:
   - Android Emulator: `http://10.0.2.2:8000`
   - iOS Simulator: `http://localhost:8000`
   - Physical Device: `http://<your-ip>:8000`

## 🎯 Testing Flow

1. Start backend: `cd backend && python app.py`
2. Test API: `curl http://localhost:8000/health`
3. Run Flutter: `cd flutter_app && flutter run`
4. Navigate to "Practice" tab
5. Click "Check Gesture" button
6. See feedback!

## 📊 Model Training Tips

- **More samples = better accuracy**: Try 50-100 samples per gesture
- **Variety matters**: Collect samples in different lighting/angles
- **Clean data**: Only capture when hand is clearly visible
- **Test accuracy**: Check training accuracy after training

## 🔍 Debugging

### Backend Logs
- Check terminal output for errors
- API docs: `http://localhost:8000/docs`

### Flutter Logs
```bash
flutter run --verbose
```

### Test API Manually
```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@test_image.jpg"
```

