from typing import List
from fastapi import APIRouter, File, UploadFile, Form

from services import clothing_service

router = APIRouter(prefix="/api", tags=["clothing-analysis"])

@router.post("/extract-clothing")
async def extract_clothing(
    image: UploadFile = File(...)
):
    """
    Extract clothing item from photo and create professional product image
    
    Args:
        image: Single image containing a clothing item
    """
    try:
        result = await clothing_service.extract_single_clothing_item(image)
        return {
            "success": True,
            "generated_image_base64": result["generated_image_base64"],
            "description": result["description"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting clothing item: {str(e)}"
        }

@router.post("/check-clothing-quality")
async def check_clothing_quality(
    image: UploadFile = File(...)
):
    """
    Check if uploaded image is a professional studio quality photo of a single clothing item
    
    Args:
        image: Single image to analyze
    """
    try:
        analysis_result = await clothing_service.analyze_clothing_quality(image)
        
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

@router.post("/itemize-clothing")
async def itemize_clothing(
    image: UploadFile = File(...)
):
    """
    Analyze uploaded image and return a list of clothing items found
    
    Args:
        image: Single image to analyze
    """
    try:
        outfit_items = await clothing_service.identify_clothing_items(image)
        
        return {
            "success": True,
            "clothing_items": outfit_items["clothing_items"],
            "accessories": outfit_items["accessories"],
            "item_count": len(outfit_items["clothing_items"]) + len(outfit_items["accessories"]),
            "filename": image.filename
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error itemizing clothing: {str(e)}",
            "clothing_items": [],
            "accessories": []
        }

@router.post("/extract-clothes-specific")
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
        result = await clothing_service.extract_specific_clothing_items(image, clothing_items)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error extracting specific clothing items: {str(e)}",
            "extracted_images": []
        }

@router.post("/extract-clothes-batch")
async def extract_clothes_batch(
    image: UploadFile = File(...),
    clothing_items: str = Form(...)
):
    """
    Extract specific clothing items using batch mode for efficiency
    
    Args:
        image: Single image containing clothing items
        clothing_items: JSON string array of specific clothing items to extract
    """
    try:
        result = await clothing_service.extract_specific_clothing_items_batch(image, clothing_items)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error in batch extraction: {str(e)}",
            "extracted_images": []
        }

@router.post("/extract-clothes-batch-file")
async def extract_clothes_batch_file(
    image: UploadFile = File(...),
    clothing_items: str = Form(...)
):
    """
    Extract specific clothing items using file-based batch mode for large requests
    
    Args:
        image: Single image containing clothing items
        clothing_items: JSON string array of specific clothing items to extract
    """
    try:
        result = await clothing_service.extract_specific_clothing_items_batch_file(image, clothing_items)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error in file-based batch extraction: {str(e)}",
            "batch_job_id": None
        }

@router.get("/batch-status/{batch_job_id}")
async def get_batch_status(batch_job_id: str):
    """
    Check the status of a batch job and retrieve results if completed
    
    Args:
        batch_job_id: The ID of the batch job to check
    """
    try:
        result = clothing_service.check_batch_status(batch_job_id)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "error": f"Error checking batch status: {str(e)}"
        }