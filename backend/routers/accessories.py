from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
import json

from .auth import verify_token
from services.accessory_service import (
    save_accessory_item_to_db,
    get_user_accessories,
    get_accessory_by_id,
    update_accessory_item,
    delete_accessory_item,
    get_accessories_by_category,
    get_unique_accessory_categories,
    upload_accessory_image_to_supabase,
    smart_save_accessory_item
)
from services.image_processing import process_uploaded_image, image_to_base64

router = APIRouter()

@router.post("/accessories")
async def create_accessory_smart(
    name: str = Form(...),
    category: str = Form(...),
    primary_color: Optional[str] = Form(None),
    secondary_color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_owned: bool = Form(True),
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """Create a new accessory item for the current user with smart image processing"""
    try:

        # Use smart creation that checks quality first
        accessory = await smart_save_accessory_item(
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
            "message": "Accessory created successfully",
            "accessory": accessory,
            "quality_check_passed": accessory.get("used_original_image", False),
            "extraction_performed": accessory.get("extraction_performed", False)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating accessory: {str(e)}")

@router.post("/accessories/basic")
async def create_accessory_basic(
    name: str = Form(...),
    category: str = Form(...),
    primary_color: Optional[str] = Form(None),
    secondary_color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_owned: bool = Form(True),
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """Create a new accessory item without smart processing (original method)"""
    try:

        # Process the uploaded image
        processed_image = process_uploaded_image(image)
        image_base64 = image_to_base64(processed_image)

        # Upload image to Supabase storage
        image_url = await upload_accessory_image_to_supabase(image_base64, image.filename)

        # Save accessory to database
        accessory = await save_accessory_item_to_db(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            size=size,
            image_url=image_url,
            is_owned=is_owned
        )

        return {
            "message": "Accessory created successfully",
            "accessory": accessory
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating accessory: {str(e)}")

@router.get("/accessories")
async def get_accessories(
    owned_only: Optional[bool] = None,
    category: Optional[str] = None,
    user_id: str = Depends(verify_token)
):
    """Get all accessories for the current user"""
    try:

        if category:
            accessories = await get_accessories_by_category(user_id, category, owned_only)
        else:
            accessories = await get_user_accessories(user_id, owned_only)

        return {
            "accessories": accessories,
            "total": len(accessories)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting accessories: {str(e)}")

@router.get("/accessories/categories")
async def get_accessory_categories(user_id: str = Depends(verify_token)):
    """Get unique accessory categories for the current user"""
    try:
        categories = await get_unique_accessory_categories(user_id)

        return {
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categories: {str(e)}")

@router.get("/accessories/{accessory_id}")
async def get_accessory(
    accessory_id: str,
    user_id: str = Depends(verify_token)
):
    """Get a specific accessory by ID"""
    try:
        accessory = await get_accessory_by_id(accessory_id, user_id)

        if not accessory:
            raise HTTPException(status_code=404, detail="Accessory not found")

        return {"accessory": accessory}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting accessory: {str(e)}")

@router.put("/accessories/{accessory_id}")
async def update_accessory(
    accessory_id: str,
    name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    primary_color: Optional[str] = Form(None),
    secondary_color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_owned: Optional[bool] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Update an accessory item"""
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

        updated_accessory = await update_accessory_item(accessory_id, user_id, **updates)

        return {
            "message": "Accessory updated successfully",
            "accessory": updated_accessory
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating accessory: {str(e)}")

@router.delete("/accessories/{accessory_id}")
async def delete_accessory(
    accessory_id: str,
    user_id: str = Depends(verify_token)
):
    """Delete an accessory item"""
    try:
        success = await delete_accessory_item(accessory_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Accessory not found or could not be deleted")

        return {"message": "Accessory deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting accessory: {str(e)}")

@router.patch("/accessories/{accessory_id}/ownership")
async def toggle_accessory_ownership(
    accessory_id: str,
    is_owned: bool = Form(...),
    user_id: str = Depends(verify_token)
):
    """Toggle ownership status of an accessory"""
    try:
        updated_accessory = await update_accessory_item(accessory_id, user_id, is_owned=is_owned)

        return {
            "message": f"Accessory ownership {'enabled' if is_owned else 'disabled'}",
            "accessory": updated_accessory
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ownership: {str(e)}")

@router.get("/accessories/stats/summary")
async def get_accessories_summary(user_id: str = Depends(verify_token)):
    """Get summary statistics about user's accessories"""
    try:

        # Get all accessories
        all_accessories = await get_user_accessories(user_id)
        owned_accessories = await get_user_accessories(user_id, owned_only=True)
        categories = await get_unique_accessory_categories(user_id)

        return {
            "total_accessories": len(all_accessories),
            "owned_accessories": len(owned_accessories),
            "wishlist_accessories": len(all_accessories) - len(owned_accessories),
            "total_categories": len(categories),
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting accessories summary: {str(e)}")