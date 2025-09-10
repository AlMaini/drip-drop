import json
import io
import base64
import sys
import os
from typing import List, Dict, Any, Optional, Union
from PIL import Image

# Add backend directory to path if running directly
if __name__ == "__main__":
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

from services.gemini_client import get_gemini_client, analysis_model
from models import *
import models.tops_config as tops_config
import models.bottoms_config as bottoms_config
import models.footwear_config as footwear_config
import models.outerwear_config as outerwear_config
import models.accessories_config as accessories_config
import models.undergarments_config as undergarments_config
import models.dresses_config as dresses_config
import models.sleepwear_config as sleepwear_config
import models.other_config as other_config


# Map category names to their config modules
CONFIG_MODULES = {
    "tops": tops_config,
    "bottoms": bottoms_config,
    "footwear": footwear_config,
    "outerwear": outerwear_config,
    "accessories": accessories_config,
    "undergarments": undergarments_config,
    "dresses": dresses_config,
    "sleepwear": sleepwear_config,
    "other": other_config
}

def get_clothing_category(clothing_type: str) -> str:
    """Determine which category a clothing type belongs to."""
    for category, config in CONFIG_MODULES.items():
        if clothing_type in config.CLOTHING_TYPES:
            return category
    return "other"

def generate_clothing_identification_prompt() -> str:
    """Generate a comprehensive prompt using all configuration files."""
    prompt_parts = [
        "Analyze this image and identify all visible clothing items and accessories. For each item, provide:",
        "",
        "1. clothing_type: The specific type (e.g., \"TShirt\", \"Jeans\", \"Sneakers\", \"Hoodie\", etc.)",
        "2. name: A descriptive name for the item",
        "3. primary_color: The main color of the item",
        "4. secondary_color: Secondary/accent color (can be same as primary if solid)",
        "5. specific_attributes: Any specific attributes relevant to that clothing type",
        "",
        "Available clothing types and their attributes:",
        ""
    ]
    
    # Add each category with its clothing types and parameters
    category_names = {
        "tops": "TOPS",
        "bottoms": "BOTTOMS", 
        "footwear": "FOOTWEAR",
        "outerwear": "OUTERWEAR",
        "accessories": "ACCESSORIES",
        "undergarments": "UNDERGARMENTS",
        "dresses": "DRESSES",
        "sleepwear": "SLEEPWEAR"
    }
    
    for category, config in CONFIG_MODULES.items():
        if category == "other":  # Skip "other" in the prompt
            continue
            
        category_display = category_names.get(category, category.upper())
        clothing_items = []
        
        for clothing_type in config.CLOTHING_TYPES:
            if clothing_type in config.PARAMETER_CONFIG:
                params = config.PARAMETER_CONFIG[clothing_type]
                optional_params = params.get("optional_params", [])
                if optional_params:
                    param_str = f" ({', '.join(optional_params)})"
                else:
                    param_str = ""
                clothing_items.append(f"{clothing_type}{param_str}")
            else:
                clothing_items.append(clothing_type)
        
        prompt_parts.append(f"{category_display}: {', '.join(clothing_items)}")
    
    prompt_parts.extend([
        "",
        "For each parameter, use only these allowed values:",
        ""
    ])
    
    # Add allowed values for key parameters
    for category, config in CONFIG_MODULES.items():
        if category == "other":
            continue
        for clothing_type in config.CLOTHING_TYPES:
            if clothing_type in config.PARAMETER_CONFIG:
                params = config.PARAMETER_CONFIG[clothing_type]
                allowed_values = params.get("allowed_values", {})
                if allowed_values:
                    for param, values in allowed_values.items():
                        if values:  # Only show if there are allowed values
                            values_str = ', '.join([f'"{v}"' if v is not None else 'null' for v in values])
                            prompt_parts.append(f"{clothing_type} {param}: [{values_str}]")
    
    prompt_parts.extend([
        "",
        "Return ONLY a valid JSON array with this exact structure:",
        "[",
        "    {",
        "        \"clothing_type\": \"TShirt\",",
        "        \"name\": \"Basic White Tee\",",
        "        \"primary_color\": \"White\",",
        "        \"secondary_color\": \"White\",",
        "        \"attributes\": {}",
        "    },",
        "    {",
        "        \"clothing_type\": \"Jeans\",",
        "        \"name\": \"Dark Blue Skinny Jeans\",",
        "        \"primary_color\": \"Dark Blue\",",
        "        \"secondary_color\": \"Blue\",",
        "        \"attributes\": {\"fit\": \"Skinny\"}",
        "    }",
        "]",
        "",
        "Be specific with clothing types - use the exact class names provided. Include all visible items.",
        "Use only the allowed values specified above for each parameter."
    ])
    
    return "\n".join(prompt_parts)

