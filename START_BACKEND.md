# Quick Start: Backend Server

## 🚀 Start the Backend Server

The Flutter app needs the backend server running to work. Follow these steps:

### Option 1: Quick Start (if model already exists)

```bash
cd backend
python3 app.py
```

The server will start on `http://localhost:8000`

### Option 2: First Time Setup

1. **Install dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Train the model (if not already done):**
   ```bash
   # Collect training data (20 samples per gesture)
   python train_model.py --collect --samples 20
   
   # Train the model
   python train_model.py --train
   ```

3. **Start the server:**
   ```bash
   python app.py
   ```

### Verify Server is Running

Open in browser: http://localhost:8000/docs

Or test with curl:
```bash
curl http://localhost:8000/health
```

### For Android Emulator

The Flutter app is already configured to use `http://10.0.2.2:8000` for Android emulator, which automatically maps to your host machine's `localhost:8000`.

### Troubleshooting

- **Port 8000 already in use?** Change the port in `app.py` (line ~188)
- **Model not found?** Run `python train_model.py --train` first
- **Import errors?** Make sure virtual environment is activated and dependencies are installed

