import time
import json
from typing import List
from fastapi import APIRouter, File, UploadFile, Form, Depends

from services import clothing_service
from .auth import verify_token

router = APIRouter(prefix="/api", tags=["clothing-analysis"])

@router.post("/extract-clothing")
async def extract_clothing(
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
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
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
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
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """
    Analyze uploaded image and return a list of clothing items found, saving them to database
    
    Args:
        image: Single image to analyze
    """
    try:
        outfit_items = await clothing_service.identify_clothing_items(image)
        saved_items = []
        
        # Process and save clothing items
        for item in outfit_items["clothing_items"]:
            try:
                # Create a temporary image URL (we'll update with real images later if needed)
                temp_image_url = f"temp://itemized-{int(time.time())}"
                
                # Extract item details
                item_name = item.get("name", "Unknown Item")
                item_type = item.get("type", "clothing")
                primary_color = item.get("primary_color")
                secondary_color = item.get("secondary_color")
                
                # Save to database
                saved_item = await clothing_service.save_clothing_item_to_db(
                    user_id=user_id,
                    name=item_name,
                    category=item_type.lower(),
                    primary_color=primary_color,
                    secondary_color=secondary_color,
                    image_url=temp_image_url,
                    features=item.get("features", {})
                )
                
                # Add saved item info to the response
                item["saved_item_id"] = saved_item["id"]
                saved_items.append(saved_item)
                
            except Exception as save_error:
                print(f"Error saving clothing item {item.get('name', 'unknown')}: {save_error}")
                item["save_error"] = str(save_error)
        
        # Process and save accessories
        for item in outfit_items["accessories"]:
            try:
                # Create a temporary image URL
                temp_image_url = f"temp://itemized-{int(time.time())}"
                
                # Extract item details
                item_name = item.get("name", "Unknown Accessory")
                item_type = item.get("type", "accessory")
                primary_color = item.get("primary_color")
                secondary_color = item.get("secondary_color")
                
                # Save to database
                saved_item = await clothing_service.save_clothing_item_to_db(
                    user_id=user_id,
                    name=item_name,
                    category=item_type.lower(),
                    primary_color=primary_color,
                    secondary_color=secondary_color,
                    image_url=temp_image_url,
                    features=item.get("features", {})
                )
                
                # Add saved item info to the response
                item["saved_item_id"] = saved_item["id"]
                saved_items.append(saved_item)
                
            except Exception as save_error:
                print(f"Error saving accessory {item.get('name', 'unknown')}: {save_error}")
                item["save_error"] = str(save_error)
        
        return {
            "success": True,
            "clothing_items": outfit_items["clothing_items"],
            "accessories": outfit_items["accessories"],
            "item_count": len(outfit_items["clothing_items"]) + len(outfit_items["accessories"]),
            "saved_items_count": len(saved_items),
            "saved_items": saved_items,
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
    clothing_items: str = Form(...),
    user_id: str = Depends(verify_token)
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

@router.post("/extract-clothes-concurrent")
async def extract_clothes_concurrent(
    image: UploadFile = File(...),
    clothing_items: str = Form(...),
    user_id: str = Depends(verify_token)
):
    """
    Extract specific clothing items using concurrent async requests for better performance
    
    Args:
        image: Single image containing clothing items
        clothing_items: JSON string array of specific clothing items to extract
    """
    try:
        result = await clothing_service.extract_specific_clothing_items_concurrent(image, clothing_items)
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error in concurrent extraction: {str(e)}",
            "extracted_images": []
        }

@router.post("/add-fit-to-wardrobe")
async def add_fit_to_wardrobe(
    image: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """
    Analyze image, extract clothing items, and save them to wardrobe with images
    
    Args:
        image: Single image containing clothing items
    """
    try:
        print(f"Starting add_fit_to_wardrobe for user: {user_id}, image: {image.filename}")
        
        # Step 1: Itemize the clothing in the image
        print("Step 1: Itemizing clothing items...")
        outfit_items = await clothing_service.identify_clothing_items(image)
        print(f"Found {len(outfit_items.get('clothing_items', []))} clothing items and {len(outfit_items.get('accessories', []))} accessories")
        
        if not outfit_items["clothing_items"] and not outfit_items["accessories"]:
            return {
                "success": False,
                "error": "No clothing items or accessories found in the image",
                "saved_items": []
            }
        
        # Step 2: Prepare items for extraction
        print("Step 2: Preparing items for extraction...")
        all_items = []
        for item in outfit_items["clothing_items"]:
            all_items.append({
                "name": item.get("name", "Unknown Item"),
                "category": item.get("type", "clothing"),
                "primary_color": item.get("primary_color"),
                "secondary_color": item.get("secondary_color"),
                "features": item.get("features", {})
            })
        
        for item in outfit_items["accessories"]:
            all_items.append({
                "name": item.get("name", "Unknown Accessory"),
                "category": item.get("type", "accessory"),
                "primary_color": item.get("primary_color"),
                "secondary_color": item.get("secondary_color"),
                "features": item.get("features", {})
            })
        
        # Step 3: Extract images for all items concurrently
        item_names = [item["name"] for item in all_items]
        print(f"Step 3: Extracting {len(item_names)} items concurrently: {item_names}")
        
        # Reset the image file pointer to the beginning so it can be read again
        await image.seek(0)
        
        extraction_result = await clothing_service.extract_specific_clothing_items_concurrent(image, json.dumps(item_names))
        print(f"Extraction completed, success: {extraction_result.get('success', False)}")
        
        if not extraction_result.get("success", False):
            return {
                "success": False,
                "error": f"Failed to extract clothing items: {extraction_result.get('error', 'Unknown error')}",
                "saved_items": []
            }
        
        # Step 4: Save items to database with uploaded images
        print("Step 4: Saving items to database with uploaded images...")
        saved_items = []
        extraction_map = {ext["item"]: ext for ext in extraction_result.get("extracted_images", [])}
        print(f"Extraction map has {len(extraction_map)} items")
        
        for item in all_items:
            try:
                item_name = item["name"]
                extracted_item = extraction_map.get(item_name)
                
                if extracted_item and extracted_item.get("success") and extracted_item.get("generated_image_base64"):
                    # Upload image to Supabase storage
                    try:
                        filename = f"{item_name.replace(' ', '-').lower()}-{int(time.time())}.png"
                        image_url = await clothing_service.upload_image_to_supabase(
                            extracted_item["generated_image_base64"], 
                            filename
                        )
                        print(f"Item {item_name} extracted and uploaded successfully to: {image_url}")
                    except Exception as upload_error:
                        print(f"Failed to upload image for {item_name}: {upload_error}")
                        # Use a placeholder if upload failed but keep the extracted image info
                        image_url = f"upload-failed://extracted-{int(time.time())}"
                else:
                    # Use a placeholder if extraction failed
                    image_url = f"temp://failed-{int(time.time())}"
                    print(f"Item {item_name} extraction failed")
                
                # Save to database
                print(f"Saving item to database: {item['name']}, category: {item['category']}")
                saved_item = await clothing_service.save_clothing_item_to_db(
                    user_id=user_id,
                    name=item["name"],
                    category=item["category"],
                    primary_color=item.get("primary_color"),
                    secondary_color=item.get("secondary_color"),
                    image_url=image_url,
                    features=item.get("features", {})
                )
                print(f"Successfully saved item with ID: {saved_item.get('id')}")
                
                # Add extraction info to saved item
                saved_item["extraction_success"] = extracted_item.get("success", False) if extracted_item else False
                saved_item["extraction_error"] = extracted_item.get("error") if extracted_item and not extracted_item.get("success") else None
                
                saved_items.append(saved_item)
                
            except Exception as item_error:
                print(f"Error processing item {item['name']}: {item_error}")
                # Still try to save item without proper image
                try:
                    saved_item = await clothing_service.save_clothing_item_to_db(
                        user_id=user_id,
                        name=item["name"],
                        category=item["category"],
                        primary_color=item.get("primary_color"),
                        secondary_color=item.get("secondary_color"),
                        image_url=f"temp://error-{int(time.time())}",
                        features=item.get("features", {})
                    )
                    saved_item["extraction_success"] = False
                    saved_item["extraction_error"] = str(item_error)
                    saved_items.append(saved_item)
                except Exception as save_error:
                    print(f"Failed to save item {item['name']} even without image: {save_error}")
        
        return {
            "success": True,
            "message": f"Added {len(saved_items)} items to your wardrobe",
            "total_items_found": len(all_items),
            "items_saved": len(saved_items),
            "items_with_images": len([item for item in saved_items if item.get("extraction_success", False)]),
            "saved_items": saved_items,
            "extraction_details": extraction_result,
            "filename": image.filename
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Full error in add_fit_to_wardrobe: {error_details}")
        return {
            "success": False,
            "error": f"Error adding fit to wardrobe: {str(e)}",
            "error_details": error_details,
            "saved_items": []
        }