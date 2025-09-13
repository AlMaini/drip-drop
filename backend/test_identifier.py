from PIL import Image
from backend.services.clothing_identifier import identify_clothing_from_image

# Load an image
image = Image.open("orange-jacket.jpg")

# Identify clothing items
results = identify_clothing_from_image(image)

# Process results
for item in results:
    clothing_type = item['type']          # e.g., "TShirt", "Jeans"
    model = item['model']                 # The clothing model instance
    confidence = item['confidence']       # Always "high" for Gemini
    raw_data = item['raw_data']          # Original API response data
    
    print(f"Found: {clothing_type}")
    print(f"Name: {model.name}")
    print(f"Primary Color: {model.primary_color}")
    print(f"Secondary Color: {model.secondary_color}")
    print("---")
    print(f"Raw Data: {raw_data}")