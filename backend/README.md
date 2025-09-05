# Drip Drop Backend

This is the FastAPI backend server for the Drip Drop application that integrates with Google's Gemini AI for advanced clothing analysis, virtual try-on, and image generation.

## Features

- **Clothing Analysis**: Extract and analyze individual clothing items from photos
- **Quality Assessment**: Check if uploaded images meet professional studio quality standards
- **Virtual Try-On**: AI-powered iterative virtual clothing try-on using Gemini AI
- **Image Generation**: Generate images with context using Gemini AI
- **Clothing Extraction**: Separate and itemize multiple clothing pieces from single images
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
./start.sh
```

The server will be available at `http://localhost:8000`

**Note**: The start script will check for a virtual environment at `../.venv` and automatically activate it.

## API Endpoints

### Health Check
- **GET `/`** - Health check endpoint

### Clothing Analysis
- **POST `/api/extract-clothing`** - Extract single clothing item from photo and create professional product image
  - `image` (file): Image containing a clothing item

- **POST `/api/check-clothing-quality`** - Check if uploaded image meets professional studio quality standards
  - `image` (file): Image to analyze for quality

- **POST `/api/itemize-clothing`** - Analyze image and return a list of clothing items found
  - `image` (file): Image to analyze for clothing items

- **POST `/api/extract-clothes-specific`** - Extract specific clothing items from photo
  - `image` (file): Image containing clothing items
  - `clothing_items` (string): JSON array of specific clothing items to extract

### Virtual Try-On
- **POST `/api/try-on-clothes`** - AI-powered iterative virtual try-on
  - `images` (files): List of images containing person and clothing items

### Image Generation
- **POST `/api/generate-image`** - Generate images using Gemini AI with context
  - `prompt` (string): Text description of image to generate
  - `style` (string): Style preference (default: "realistic")
  - `context_description` (string, optional): Additional context about reference images
  - `context_images` (files, optional): Reference images for context

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

Key dependencies (see `requirements.txt` for complete list):
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `google-generativeai==0.3.2` - Gemini AI client
- `pillow==10.1.0` - Image processing
- `python-multipart==0.0.6` - File upload support

## Notes

- The backend uses Gemini AI for advanced image analysis and generation capabilities
- Images are automatically processed and resized to meet API requirements
- Virtual try-on feature uses iterative AI processing for realistic results
- CORS is configured for local development (ports 3000 and 3001)
- All endpoints return JSON responses with success/error status
