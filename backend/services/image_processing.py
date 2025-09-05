import io
import base64
from typing import Optional
from fastapi import UploadFile, HTTPException
from PIL import Image

def process_uploaded_image(uploaded_file: UploadFile) -> Image.Image:
    """Process uploaded image file and return PIL Image object"""
    try:
        image_data = uploaded_file.file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Resize if too large (Gemini has size limits) while maintaining aspect ratio
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str