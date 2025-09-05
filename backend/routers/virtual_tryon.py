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