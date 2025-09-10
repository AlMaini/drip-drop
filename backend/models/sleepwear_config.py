"""
Configuration for sleepwear clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the sleepwear category
CLOTHING_TYPES = [
    "Pajamas",
    "Nightgown",
    "Robe"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Pajamas": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Set"},
        "allowed_values": {
            "style": [
                "Set", "Top Only", "Bottom Only", "One Piece", "Shorts Set"
            ]
        }
    },
    
    "Nightgown": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Knee-Length"},
        "allowed_values": {
            "length": [
                "Short", "Knee-Length", "Mid-Calf", "Long", "Floor-Length"
            ]
        }
    },
    
    "Robe": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["material"],
        "defaults": {"material": "Cotton"},
        "allowed_values": {
            "material": [
                "Cotton", "Silk", "Terry Cloth", "Fleece", "Satin"
            ]
        }
    }
}

# Pajama styles and types
PAJAMA_STYLES = [
    "Traditional", "Classic", "Button-Up", "Pullover", "Henley", "V-Neck",
    "Crew Neck", "Scoop Neck", "Tank Top", "Camisole", "Shorts", "Long Pants",
    "Capri", "3/4 Length", "Ankle Length", "Cropped", "Footed", "Onesie",
    "Union Suit", "Long Johns", "Thermal"
]

# Nightgown styles
NIGHTGOWN_STYLES = [
    "Slip", "Chemise", "Babydoll", "A-Line", "Fit and Flare", "Shift",
    "Empire Waist", "Princess", "Tent", "Straight", "Wrap", "Kimono",
    "Button-Up", "Pullover", "Sleep Shirt", "Sleep Dress"
]

# Robe styles
ROBE_STYLES = [
    "Bathrobe", "Kimono", "Wrap", "Shawl Collar", "Hooded", "Zip-Up",
    "Button-Up", "Open Front", "Belted", "Sash Tie", "Short", "Long",
    "3/4 Length", "Full Length", "Spa", "Hotel", "Luxury", "Plush"
]

# Sleeve lengths
SLEEVE_LENGTHS = [
    "Sleeveless", "Tank", "Cap Sleeve", "Short Sleeve", "3/4 Sleeve",
    "Long Sleeve", "Extended Sleeve", "Bell Sleeve", "Kimono Sleeve",
    "Raglan Sleeve", "Set-In Sleeve"
]

# Neckline styles
NECKLINES = [
    "Crew Neck", "V-Neck", "Scoop Neck", "Round Neck", "Square Neck",
    "Boat Neck", "Off Shoulder", "One Shoulder", "Halter", "High Neck",
    "Mock Neck", "Turtleneck", "Cowl Neck", "Keyhole", "Button-Up Collar",
    "Shawl Collar", "Notched Collar"
]

# Bottom styles (for pajama bottoms)
BOTTOM_STYLES = [
    "Straight Leg", "Wide Leg", "Bootcut", "Tapered", "Relaxed Fit",
    "Loose Fit", "Fitted", "Skinny", "Capri", "Shorts", "Boy Shorts",
    "Bermuda", "Mid-Thigh", "Above Knee", "Knee Length", "Long Pants",
    "Full Length", "Ankle Length", "Cropped"
]

# Waistband types
WAISTBAND_TYPES = [
    "Elastic", "Drawstring", "Tie", "Adjustable", "Wide Elastic",
    "Fold-Over", "Yoga Style", "Low Rise", "Mid Rise", "High Rise",
    "Natural Waist", "Empire", "Drop Waist"
]

# Fabric weights
FABRIC_WEIGHTS = [
    "Lightweight", "Medium Weight", "Heavyweight", "Ultra Light", "Gossamer",
    "Sheer", "Opaque", "Semi-Sheer", "Thick", "Thin", "Plush", "Smooth"
]

# Fabric textures
FABRIC_TEXTURES = [
    "Smooth", "Soft", "Silky", "Crisp", "Brushed", "Napped", "Ribbed",
    "Waffle", "Honeycomb", "Textured", "Plush", "Fuzzy", "Sleek", "Matte",
    "Shiny", "Lustrous", "Peached", "Sueded"
]

# Patterns for sleepwear
PATTERNS = [
    "Solid", "Striped", "Polka Dot", "Floral", "Paisley", "Geometric",
    "Abstract", "Animal Print", "Heart", "Star", "Moon", "Cloud",
    "Plaid", "Checkered", "Gingham", "Toile", "Damask", "Lace Print"
]

# Colors commonly used for sleepwear
SLEEPWEAR_COLORS = [
    "White", "Ivory", "Cream", "Beige", "Nude", "Blush", "Pink", "Rose",
    "Lavender", "Purple", "Blue", "Navy", "Light Blue", "Mint", "Green",
    "Gray", "Charcoal", "Black", "Red", "Burgundy", "Yellow", "Peach"
]

# Closure types
CLOSURES = [
    "Button-Up", "Snap", "Zip", "Tie", "Wrap", "Pullover", "Open Front",
    "Hidden Buttons", "Partial Button", "Henley", "Quarter Zip", "Full Zip"
]

# Features
FEATURES = [
    "Pockets", "Side Pockets", "Chest Pocket", "No Pockets", "Piping",
    "Contrasting Trim", "Lace Trim", "Embroidered", "Monogrammed",
    "Personalized", "Matching Set", "Mix and Match", "Coordinating",
    "Reversible", "Two-Sided", "Lined", "Unlined"
]

# Seasons
SEASONS = [
    "Summer", "Winter", "Spring", "Fall", "All Season", "Warm Weather",
    "Cool Weather", "Transitional", "Holiday", "Year Round"
]

# Care instructions
CARE_INSTRUCTIONS = [
    "Machine Wash", "Hand Wash", "Delicate Cycle", "Cold Water", "Warm Water",
    "Tumble Dry Low", "Air Dry", "Line Dry", "Lay Flat", "Do Not Bleach",
    "Iron Low Heat", "Do Not Iron", "Dry Clean", "Pre-Shrunk", "Color Safe"
]

# Size ranges
SIZES = [
    "XS", "S", "M", "L", "XL", "XXL", "XXXL", "Plus Size",
    "0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"
]

# Fit types
FIT_TYPES = [
    "Relaxed", "Loose", "Comfortable", "Roomy", "Oversized", "Fitted",
    "Slim", "Regular", "Classic", "Traditional", "Modern", "Contemporary"
]

# Occasion types
OCCASIONS = [
    "Everyday", "Sleep", "Lounging", "Relaxing", "Weekend", "Vacation",
    "Travel", "Hospital", "Maternity", "Nursing", "Post-Surgery",
    "Recovery", "Spa", "Hotel", "Gift", "Bridal", "Honeymoon"
]

# Age groups
AGE_GROUPS = [
    "Adult", "Teen", "Junior", "Misses", "Womens", "Mens", "Unisex",
    "Maternity", "Plus Size", "Petite", "Tall"
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