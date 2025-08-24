#!/bin/bash

# EcoSort Backend Startup Script

echo "🌱 Starting EcoSort AI Waste Classifier Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements_simple.txt

# Create uploads directory
mkdir -p uploads

# Start the server
echo "🚀 Starting Flask server on http://localhost:5000"
python app_simple.py