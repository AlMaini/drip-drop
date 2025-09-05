import io
import json
from typing import List
from fastapi import UploadFile
from PIL import Image

from .gemini_client import get_gemini_client, editing_model, analysis_model
from .image_processing import process_uploaded_image, image_to_base64
import processing.utility.image_utils as image_utils

async def extract_single_clothing_item(image: UploadFile) -> dict:
    """Extract clothing item from photo and create professional product image"""
    client = get_gemini_client()
    
    # Process uploaded image
    processed_image = process_uploaded_image(image)
    
    # Create the extraction prompt
    prompt = "Take the clothing item in this photo and make a full view image of the item with a white background as a professionally shot image for a clothing item on an online store."
    
    # Prepare content for Gemini
    contents = [prompt, processed_image]
    
    # Generate the professional product image
    response = client.models.generate_content(
        model=editing_model,
        contents=contents
    )
    
    # Process response - check for both generated image and text description
    generated_image_base64 = None
    description_text = None
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            description_text = part.text
        elif part.inline_data is not None:
            image_data = Image.open(io.BytesIO(part.inline_data.data))
            padded_image = image_utils.pad_image_to_square(image_data)
            generated_image_base64 = image_to_base64(padded_image)

    return {
        "generated_image_base64": generated_image_base64,
        "description": description_text if description_text else "Professional clothing product image generated"
    }

async def analyze_clothing_quality(image: UploadFile) -> dict:
    """Check if an image is a professional studio quality photo of a single clothing item"""
    processed_image = process_uploaded_image(image)
    return check_professional_clothing_image(processed_image)

def check_professional_clothing_image(image: Image.Image) -> dict:
    """
    Check if an image is a professional studio quality photo of a single clothing item
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        dict: Analysis results containing is_professional, is_single_item, item_type, and confidence
    """
    client = get_gemini_client()
    
    try:
        # Create analysis prompt
        prompt = """
        Analyze this image and determine if it meets the following criteria:
        1. Is it a professional studio quality photograph?
        2. Does it contain exactly one clothing item?
        3. Is the background clean/plain (preferably white or neutral)?
        4. Is the lighting professional and even?
        5. Is the clothing item the main focus and clearly visible?
        
        Please respond in the following JSON format:
        {
            "is_professional": true/false,
            "is_single_item": true/false,
            "item_type": "shirt/pants/dress/shoes/etc or null if not clothing",
            "background_quality": "excellent/good/poor",
            "lighting_quality": "excellent/good/poor",
            "overall_confidence": 0.0-1.0,
            "issues": ["list of any issues found"],
            "reasoning": "brief explanation of the assessment"
        }
        
        Only respond with the JSON object, no additional text.
        """
        
        # Prepare content for Gemini
        contents = [prompt, image]
        
        # Call Gemini 1.5 Flash for analysis
        response = client.models.generate_content(
            model=analysis_model,
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        if not analysis_text:
            return {
                "error": "No analysis text received from Gemini",
                "is_professional": False,
                "is_single_item": False
            }
        
        # Try to parse JSON response
        try:
            # Clean the response text by removing markdown code blocks
            cleaned_text = analysis_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            analysis_result = json.loads(cleaned_text)
            return analysis_result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a basic structure
            return {
                "error": "Failed to parse Gemini response as JSON",
                "raw_response": analysis_text,
                "is_professional": False,
                "is_single_item": False
            }
            
    except Exception as e:
        return {
            "error": f"Error analyzing image: {str(e)}",
            "is_professional": False,
            "is_single_item": False
        }

async def identify_clothing_items(image: UploadFile) -> List[str]:
    """Analyze uploaded image and return a list of clothing items found"""
    processed_image = process_uploaded_image(image)
    return itemize_photo(processed_image)

def itemize_photo(image: Image.Image) -> List[str]:
    """
    Analyze an image and return a list of clothing items found
    
    Args:
        image: PIL Image object to analyze
        
    Returns:
        List[str]: List of clothing items found in the image
    """
    client = get_gemini_client()
    
    try:
        # Create analysis prompt
        prompt = """
        Analyze this image and identify all the clothing items visible in the photo.
        
        Please respond with a JSON array containing only the clothing items you can clearly identify.
        Use specific, descriptive names for each item (e.g., "blue denim jeans", "white cotton t-shirt", "black leather jacket").
        
        Only include actual clothing items (shirts, pants, dresses, shoes, accessories like belts, hats, etc.).
        Do not include people, backgrounds, or non-clothing objects.
        
        Response format: ["item1", "item2", "item3", ...]
        
        Only respond with the JSON array, no additional text.
        """
        
        # Prepare content for Gemini
        contents = [prompt, image]
        
        # Call Gemini 1.5 Flash for analysis
        response = client.models.generate_content(
            model=analysis_model,
            contents=contents
        )
        
        # Extract text response
        analysis_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                analysis_text = part.text
                break
        
        if not analysis_text:
            return []
        
        # Try to parse JSON response
        try:
            # Clean the response text by removing markdown code blocks
            cleaned_text = analysis_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove ```
            cleaned_text = cleaned_text.strip()
            
            clothing_items = json.loads(cleaned_text)
            
            # Ensure we return a list
            if isinstance(clothing_items, list):
                return clothing_items
            else:
                return []
                
        except json.JSONDecodeError:
            # If JSON parsing fails, return empty list
            return []
            
    except Exception as e:
        # Log error and return empty list
        print(f"Error itemizing photo: {str(e)}")
        return []

async def extract_specific_clothing_items(image: UploadFile, clothing_items: str) -> dict:
    """Extract specific clothing items from photo and create professional product images"""
    client = get_gemini_client()
    
    # Process uploaded image
    processed_image = process_uploaded_image(image)
    
    # Parse the clothing items list
    try:
        items_list = json.loads(clothing_items)
        if not isinstance(items_list, list):
            raise ValueError("clothing_items must be a JSON array")
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "Invalid JSON format for clothing_items"
        }
    
    if not items_list:
        return {
            "success": False,
            "error": "No clothing items specified"
        }
    
    extracted_images = []
    
    # Loop through each clothing item and extract it
    for item in items_list:
        try:
            # Create the extraction prompt for specific item
            prompt = f"Take the {item} in this photo and make a full view image of just that item with a white background as a professionally shot image for a clothing item on an online store. Focus only on the {item} and exclude all other clothing items or objects."
            
            # Prepare content for Gemini
            contents = [prompt, processed_image]
            
            # Generate the professional product image
            response = client.models.generate_content(
                model=editing_model,
                contents=contents
            )
            
            # Process response - check for both generated image and text description
            generated_image_base64 = None
            description_text = None
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    description_text = part.text
                elif part.inline_data is not None:
                    image_data = Image.open(io.BytesIO(part.inline_data.data))
                    generated_image_base64 = image_to_base64(image_data)
            
            # Add to results
            extracted_images.append({
                "item": item,
                "success": True,
                "generated_image_base64": generated_image_base64,
                "description": description_text if description_text else f"Professional {item} product image generated"
            })
            
        except Exception as item_error:
            # If extraction fails for this item, add error to results
            extracted_images.append({
                "item": item,
                "success": False,
                "error": f"Error extracting {item}: {str(item_error)}",
                "generated_image_base64": None,
                "description": None
            })
    
    # Count successful extractions
    successful_extractions = sum(1 for result in extracted_images if result["success"])
    
    return {
        "success": True,
        "extracted_images": extracted_images,
        "total_items": len(items_list),
        "successful_extractions": successful_extractions,
        "filename": image.filename
    }