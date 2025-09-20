import json
from typing import List, Dict, Any, Optional
from .authService import get_supabase_client

async def create_outfit(user_id: str, name: str, description: str = None) -> Dict[str, Any]:
    """Create a new outfit for a user"""
    try:
        supabase = get_supabase_client()

        outfit_data = {
            "profile_id": user_id,
            "name": name,
            "description": description
        }

        result = supabase.table("outfits").insert(outfit_data).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception(f"Database insert failed: {result}")

    except Exception as e:
        print(f"Error creating outfit: {e}")
        raise e

async def get_user_outfits(user_id: str) -> List[Dict[str, Any]]:
    """Get all outfits for a user with their items"""
    try:
        supabase = get_supabase_client()

        # Get outfits
        outfits_result = supabase.table("outfits").select("*").eq("profile_id", user_id).order("created_at", desc=True).execute()

        if not outfits_result.data:
            return []

        outfits = []
        for outfit in outfits_result.data:
            # Get outfit items for each outfit
            outfit_items = await get_outfit_items_with_details(outfit['id'])
            outfit['items'] = outfit_items
            outfits.append(outfit)

        return outfits

    except Exception as e:
        print(f"Error getting user outfits: {e}")
        return []

async def get_outfit_by_id(outfit_id: str, user_id: str = None) -> Dict[str, Any]:
    """Get a specific outfit by ID with its items"""
    try:
        supabase = get_supabase_client()

        query = supabase.table("outfits").select("*").eq("id", outfit_id)

        if user_id:
            query = query.eq("profile_id", user_id)

        result = query.limit(1).execute()

        if result.data and len(result.data) > 0:
            outfit = result.data[0]
            # Get outfit items
            outfit['items'] = await get_outfit_items_with_details(outfit_id)
            return outfit
        else:
            return None

    except Exception as e:
        print(f"Error getting outfit by ID: {e}")
        return None

async def update_outfit(outfit_id: str, user_id: str, **updates) -> Dict[str, Any]:
    """Update an outfit"""
    try:
        supabase = get_supabase_client()

        # Filter out None values and ensure we only update allowed fields
        allowed_fields = ['name', 'description']
        update_data = {k: v for k, v in updates.items() if v is not None and k in allowed_fields}

        if not update_data:
            raise ValueError("No valid update data provided")

        result = supabase.table("outfits").update(update_data).eq("id", outfit_id).eq("profile_id", user_id).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception(f"Database update failed: {result}")

    except Exception as e:
        print(f"Error updating outfit: {e}")
        raise e

async def delete_outfit(outfit_id: str, user_id: str) -> bool:
    """Delete an outfit and all its items"""
    try:
        supabase = get_supabase_client()

        # Delete the outfit (outfit_items will be deleted automatically due to CASCADE)
        result = supabase.table("outfits").delete().eq("id", outfit_id).eq("profile_id", user_id).execute()

        return len(result.data) > 0 if result.data else False

    except Exception as e:
        print(f"Error deleting outfit: {e}")
        return False

async def add_item_to_outfit(outfit_id: str, item_id: str, item_type: str, user_id: str = None) -> Dict[str, Any]:
    """Add a clothing item or accessory to an outfit"""
    try:
        if item_type not in ['clothing', 'accessory']:
            raise ValueError("item_type must be 'clothing' or 'accessory'")

        supabase = get_supabase_client()

        # If user_id is provided, verify the outfit belongs to the user
        if user_id:
            outfit = await get_outfit_by_id(outfit_id, user_id)
            if not outfit:
                raise Exception("Outfit not found or access denied")

        # Check if item is already in the outfit
        existing_result = supabase.table("outfit_items").select("*").eq("outfit_id", outfit_id).eq("item_id", item_id).eq("item_type", item_type).execute()

        if existing_result.data:
            raise Exception("Item already in outfit")

        # Add item to outfit
        outfit_item_data = {
            "outfit_id": outfit_id,
            "item_id": item_id,
            "item_type": item_type
        }

        result = supabase.table("outfit_items").insert(outfit_item_data).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception(f"Database insert failed: {result}")

    except Exception as e:
        print(f"Error adding item to outfit: {e}")
        raise e

async def remove_item_from_outfit(outfit_id: str, item_id: str, item_type: str, user_id: str = None) -> bool:
    """Remove an item from an outfit"""
    try:
        supabase = get_supabase_client()

        # If user_id is provided, verify the outfit belongs to the user
        if user_id:
            outfit = await get_outfit_by_id(outfit_id, user_id)
            if not outfit:
                return False

        result = supabase.table("outfit_items").delete().eq("outfit_id", outfit_id).eq("item_id", item_id).eq("item_type", item_type).execute()

        return len(result.data) > 0 if result.data else False

    except Exception as e:
        print(f"Error removing item from outfit: {e}")
        return False

