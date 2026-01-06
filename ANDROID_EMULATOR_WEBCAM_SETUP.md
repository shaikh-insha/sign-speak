# Android Emulator Webcam Setup Guide

## Overview
This guide shows how to configure the Android Emulator to use your MacBook's real webcam instead of the synthetic/pixelated camera feed.

**Note:** This is an emulator configuration task, not a Flutter issue. The pixelated feed is the emulator's default synthetic camera.

---

## Step-by-Step Instructions

### Step 1: Open Extended Controls
1. While the Android Emulator is running, look for the **three dots (⋯)** icon in the right sidebar
2. Click the three dots to open **Extended Controls**
   - Alternatively: Press `Cmd + /` or click the menu button

### Step 2: Navigate to Camera Settings
1. In the Extended Controls window, click **Camera** in the left sidebar
2. You'll see two camera options:
   - **Front Camera**
   - **Back Camera**

### Step 3: Configure Front Camera
1. Under **Front Camera**, click the dropdown menu
2. Select **Webcam0** (this is your MacBook's built-in webcam)
3. If **Webcam0** doesn't appear:
   - Make sure no other app is using the webcam
   - Try closing other apps that might be accessing the camera
   - Restart the emulator and try again

### Step 4: Configure Back Camera
1. Under **Back Camera**, click the dropdown menu
2. Select **Webcam0** (same webcam, but emulated as back camera)
3. Note: Both cameras will use the same physical webcam, but the emulator treats them as separate

### Step 5: Apply Settings
1. Click **Done** or close the Extended Controls window
2. **Important:** The emulator must be restarted for changes to take effect

---

## Emulator Restart Steps

### Method 1: Cold Boot (Recommended)
1. Close the Android Emulator completely
2. Wait a few seconds for it to fully shut down
3. Restart the emulator from Android Studio or command line
4. The webcam settings will be applied on startup

### Method 2: Quick Restart
1. In the emulator, click the **Power** button (or press `Cmd + P`)
2. Select **Restart** from the power menu
3. Wait for the emulator to reboot

### Verification After Restart
- The emulator should now use your MacBook's webcam
- You'll see a real camera feed instead of the pixelated green screen

---

## How to Verify Webcam is Active

### Method 1: Built-in Camera App
1. Open the **Camera** app on the emulator
2. You should see a live feed from your MacBook's webcam
3. Switch between front/back camera - both should show the webcam feed

### Method 2: Your Flutter App
1. Open your SignSpeak app
2. Navigate to the **Practice** tab
3. The camera preview should show a real video feed instead of pixelated blocks
4. You should see yourself or your surroundings clearly

### Method 3: Third-Party Camera App
1. Install any camera app from Play Store
2. Open it and verify the camera feed is real

### Method 4: Command Line Verification (Optional)
```bash
# Check if emulator is using webcam
adb shell dumpsys media.camera | grep -i "camera"
```

---

## Common Pitfalls & Solutions

### ❌ Problem: Webcam0 Not Available
**Solution:**
- Close all apps using the webcam (Zoom, Teams, FaceTime, etc.)
- Restart the emulator
- Check System Preferences → Security & Privacy → Camera to ensure emulator has permission

### ❌ Problem: Settings Don't Apply
**Solution:**
- **You must restart the emulator** - settings don't apply until restart
- Use Cold Boot (completely close and reopen) instead of quick restart

### ❌ Problem: Camera Still Shows Pixelated Feed
**Solution:**
- Verify settings were saved (check Extended Controls again)
- Ensure you selected **Webcam0** (not "VirtualScene" or "Emulated")
- Try a cold boot restart
- Check macOS Camera permissions for the emulator

### ❌ Problem: Camera Works But App Crashes
**Solution:**
- This is likely a Flutter/camera plugin issue, not emulator config
- Check camera permissions in AndroidManifest.xml
- Verify camera plugin version compatibility

### ❌ Problem: Only Front Camera Works
**Solution:**
- Both front and back should be set to **Webcam0**
- The emulator will use the same physical camera for both
- This is expected behavior - real devices have separate cameras

---

## Hardware Limitations

### Supported Configurations
- ✅ **macOS with Intel/Apple Silicon** - Webcam passthrough works
- ✅ **Most modern MacBooks** - Built-in webcam supported
- ⚠️ **External USB webcams** - May work but not guaranteed

### Not Supported
- ❌ Some older emulator versions may not support webcam passthrough
- ❌ Virtual machines running Android Emulator may have limitations
- ❌ Some hardware configurations may not expose webcam properly

---

## Best Practices

### For Development
- ✅ Using webcam passthrough is fine for development and testing
- ✅ Helps test camera functionality without a physical device
- ✅ Faster iteration during development

### For Demo/Production
- ⚠️ **Always test on real Android devices** before demos
- ⚠️ Real devices have better camera performance
- ⚠️ Emulator camera may have slight delays or quality differences

---

## Troubleshooting Checklist

- [ ] Extended Controls opened successfully
- [ ] Both Front and Back cameras set to **Webcam0**
- [ ] Settings saved (clicked Done)
- [ ] Emulator restarted (cold boot recommended)
- [ ] No other apps using the webcam
- [ ] macOS Camera permissions granted to emulator
- [ ] Verified in Camera app or Flutter app

---

## Quick Reference

**Settings Location:** Extended Controls (⋯) → Camera  
**Front Camera:** Webcam0  
**Back Camera:** Webcam0  
**Restart Required:** Yes (Cold Boot)  
**Verification:** Open Camera app or your Flutter app

---

## Additional Notes

- The emulator uses the same physical webcam for both front and back cameras
- Camera quality may be slightly different from real devices
- Some camera features (flash, autofocus) may not work in emulator
- This configuration persists across emulator sessions

---

**Remember:** This is purely an emulator configuration. Your Flutter code doesn't need any changes - it will automatically use the webcam once configured.

