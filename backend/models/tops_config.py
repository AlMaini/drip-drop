"""
Configuration for tops clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the tops category
CLOTHING_TYPES = [
    "TShirt",
    "DressShirt", 
    "Blouse",
    "TankTop",
    "Sweater",
    "Hoodie",
    "Sweatshirt",
    "Cardigan",
    "WorkoutTop"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "TShirt": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": {},
        "defaults": {},
        "allowed_values": {}
    },
    
    "DressShirt": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["pattern"],
        "defaults": {"pattern": None},
        "allowed_values": {
            "pattern": [
                None, "Striped", "Checkered", "Solid", "Polka Dot", "Paisley"
            ]
        }
    },
    
    "Blouse": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["sleeve_type"],
        "defaults": {"sleeve_type": "Long"},
        "allowed_values": {
            "sleeve_type": [
                "Long", "Short", "3/4", "Sleeveless", "Bell", "Puff"
            ]
        }
    },
    
    "TankTop": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": {},
        "defaults": {},
        "allowed_values": {}
    },
    
    "Sweater": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Cotton"},
        "allowed_values": {
            "material": [
                "Cotton", "Wool", "Cashmere", "Acrylic", "Alpaca", "Merino"
            ]
        }
    },
    
    "Hoodie": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["has_zipper"],
        "defaults": {"has_zipper": False},
        "allowed_values": {
            "has_zipper": [True, False]
        }
    },
    
    "Sweatshirt": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": {},
        "defaults": {},
        "allowed_values": {}
    },
    
    "Cardigan": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Wool"},
        "allowed_values": {
            "material": [
                "Wool", "Cotton", "Cashmere", "Acrylic", "Alpaca"
            ]
        }
    },
    
    "WorkoutTop": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Tank"},
        "allowed_values": {
            "style": [
                "Tank", "T-Shirt", "Long Sleeve", "Crop Top", "Sports Bra"
            ]
        }
    }
}

# Common color options (can be extended)
COMMON_COLORS = [
    "White", "Black", "Gray", "Grey", "Navy", "Blue", "Light Blue", "Dark Blue",
    "Red", "Burgundy", "Maroon", "Pink", "Hot Pink", "Purple", "Lavender",
    "Green", "Forest Green", "Olive", "Lime", "Mint", "Yellow", "Gold",
    "Orange", "Brown", "Tan", "Beige", "Cream", "Khaki", "Silver",
    "Multicolor", "Printed", "Patterned"
]

# Size options
SIZES = [
    "XS", "S", "M", "L", "XL", "XXL", "XXXL",
    "0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20"
]

# Fit types that can apply to various tops
FITS = [
    "Slim", "Regular", "Relaxed", "Loose", "Fitted", "Oversized",
    "Tailored", "Straight", "Cropped", "Tunic", "Bodycon", "A-Line"
]

# Neckline options
NECKLINES = [
    "Crew Neck", "V-Neck", "Scoop Neck", "Round Neck", "High Neck",
    "Turtleneck", "Mock Neck", "Boat Neck", "Off Shoulder", "One Shoulder",
    "Halter", "Square Neck", "Sweetheart", "Deep V", "Cowl Neck",
    "Keyhole", "Choker Neck", "Strapless"
]

# Fabric textures and finishes
FABRIC_TEXTURES = [
    "Smooth", "Textured", "Ribbed", "Cable Knit", "Waffle Knit",
    "Jersey", "French Terry", "Fleece", "Velour", "Satin",
    "Matte", "Glossy", "Metallic", "Sequined", "Beaded",
    "Embroidered", "Lace", "Mesh", "Perforated"
]

# Season appropriateness
SEASONS = [
    "Spring", "Summer", "Fall", "Winter", "All Season",
    "Transitional", "Layering"
]

def validate_parameters(clothing_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for a specific clothing type.
    
    Args:
        clothing_type (str): The type of clothing
        parameters (Dict[str, Any]): Parameters to validate
        
    Returns:
        Dict[str, Any]: Validation results with errors and warnings
    """
    if clothing_type not in PARAMETER_CONFIG:
        return {
            "valid": False,
            "errors": [f"Unknown clothing type: {clothing_type}"],
            "warnings": []
        }
    
    config = PARAMETER_CONFIG[clothing_type]
    errors = []
    warnings = []
    
    # Check required parameters
    for param in config["required_params"]:
        if param not in parameters:
            errors.append(f"Missing required parameter: {param}")
    
    # Check parameter values against allowed values
    for param, value in parameters.items():
        if param in config.get("allowed_values", {}):
            allowed = config["allowed_values"][param]
            if value not in allowed:
                warnings.append(f"Parameter '{param}' value '{value}' not in recommended list: {allowed}")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def get_default_parameters(clothing_type: str) -> Dict[str, Any]:
    """
    Get default parameters for a clothing type.
    
    Args:
        clothing_type (str): The type of clothing
        
    Returns:
        Dict[str, Any]: Default parameters
    """
    if clothing_type not in PARAMETER_CONFIG:
        return {}
    
    return PARAMETER_CONFIG[clothing_type].get("defaults", {})

def get_allowed_values(clothing_type: str, parameter: str) -> List[Any]:
    """
    Get allowed values for a specific parameter of a clothing type.
    
    Args:
        clothing_type (str): The type of clothing
        parameter (str): The parameter name
        
    Returns:
        List[Any]: List of allowed values
    """
    if clothing_type not in PARAMETER_CONFIG:
        return []
    
    config = PARAMETER_CONFIG[clothing_type]
    return config.get("allowed_values", {}).get(parameter, [])