# Quick Model Training Guide

## The Error You're Seeing
```
Model not loaded. Please train a model first.
```

This is **normal** - you need to train the ML model before gesture recognition will work.

---

## Step-by-Step Training Instructions

### Step 1: Open Terminal
Open a **new terminal window** (keep your Flutter app running).

### Step 2: Navigate to Backend
```bash
cd /Users/inshashaikh/Desktop/MySpace/Projects/SignSpeak/backend
```

### Step 3: Collect Training Data
```bash
python3 train_model.py --collect --samples 20
```

**What happens:**
- A camera window will open
- You'll see yourself in the camera feed
- Instructions will appear in the terminal

**How to use:**
1. **Press number keys 1-5** to select a gesture:
   - `1` = Hello
   - `2` = Thank You
   - `3` = Yes
   - `4` = No
   - `5` = I Love You

2. **Show the gesture** to the camera (make sure your hand is clearly visible)

3. **Press SPACE** to capture a sample
   - You'll see "Captured sample X/20" in the terminal
   - Repeat until you have 20 samples for that gesture

4. **Move to next gesture:**
   - Press the next number key (1-5)
   - Repeat steps 2-3

5. **When done with all gestures:**
   - Press `q` to quit
   - Data will be saved automatically

**Tips:**
- Make sure your hand is clearly visible
- Try different angles and lighting
- Keep your hand steady when pressing SPACE
- You need 20 samples per gesture (100 total)

### Step 4: Train the Model
```bash
python3 train_model.py --train
```

**What happens:**
- The script loads your collected data
- Trains a KNN classifier
- Saves the model as `trained_model.pkl`
- Shows training accuracy

**Expected output:**
```
Training samples: 100
Features per sample: 42
Number of classes: 5
Model trained on 100 samples
✓ Training accuracy: 85.00%
✓ Model saved to trained_model.pkl
```

### Step 5: Restart Backend (if needed)
If your backend server is already running, it should automatically detect the new model. If not:

```bash
# Stop the current server (Ctrl+C if running in terminal)
# Then restart:
python3 app.py
```

### Step 6: Test in Flutter App
1. Go back to your Flutter app
2. Click "Check Gesture" button
3. Show a hand gesture to the camera
4. You should see feedback! ✅

---

## Quick Training (Minimum)

If you want to test quickly with fewer samples:

```bash
# Collect only 5 samples per gesture (25 total)
python3 train_model.py --collect --samples 5

# Train
python3 train_model.py --train
```

**Note:** More samples = better accuracy. 20 samples per gesture is recommended.

---

## Troubleshooting

### "No module named 'cv2'" or other import errors
```bash
cd backend
pip3 install -r requirements.txt
```

### Camera not opening
- Make sure no other app is using the camera
- Check macOS Camera permissions
- Try closing other camera apps

### "No hand detected" during collection
- Make sure your hand is clearly visible
- Good lighting helps
- Try moving closer to the camera

### Model accuracy is low
- Collect more samples (try 30-50 per gesture)
- Make sure samples are diverse (different angles, lighting)
- Check that your gestures are clear and distinct

---

## What Gets Created

After training, you'll have:
- `training_data/training_data.npz` - Your collected samples
- `trained_model.pkl` - The trained ML model

Both files are needed for the app to work.

---

## Next Steps After Training

1. ✅ Model is trained
2. ✅ Backend server is running
3. ✅ Flutter app can connect
4. ✅ Gesture recognition works!

Try different gestures and see the confidence scores!

