"""
Configuration for accessories clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the accessories category
CLOTHING_TYPES = [
    "Hat",
    "Cap",
    "Belt",
    "Scarf",
    "Gloves",
    "Sunglasses",
    "Watch"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Hat": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Baseball Cap"},
        "allowed_values": {
            "style": [
                "Baseball Cap", "Beanie", "Fedora", "Beret", "Sun Hat", "Bucket Hat"
            ]
        }
    },
    
    "Cap": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Baseball"},
        "allowed_values": {
            "style": [
                "Baseball", "Snapback", "Trucker", "Dad Hat", "Fitted"
            ]
        }
    },
    
    "Belt": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Leather"},
        "allowed_values": {
            "material": [
                "Leather", "Canvas", "Fabric", "Chain", "Elastic"
            ]
        }
    },
    
    "Scarf": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Wool"},
        "allowed_values": {
            "material": [
                "Wool", "Silk", "Cotton", "Cashmere", "Acrylic"
            ]
        }
    },
    
    "Gloves": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Leather"},
        "allowed_values": {
            "material": [
                "Leather", "Wool", "Cotton", "Synthetic", "Cashmere"
            ]
        }
    },
    
    "Sunglasses": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["lens_color"],
        "defaults": {"lens_color": "Black"},
        "allowed_values": {
            "lens_color": [
                "Black", "Brown", "Blue", "Green", "Gray", "Mirror"
            ]
        }
    },
    
    "Watch": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["band_material"],
        "defaults": {"band_material": "Leather"},
        "allowed_values": {
            "band_material": [
                "Leather", "Metal", "Rubber", "Fabric", "Plastic"
            ]
        }
    }
}

# Hat sizes
HAT_SIZES = [
    "XS", "S", "M", "L", "XL", "XXL",
    "6 1/2", "6 5/8", "6 3/4", "6 7/8", "7", "7 1/8", "7 1/4", "7 3/8", "7 1/2", 
    "7 5/8", "7 3/4", "7 7/8", "8", "One Size", "Adjustable"
]

# Belt sizes (waist measurements)
BELT_SIZES = [
    "XS", "S", "M", "L", "XL", "XXL", "XXXL",
    "28", "30", "32", "34", "36", "38", "40", "42", "44", "46", "48", "50"
]

# Buckle types
BUCKLE_TYPES = [
    "Prong", "Single Prong", "Double Prong", "Plate", "Box Frame",
    "D-Ring", "Slide", "Clip", "Magnetic", "Automatic", "Ratchet",
    "Military", "Western", "Decorative", "Logo", "Plain"
]

# Scarf types and styles
SCARF_TYPES = [
    "Rectangle", "Square", "Triangle", "Circle", "Infinity", "Loop",
    "Blanket", "Wrap", "Shawl", "Pashmina", "Stole", "Cowl", "Snood",
    "Bandana", "Neckerchief", "Ascot", "Cravat", "Pocket Square"
]

# Glove types
GLOVE_TYPES = [
    "Full Finger", "Fingerless", "Mittens", "Convertible", "Touch Screen",
    "Driving", "Work", "Gardening", "Winter", "Thermal", "Waterproof",
    "Dress", "Evening", "Formal", "Casual", "Athletic", "Medical",
    "Disposable", "Reusable", "Lined", "Unlined"
]

# Sunglasses frame styles
FRAME_STYLES = [
    "Aviator", "Wayfarer", "Round", "Square", "Rectangle", "Cat Eye",
    "Oval", "Shield", "Wrap Around", "Butterfly", "Oversized", "Vintage",
    "Retro", "Classic", "Modern", "Sport", "Fashion", "Pilot",
    "Clubmaster", "Browline", "Rimless", "Semi-Rimless", "Full Rim"
]

# Watch types
WATCH_TYPES = [
    "Analog", "Digital", "Chronograph", "Dress", "Sport", "Casual",
    "Smart Watch", "Fitness Tracker", "Dive", "Aviation", "Military",
    "Fashion", "Luxury", "Skeleton", "Automatic", "Quartz", "Mechanical"
]

# Watch case materials
WATCH_CASE_MATERIALS = [
    "Stainless Steel", "Titanium", "Gold", "Rose Gold", "Yellow Gold",
    "White Gold", "Silver", "Platinum", "Aluminum", "Ceramic", "Carbon Fiber",
    "Plastic", "Resin", "Brass", "Bronze", "Copper"
]

# Jewelry finishes
JEWELRY_FINISHES = [
    "Polished", "Brushed", "Matte", "Satin", "Antique", "Vintage",
    "Oxidized", "Plated", "PVD Coated", "DLC Coated", "Two-Tone",
    "Rose Gold Plated", "Gold Plated", "Silver Plated", "Black"
]

# Accessory occasions
OCCASIONS = [
    "Casual", "Formal", "Business", "Evening", "Party", "Wedding",
    "Special Occasion", "Everyday", "Weekend", "Work", "Travel",
    "Sport", "Outdoor", "Beach", "Winter", "Summer"
]

# Care instructions
CARE_INSTRUCTIONS = [
    "Hand Wash", "Machine Wash", "Dry Clean Only", "Spot Clean",
    "Air Dry", "Tumble Dry", "Lay Flat", "Hang to Dry", "Steam",
    "Iron", "Do Not Iron", "Store Flat", "Store Hanging"
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