async def get_outfit_items_with_details(outfit_id: str) -> List[Dict[str, Any]]:
    """Get all items in an outfit with their full details"""
    try:
        supabase = get_supabase_client()

        # Get outfit items
        outfit_items_result = supabase.table("outfit_items").select("*").eq("outfit_id", outfit_id).execute()

        if not outfit_items_result.data:
            return []

        items_with_details = []

        for outfit_item in outfit_items_result.data:
            item_id = outfit_item['item_id']
            item_type = outfit_item['item_type']

            # Fetch full item details from appropriate table
            if item_type == 'clothing':
                item_result = supabase.table("clothes").select("*").eq("id", item_id).execute()
            elif item_type == 'accessory':
                item_result = supabase.table("accessories").select("*").eq("id", item_id).execute()
            else:
                continue

            if item_result.data and len(item_result.data) > 0:
                item_details = item_result.data[0]
                item_details['item_type'] = item_type
                item_details['outfit_item_id'] = outfit_item['id']
                items_with_details.append(item_details)

        return items_with_details

    except Exception as e:
        print(f"Error getting outfit items with details: {e}")
        return []

async def get_outfits_containing_item(user_id: str, item_id: str, item_type: str) -> List[Dict[str, Any]]:
    """Get all outfits that contain a specific item"""
    try:
        supabase = get_supabase_client()

        # Get outfit_items that match the item
        outfit_items_result = supabase.table("outfit_items").select("outfit_id").eq("item_id", item_id).eq("item_type", item_type).execute()

        if not outfit_items_result.data:
            return []

        outfit_ids = [item['outfit_id'] for item in outfit_items_result.data]

        # Get the outfits that belong to the user
        outfits_result = supabase.table("outfits").select("*").eq("profile_id", user_id).in_("id", outfit_ids).execute()

        return outfits_result.data if outfits_result.data else []

    except Exception as e:
        print(f"Error getting outfits containing item: {e}")
        return []

async def duplicate_outfit(outfit_id: str, user_id: str, new_name: str = None) -> Dict[str, Any]:
    """Create a duplicate of an existing outfit"""
    try:
        # Get the original outfit
        original_outfit = await get_outfit_by_id(outfit_id, user_id)
        if not original_outfit:
            raise Exception("Outfit not found or access denied")

        # Create new outfit
        duplicate_name = new_name or f"{original_outfit['name']} (Copy)"
        new_outfit = await create_outfit(user_id, duplicate_name, original_outfit.get('description'))

        # Copy all items to the new outfit
        for item in original_outfit.get('items', []):
            await add_item_to_outfit(new_outfit['id'], item['id'], item['item_type'], user_id)

        # Return the new outfit with items
        return await get_outfit_by_id(new_outfit['id'], user_id)

    except Exception as e:
        print(f"Error duplicating outfit: {e}")
        raise e

async def get_outfit_statistics(user_id: str) -> Dict[str, Any]:
    """Get statistics about user's outfits"""
    try:
        supabase = get_supabase_client()

        # Get total outfits count
        outfits_result = supabase.table("outfits").select("id", count="exact").eq("profile_id", user_id).execute()
        total_outfits = outfits_result.count or 0

        # Get outfit items count
        outfit_items_result = supabase.rpc('get_outfit_items_count_by_user', {'user_id': user_id}).execute()

        # If the RPC doesn't exist, calculate manually
        if not outfit_items_result.data:
            # Get all user outfits
            user_outfits = supabase.table("outfits").select("id").eq("profile_id", user_id).execute()
            if user_outfits.data:
                outfit_ids = [outfit['id'] for outfit in user_outfits.data]
                items_result = supabase.table("outfit_items").select("item_type", count="exact").in_("outfit_id", outfit_ids).execute()
                total_items = items_result.count or 0
            else:
                total_items = 0
        else:
            total_items = outfit_items_result.data[0].get('total_items', 0) if outfit_items_result.data else 0

        return {
            "total_outfits": total_outfits,
            "total_items_in_outfits": total_items,
            "average_items_per_outfit": round(total_items / total_outfits, 2) if total_outfits > 0 else 0
        }

    except Exception as e:
        print(f"Error getting outfit statistics: {e}")
        return {
            "total_outfits": 0,
            "total_items_in_outfits": 0,
            "average_items_per_outfit": 0
        }

async def search_outfits(user_id: str, query: str) -> List[Dict[str, Any]]:
    """Search outfits by name or description"""
    try:
        supabase = get_supabase_client()

        # Search in outfit names and descriptions
        result = supabase.table("outfits").select("*").eq("profile_id", user_id).or_(f"name.ilike.%{query}%,description.ilike.%{query}%").execute()

        if not result.data:
            return []

        outfits = []
        for outfit in result.data:
            # Get outfit items for each matching outfit
            outfit_items = await get_outfit_items_with_details(outfit['id'])
            outfit['items'] = outfit_items
            outfits.append(outfit)

        return outfits

    except Exception as e:
        print(f"Error searching outfits: {e}")
        return []