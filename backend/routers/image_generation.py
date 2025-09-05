from typing import Optional, List
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services import image_service

router = APIRouter(prefix="/api", tags=["image-generation"])

class ImageGenerationResponse(BaseModel):
    success: bool
    image_url: Optional[str] = None
    generated_image_base64: Optional[str] = None
    error: Optional[str] = None

@router.post("/generate-image", response_model=ImageGenerationResponse)
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
        result = await image_service.generate_image_with_context(
            prompt=prompt,
            style=style,
            context_description=context_description,
            context_images=context_images
        )
        
        return ImageGenerationResponse(
            success=True,
            image_url=None,
            generated_image_base64=result["generated_image_base64"],
            error=None
        )
        
    except Exception as e:
        return ImageGenerationResponse(
            success=False,
            error=f"Error generating image: {str(e)}"
        )