def identify_clothing_from_image(image: Image.Image, generate_id: bool = True) -> List[Dict[str, Any]]:
    """
    Identify clothing items in an image using Gemini 1.5 and return appropriate clothing models.
    
    Args:
        image (PIL.Image): The image to analyze
        generate_id (bool): Whether to generate unique IDs for clothing items
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries containing clothing information and model instances
        
    Example:
        >>> from PIL import Image
        >>> image = Image.open("outfit.jpg")
        >>> results = identify_clothing_from_image(image)
        >>> for item in results:
        ...     print(f"Found {item['type']}: {item['model'].name}")
    """
    client = get_gemini_client()
    
    # Convert PIL image to base64 for API
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    image_data = base64.b64encode(buffer.getvalue()).decode()
    
    # Create comprehensive prompt using configuration files
    prompt = generate_clothing_identification_prompt()
    
    try:
        # Send request to Gemini
        response = client.models.generate_content(
            model=analysis_model,
            contents=[
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }
            ]
        )
        
        # Parse response
        response_text = response.text.strip()
        
        # Extract JSON from response (handle potential markdown formatting)
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        else:
            json_text = response_text
        
        # Parse JSON response
        try:
            clothing_data = json.loads(json_text)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON array from text
            import re
            json_match = re.search(r'\[.*\]', json_text, re.DOTALL)
            if json_match:
                clothing_data = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse JSON response")
        
        # Convert to clothing models
        results = []
        for i, item in enumerate(clothing_data):
            try:
                clothing_model = create_clothing_model(
                    clothing_type=item['clothing_type'],
                    name=item['name'],
                    primary_color=item['primary_color'],
                    secondary_color=item['secondary_color'],
                    image=image,
                    attributes=item.get('attributes', {}),
                    item_id=i + 1 if generate_id else None
                )
                
                if clothing_model:
                    results.append({
                        'type': item['clothing_type'],
                        'model': clothing_model,
                        'confidence': 'high',  # Gemini doesn't provide confidence scores
                        'raw_data': item
                    })
            except Exception as e:
                print(f"Error creating model for {item.get('clothing_type', 'unknown')}: {e}")
                continue
        
        return results
        
    except Exception as e:
        print(f"Error in clothing identification: {e}")
        return []


