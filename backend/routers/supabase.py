from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from routers.auth import verify_token, supabase
import models.tops_config as tops_config
import models.bottoms_config as bottoms_config
import models.footwear_config as footwear_config
import models.outerwear_config as outerwear_config
import models.accessories_config as accessories_config
import models.undergarments_config as undergarments_config
import models.dresses_config as dresses_config
import models.sleepwear_config as sleepwear_config

router = APIRouter(prefix="/supabase", tags=["database"])

# Category mapping based on model configs
CATEGORY_CONFIGS = {
    "tops": tops_config,
    "bottoms": bottoms_config,
    "footwear": footwear_config,
    "outerwear": outerwear_config,
    "accessories": accessories_config,
    "undergarments": undergarments_config,
    "dresses": dresses_config,
    "sleepwear": sleepwear_config
}

def categorize_clothing_item(category: str) -> str:
    """
    Categorize a clothing item based on its stored category field.
    Maps database categories to display categories.
    """
    if not category:
        return "other"
    
    category_lower = category.lower()
    
    # Check each config to see if the category matches any clothing types
    for display_category, config in CATEGORY_CONFIGS.items():
        if hasattr(config, 'CLOTHING_TYPES'):
            # Check if the category matches any clothing type in this config
            for clothing_type in config.CLOTHING_TYPES:
                if category_lower == clothing_type.lower() or category_lower in clothing_type.lower():
                    return display_category
    
    # Also check for common category names
    category_mapping = {
        "clothing": "tops",  # Default fallback
        "accessory": "accessories",
        "top": "tops",
        "bottom": "bottoms",
        "shoe": "footwear",
        "shoes": "footwear",
        "jacket": "outerwear",
        "coat": "outerwear",
        "dress": "dresses",
        "underwear": "undergarments",
        "sleepwear": "sleepwear"
    }
    
    return category_mapping.get(category_lower, "other")

class ProfileCreate(BaseModel):
    email: str

class ProfileResponse(BaseModel):
    id: str
    email: str
    created_at: str

class ClothingItem(BaseModel):
    name: str
    category: str
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    size: Optional[str] = None
    image_url: str

class ClothingItemResponse(BaseModel):
    id: str
    profile_id: str
    name: str
    category: str
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    size: Optional[str] = None
    image_url: str
    created_at: str

@router.post("/init-database")
async def initialize_database():
    """Initialize database tables"""
    try:
        # Create profiles table
        profiles_result = supabase.rpc('create_profiles_table').execute()
        
        # Create clothes table
        clothes_result = supabase.rpc('create_clothes_table').execute()
        
        return {"message": "Database initialized successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize database: {str(e)}"
        )

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user_id: str = Depends(verify_token)):
    """Get user profile"""
    try:
        response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        
        if response.data:
            profile = response.data[0]
            return ProfileResponse(**profile)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get profile: {str(e)}"
        )

@router.post("/clothes", response_model=ClothingItemResponse)
async def add_clothing_item(item: ClothingItem, user_id: str = Depends(verify_token)):
    """Add a clothing item"""
    try:
        item_data = {
            "profile_id": user_id,
            "name": item.name,
            "category": item.category,
            "primary_color": item.primary_color,
            "secondary_color": item.secondary_color,
            "size": item.size,
            "image_url": item.image_url
        }
        
        response = supabase.table("clothes").insert(item_data).execute()
        
        if response.data:
            return ClothingItemResponse(**response.data[0])
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add clothing item"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add clothing item: {str(e)}"
        )

@router.get("/clothes", response_model=List[ClothingItemResponse])
async def get_clothing_items(user_id: str = Depends(verify_token)):
    """Get all clothing items for user"""
    try:
        response = supabase.table("clothes").select("*").eq("profile_id", user_id).execute()
        
        return [ClothingItemResponse(**item) for item in response.data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get clothing items: {str(e)}"
        )

@router.get("/clothes/categorized")
async def get_categorized_clothing_items(user_id: str = Depends(verify_token)):
    """Get clothing items organized by category"""
    try:
        response = supabase.table("clothes").select("*").eq("profile_id", user_id).execute()
        
        # Initialize categories
        categorized_items = {
            "accessories": [],
            "bottoms": [],
            "dresses": [],
            "footwear": [],
            "outerwear": [],
            "sleepwear": [],
            "tops": [],
            "undergarments": [],
            "other": []
        }
        
        # Categorize each item
        for item in response.data:
            category = categorize_clothing_item(item.get("category", ""))
            if category not in categorized_items:
                categorized_items["other"].append(item)
            else:
                categorized_items[category].append(item)
        
        return {
            "success": True,
            "categories": categorized_items,
            "total_items": len(response.data)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get categorized clothing items: {str(e)}"
        )

@router.delete("/clothes/{item_id}")
async def delete_clothing_item(item_id: str, user_id: str = Depends(verify_token)):
    """Delete a clothing item"""
    try:
        # First check if the item belongs to the user
        check_response = supabase.table("clothes").select("profile_id").eq("id", item_id).execute()
        
        if not check_response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clothing item not found"
            )
        
        if check_response.data[0]["profile_id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this item"
            )
        
        # Delete the item
        response = supabase.table("clothes").delete().eq("id", item_id).execute()
        
        return {"message": "Clothing item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete clothing item: {str(e)}"
        )