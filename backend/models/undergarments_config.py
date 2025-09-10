"""
Configuration for undergarments clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the undergarments category
CLOTHING_TYPES = [
    "Underwear",
    "Bra",
    "SportsBra",
    "Undershirt",
    "Socks",
    "Pantyhose",
    "Tights"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Underwear": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Brief"},
        "allowed_values": {
            "style": [
                "Brief", "Boxer", "Boxer Brief", "Thong", "Bikini"
            ]
        }
    },
    
    "Bra": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Regular"},
        "allowed_values": {
            "style": [
                "Regular", "Push-Up", "Wireless", "Padded", "Strapless"
            ]
        }
    },
    
    "SportsBra": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["support_level"],
        "defaults": {"support_level": "Medium"},
        "allowed_values": {
            "support_level": [
                "Low", "Medium", "High", "Maximum"
            ]
        }
    },
    
    "Undershirt": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Crew Neck"},
        "allowed_values": {
            "style": [
                "Crew Neck", "V-Neck", "Tank Top", "Long Sleeve"
            ]
        }
    },
    
    "Socks": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Crew"},
        "allowed_values": {
            "length": [
                "Ankle", "Crew", "Mid-Calf", "Knee-High", "No-Show"
            ]
        }
    },
    
    "Pantyhose": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["denier"],
        "defaults": {"denier": 15},
        "allowed_values": {
            "denier": [5, 8, 10, 12, 15, 20, 30, 40, 50, 60, 70, 80]
        }
    },
    
    "Tights": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["denier"],
        "defaults": {"denier": 40},
        "allowed_values": {
            "denier": [40, 50, 60, 70, 80, 90, 100, 120, 150, 200, 250, 300]
        }
    }
}

# Underwear sizes
UNDERWEAR_SIZES = [
    "XS", "S", "M", "L", "XL", "XXL", "XXXL",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
]

# Bra sizes
BRA_BAND_SIZES = ["30", "32", "34", "36", "38", "40", "42", "44", "46", "48", "50"]
BRA_CUP_SIZES = ["AA", "A", "B", "C", "D", "DD", "DDD", "E", "F", "G", "H", "I", "J"]

# Sock sizes
SOCK_SIZES = [
    "XS", "S", "M", "L", "XL",
    "6-8", "8-10", "9-11", "10-12", "12-14", "13-15",
    "One Size"
]

# Hosiery sizes
HOSIERY_SIZES = [
    "XS", "S", "M", "L", "XL", "XXL",
    "A", "B", "C", "D", "E", "Queen", "Plus Size"
]

# Materials for undergarments
MATERIALS = [
    "Cotton", "Organic Cotton", "Modal", "Bamboo", "Microfiber", "Polyester",
    "Nylon", "Spandex", "Lycra", "Elastane", "Silk", "Lace", "Mesh",
    "Satin", "Polyamide", "Viscose", "Rayon", "Wool", "Merino Wool",
    "Cashmere", "Alpaca", "Performance", "Moisture Wicking", "Antimicrobial"
]

# Construction types
CONSTRUCTION_TYPES = [
    "Seamless", "Flat Seam", "Traditional Seam", "Laser Cut", "Heat Sealed",
    "Bonded", "Molded", "Knitted", "Woven", "Compression", "Stretch",
    "No Show", "Tag Free", "Label Free"
]

# Features for undergarments
FEATURES = [
    "Breathable", "Moisture Wicking", "Quick Dry", "Antimicrobial", "Odor Control",
    "Temperature Regulating", "Seamless", "Tag Free", "Hypoallergenic",
    "Eco Friendly", "Sustainable", "Organic", "Recycled", "UV Protection",
    "Compression", "Support", "Lift", "Shape", "Control", "Smoothing"
]

# Care instructions
CARE_INSTRUCTIONS = [
    "Machine Wash Cold", "Hand Wash", "Delicate Cycle", "Air Dry", "Tumble Dry Low",
    "No Bleach", "No Fabric Softener", "Wash Dark Colors Separately",
    "Turn Inside Out", "Use Lingerie Bag", "Line Dry", "Lay Flat to Dry"
]

# Color categories for nude/skin tones
NUDE_TONES = [
    "Fair", "Light", "Medium", "Tan", "Deep", "Rich", "Universal Nude",
    "Ivory", "Beige", "Caramel", "Chocolate", "Cocoa", "Espresso"
]

# Pantyhose/tights types
HOSIERY_TYPES = [
    "Sheer", "Semi Opaque", "Opaque", "Control Top", "Reinforced Toe",
    "Sandal Foot", "Open Toe", "Toeless", "Backseam", "Patterned",
    "Textured", "Fishnet", "Lace", "Cable Knit", "Ribbed", "Footless"
]

# Support levels for bras
SUPPORT_LEVELS = [
    "None", "Light", "Medium", "High", "Maximum", "Ultra Support",
    "Everyday", "Active", "High Impact", "Low Impact", "Medium Impact"
]

# Bra cup shapes
CUP_SHAPES = [
    "Full Cup", "Demi Cup", "3/4 Cup", "1/2 Cup", "Plunge", "Balconette",
    "Push Up", "Contour", "T-Shirt", "Spacer", "Molded", "Unlined",
    "Lightly Lined", "Heavily Padded", "Memory Foam", "Gel"
]

# Underwear rise levels
RISE_LEVELS = [
    "Low Rise", "Mid Rise", "High Rise", "Super High Rise", "Natural Waist",
    "Below Waist", "At Waist", "Above Waist"
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