# Drip Drop Backend

This is the FastAPI backend server for the Drip Drop application that integrates with Google's Gemini AI for image analysis and outfit suggestions.

## Features

- **Image Analysis**: Analyze clothing images using Gemini Vision API
- **Outfit Suggestions**: Get AI-powered outfit recommendations based on wardrobe images
- **Style Context**: Use existing images as context for style analysis
- **CORS Support**: Configured for frontend integration

## Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Get a Gemini API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy it to your `.env` file

## Running the Server

```bash
python server.py
```

Or using uvicorn directly:
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`

## API Endpoints

### GET `/`
Health check endpoint

### POST `/analyze-images`
Analyze uploaded images with a custom prompt
- **Parameters**: 
  - `prompt` (string): Question or instruction about the images
  - `images` (files): Images to analyze

### POST `/suggest-outfit`
Get outfit suggestions based on wardrobe images
- **Parameters**:
  - `occasion` (string): The occasion (work, casual, formal, etc.)
  - `weather` (string): Weather conditions (hot, cold, rainy, mild)
  - `style_preference` (string): Style preference (casual, formal, trendy, classic)
  - `wardrobe_images` (files): Images of clothing items

### POST `/generate-image`
Generate image descriptions using context images (Note: Actual image generation requires additional services)
- **Parameters**:
  - `prompt` (string): Description of image to generate
  - `style` (string): Style preference
  - `context_description` (string): Additional context
  - `context_images` (files): Reference images

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notes

- The current Gemini Pro Vision model excels at image analysis but doesn't directly generate images
- For actual image generation, consider integrating with DALL-E, Midjourney, or Stable Diffusion APIs
- Images are automatically resized to meet API requirements
- CORS is configured for local development
