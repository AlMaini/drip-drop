#!/usr/bin/env python3
"""
Test script for the Drip Drop FastAPI server
"""
import os
import sys

# Set a dummy API key for testing imports
os.environ["GEMINI_API_KEY"] = "test_key"

try:
    import server
    print("✅ Server imports successfully!")
    print("✅ All dependencies are properly installed")
    print("✅ FastAPI app is configured")
    print("\nTo run the server:")
    print("1. Copy .env.example to .env")
    print("2. Add your real Gemini API key to .env")
    print("3. Run: python server.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
