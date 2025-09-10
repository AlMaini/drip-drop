from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException

from services import virtual_tryon_service

router = APIRouter(prefix="/api", tags=["virtual-tryon"])

@router.post("/try-on-clothes")
async def try_on_clothes(
    images: List[UploadFile] = File(...)
):
    """
    Virtual try-on using Gemini AI - make the person wear the provided clothes iteratively
    
    Args:
        images: List of images containing person and clothing items
    """
    try:
        if not images:
            raise HTTPException(status_code=400, detail="At least one image is required")
        
        result = await virtual_tryon_service.perform_iterative_tryon(images)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error generating iterative try-on visualization: {str(e)}"
        }

@router.post("/fit-transfer")
async def fit_transfer(
    clothing_image: UploadFile = File(...),
    person_image: UploadFile = File(...)
):
    """
    Perform virtual try-on by transferring clothing onto a model image
    
    Args:
        clothing_image: Image of the clothing item
        model_image: Image of the model/person
    """
    try:
        result = await virtual_tryon_service.perform_fit_transfer(clothing_image, person_image)
        return {
            "success": True,
            "tryon_image_base64": result["tryon_image_base64"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error performing fit transfer: {str(e)}"
        }