import os
import base64
import io
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google import genai
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
            
        # Resize if too large (Gemini has size limits) while maintaining aspect ratio
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


@app.post("/try-on-clothes")
async def try_on_clothes(
    images: List[UploadFile] = File(...)
):
    """
    Virtual try-on using Gemini AI - make the person wear the provided clothes
    
    Args:
        images: List of images containing person and clothing items
    """
    try:
        if not images:
            raise HTTPException(status_code=400, detail="At least one image is required")
        
        # Process uploaded images
        processed_images = []
        for uploaded_file in images:
            processed_image = process_uploaded_image(uploaded_file)
            processed_images.append(processed_image)
        
        # Create the try-on prompt
        prompt = "Make the person wear the clothes shown in these images. Create a realistic visualization of how the clothing items would look when worn by the person, maintaining proper fit, proportions, and styling. Do not change the colors of the clothes. Do not add additional clothing items other than the ones in the context. Maintain the aspect ratio from the image of the person."
        
        # Prepare content for Gemini
        contents = [prompt]
        contents.extend(processed_images)
        
        # Generate the try-on visualization
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )
        
        # Process response - check for both generated image and text description
        generated_image_base64 = None
        description_text = None
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                description_text = part.text
            elif part.inline_data is not None:
                image = Image.open(io.BytesIO(part.inline_data.data))
                generated_image_base64 = image_to_base64(image)
        
        return {
            "success": True,
            "generated_image_base64": generated_image_base64,
            "description": description_text if description_text else "Try-on visualization generated",
            "images_processed": len(processed_images)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error generating try-on visualization: {str(e)}"
        }

@app.post("/extract-clothing")
async def extract_clothing(
    image: UploadFile = File(...)
):
    """
    Extract clothing item from photo and create professional product image
    
    Args:
        image: Single image containing a clothing item
    """
    try:
        # Process uploaded image
        processed_image = process_uploaded_image(image)
        
        # Create the extraction prompt
        prompt = "Take the clothing item in this photo and make a full view image of the item with a white background as a professionally shot image for a clothing item on an online store."
        
        # Prepare content for Gemini
        contents = [prompt, processed_image]
        
        # Generate the professional product image
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )
        
        # Process response - check for both generated image and text description
        generated_image_base64 = None
        description_text = None
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                description_text = part.text
            elif part.inline_data is not None:
                image_data = Image.open(io.BytesIO(part.inline_data.data))
                generated_image_base64 = image_to_base64(image_data)
        
        return {
            "success": True,
            "generated_image_base64": generated_image_base64,
            "description": description_text if description_text else "Professional clothing product image generated"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting clothing item: {str(e)}"
        }

def check_professional_clothing_image(image: Image.Image) -> dict:
    """
    Check if an image is a professional studio quality photo of a single clothing item
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        dict: Analysis results containing is_professional, is_single_item, item_type, and confidence
    """
    try:
        # Create analysis prompt
        prompt = """
        Analyze this image and determine if it meets the following criteria:
        1. Is it a professional studio quality photograph?
        2. Does it contain exactly one clothing item?
        3. Is the background clean/plain (preferably white or neutral)?
        4. Is the lighting professional and even?
        5. Is the clothing item the main focus and clearly visible?
        
        Please respond in the following JSON format:
        {
            "is_professional": true/false,
            "is_single_item": true/false,
            "item_type": "shirt/pants/dress/shoes/etc or null if not clothing",
            "background_quality": "excellent/good/poor",
            "lighting_quality": "excellent/good/poor",
            "overall_confidence": 0.0-1.0,
            "issues": ["list of any issues found"],
            "reasoning": "brief explanation of the assessment"
        }
        
        Only respond with the JSON object, no additional text.
        """
        
        # Prepare content for Gemini
        contents = [prompt, image]
        
        # Call Gemini 1.5 Flash for analysis
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        if not analysis_text:
            return {
                "error": "No analysis text received from Gemini",
                "is_professional": False,
                "is_single_item": False
            }
        
        # Try to parse JSON response
        import json
        try:
            # Clean the response text by removing markdown code blocks
            cleaned_text = analysis_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            analysis_result = json.loads(cleaned_text)
            return analysis_result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a basic structure
            return {
                "error": "Failed to parse Gemini response as JSON",
                "raw_response": analysis_text,
                "is_professional": False,
                "is_single_item": False
            }
            
    except Exception as e:
        return {
            "error": f"Error analyzing image: {str(e)}",
            "is_professional": False,
            "is_single_item": False
        }

