"""
Configuration for bottoms clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the bottoms category
CLOTHING_TYPES = [
    "Pants",
    "Shorts", 
    "Jeans",
    "DressPants",
    "Trousers",
    "Chinos",
    "Skirt",
    "Leggings",
    "SweatPants",
    "Joggers",
    "AthleticShorts",
    "YogaPants"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Pants": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["fit"],
        "defaults": {"fit": "Regular"},
        "allowed_values": {
            "fit": [
                "Regular", "Slim", "Relaxed", "Straight", "Bootcut", "Wide Leg"
            ]
        }
    },
    
    "Shorts": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Knee-Length"},
        "allowed_values": {
            "length": [
                "Knee-Length", "Mid-Thigh", "Bermuda", "Hot Pants", "Basketball"
            ]
        }
    },
    
    "Jeans": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["fit"],
        "defaults": {"fit": "Regular"},
        "allowed_values": {
            "fit": [
                "Regular", "Slim", "Skinny", "Straight", "Bootcut", "Relaxed", "Wide Leg"
            ]
        }
    },
    
    "DressPants": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Wool"},
        "allowed_values": {
            "material": [
                "Wool", "Cotton", "Polyester", "Linen", "Silk"
            ]
        }
    },
    
    "Trousers": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["fit"],
        "defaults": {"fit": "Regular"},
        "allowed_values": {
            "fit": [
                "Regular", "Slim", "Straight", "Relaxed", "Wide Leg",
                "Tapered", "Cropped", "Pleated", "Flat Front", "Cuffed",
                "High Waisted", "Mid Rise", "Low Rise", "Palazzo"
            ]
        }
    },
    
    "Chinos": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["fit"],
        "defaults": {"fit": "Slim"},
        "allowed_values": {
            "fit": [
                "Slim", "Regular", "Straight", "Tapered", "Relaxed",
                "Cropped", "Ankle", "High Waisted", "Mid Rise", "Low Rise",
                "Flat Front", "Pleated", "Cuffed"
            ]
        }
    },
    
    "Skirt": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Knee-Length"},
        "allowed_values": {
            "length": [
                "Mini", "Knee-Length", "Midi", "Maxi", "Floor-Length"
            ]
        }
    },
    
    "Leggings": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Cotton Blend"},
        "allowed_values": {
            "material": [
                "Cotton Blend", "Spandex", "Polyester", "Nylon Blend"
            ]
        }
    },
    
    "SweatPants": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["fit"],
        "defaults": {"fit": "Regular"},
        "allowed_values": {
            "fit": [
                "Regular", "Slim", "Relaxed", "Loose", "Tapered", "Straight",
                "Cuffed", "Open Hem", "High Waisted", "Mid Rise", "Low Rise",
                "Cropped", "Full Length", "Fleece", "French Terry"
            ]
        }
    },
    
    "Joggers": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Cotton Blend"},
        "allowed_values": {
            "material": [
                "Cotton Blend", "Polyester", "French Terry", "Fleece",
                "Modal", "Bamboo", "Performance", "Moisture Wicking",
                "Breathable", "Stretch", "Organic Cotton"
            ]
        }
    },
    
    "AthleticShorts": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Mid-Thigh"},
        "allowed_values": {
            "length": [
                "Short", "Mid-Thigh", "Knee-Length", "Long", "Compression",
                "Loose Fit", "Basketball", "Running", "Training", "Board",
                "Swim", "Cycling", "Tennis", "Golf"
            ]
        }
    },
    
    "YogaPants": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Spandex Blend"},
        "allowed_values": {
            "material": [
                "Spandex Blend", "Lycra", "Nylon Blend", "Polyester Blend",
                "Bamboo", "Modal", "Cotton Blend", "Compression", "Performance",
                "Moisture Wicking", "Four-Way Stretch", "Seamless", "Buttery Soft"
            ]
        }
    }
}

# Common waist styles
WAIST_STYLES = [
    "High Waisted", "Mid Rise", "Low Rise", "Natural Waist",
    "Empire", "Drop Waist", "Elastic Waist", "Drawstring",
    "Belt Loops", "No Belt Loops", "Paper Bag Waist"
]

# Length categories
LENGTHS = [
    "Micro", "Mini", "Short", "Mid-Thigh", "Knee-Length", "Below Knee",
    "Midi", "Tea Length", "Ankle", "Full Length", "Maxi", "Floor Length",
    "Cropped", "Capri", "7/8 Length", "Bermuda"
]

# Closure types
CLOSURES = [
    "Button Fly", "Zip Fly", "Elastic Waist", "Drawstring", "Hook and Eye",
    "Side Zip", "Back Zip", "Pull On", "Snap", "Tie", "Wrap"
]

# Pocket styles
POCKET_STYLES = [
    "No Pockets", "Front Pockets", "Back Pockets", "Side Pockets",
    "Cargo Pockets", "Patch Pockets", "Welt Pockets", "Slash Pockets",
    "Coin Pocket", "Phone Pocket", "Hidden Pockets"
]

# Hem styles
HEM_STYLES = [
    "Straight Hem", "Raw Hem", "Rolled Hem", "Cuffed", "Frayed",
    "Asymmetrical", "High-Low", "Scalloped", "Lettuce Edge",
    "Blind Hem", "Faced Hem"
]

# Common patterns for bottoms
PATTERNS = [
    "Solid", "Striped", "Plaid", "Checkered", "Polka Dot", "Floral",
    "Geometric", "Animal Print", "Camouflage", "Tie Dye", "Ombre",
    "Color Block", "Gradient", "Abstract", "Paisley"
]

# Denim washes (for jeans)
DENIM_WASHES = [
    "Raw", "Light Wash", "Medium Wash", "Dark Wash", "Black",
    "Stone Washed", "Acid Washed", "Bleached", "Vintage", "Faded",
    "Distressed", "Clean", "Rinse", "Indigo", "White"
]

# Skirt styles
SKIRT_STYLES = [
    "A-Line", "Pencil", "Pleated", "Circle", "Straight", "Wrap",
    "Tulip", "Bubble", "Tiered", "Asymmetrical", "Mermaid",
    "Trumpet", "Godet", "Flare", "Fit and Flare"
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