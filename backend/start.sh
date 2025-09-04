#!/bin/bash

# Drip Drop Backend Startup Script

echo "🎨 Starting Drip Drop Backend Server..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your Gemini API key"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment and start server
echo "🚀 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

../.venv/bin/python server.py
