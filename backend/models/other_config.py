"""
Configuration for 'other' clothing category for unclassified or miscellaneous items.
This category handles any clothing that doesn't fit into the standard categories.
"""

from typing import Dict, List, Any

# Available clothing types in the other category
CLOTHING_TYPES = [
    "Other"
]

# Parameter configurations for each clothing type
PARAMETER_CONFIG = {
    "Other": {
        "required_params": ["id", "name", "primary_color", "secondary_color", "image"],
        "optional_params": ["category", "subcategory", "style", "material", "size", "fit", "length", "occasion"],
        "defaults": {
            "category": "Miscellaneous",
            "subcategory": "Unclassified",
            "style": "General",
            "material": "Unknown",
            "size": "One Size",
            "fit": "Regular",
            "length": "Standard",
            "occasion": "Casual"
        },
        "allowed_values": {
            "category": [
                "Miscellaneous", "Specialty", "Vintage", "Costume", "Performance",
                "Cultural", "Traditional", "Religious", "Medical", "Safety",
                "Work Uniform", "Sports Uniform", "Protective", "Technical",
                "Experimental", "Custom", "Handmade", "Artisan", "Unique"
            ],
            "subcategory": [
                "Unclassified", "Vintage Piece", "Costume", "Theatrical", "Dance",
                "Cosplay", "Historical", "Cultural Dress", "Religious Garment",
                "Work Gear", "Protective Equipment", "Medical Garment", "Athletic Gear",
                "Specialty Item", "Custom Design", "Art Piece", "Experimental",
                "Prototype", "Sample", "One-Off", "Limited Edition"
            ],
            "style": [
                "General", "Vintage", "Retro", "Classic", "Modern", "Contemporary",
                "Traditional", "Cultural", "Ethnic", "Bohemian", "Gothic", "Punk",
                "Grunge", "Hippie", "Preppy", "Minimalist", "Maximalist", "Artsy",
                "Avant-Garde", "Futuristic", "Steampunk", "Victorian", "Medieval",
                "Renaissance", "Art Deco", "Mid-Century", "Industrial", "Military"
            ],
            "material": [
                "Unknown", "Mixed Materials", "Cotton", "Polyester", "Nylon", "Wool",
                "Silk", "Linen", "Leather", "Synthetic", "Natural", "Organic",
                "Recycled", "Sustainable", "Eco-Friendly", "Performance", "Technical",
                "Waterproof", "Breathable", "Stretch", "Non-Stretch", "Metallic",
                "Reflective", "Transparent", "Mesh", "Lace", "Velvet", "Fur",
                "Faux Fur", "Denim", "Canvas", "Vinyl", "Rubber", "Plastic"
            ],
            "size": [
                "One Size", "XS", "S", "M", "L", "XL", "XXL", "XXXL", "Custom",
                "Adjustable", "Variable", "Standard", "Oversized", "Fitted",
                "Plus Size", "Petite", "Tall", "Regular", "Junior", "Adult"
            ],
            "fit": [
                "Regular", "Loose", "Fitted", "Oversized", "Relaxed", "Slim",
                "Tailored", "Custom", "Adjustable", "Flexible", "Structured",
                "Unstructured", "Form-Fitting", "Flowing", "Draped", "Sculpted"
            ],
            "length": [
                "Standard", "Short", "Long", "Mini", "Midi", "Maxi", "Cropped",
                "Extended", "Floor Length", "Ankle Length", "Knee Length",
                "Thigh Length", "Hip Length", "Waist Length", "Variable",
                "Adjustable", "Custom"
            ],
            "occasion": [
                "Casual", "Formal", "Work", "Party", "Special Event", "Performance",
                "Costume", "Athletic", "Outdoor", "Indoor", "Ceremonial",
                "Religious", "Cultural", "Traditional", "Holiday", "Festival",
                "Convention", "Theater", "Film", "Photography", "Art"
            ]
        }
    }
}

# General clothing categories for uncategorized items
GENERAL_CATEGORIES = [
    "Headwear", "Neckwear", "Handwear", "Legwear", "Footwear", "Bodywear",
    "Outerwear", "Underwear", "Accessories", "Jewelry", "Protective Gear",
    "Specialty Clothing", "Performance Wear", "Costume", "Uniform",
    "Cultural Dress", "Religious Garment", "Medical Apparel", "Safety Equipment"
]

# Specialty item types
SPECIALTY_ITEMS = [
    "Apron", "Bib", "Mask", "Collar", "Cuffs", "Garter", "Suspenders",
    "Shoulder Pads", "Petticoat", "Bustle", "Corset", "Girdle", "Crinoline",
    "Farthingale", "Chemise", "Shift", "Smock", "Tabard", "Surplice",
    "Cassock", "Habit", "Vestment", "Regalia", "Insignia", "Badge"
]

# Costume and theatrical items
COSTUME_ITEMS = [
    "Character Costume", "Historical Costume", "Fantasy Costume", "Superhero Costume",
    "Animal Costume", "Mascot Costume", "Halloween Costume", "Carnival Costume",
    "Theatrical Costume", "Opera Costume", "Ballet Costume", "Dance Costume",
    "Stage Wear", "Performance Wear", "Drag Outfit", "Cosplay Outfit"
]