@app.post("/check-clothing-quality")
async def check_clothing_quality(
    image: UploadFile = File(...)
):
    """
    Check if uploaded image is a professional studio quality photo of a single clothing item
    
    Args:
        image: Single image to analyze
    """
    try:
        # Process uploaded image
        processed_image = process_uploaded_image(image)
        
        # Analyze the image
        analysis_result = check_professional_clothing_image(processed_image)
        
        return {
            "success": True,
            "analysis": analysis_result,
            "filename": image.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error checking image quality: {str(e)}"
        }

def itemize_photo(image: Image.Image) -> List[str]:
    """
    Analyze an image and return a list of clothing items found
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        List[str]: List of clothing items found in the image
    """
    try:
        # Create analysis prompt
        prompt = """
        Analyze this image and identify all the clothing items visible in the photo.
        
        Please respond with a JSON array containing only the clothing items you can clearly identify.
        Use specific, descriptive names for each item (e.g., "blue denim jeans", "white cotton t-shirt", "black leather jacket").
        
        Only include actual clothing items (shirts, pants, dresses, shoes, accessories like belts, hats, etc.).
        Do not include people, backgrounds, or non-clothing objects.
        
        Response format: ["item1", "item2", "item3", ...]
        
        Only respond with the JSON array, no additional text.
        """
        
        # Prepare content for Gemini
        contents = [prompt, image]
        
        # Call Gemini 1.5 Flash for analysis
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        if not analysis_text:
            return []
        
        # Try to parse JSON response
        import json
        try:
            # Clean the response text by removing markdown code blocks
            cleaned_text = analysis_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            clothing_items = json.loads(cleaned_text)
            
            # Ensure we return a list
            if isinstance(clothing_items, list):
                return clothing_items
            else:
                return []
                
        except json.JSONDecodeError:
            # If JSON parsing fails, return empty list
            return []
            
    except Exception as e:
        # Log error and return empty list
        print(f"Error itemizing photo: {str(e)}")
        return []

@app.post("/itemize-clothing")
async def itemize_clothing(
    image: UploadFile = File(...)
):
    """
    Analyze uploaded image and return a list of clothing items found
    
    Args:
        image: Single image to analyze
    """
    try:
        # Process uploaded image
        processed_image = process_uploaded_image(image)
        
        # Get list of clothing items
        clothing_items = itemize_photo(processed_image)
        
        return {
            "success": True,
            "clothing_items": clothing_items,
            "item_count": len(clothing_items),
            "filename": image.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error itemizing clothing: {str(e)}",
            "clothing_items": []
        }

@app.post("/extract-clothes-specific")
async def extract_clothes_specific(
    image: UploadFile = File(...),
    clothing_items: str = Form(...)
):
    """
    Extract specific clothing items from photo and create professional product images
    
    Args:
        image: Single image containing clothing items
        clothing_items: JSON string array of specific clothing items to extract
    """
    try:
        # Process uploaded image
        processed_image = process_uploaded_image(image)
        
        # Parse the clothing items list
        import json
        try:
            items_list = json.loads(clothing_items)
            if not isinstance(items_list, list):
                raise ValueError("clothing_items must be a JSON array")
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid JSON format for clothing_items"
            }
        
        if not items_list:
            return {
                "success": False,
                "error": "No clothing items specified"
            }
        
        extracted_images = []
        
        # Loop through each clothing item and extract it
        for item in items_list:
            try:
                # Create the extraction prompt for specific item
                prompt = f"Take the {item} in this photo and make a full view image of just that item with a white background as a professionally shot image for a clothing item on an online store. Focus only on the {item} and exclude all other clothing items or objects."
                
                # Prepare content for Gemini
                contents = [prompt, processed_image]
                
                # Generate the professional product image
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image-preview",
                    contents=contents
                )
                
                # Process response - check for both generated image and text description
                generated_image_base64 = None
                description_text = None
                
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        description_text = part.text
                    elif part.inline_data is not None:
                        image_data = Image.open(io.BytesIO(part.inline_data.data))
                        generated_image_base64 = image_to_base64(image_data)
                
                # Add to results
                extracted_images.append({
                    "item": item,
                    "success": True,
                    "generated_image_base64": generated_image_base64,
                    "description": description_text if description_text else f"Professional {item} product image generated"
                })
                
            except Exception as item_error:
                # If extraction fails for this item, add error to results
                extracted_images.append({
                    "item": item,
                    "success": False,
                    "error": f"Error extracting {item}: {str(item_error)}",
                    "generated_image_base64": None,
                    "description": None
                })
        
        # Count successful extractions
        successful_extractions = sum(1 for result in extracted_images if result["success"])
        
        return {
            "success": True,
            "extracted_images": extracted_images,
            "total_items": len(items_list),
            "successful_extractions": successful_extractions,
            "filename": image.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting specific clothing items: {str(e)}",
            "extracted_images": []
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)