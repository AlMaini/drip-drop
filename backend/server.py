import os
import base64
import io
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Drip Drop Image Generator", description="Generate images using Gemini AI with context images")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

client = genai.Client(api_key=GEMINI_API_KEY)

# Pydantic models
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "realistic"
    context_description: Optional[str] = None

class ImageGenerationResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    generated_image_base64: Optional[str] = None
    error: Optional[str] = None

def process_uploaded_image(uploaded_file: UploadFile) -> Image.Image:
    """Process uploaded image file and return PIL Image object"""
    try:
        image_data = uploaded_file.file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Resize if too large (Gemini has size limits)
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

@app.get("/")
async def root():
    return {"message": "Drip Drop Image Generator API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "image-generator"}

@app.post("/generate-image", response_model=ImageGenerationResponse)
async def generate_image(
    prompt: str = Form(...),
    style: str = Form(default="realistic"),
    context_description: Optional[str] = Form(default=None),
    context_images: List[UploadFile] = File(default=[])
):
    """
    Generate an image using Gemini AI with optional context images
    
    Args:
        prompt: Text description of the image to generate
        style: Style of the image (realistic, artistic, cartoon, etc.)
        context_description: Additional context about the reference images
        context_images: List of reference images to provide context
    """
    try:
        # Prepare the generation prompt
        generation_prompt = f"""
        Create a detailed image based on the following description: {prompt}
        
        Style: {style}
        
        {f"Additional context: {context_description}" if context_description else ""}
        
        Please analyze any provided reference images and use them as context for style, composition, lighting, or other visual elements while creating the new image described in the prompt.
        
        Generate an image that incorporates the visual elements and style from the reference images while fulfilling the specific requirements in the prompt.
        """
        
        # Process context images if provided
        processed_images = []
        if context_images:
            for uploaded_file in context_images:
                if uploaded_file.filename:  # Check if file was actually uploaded
                    processed_image = process_uploaded_image(uploaded_file)
                    processed_images.append(processed_image)
        
        # Prepare content for Gemini
        contents = [generation_prompt]
        contents.extend(processed_images)
        
        # Generate content with Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )
        
        # Process response
        generated_image_base64 = None
        response_text = None
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                response_text = part.text
            elif part.inline_data is not None:
                image = Image.open(io.BytesIO(part.inline_data.data))
                generated_image_base64 = image_to_base64(image)
        
        return ImageGenerationResponse(
            success=True,
            image_url=None,
            generated_image_base64=generated_image_base64,
            error=None
        )
        
    except Exception as e:
        return ImageGenerationResponse(
            success=False,
            error=f"Error generating image: {str(e)}"
        )

@app.post("/analyze-images")
async def analyze_images(
    prompt: str = Form(...),
    images: List[UploadFile] = File(...)
):
    """
    Analyze uploaded images using Gemini Vision API
    
    Args:
        prompt: Question or instruction about the images
        images: List of images to analyze
    """
    try:
        if not images:
            raise HTTPException(status_code=400, detail="At least one image is required")
        
        # Process uploaded images
        processed_images = []
        for uploaded_file in images:
            processed_image = process_uploaded_image(uploaded_file)
            processed_images.append(processed_image)
        
        # Prepare content for analysis
        contents = [prompt]
        contents.extend(processed_images)
        
        # Analyze images
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        return {
            "success": True,
            "analysis": analysis_text if analysis_text else "No analysis generated",
            "image_count": len(processed_images)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error analyzing images: {str(e)}"
        }

@app.post("/suggest-outfit")
async def suggest_outfit(
    occasion: str = Form(...),
    weather: str = Form(default="mild"),
    style_preference: str = Form(default="casual"),
    wardrobe_images: List[UploadFile] = File(default=[])
):
    """
    Suggest outfit combinations based on wardrobe images and preferences
    
    Args:
        occasion: The occasion for the outfit (work, casual, formal, etc.)
        weather: Weather conditions (hot, cold, rainy, mild)
        style_preference: Preferred style (casual, formal, trendy, classic)
        wardrobe_images: Images of clothing items in the wardrobe
    """
    try:
        prompt = f"""
        Analyze the provided wardrobe images and suggest outfit combinations for the following:
        
        Occasion: {occasion}
        Weather: {weather}
        Style Preference: {style_preference}
        
        Please provide:
        1. Recommended outfit combinations from the visible clothing items
        2. Styling tips for the occasion and weather
        3. Color coordination suggestions
        4. Any missing pieces that would complete the outfit
        
        Be specific about which items from the images work well together.
        """
        
        # Process wardrobe images
        processed_images = []
        if wardrobe_images:
            for uploaded_file in wardrobe_images:
                if uploaded_file.filename:
                    processed_image = process_uploaded_image(uploaded_file)
                    processed_images.append(processed_image)
        
        if not processed_images:
            return {
                "success": False,
                "error": "No wardrobe images provided"
            }
        
        # Prepare content
        contents = [prompt]
        contents.extend(processed_images)
        
        # Get suggestions
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )
        
        # Extract text response
        suggestions_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                suggestions_text = part.text
                break
        
        return {
            "success": True,
            "suggestions": suggestions_text if suggestions_text else "No suggestions generated",
            "wardrobe_items_analyzed": len(processed_images),
            "occasion": occasion,
            "weather": weather,
            "style_preference": style_preference
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error generating outfit suggestions: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)