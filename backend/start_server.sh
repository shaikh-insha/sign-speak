#!/bin/bash

# Quick start script for FastAPI server

echo "Starting SignSpeak AI Backend Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.dependencies_installed
fi

# Check if model exists
if [ ! -f "trained_model.pkl" ]; then
    echo ""
    echo "⚠️  WARNING: Model not found!"
    echo "Please train a model first:"
    echo "  python train_model.py --collect  # Collect training data"
    echo "  python train_model.py --train    # Train model"
    echo ""
    echo "Starting server anyway (will show error on /predict endpoint)..."
    echo ""
fi

# Start server
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
python app.py

