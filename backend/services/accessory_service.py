import io
import json
import time
import base64
import os
import asyncio
from typing import List, Dict, Any
from fastapi import UploadFile
from PIL import Image

from .authService import get_supabase_client
from .image_processing import image_to_base64

async def upload_accessory_image_to_supabase(image_base64: str, filename: str) -> str:
    """Upload base64 accessory image to Supabase storage and return public URL"""
    try:
        supabase = get_supabase_client()

        # Convert base64 to bytes
        image_bytes = base64.b64decode(image_base64)

        # Create unique filename
        unique_filename = f'accessories/{int(time.time())}-{filename}'
        print(f"Uploading accessory image: {unique_filename}, size: {len(image_bytes)} bytes")

        # Upload to Supabase storage
        result = supabase.storage.from_('clothing-items').upload(
            unique_filename,
            image_bytes,
            file_options={'content-type': 'image/png'}
        )

        print(f"Upload result: {result}")

        if result and hasattr(result, 'path'):
            # Get public URL using the path from the upload response
            public_url = supabase.storage.from_('clothing-items').get_public_url(result.path)
            print(f"Generated public URL: {public_url}")
            return public_url
        else:
            raise Exception(f"Upload failed: {result}")

    except Exception as e:
        print(f"Error uploading accessory image to Supabase: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise e

async def save_accessory_item_to_db(user_id: str, name: str, category: str,
                                  primary_color: str = None, secondary_color: str = None,
                                  size: str = None, image_url: str = None,
                                  is_owned: bool = True) -> Dict[str, Any]:
    """Save accessory item to Supabase database"""
    try:
        supabase = get_supabase_client()

        item_data = {
            "profile_id": user_id,
            "name": name,
            "category": category,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "size": size,
            "image_url": image_url,
            "is_owned": is_owned
        }

        result = supabase.table("accessories").insert(item_data).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception(f"Database insert failed: {result}")

    except Exception as e:
        print(f"Error saving accessory item to database: {e}")
        raise e

async def update_accessory_item_image_url(item_id: str, image_url: str) -> Dict[str, Any]:
    """Update the image URL for an accessory item in the database"""
    try:
        supabase = get_supabase_client()

        result = supabase.table("accessories").update({
            "image_url": image_url
        }).eq("id", item_id).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception(f"Database update failed: {result}")

    except Exception as e:
        print(f"Error updating accessory item image URL: {e}")
        raise e

async def find_accessory_item_by_name_and_user(user_id: str, name: str) -> Dict[str, Any]:
    """Find an accessory item by name and user ID"""
    try:
        supabase = get_supabase_client()

        result = supabase.table("accessories").select("*").eq("profile_id", user_id).eq("name", name).limit(1).execute()

        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            return None

    except Exception as e:
        print(f"Error finding accessory item: {e}")
        return None

async def get_user_accessories(user_id: str, owned_only: bool = None) -> List[Dict[str, Any]]:
    """Get all accessory items for a user, optionally filtered by ownership"""
    try:
        supabase = get_supabase_client()

        query = supabase.table("accessories").select("*").eq("profile_id", user_id)

        if owned_only is not None:
            query = query.eq("is_owned", owned_only)

        result = query.order("created_at", desc=True).execute()

        return result.data if result.data else []

    except Exception as e:
        print(f"Error getting user accessories: {e}")
        return []

async def smart_save_accessory_item(user_id: str, name: str, category: str,
                                   primary_color: str = None, secondary_color: str = None,
                                   size: str = None, is_owned: bool = True,
                                   image: UploadFile = None) -> Dict[str, Any]:
    """
    Smart accessory item creation that checks quality first and extracts if needed

    This function:
    1. Checks if the image is already professional quality
    2. If quality check passes, uses the original image
    3. If quality check fails, extracts the accessory item to create professional image
    4. Saves the accessory item to database with the best available image
    """
    try:
        if not image:
            raise ValueError("Image is required for accessory item creation")

        # Import clothing service functions for image processing
        from .clothing_service import (
            process_uploaded_image,
            check_professional_clothing_image,
            image_to_base64,
            extract_single_clothing_item
        )

        # Step 1: Check image quality
        print(f"Checking image quality for accessory item: {name}")
        processed_image = process_uploaded_image(image)
        quality_analysis = check_professional_clothing_image(processed_image)

        use_original_image = quality_analysis.get("passed", False)
        print(f"Quality check result - passed: {use_original_image}")

        if use_original_image:
            # Use original image since it passed quality check
            print("Using original image (quality check passed)")
            image_base64 = image_to_base64(processed_image)

        else:
            # Extract accessory item to create professional image
            print("Extracting accessory item (quality check failed)")

            # Reset image file pointer
            await image.seek(0)

            # Extract single clothing/accessory item (same function works for accessories)
            extraction_result = await extract_single_clothing_item(image)

            if not extraction_result.get("generated_image_base64"):
                # Fallback to original image if extraction fails
                print("Extraction failed, falling back to original image")
                await image.seek(0)
                processed_image = process_uploaded_image(image)
                image_base64 = image_to_base64(processed_image)
            else:
                print("Successfully extracted accessory item")
                image_base64 = extraction_result["generated_image_base64"]

        # Step 2: Upload image to Supabase storage
        filename = f"accessory-{name.replace(' ', '-').lower()}-{int(time.time())}.png"
        image_url = await upload_accessory_image_to_supabase(image_base64, filename)
        print(f"Accessory image uploaded successfully: {image_url}")

        # Step 3: Save to database
        saved_item = await save_accessory_item_to_db(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            size=size,
            image_url=image_url,
            is_owned=is_owned
        )

        # Add metadata about the process
        saved_item["quality_analysis"] = quality_analysis
        saved_item["used_original_image"] = use_original_image
        saved_item["extraction_performed"] = not use_original_image

        return saved_item

    except Exception as e:
        print(f"Error in smart accessory item creation: {e}")
        raise e

async def get_accessory_by_id(accessory_id: str, user_id: str = None) -> Dict[str, Any]:
    """Get a specific accessory item by ID"""
    try:
        supabase = get_supabase_client()

        query = supabase.table("accessories").select("*").eq("id", accessory_id)

        if user_id:
            query = query.eq("profile_id", user_id)

        result = query.limit(1).execute()

        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            return None

    except Exception as e:
        print(f"Error getting accessory by ID: {e}")
        return None

async def update_accessory_item(item_id: str, user_id: str, **updates) -> Dict[str, Any]:
    """Update an accessory item"""
    try:
        supabase = get_supabase_client()

        # Filter out None values and ensure we only update allowed fields
        allowed_fields = ['name', 'category', 'primary_color', 'secondary_color', 'size', 'is_owned']
        update_data = {k: v for k, v in updates.items() if v is not None and k in allowed_fields}

        if not update_data:
            raise ValueError("No valid update data provided")

        result = supabase.table("accessories").update(update_data).eq("id", item_id).eq("profile_id", user_id).execute()

        if result.data:
            return result.data[0]
        else:
            raise Exception(f"Database update failed: {result}")

    except Exception as e:
        print(f"Error updating accessory item: {e}")
        raise e

async def delete_accessory_item(item_id: str, user_id: str) -> bool:
    """Delete an accessory item"""
    try:
        supabase = get_supabase_client()

        result = supabase.table("accessories").delete().eq("id", item_id).eq("profile_id", user_id).execute()

        return len(result.data) > 0 if result.data else False

    except Exception as e:
        print(f"Error deleting accessory item: {e}")
        return False

async def get_accessories_by_category(user_id: str, category: str, owned_only: bool = None) -> List[Dict[str, Any]]:
    """Get accessory items by category for a user"""
    try:
        supabase = get_supabase_client()

        query = supabase.table("accessories").select("*").eq("profile_id", user_id).eq("category", category)

        if owned_only is not None:
            query = query.eq("is_owned", owned_only)

        result = query.order("created_at", desc=True).execute()

        return result.data if result.data else []

    except Exception as e:
        print(f"Error getting accessories by category: {e}")
        return []

async def smart_save_accessory_item(user_id: str, name: str, category: str,
                                   primary_color: str = None, secondary_color: str = None,
                                   size: str = None, is_owned: bool = True,
                                   image: UploadFile = None) -> Dict[str, Any]:
    """
    Smart accessory item creation that checks quality first and extracts if needed

    This function:
    1. Checks if the image is already professional quality
    2. If quality check passes, uses the original image
    3. If quality check fails, extracts the accessory item to create professional image
    4. Saves the accessory item to database with the best available image
    """
    try:
        if not image:
            raise ValueError("Image is required for accessory item creation")

        # Import clothing service functions for image processing
        from .clothing_service import (
            process_uploaded_image,
            check_professional_clothing_image,
            image_to_base64,
            extract_single_clothing_item
        )

        # Step 1: Check image quality
        print(f"Checking image quality for accessory item: {name}")
        processed_image = process_uploaded_image(image)
        quality_analysis = check_professional_clothing_image(processed_image)

        use_original_image = quality_analysis.get("passed", False)
        print(f"Quality check result - passed: {use_original_image}")

        if use_original_image:
            # Use original image since it passed quality check
            print("Using original image (quality check passed)")
            image_base64 = image_to_base64(processed_image)

        else:
            # Extract accessory item to create professional image
            print("Extracting accessory item (quality check failed)")

            # Reset image file pointer
            await image.seek(0)

            # Extract single clothing/accessory item (same function works for accessories)
            extraction_result = await extract_single_clothing_item(image)

            if not extraction_result.get("generated_image_base64"):
                # Fallback to original image if extraction fails
                print("Extraction failed, falling back to original image")
                await image.seek(0)
                processed_image = process_uploaded_image(image)
                image_base64 = image_to_base64(processed_image)
            else:
                print("Successfully extracted accessory item")
                image_base64 = extraction_result["generated_image_base64"]

        # Step 2: Upload image to Supabase storage
        filename = f"accessory-{name.replace(' ', '-').lower()}-{int(time.time())}.png"
        image_url = await upload_accessory_image_to_supabase(image_base64, filename)
        print(f"Accessory image uploaded successfully: {image_url}")

        # Step 3: Save to database
        saved_item = await save_accessory_item_to_db(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            size=size,
            image_url=image_url,
            is_owned=is_owned
        )

        # Add metadata about the process
        saved_item["quality_analysis"] = quality_analysis
        saved_item["used_original_image"] = use_original_image
        saved_item["extraction_performed"] = not use_original_image

        return saved_item

    except Exception as e:
        print(f"Error in smart accessory item creation: {e}")
        raise e

async def get_unique_accessory_categories(user_id: str) -> List[str]:
    """Get list of unique accessory categories for a user"""
    try:
        supabase = get_supabase_client()

        result = supabase.table("accessories").select("category").eq("profile_id", user_id).execute()

        if result.data:
            categories = list(set([item['category'] for item in result.data if item.get('category')]))
            return sorted(categories)
        else:
            return []

    except Exception as e:
        print(f"Error getting unique accessory categories: {e}")
        return []

async def smart_save_accessory_item(user_id: str, name: str, category: str,
                                   primary_color: str = None, secondary_color: str = None,
                                   size: str = None, is_owned: bool = True,
                                   image: UploadFile = None) -> Dict[str, Any]:
    """
    Smart accessory item creation that checks quality first and extracts if needed

    This function:
    1. Checks if the image is already professional quality
    2. If quality check passes, uses the original image
    3. If quality check fails, extracts the accessory item to create professional image
    4. Saves the accessory item to database with the best available image
    """
    try:
        if not image:
            raise ValueError("Image is required for accessory item creation")

        # Import clothing service functions for image processing
        from .clothing_service import (
            process_uploaded_image,
            check_professional_clothing_image,
            image_to_base64,
            extract_single_clothing_item
        )

        # Step 1: Check image quality
        print(f"Checking image quality for accessory item: {name}")
        processed_image = process_uploaded_image(image)
        quality_analysis = check_professional_clothing_image(processed_image)

        use_original_image = quality_analysis.get("passed", False)
        print(f"Quality check result - passed: {use_original_image}")

        if use_original_image:
            # Use original image since it passed quality check
            print("Using original image (quality check passed)")
            image_base64 = image_to_base64(processed_image)

        else:
            # Extract accessory item to create professional image
            print("Extracting accessory item (quality check failed)")

            # Reset image file pointer
            await image.seek(0)

            # Extract single clothing/accessory item (same function works for accessories)
            extraction_result = await extract_single_clothing_item(image)

            if not extraction_result.get("generated_image_base64"):
                # Fallback to original image if extraction fails
                print("Extraction failed, falling back to original image")
                await image.seek(0)
                processed_image = process_uploaded_image(image)
                image_base64 = image_to_base64(processed_image)
            else:
                print("Successfully extracted accessory item")
                image_base64 = extraction_result["generated_image_base64"]

        # Step 2: Upload image to Supabase storage
        filename = f"accessory-{name.replace(' ', '-').lower()}-{int(time.time())}.png"
        image_url = await upload_accessory_image_to_supabase(image_base64, filename)
        print(f"Accessory image uploaded successfully: {image_url}")

        # Step 3: Save to database
        saved_item = await save_accessory_item_to_db(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            size=size,
            image_url=image_url,
            is_owned=is_owned
        )

        # Add metadata about the process
        saved_item["quality_analysis"] = quality_analysis
        saved_item["used_original_image"] = use_original_image
        saved_item["extraction_performed"] = not use_original_image

        return saved_item

    except Exception as e:
        print(f"Error in smart accessory item creation: {e}")
        raise e

    except Exception as e:
        print(f"Error getting unique accessory categories: {e}")
        return []

async def smart_save_accessory_item(user_id: str, name: str, category: str,
                                   primary_color: str = None, secondary_color: str = None,
                                   size: str = None, is_owned: bool = True,
                                   image: UploadFile = None) -> Dict[str, Any]:
    """
    Smart accessory item creation that checks quality first and extracts if needed

    This function:
    1. Checks if the image is already professional quality
    2. If quality check passes, uses the original image
    3. If quality check fails, extracts the accessory item to create professional image
    4. Saves the accessory item to database with the best available image
    """
    try:
        if not image:
            raise ValueError("Image is required for accessory item creation")

        # Import clothing service functions for image processing
        from .clothing_service import (
            process_uploaded_image,
            check_professional_clothing_image,
            image_to_base64,
            extract_single_clothing_item
        )

        # Step 1: Check image quality
        print(f"Checking image quality for accessory item: {name}")
        processed_image = process_uploaded_image(image)
        quality_analysis = check_professional_clothing_image(processed_image)

        use_original_image = quality_analysis.get("passed", False)
        print(f"Quality check result - passed: {use_original_image}")

        if use_original_image:
            # Use original image since it passed quality check
            print("Using original image (quality check passed)")
            image_base64 = image_to_base64(processed_image)

        else:
            # Extract accessory item to create professional image
            print("Extracting accessory item (quality check failed)")

            # Reset image file pointer
            await image.seek(0)

            # Extract single clothing/accessory item (same function works for accessories)
            extraction_result = await extract_single_clothing_item(image)

            if not extraction_result.get("generated_image_base64"):
                # Fallback to original image if extraction fails
                print("Extraction failed, falling back to original image")
                await image.seek(0)
                processed_image = process_uploaded_image(image)
                image_base64 = image_to_base64(processed_image)
            else:
                print("Successfully extracted accessory item")
                image_base64 = extraction_result["generated_image_base64"]

        # Step 2: Upload image to Supabase storage
        filename = f"accessory-{name.replace(' ', '-').lower()}-{int(time.time())}.png"
        image_url = await upload_accessory_image_to_supabase(image_base64, filename)
        print(f"Accessory image uploaded successfully: {image_url}")

        # Step 3: Save to database
        saved_item = await save_accessory_item_to_db(
            user_id=user_id,
            name=name,
            category=category,
            primary_color=primary_color,
            secondary_color=secondary_color,
            size=size,
            image_url=image_url,
            is_owned=is_owned
        )

        # Add metadata about the process
        saved_item["quality_analysis"] = quality_analysis
        saved_item["used_original_image"] = use_original_image
        saved_item["extraction_performed"] = not use_original_image

        return saved_item

    except Exception as e:
        print(f"Error in smart accessory item creation: {e}")
        raise e