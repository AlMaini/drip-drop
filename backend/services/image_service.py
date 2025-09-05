import io
from typing import Optional, List
from fastapi import UploadFile
from PIL import Image

from .gemini_client import get_gemini_client, editing_model
from .image_processing import process_uploaded_image, image_to_base64

async def generate_image_with_context(
    prompt: str, 
    style: str = "realistic", 
    context_description: Optional[str] = None,
    context_images: List[UploadFile] = []
) -> dict:
    """
    Generate an image using Gemini AI with optional context images
    """
    client = get_gemini_client()
    
    # Prepare the generation prompt
    generation_prompt = f"""
    Create a detailed image based on the following description: {prompt}
    
    Style: {style}
    
    {f"Additional context: {context_description}" if context_description else ""}
    
    Please analyze any provided reference images and use them as context for style, composition, lighting, or other visual elements while creating the new image described in the prompt.
    
    Generate an image that incorporates the visual elements and style from the reference images while fulfilling the specific requirements in the prompt.
    """
    
    # Process context images if provided
    processed_images = []
    if context_images:
        for uploaded_file in context_images:
            if uploaded_file.filename:  # Check if file was actually uploaded
                processed_image = process_uploaded_image(uploaded_file)
                processed_images.append(processed_image)
    
    # Prepare content for Gemini
    contents = [generation_prompt]
    contents.extend(processed_images)
    
    # Generate content with Gemini
    response = client.models.generate_content(
        model=editing_model,
        contents=contents
    )
    
    # Process response
    generated_image_base64 = None
    response_text = None
    
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            response_text = part.text
        elif part.inline_data is not None:
            image = Image.open(io.BytesIO(part.inline_data.data))
            generated_image_base64 = image_to_base64(image)
    
    return {
        "generated_image_base64": generated_image_base64,
        "description": response_text
    }