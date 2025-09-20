from fastapi import APIRouter, HTTPException, Depends, Form
from typing import List, Optional
import json

from .auth import verify_token
from services.outfit_service import (
    create_outfit,
    get_user_outfits,
    get_outfit_by_id,
    update_outfit,
    delete_outfit,
    add_item_to_outfit,
    remove_item_from_outfit,
    duplicate_outfit,
    get_outfit_statistics,
    search_outfits,
    get_outfits_containing_item
)

router = APIRouter()

@router.post("/outfits")
async def create_outfit_endpoint(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Create a new outfit for the current user"""
    try:
        outfit = await create_outfit(user_id, name, description)

        return {
            "message": "Outfit created successfully",
            "outfit": outfit
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating outfit: {str(e)}")

@router.get("/outfits")
async def get_outfits(
    search: Optional[str] = None,
    user_id: str = Depends(verify_token)
):
    """Get all outfits for the current user"""
    try:

        if search:
            outfits = await search_outfits(user_id, search)
        else:
            outfits = await get_user_outfits(user_id)

        return {
            "outfits": outfits,
            "total": len(outfits)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting outfits: {str(e)}")

@router.get("/outfits/stats")
async def get_outfits_statistics(user_id: str = Depends(verify_token)):
    """Get statistics about user's outfits"""
    try:
        stats = await get_outfit_statistics(user_id)

        return {"statistics": stats}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting outfit statistics: {str(e)}")

@router.get("/outfits/{outfit_id}")
async def get_outfit(
    outfit_id: str,
    user_id: str = Depends(verify_token)
):
    """Get a specific outfit by ID"""
    try:
        outfit = await get_outfit_by_id(outfit_id, user_id)

        if not outfit:
            raise HTTPException(status_code=404, detail="Outfit not found")

        return {"outfit": outfit}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting outfit: {str(e)}")

@router.put("/outfits/{outfit_id}")
async def update_outfit_endpoint(
    outfit_id: str,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Update an outfit"""
    try:

        # Prepare update data
        updates = {}
        if name is not None:
            updates['name'] = name
        if description is not None:
            updates['description'] = description

        if not updates:
            raise HTTPException(status_code=400, detail="No update data provided")

        updated_outfit = await update_outfit(outfit_id, user_id, **updates)

        return {
            "message": "Outfit updated successfully",
            "outfit": updated_outfit
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating outfit: {str(e)}")

@router.delete("/outfits/{outfit_id}")
async def delete_outfit_endpoint(
    outfit_id: str,
    user_id: str = Depends(verify_token)
):
    """Delete an outfit"""
    try:
        success = await delete_outfit(outfit_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Outfit not found or could not be deleted")

        return {"message": "Outfit deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting outfit: {str(e)}")

@router.post("/outfits/{outfit_id}/items")
async def add_item_to_outfit_endpoint(
    outfit_id: str,
    item_id: str = Form(...),
    item_type: str = Form(...),
    user_id: str = Depends(verify_token)
):
    """Add an item (clothing or accessory) to an outfit"""
    try:

        if item_type not in ['clothing', 'accessory']:
            raise HTTPException(status_code=400, detail="item_type must be 'clothing' or 'accessory'")

        outfit_item = await add_item_to_outfit(outfit_id, item_id, item_type, user_id)

        return {
            "message": f"{item_type.title()} item added to outfit successfully",
            "outfit_item": outfit_item
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding item to outfit: {str(e)}")

@router.delete("/outfits/{outfit_id}/items")
async def remove_item_from_outfit_endpoint(
    outfit_id: str,
    item_id: str = Form(...),
    item_type: str = Form(...),
    user_id: str = Depends(verify_token)
):
    """Remove an item from an outfit"""
    try:

        if item_type not in ['clothing', 'accessory']:
            raise HTTPException(status_code=400, detail="item_type must be 'clothing' or 'accessory'")

        success = await remove_item_from_outfit(outfit_id, item_id, item_type, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Item not found in outfit or could not be removed")

        return {"message": f"{item_type.title()} item removed from outfit successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing item from outfit: {str(e)}")

@router.post("/outfits/{outfit_id}/duplicate")
async def duplicate_outfit_endpoint(
    outfit_id: str,
    new_name: Optional[str] = Form(None),
    user_id: str = Depends(verify_token)
):
    """Create a duplicate of an existing outfit"""
    try:
        duplicated_outfit = await duplicate_outfit(outfit_id, user_id, new_name)

        return {
            "message": "Outfit duplicated successfully",
            "outfit": duplicated_outfit
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error duplicating outfit: {str(e)}")

@router.get("/outfits/containing/{item_type}/{item_id}")
async def get_outfits_with_item(
    item_type: str,
    item_id: str,
    user_id: str = Depends(verify_token)
):
    """Get all outfits that contain a specific item"""
    try:
        if item_type not in ['clothing', 'accessory']:
            raise HTTPException(status_code=400, detail="item_type must be 'clothing' or 'accessory'")

        outfits = await get_outfits_containing_item(user_id, item_id, item_type)

        return {
            "outfits": outfits,
            "total": len(outfits)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting outfits containing item: {str(e)}")

@router.post("/outfits/bulk-create")
async def bulk_create_outfits_from_items(
    outfit_data: str = Form(...),  # JSON string with outfit definitions
    user_id: str = Depends(verify_token)
):
    """Create multiple outfits from a batch of items"""
    try:

        # Parse outfit data
        try:
            outfits_data = json.loads(outfit_data)
            if not isinstance(outfits_data, list):
                raise ValueError("outfit_data must be a JSON array")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for outfit_data")

        created_outfits = []
        errors = []

        for outfit_info in outfits_data:
            try:
                # Create outfit
                outfit_name = outfit_info.get('name')
                outfit_description = outfit_info.get('description')
                items = outfit_info.get('items', [])

                if not outfit_name:
                    errors.append({"outfit": outfit_info, "error": "Name is required"})
                    continue

                # Create the outfit
                new_outfit = await create_outfit(user_id, outfit_name, outfit_description)

                # Add items to outfit
                items_added = 0
                for item in items:
                    item_id = item.get('id')
                    item_type = item.get('type')

                    if item_id and item_type and item_type in ['clothing', 'accessory']:
                        try:
                            await add_item_to_outfit(new_outfit['id'], item_id, item_type, user_id)
                            items_added += 1
                        except Exception as item_error:
                            # Continue adding other items even if one fails
                            print(f"Error adding item {item_id} to outfit: {item_error}")

                # Get the complete outfit with items
                complete_outfit = await get_outfit_by_id(new_outfit['id'], user_id)
                complete_outfit['items_added'] = items_added
                created_outfits.append(complete_outfit)

            except Exception as outfit_error:
                errors.append({"outfit": outfit_info, "error": str(outfit_error)})

        return {
            "message": f"Bulk outfit creation completed",
            "created_outfits": created_outfits,
            "total_created": len(created_outfits),
            "errors": errors,
            "total_errors": len(errors)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in bulk outfit creation: {str(e)}")

@router.get("/outfits/{outfit_id}/share")
async def get_outfit_share_data(
    outfit_id: str,
    user_id: str = Depends(verify_token)
):
    """Get outfit data formatted for sharing"""
    try:
        outfit = await get_outfit_by_id(outfit_id, user_id)

        if not outfit:
            raise HTTPException(status_code=404, detail="Outfit not found")

        # Format data for sharing (remove sensitive information)
        share_data = {
            "name": outfit.get('name'),
            "description": outfit.get('description'),
            "items": []
        }

        for item in outfit.get('items', []):
            share_item = {
                "name": item.get('name'),
                "category": item.get('category'),
                "primary_color": item.get('primary_color'),
                "secondary_color": item.get('secondary_color'),
                "type": item.get('item_type'),
                "image_url": item.get('image_url')
            }
            share_data["items"].append(share_item)

        return {
            "share_data": share_data,
            "total_items": len(share_data["items"])
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting outfit share data: {str(e)}")