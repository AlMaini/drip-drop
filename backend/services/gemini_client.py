import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

client = genai.Client(api_key=GEMINI_API_KEY)
editing_model = "gemini-2.5-flash-image-preview"
analysis_model = "gemini-1.5-flash"

def get_gemini_client():
    """Get the configured Gemini client"""
    return client