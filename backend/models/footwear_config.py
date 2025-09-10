"""
Configuration for footwear clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the footwear category
CLOTHING_TYPES = [
    "Sneakers",
    "DressShoes",
    "Boots",
    "Sandals",
    "Flats",
    "Heels",
    "AthleticShoes"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Sneakers": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Athletic"},
        "allowed_values": {
            "style": [
                "Athletic", "Casual", "High-Top", "Low-Top", "Slip-On"
            ]
        }
    },
    
    "DressShoes": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Oxford"},
        "allowed_values": {
            "style": [
                "Oxford", "Derby", "Loafer", "Monk Strap", "Brogue"
            ]
        }
    },
    
    "Boots": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["height"],
        "defaults": {"height": "Ankle"},
        "allowed_values": {
            "height": [
                "Ankle", "Mid-Calf", "Knee-High", "Thigh-High", "Combat", "Chelsea"
            ]
        }
    },
    
    "Sandals": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Flat"},
        "allowed_values": {
            "style": [
                "Flat", "Gladiator", "Flip-Flop", "Platform", "Wedge"
            ]
        }
    },
    
    "Flats": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Ballet"},
        "allowed_values": {
            "style": [
                "Ballet", "Pointed Toe", "Round Toe", "Square Toe", "Loafer"
            ]
        }
    },
    
    "Heels": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["height"],
        "defaults": {"height": "Medium"},
        "allowed_values": {
            "height": [
                "Low", "Medium", "High", "Platform", "Stiletto"
            ]
        }
    },
    
    "AthleticShoes": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["sport"],
        "defaults": {"sport": "Running"},
        "allowed_values": {
            "sport": [
                "Running", "Basketball", "Tennis", "Cross-Training", "Soccer"
            ]
        }
    }
}

# Shoe sizes (US sizing)
SIZES = [
    # Women's sizes
    "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12",
    # Men's sizes  
    "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12", "12.5", "13", "13.5", "14", "15"
]

# Shoe widths
WIDTHS = [
    "AAAA", "AAA", "AA", "A", "B", "C", "D", "E", "EE", "EEE", "EEEE",
    "Narrow", "Medium", "Wide", "Extra Wide"
]

# Materials for footwear
MATERIALS = [
    "Leather", "Genuine Leather", "Full Grain Leather", "Top Grain Leather",
    "Patent Leather", "Suede", "Nubuck", "Canvas", "Mesh", "Synthetic",
    "Rubber", "Vinyl", "Fabric", "Denim", "Satin", "Silk", "Velvet",
    "Cork", "Jute", "Rope", "Plastic", "Wood", "Metal", "Chain"
]

# Toe shapes
TOE_SHAPES = [
    "Round", "Pointed", "Square", "Almond", "Oval", "Chisel", "Oblique",
    "Open", "Closed", "Peep", "Cut-Out"
]

# Heel types (for heeled shoes)
HEEL_TYPES = [
    "Stiletto", "Block", "Chunky", "Kitten", "Platform", "Wedge", "Cone",
    "Curved", "Flare", "Louis", "Cuban", "Continental", "Comma", "Needle",
    "Pyramid", "Spool", "Tapered"
]

# Fastening types
FASTENINGS = [
    "Lace-Up", "Slip-On", "Velcro", "Hook and Loop", "Buckle", "Strap",
    "Zipper", "Elastic", "Toggle", "Button", "Snap", "Tie", "Wrap"
]

# Sole types
SOLE_TYPES = [
    "Rubber", "Leather", "Synthetic", "Crepe", "Vibram", "EVA", "PU",
    "Cork", "Wood", "Platform", "Wedge", "Flat", "Cushioned", "Gel",
    "Air", "Memory Foam", "Athletic", "Dress", "Work", "Non-Slip"
]

# Occasion categories
OCCASIONS = [
    "Casual", "Formal", "Business", "Athletic", "Evening", "Wedding",
    "Party", "Work", "Outdoor", "Beach", "Travel", "Comfort", "Fashion",
    "Special Occasion", "Everyday", "Weekend", "Professional"
]

# Shoe features
FEATURES = [
    "Waterproof", "Water Resistant", "Breathable", "Non-Slip", "Cushioned",
    "Arch Support", "Orthopedic", "Memory Foam", "Gel Insert", "Air Cushion",
    "Shock Absorbing", "Flexible", "Lightweight", "Durable", "Steel Toe",
    "Composite Toe", "Slip Resistant", "Oil Resistant", "Insulated",
    "Lined", "Unlined", "Perforated", "Ventilated"
]

# Lacing styles
LACING_STYLES = [
    "Standard", "Straight Bar", "Ladder", "Zigzag", "Army", "Railway",
    "Spider Web", "Checkerboard", "Hash", "Double Back", "Loop Back",
    "Bow Tie", "Hidden Knot", "Ian Knot", "Surgeon's Knot"
]

# Brand categories (generic)
BRAND_CATEGORIES = [
    "Luxury", "Designer", "Premium", "Mid-Range", "Budget", "Athletic",
    "Performance", "Comfort", "Fashion", "Classic", "Contemporary",
    "Vintage", "Artisan", "Handmade", "Mass Market", "Specialty"
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