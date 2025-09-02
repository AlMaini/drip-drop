# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Drip Drop is a wardrobe organizer/planner AI app that combines a FastAPI backend with a React frontend. The app provides:
- Image analysis of clothing items using Google Gemini Vision API
- AI-powered outfit suggestions based on wardrobe, weather, occasion, and style
- Virtual try-on and styling recommendations
- Image generation capabilities for outfit visualization

## Architecture

**Backend (FastAPI)**: Single-file server (`backend/server.py`) with three main endpoints:
- `/analyze-images` - Analyzes clothing images with custom prompts
- `/suggest-outfit` - Generates outfit recommendations based on wardrobe images and preferences
- `/generate-image` - Creates image descriptions/generations using Gemini Vision API

**Frontend (React)**: Standard Create React App structure with a single main component (`frontend/src/App.js`) that provides an image upload interface for generating images with context.

## Common Commands

### Backend
```bash
# Install dependencies
cd backend && pip install -r requirements.txt

# Run development server
cd backend && python server.py
# OR
cd backend && uvicorn server:app --reload --host 0.0.0.0 --port 8000

# API documentation available at:
# http://localhost:8000/docs (Swagger)
# http://localhost:8000/redoc (ReDoc)
```

### Frontend
```bash
# Install dependencies
cd frontend && npm install

# Start development server
cd frontend && npm start

# Run tests
cd frontend && npm test

# Build for production
cd frontend && npm run build
```

## Environment Configuration

Backend requires a `.env` file with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Copy `backend/.env.example` to `backend/.env` and add your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Key Dependencies

**Backend**:
- fastapi, uvicorn - Web framework and server
- google-genai - Gemini AI integration
- pillow - Image processing
- python-multipart - File upload handling

**Frontend**:
- React 19.1.1 with Create React App
- Standard testing setup with Jest and React Testing Library

## Development Notes

- Backend runs on port 8000, frontend on port 3000
- CORS is configured for local development
- Images are automatically resized to meet Gemini API requirements
- The current implementation uses Gemini Pro Vision for analysis but not actual image generation
- For production image generation, consider integrating DALL-E, Midjourney, or Stable Diffusion APIs