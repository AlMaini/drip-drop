from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from routers.auth import verify_token, supabase

router = APIRouter(prefix="/supabase", tags=["database"])

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