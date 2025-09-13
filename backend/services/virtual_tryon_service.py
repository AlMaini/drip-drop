import io
from typing import List
from fastapi import UploadFile
from PIL import Image

from .gemini_client import get_gemini_client, editing_model
from .image_processing import process_uploaded_image, image_to_base64
from .clothing_service import itemize_photo
import processing.utility.image_utils as image_utils

async def perform_iterative_tryon(images: List[UploadFile]) -> dict:
    """
    Virtual try-on using Gemini AI - make the person wear the provided clothes iteratively
    
    Args:
        images: List of images containing person and clothing items
    """
    client = get_gemini_client()
    
    # Process uploaded images
    processed_images = []
    for i in range(len(images)):
        uploaded_file = images[i]
        processed_image = process_uploaded_image(uploaded_file)
        # if not the person image
        if i != 0:
            processed_image = image_utils.pad_image_to_aspect_ratio(processed_image, target_width=processed_images[0].width, target_height=processed_images[0].height)
        processed_images.append(processed_image)
    
    if len(processed_images) < 2:
        raise ValueError("At least 2 images required (person + clothing)")
    
    # Assume first image is the person, rest are clothing items
    person_image = processed_images[0]
    clothing_images = processed_images[1:]
    
    # Analyze each clothing item to identify what it is
    clothing_descriptions = []
    for i, clothing_image in enumerate(clothing_images):
        try:
            items = itemize_photo(clothing_image)
            if items:
                # Join multiple items with "and" if found
                description = " and ".join(items)
            else:
                description = f"clothing item {i+1}"
            clothing_descriptions.append(description)
        except Exception:
            # Fallback if analysis fails
            clothing_descriptions.append(f"clothing item {i+1}")
    
    # Start with the person image as the base
    current_result_image = person_image
    iteration_results = []
    
    # Process clothing items in batches of 1-2 items
    batch_size = 2
    for i in range(0, len(clothing_images), batch_size):
        # Get current batch of clothing items (1-2 items)
        current_batch = clothing_images[i:i + batch_size]
        current_descriptions = clothing_descriptions[i:i + batch_size]
        batch_items = len(current_batch)
        
        try:
            # Create the try-on prompt for current batch with specific item descriptions
            if batch_items == 1:
                items_text = current_descriptions[0]
            else:
                items_text = " and ".join(current_descriptions)
               
            prompt = f"Make the person in the first image wear the {items_text} shown in the following images. Create a realistic visualization of how the clothing items would look when worn by the person, maintaining proper fit, proportions, and styling. Maintain the pose of the person. Do not add any additional items or accessories."

            # Prepare content for Gemini: current result + current clothing batch
            contents = [prompt, current_result_image]
            contents.extend(current_batch)
            
            # Generate the try-on visualization for this batch
            response = client.models.generate_content(
                model=editing_model,
                contents=contents
            )
            
            # Process response
            generated_image_base64 = None
            description_text = None
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    description_text = part.text
                elif part.inline_data is not None:
                    image_data = Image.open(io.BytesIO(part.inline_data.data))
                    generated_image_base64 = image_to_base64(image_data)
                    # Update current result image for next iteration
                    current_result_image = image_data
            
            # Store iteration result with clothing descriptions
            iteration_results.append({
                "iteration": (i // batch_size) + 1,
                "items_added": batch_items,
                "clothing_descriptions": current_descriptions,
                "success": True,
                "generated_image_base64": generated_image_base64,
                "description": description_text if description_text else f"Applied {' and '.join(current_descriptions)}"
            })
            
        except Exception as batch_error:
            # If this batch fails, record error but continue with next batch
            iteration_results.append({
                "iteration": (i // batch_size) + 1,
                "items_added": batch_items,
                "clothing_descriptions": current_descriptions,
                "success": False,
                "error": f"Error processing batch: {str(batch_error)}",
                "generated_image_base64": None,
                "description": None
            })
            # Continue with previous result image
    
    # Get final result
    final_result = None
    successful_iterations = 0
    
    for result in reversed(iteration_results):
        if result["success"] and result["generated_image_base64"]:
            final_result = result["generated_image_base64"]
            break
    
    successful_iterations = sum(1 for result in iteration_results if result["success"])
    
    return {
        "success": True,
        "final_image_base64": final_result,
        "iteration_results": iteration_results,
        "total_iterations": len(iteration_results),
        "successful_iterations": successful_iterations,
        "total_clothing_items": len(clothing_images),
        "clothing_descriptions": clothing_descriptions,
        "images_processed": len(processed_images),
        "description": "Iterative try-on visualization completed with item analysis"
    }

async def perform_fit_transfer(clothing_image: UploadFile, person_image: UploadFile) -> dict:
    """
    Perform virtual try-on by transferring clothing onto a model image
    
    Args:
        clothing_image: Image of the clothing item
        model_image: Image of the model/person
    """
    client = get_gemini_client()
    
    # Process uploaded images
    processed_clothing_image = process_uploaded_image(clothing_image)
    processed_person_image = process_uploaded_image(person_image)
    
    prompt = "Make the person in the first image wear the outfit shown in the second image. Create a realistic visualization of how the outfit would look when worn by the person, maintaining proper fit, proportions, and styling. Do not change the color of the outfit. Maintain the pose of the person."

    try:
        response = client.models.generate_content(
            model=editing_model,
            contents=[prompt, processed_person_image, processed_clothing_image]
        )
        
        generated_image_base64 = None
        description_text = None
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                description_text = part.text
            elif part.inline_data is not None:
                image_data = Image.open(io.BytesIO(part.inline_data.data))
                generated_image_base64 = image_to_base64(image_data)
        
        return {
            "success": True,
            "tryon_image_base64": generated_image_base64,
            "description": description_text if description_text else "Fit transfer completed"
        }

    except Exception as e:
        raise RuntimeError(f"Error during fit transfer: {str(e)}")