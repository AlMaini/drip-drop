"""
Configuration for dresses clothing category including all parameters and allowed values.
"""

from typing import Dict, List, Any

# Available clothing types in the dresses category
CLOTHING_TYPES = [
    "CasualDress",
    "FormalDress",
    "MaxiDress",
    "MiniDress",
    "Jumpsuit",
    "Romper"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "CasualDress": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Knee-Length"},
        "allowed_values": {
            "length": [
                "Mini", "Knee-Length", "Midi", "Maxi", "Floor-Length"
            ]
        }
    },
    
    "FormalDress": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["length"],
        "defaults": {"length": "Floor-Length"},
        "allowed_values": {
            "length": [
                "Cocktail", "Tea Length", "Midi", "Knee-Length", "Ankle Length",
                "Floor Length", "Chapel Train", "Court Train", "Cathedral Train",
                "Sweep Train", "Brush Train", "Watteau Train"
            ]
        }
    },
    
    "MaxiDress": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": [],
        "defaults": {},
        "allowed_values": {}
    },
    
    "MiniDress": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": [],
        "defaults": {},
        "allowed_values": {}
    },
    
    "Jumpsuit": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["style"],
        "defaults": {"style": "Long"},
        "allowed_values": {
            "style": [
                "Long", "Cropped", "Wide Leg", "Fitted", "Culotte"
            ]
        }
    },
    
    "Romper": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": [],
        "defaults": {},
        "allowed_values": {}
    }
}

# Dress silhouettes and styles
DRESS_SILHOUETTES = [
    "A-Line", "Fit and Flare", "Sheath", "Shift", "Wrap", "Bodycon",
    "Mermaid", "Trumpet", "Ball Gown", "Empire", "Princess", "Column",
    "Straight", "Tent", "Tunic", "Babydoll", "Peplum", "Asymmetrical",
    "High-Low", "Two-Piece", "Cut-Out", "Backless", "Halter"
]

# Neckline styles
NECKLINES = [
    "Crew Neck", "Scoop Neck", "V-Neck", "Deep V", "Square Neck", "Boat Neck",
    "Off Shoulder", "One Shoulder", "Cold Shoulder", "Halter", "High Neck",
    "Turtleneck", "Mock Neck", "Cowl Neck", "Keyhole", "Sweetheart",
    "Strapless", "Bandeau", "Plunge", "Asymmetrical", "Round Neck"
]

# Sleeve styles
SLEEVE_STYLES = [
    "Sleeveless", "Strapless", "Cap Sleeve", "Short Sleeve", "3/4 Sleeve",
    "Long Sleeve", "Bell Sleeve", "Puff Sleeve", "Bishop Sleeve", "Balloon Sleeve",
    "Flutter Sleeve", "Kimono Sleeve", "Dolman Sleeve", "Raglan Sleeve",
    "Cold Shoulder", "Cut-Out Sleeve", "Sheer Sleeve", "Lace Sleeve"
]

# Dress lengths
DRESS_LENGTHS = [
    "Micro Mini", "Mini", "Above Knee", "Knee-Length", "Below Knee",
    "Midi", "Tea Length", "Calf Length", "Ankle Length", "Maxi",
    "Floor Length", "Sweep", "Court Train", "Chapel Train", "Cathedral Train"
]

# Waistlines
WAISTLINES = [
    "Natural", "High Waisted", "Empire", "Drop Waist", "Basque",
    "Princess", "No Waist", "Belted", "Sash", "Corset", "Fitted"
]

# Dress occasions
OCCASIONS = [
    "Casual", "Work", "Business", "Cocktail", "Semi-Formal", "Formal",
    "Black Tie", "Wedding Guest", "Mother of Bride", "Bridesmaid",
    "Prom", "Homecoming", "Graduation", "Party", "Holiday", "Date Night",
    "Vacation", "Beach", "Summer", "Spring", "Fall", "Winter"
]

# Fabric types for dresses
FABRIC_TYPES = [
    "Cotton", "Linen", "Silk", "Chiffon", "Georgette", "Crepe", "Satin",
    "Taffeta", "Organza", "Tulle", "Lace", "Velvet", "Velour", "Jersey",
    "Knit", "Ponte", "Scuba", "Neoprene", "Polyester", "Viscose",
    "Rayon", "Modal", "Spandex", "Elastane", "Denim", "Corduroy"
]

# Dress patterns
PATTERNS = [
    "Solid", "Striped", "Polka Dot", "Floral", "Abstract", "Geometric",
    "Animal Print", "Paisley", "Plaid", "Checkered", "Tie Dye", "Ombre",
    "Color Block", "Lace", "Embroidered", "Beaded", "Sequined", "Metallic"
]

# Dress features
FEATURES = [
    "Lined", "Unlined", "Built-in Bra", "Padded Bra", "Removable Straps",
    "Adjustable Straps", "Zipper", "Button Up", "Wrap Style", "Tie Waist",
    "Pockets", "Side Slits", "Back Slit", "Pleated", "Ruched", "Gathered",
    "Smocked", "Shirred", "Draped", "Layered", "Ruffles", "Fringe"
]

# Closure types
CLOSURES = [
    "Back Zip", "Side Zip", "Front Zip", "Hidden Zip", "Invisible Zip",
    "Button Up", "Snap", "Hook and Eye", "Tie", "Wrap", "Pull Over",
    "Pullover", "Slip On", "Lace Up", "Corset Back", "Open Back"
]

# Jumpsuit leg styles
JUMPSUIT_LEG_STYLES = [
    "Straight", "Wide Leg", "Palazzo", "Culotte", "Cropped", "Ankle Length",
    "Full Length", "Skinny", "Fitted", "Loose", "Tapered", "Flare",
    "Bootcut", "High Waisted", "Mid Rise", "Low Rise"
]

# Romper styles
ROMPER_STYLES = [
    "Shorts", "Fitted Shorts", "Loose Shorts", "High Waisted", "Mid Rise",
    "Strapless", "Halter", "Off Shoulder", "Long Sleeve", "Short Sleeve",
    "Sleeveless", "Wrap", "Button Up", "Zip Front", "Tie Front"
]

# Formality levels
FORMALITY_LEVELS = [
    "Very Casual", "Casual", "Smart Casual", "Business Casual", "Semi-Formal",
    "Cocktail", "Formal", "Black Tie Optional", "Black Tie", "White Tie"
]

# Season appropriateness
SEASONS = [
    "Spring", "Summer", "Fall", "Winter", "All Season", "Transitional",
    "Holiday", "Resort", "Cruise", "Destination Wedding"
]

# Body types (for styling recommendations)
BODY_TYPES = [
    "Pear", "Apple", "Hourglass", "Rectangle", "Inverted Triangle",
    "Petite", "Plus Size", "Tall", "Curvy", "Athletic"
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