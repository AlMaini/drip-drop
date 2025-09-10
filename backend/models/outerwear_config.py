"""
Configuration for outerwear clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the outerwear category
CLOTHING_TYPES = [
    "Jacket",
    "Blazer",
    "Coat",
    "WinterCoat",
    "RainJacket",
    "Windbreaker",
    "Vest"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Jacket": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Denim"},
        "allowed_values": {
            "material": [
                "Denim", "Leather", "Cotton", "Polyester", "Nylon"
            ]
        }
    },
    
    "Blazer": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Single-Breasted"},
        "allowed_values": {
            "style": [
                "Single-Breasted", "Double-Breasted", "Unstructured", "Fitted"
            ]
        }
    },
    
    "Coat": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Mid-Length"},
        "allowed_values": {
            "length": [
                "Short", "Mid-Length", "Long", "Trench", "Pea Coat"
            ]
        }
    },
    
    "WinterCoat": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["insulation"],
        "defaults": {"insulation": "Down"},
        "allowed_values": {
            "insulation": [
                "Down", "Synthetic", "Wool", "Fleece", "Thinsulate"
            ]
        }
    },
    
    "RainJacket": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["waterproof"],
        "defaults": {"waterproof": True},
        "allowed_values": {
            "waterproof": [True, False]
        }
    },
    
    "Windbreaker": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": [],
        "defaults": {},
        "allowed_values": {}
    },
    
    "Vest": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Puffer"},
        "allowed_values": {
            "style": [
                "Puffer", "Fleece", "Wool", "Down", "Utility"
            ]
        }
    }
}

# Closure types for outerwear
CLOSURE_TYPES = [
    "Zipper", "Button", "Snap", "Hook and Eye", "Toggle", "Drawstring",
    "Velcro", "Magnetic", "Two-Way Zipper", "Hidden Zipper", "Exposed Zipper",
    "Open Front", "Wrap", "Belt", "Buckle"
]

# Hood styles
HOOD_STYLES = [
    "No Hood", "Fixed Hood", "Detachable Hood", "Fur Trim Hood",
    "Drawstring Hood", "Adjustable Hood", "Lined Hood", "Unlined Hood",
    "Oversized Hood", "Fitted Hood", "Roll-Up Hood"
]

# Collar styles
COLLAR_STYLES = [
    "Stand Collar", "Shirt Collar", "Notched Lapel", "Peak Lapel",
    "Shawl Collar", "Mandarin Collar", "Mock Neck", "Turtleneck",
    "Cowl Neck", "Funnel Neck", "No Collar", "Zip-Up Collar",
    "Fold-Over Collar", "Military Collar"
]

# Sleeve styles
SLEEVE_STYLES = [
    "Long Sleeve", "Short Sleeve", "3/4 Sleeve", "Sleeveless",
    "Raglan Sleeve", "Set-In Sleeve", "Dolman Sleeve", "Bell Sleeve",
    "Puff Sleeve", "Gathered Sleeve", "Adjustable Sleeve", "Roll-Up Sleeve"
]

# Fit types
FIT_TYPES = [
    "Slim Fit", "Regular Fit", "Relaxed Fit", "Oversized", "Fitted",
    "Loose", "Tailored", "Boxy", "Cropped", "Long", "Tunic",
    "A-Line", "Straight", "Flared"
]

# Pocket styles
POCKET_STYLES = [
    "No Pockets", "Chest Pockets", "Hand Pockets", "Side Pockets",
    "Interior Pockets", "Cargo Pockets", "Patch Pockets", "Welt Pockets",
    "Slash Pockets", "Zippered Pockets", "Snap Pockets", "Button Pockets",
    "Hidden Pockets", "Multiple Pockets"
]

# Weather protection features
WEATHER_FEATURES = [
    "Waterproof", "Water Resistant", "Water Repellent", "Windproof",
    "Wind Resistant", "Breathable", "Insulated", "Thermal", "UV Protection",
    "Moisture Wicking", "Quick Dry", "Sealed Seams", "Taped Seams"
]

# Lining types
LINING_TYPES = [
    "No Lining", "Full Lining", "Partial Lining", "Quilted Lining",
    "Fleece Lining", "Sherpa Lining", "Fur Lining", "Thermal Lining",
    "Mesh Lining", "Satin Lining", "Polyester Lining", "Cotton Lining"
]

# Outerwear styles
OUTERWEAR_STYLES = [
    "Bomber", "Moto", "Biker", "Military", "Utility", "Safari",
    "Trench", "Peacoat", "Duffle", "Parka", "Anorak", "Poncho",
    "Cape", "Cloak", "Wrap", "Kimono", "Cardigan", "Shrug",
    "Bolero", "Cropped", "Longline", "Duster"
]

# Season appropriateness
SEASONS = [
    "Spring", "Summer", "Fall", "Winter", "All Season", "Transitional",
    "Light Layer", "Heavy Layer", "Mid Layer", "Outer Layer"
]

# Formality levels
FORMALITY_LEVELS = [
    "Casual", "Smart Casual", "Business Casual", "Business", "Formal",
    "Black Tie", "Evening", "Cocktail", "Dressy", "Relaxed"
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