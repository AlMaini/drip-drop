from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
import json

from .auth import verify_token
from services.clothing_service import (
    save_clothing_item_to_db,
    get_user_clothes,
    get_clothing_by_id,
    update_clothing_item,
    delete_clothing_item,
    get_clothes_by_category,
    get_unique_clothing_categories,
    upload_image_to_supabase,
    smart_save_clothing_item
)
from services.image_processing import process_uploaded_image, image_to_base64

router = APIRouter()

@router.post("/clothing")
async def create_clothing_smart(
    name: str = Form(...),
    category: str = Form(...),
    primary_color: Optional[str] = Form(None),
    secondary_color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_owned: bool = Form(True),
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """Create a new clothing item for the current user with smart image processing"""
    try:

        # Use smart creation that checks quality first
        clothing = await smart_save_clothing_item(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            size=size,
            is_owned=is_owned,
            image=image
        )

        return {
            "message": "Clothing item created successfully",
            "clothing": clothing,
            "quality_check_passed": clothing.get("used_original_image", False),
            "extraction_performed": clothing.get("extraction_performed", False)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating clothing item: {str(e)}")

@router.post("/clothing/basic")
async def create_clothing_basic(
    name: str = Form(...),
    category: str = Form(...),
    primary_color: Optional[str] = Form(None),
    secondary_color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_owned: bool = Form(True),
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """Create a new clothing item without smart processing (original method)"""
    try:

        # Process the uploaded image
        processed_image = process_uploaded_image(image)
        image_base64 = image_to_base64(processed_image)

        # Upload image to Supabase storage
        image_url = await upload_image_to_supabase(image_base64, image.filename)

        # Save clothing to database
        clothing = await save_clothing_item_to_db(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            image_url=image_url,
            is_owned=is_owned
        )

        return {
            "message": "Clothing item created successfully",
            "clothing": clothing
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating clothing item: {str(e)}")

@router.get("/clothing")
async def get_clothing(
    owned_only: Optional[bool] = None,
    category: Optional[str] = None,
    user_id: str = Depends(verify_token)
):
    """Get all clothing for the current user"""
    try:

        if category:
            clothing = await get_clothes_by_category(user_id, category, owned_only)
        else:
            clothing = await get_user_clothes(user_id, owned_only)

        return {
            "clothing": clothing,
            "total": len(clothing)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting clothing: {str(e)}")

@router.get("/clothing/categories")
async def get_clothing_categories(user_id: str = Depends(verify_token)):
    """Get unique clothing categories for the current user"""
    try:
        categories = await get_unique_clothing_categories(user_id)

        return {
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories: {str(e)}")

@router.get("/clothing/{clothing_id}")
async def get_clothing_item(
    clothing_id: str,
    user_id: str = Depends(verify_token)
):
    """Get a specific clothing item by ID"""
    try:
        clothing = await get_clothing_by_id(clothing_id, user_id)

        if not clothing:
            raise HTTPException(status_code=404, detail="Clothing item not found")

        return {"clothing": clothing}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting clothing item: {str(e)}")

@router.put("/clothing/{clothing_id}")
async def update_clothing(
    clothing_id: str,
    name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    primary_color: Optional[str] = Form(None),
    secondary_color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_owned: Optional[bool] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Update a clothing item"""
    try:

        # Prepare update data
        updates = {}
        if name is not None:
            updates['name'] = name
        if category is not None:
            updates['category'] = category
        if primary_color is not None:
            updates['primary_color'] = primary_color
        if secondary_color is not None:
            updates['secondary_color'] = secondary_color
        if size is not None:
            updates['size'] = size
        if is_owned is not None:
            updates['is_owned'] = is_owned

        if not updates:
            raise HTTPException(status_code=400, detail="No update data provided")

        updated_clothing = await update_clothing_item(clothing_id, user_id, **updates)

        return {
            "message": "Clothing item updated successfully",
            "clothing": updated_clothing
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating clothing item: {str(e)}")

@router.delete("/clothing/{clothing_id}")
async def delete_clothing(
    clothing_id: str,
    user_id: str = Depends(verify_token)
):
    """Delete a clothing item"""
    try:
        success = await delete_clothing_item(clothing_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Clothing item not found or could not be deleted")

        return {"message": "Clothing item deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting clothing item: {str(e)}")

@router.patch("/clothing/{clothing_id}/ownership")
async def toggle_clothing_ownership(
    clothing_id: str,
    is_owned: bool = Form(...),
    user_id: str = Depends(verify_token)
):
    """Toggle ownership status of a clothing item"""
    try:
        updated_clothing = await update_clothing_item(clothing_id, user_id, is_owned=is_owned)

        return {
            "message": f"Clothing ownership {'enabled' if is_owned else 'disabled'}",
            "clothing": updated_clothing
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ownership: {str(e)}")

@router.get("/clothing/stats/summary")
async def get_clothing_summary(user_id: str = Depends(verify_token)):
    """Get summary statistics about user's clothing"""
    try:

        # Get all clothing
        all_clothing = await get_user_clothes(user_id)
        owned_clothing = await get_user_clothes(user_id, owned_only=True)
        categories = await get_unique_clothing_categories(user_id)

        return {
            "total_clothing": len(all_clothing),
            "owned_clothing": len(owned_clothing),
            "wishlist_clothing": len(all_clothing) - len(owned_clothing),
            "total_categories": len(categories),
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting clothing summary: {str(e)}")