def create_clothing_model(clothing_type: str, name: str, primary_color: str, 
                         secondary_color: str, image: Image.Image, 
                         attributes: Dict[str, Any], item_id: Optional[int] = None) -> Optional[Any]:
    """
    Create a clothing model instance based on the identified type and attributes.
    Uses configuration files for validation and default values.
    
    Args:
        clothing_type (str): The clothing type class name
        name (str): Name of the clothing item
        primary_color (str): Primary color
        secondary_color (str): Secondary color  
        image (PIL.Image): The image of the clothing
        attributes (Dict): Specific attributes for the clothing type
        item_id (Optional[int]): ID for the clothing item
        
    Returns:
        Clothing model instance or None if type not found
    """
    # Map clothing types to their classes
    clothing_classes = {
        # Tops
        'TShirt': TShirt,
        'DressShirt': DressShirt,
        'Blouse': Blouse,
        'TankTop': TankTop,
        'Sweater': Sweater,
        'Hoodie': Hoodie,
        'Sweatshirt': Sweatshirt,
        'Cardigan': Cardigan,
        'WorkoutTop': WorkoutTop,
        
        # Bottoms
        'Pants': Pants,
        'Shorts': Shorts,
        'Jeans': Jeans,
        'DressPants': DressPants,
        'Trousers': Trousers,
        'Chinos': Chinos,
        'Skirt': Skirt,
        'Leggings': Leggings,
        'SweatPants': SweatPants,
        'Joggers': Joggers,
        'AthleticShorts': AthleticShorts,
        'YogaPants': YogaPants,
        
        # Footwear
        'Sneakers': Sneakers,
        'DressShoes': DressShoes,
        'Boots': Boots,
        'Sandals': Sandals,
        'Flats': Flats,
        'Heels': Heels,
        'AthleticShoes': AthleticShoes,
        
        # Outerwear
        'Jacket': Jacket,
        'Blazer': Blazer,
        'Coat': Coat,
        'WinterCoat': WinterCoat,
        'RainJacket': RainJacket,
        'Windbreaker': Windbreaker,
        'Vest': Vest,
        
        # Accessories
        'Hat': Hat,
        'Cap': Cap,
        'Belt': Belt,
        'Scarf': Scarf,
        'Gloves': Gloves,
        'Sunglasses': Sunglasses,
        'Watch': Watch,
        
        # Undergarments
        'Underwear': Underwear,
        'Bra': Bra,
        'SportsBra': SportsBra,
        'Undershirt': Undershirt,
        'Socks': Socks,
        'Pantyhose': Pantyhose,
        'Tights': Tights,
        
        # Dresses
        'CasualDress': CasualDress,
        'FormalDress': FormalDress,
        'MaxiDress': MaxiDress,
        'MiniDress': MiniDress,
        'Jumpsuit': Jumpsuit,
        'Romper': Romper,
        
        # Sleepwear
        'Pajamas': Pajamas,
        'Nightgown': Nightgown,
        'Robe': Robe,
        
        # Other
        'Other': Other,
    }
    
    if clothing_type not in clothing_classes:
        print(f"Unknown clothing type: {clothing_type}")
        return None
    
    clothing_class = clothing_classes[clothing_type]
    
    # Get the category for this clothing type to access configuration
    category = get_clothing_category(clothing_type)
    config_module = CONFIG_MODULES.get(category)
    
    # Validate attributes using configuration
    if config_module and hasattr(config_module, 'validate_parameters'):
        validation_result = config_module.validate_parameters(clothing_type, attributes)
        if validation_result.get("warnings"):
            for warning in validation_result["warnings"]:
                print(f"Warning for {clothing_type}: {warning}")
    
    # Get default parameters and merge with provided attributes
    final_attributes = {}
    if config_module and hasattr(config_module, 'get_default_parameters'):
        defaults = config_module.get_default_parameters(clothing_type)
        final_attributes.update(defaults)
    
    # Override with provided attributes
    if attributes:
        final_attributes.update(attributes)
    
    # Base arguments for all clothing items
    base_args = [item_id, name, primary_color, secondary_color, image]
    
    try:
        # Create instance with final attributes (defaults + provided)
        if final_attributes:
            return clothing_class(*base_args, **final_attributes)
        else:
            return clothing_class(*base_args)
    except Exception as e:
        print(f"Error creating {clothing_type} instance with attributes {final_attributes}: {e}")
        try:
            # Fallback to base arguments only
            return clothing_class(*base_args)
        except Exception as e2:
            print(f"Fallback failed for {clothing_type}: {e2}")
            return None


def batch_identify_clothing(images: List[Image.Image]) -> List[List[Dict[str, Any]]]:
    """
    Identify clothing items in multiple images.
    
    Args:
        images (List[PIL.Image]): List of images to analyze
        
    Returns:
        List[List[Dict]]: Results for each image
    """
    results = []
    for i, image in enumerate(images):
        print(f"Processing image {i + 1}/{len(images)}...")
        image_results = identify_clothing_from_image(image, generate_id=True)
        results.append(image_results)
    return results


def get_clothing_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a summary of identified clothing items.
    
    Args:
        results (List[Dict]): Results from identify_clothing_from_image
        
    Returns:
        Dict: Summary statistics
    """
    if not results:
        return {"total_items": 0, "categories": {}, "colors": {}}
    
    categories = {}
    colors = {}
    
    for item in results:
        clothing_type = item['type']
        model = item['model']
        
        # Count categories
        categories[clothing_type] = categories.get(clothing_type, 0) + 1
        
        # Count colors
        primary_color = model.primary_color
        colors[primary_color] = colors.get(primary_color, 0) + 1
    
    return {
        "total_items": len(results),
        "categories": categories,
        "colors": colors,
        "most_common_category": max(categories.items(), key=lambda x: x[1])[0] if categories else None,
        "most_common_color": max(colors.items(), key=lambda x: x[1])[0] if colors else None
    }


# Example usage and testing functions
def test_clothing_identification():
    """Test function for clothing identification (requires test images)"""
    try:
        from PIL import Image
        import os
        
        # Test with a sample image (you'll need to provide this)
        test_image_path = "mothman.png"
        if os.path.exists(test_image_path):
            image = Image.open(test_image_path)
            results = identify_clothing_from_image(image)
            
            print(f"Identified {len(results)} clothing items:")
            for item in results:
                model = item['model']
                print(f"- {item['type']}: {model.name} ({model.primary_color})")
            
            summary = get_clothing_summary(results)
            print(f"\nSummary: {summary}")
            
            return results
        else:
            print(f"Test image not found: {test_image_path}")
            return []
    except Exception as e:
        print(f"Test failed: {e}")
        return []


if __name__ == "__main__":
    # Run test if executed directly
    test_clothing_identification()