# Work and professional wear
WORK_WEAR = [
    "Chef Coat", "Lab Coat", "Medical Scrubs", "Nurse Uniform", "Doctor Coat",
    "Safety Vest", "Hard Hat", "Work Boots", "Steel Toe Boots", "Coveralls",
    "Overalls", "Jumpsuit", "Boiler Suit", "Hazmat Suit", "Clean Room Suit",
    "Military Uniform", "Police Uniform", "Fire Fighter Gear", "EMT Uniform"
]

# Cultural and traditional items
CULTURAL_ITEMS = [
    "Kimono", "Sari", "Sarong", "Kilt", "Dirndl", "Lederhosen", "Hanbok",
    "Cheongsam", "Qipao", "Dashiki", "Kaftan", "Thobe", "Abaya", "Hijab",
    "Turban", "Keffiyeh", "Poncho", "Serape", "Huipil", "Dhoti", "Lungi"
]

# Religious garments
RELIGIOUS_ITEMS = [
    "Vestment", "Surplice", "Cassock", "Chasuble", "Dalmatic", "Alb", "Amice",
    "Stole", "Maniple", "Biretta", "Zucchetto", "Habit", "Scapular", "Cincture",
    "Tallit", "Kippah", "Phylacteries", "Prayer Shawl", "Burqa", "Niqab"
]

# Sports and athletic specialty items
ATHLETIC_SPECIALTY = [
    "Wetsuit", "Drysuit", "Swimsuit", "Bikini", "Swim Trunks", "Rash Guard",
    "Cycling Jersey", "Cycling Shorts", "Running Tights", "Compression Wear",
    "Base Layer", "Thermal Underwear", "Athletic Supporter", "Sports Cup",
    "Shin Guards", "Knee Pads", "Elbow Pads", "Protective Padding"
]

# Vintage and historical items
VINTAGE_ITEMS = [
    "Victorian Dress", "Edwardian Blouse", "1920s Flapper Dress", "1950s Circle Skirt",
    "1960s Mini Dress", "1970s Bell Bottoms", "1980s Shoulder Pads", "Vintage Suit",
    "Antique Gown", "Historical Reproduction", "Period Costume", "Vintage Accessory"
]

# Materials commonly found in specialty items
SPECIALTY_MATERIALS = [
    "Velvet", "Brocade", "Taffeta", "Organza", "Tulle", "Chiffon", "Satin",
    "Silk", "Lace", "Embroidered", "Beaded", "Sequined", "Metallic", "Lamé",
    "Vinyl", "PVC", "Latex", "Rubber", "Neoprene", "Gore-Tex", "Ripstop",
    "Canvas", "Duck", "Twill", "Denim", "Corduroy", "Fleece", "Sherpa"
]

# Care instructions for specialty items
SPECIALTY_CARE = [
    "Dry Clean Only", "Professional Cleaning", "Spot Clean", "Hand Wash Only",
    "Delicate Cycle", "Air Dry", "Lay Flat", "Hang to Dry", "Steam Only",
    "Do Not Iron", "Iron with Care", "Store Hanging", "Store Flat",
    "Protect from Light", "Moth Protection", "Climate Controlled Storage"
]

# Rarity and value categories
RARITY_CATEGORIES = [
    "Common", "Uncommon", "Rare", "Very Rare", "Unique", "One of a Kind",
    "Limited Edition", "Prototype", "Sample", "Vintage", "Antique",
    "Designer", "Haute Couture", "Custom Made", "Handmade", "Artisan"
]

# Condition categories
CONDITION_CATEGORIES = [
    "New", "Like New", "Excellent", "Very Good", "Good", "Fair", "Poor",
    "Vintage Condition", "Needs Repair", "For Parts", "Restoration Project"
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
    
    # For "Other" category, be more lenient with warnings
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings  # Warnings are less critical for "Other" items
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

def suggest_category(item_name: str, description: str = "") -> str:
    """
    Suggest a more specific category for an 'Other' item based on its name and description.
    
    Args:
        item_name (str): Name of the clothing item
        description (str): Optional description
        
    Returns:
        str: Suggested category
    """
    item_lower = item_name.lower()
    desc_lower = description.lower()
    combined = f"{item_lower} {desc_lower}"
    
    # Check for specialty items
    for specialty in SPECIALTY_ITEMS:
        if specialty.lower() in combined:
            return "Specialty"
    
    # Check for costume items
    for costume in COSTUME_ITEMS:
        if any(word in combined for word in costume.lower().split()):
            return "Costume"
    
    # Check for work wear
    for work in WORK_WEAR:
        if any(word in combined for word in work.lower().split()):
            return "Work Uniform"
    
    # Check for cultural items
    for cultural in CULTURAL_ITEMS:
        if cultural.lower() in combined:
            return "Cultural"
    
    # Check for religious items
    for religious in RELIGIOUS_ITEMS:
        if religious.lower() in combined:
            return "Religious"
    
    # Check for athletic specialty
    for athletic in ATHLETIC_SPECIALTY:
        if any(word in combined for word in athletic.lower().split()):
            return "Athletic Gear"
    
    # Check for vintage items
    for vintage in VINTAGE_ITEMS:
        if any(word in combined for word in vintage.lower().split()):
            return "Vintage"
    
    return "Miscellaneous"