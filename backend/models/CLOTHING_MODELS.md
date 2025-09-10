# Clothing Models Documentation

This document provides a comprehensive overview of all clothing models available in the drip-drop application, including their parameters, default values, and supported options.

## Base Class

### Clothes
The base class for all clothing items.

**Parameters:**
- `id` (required): Unique identifier for the clothing item
- `clothing_category` (required): Category name (set automatically by subclasses)
- `name` (required): Display name of the clothing item
- `primary_color` (required): Primary color of the item
- `secondary_color` (required): Secondary/accent color of the item  
- `image` (required): PIL Image object of the clothing item

---

## Tops

### TShirt
Basic t-shirt clothing item.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Shirt"

**Example:**
```python
from PIL import Image
from models.tops import TShirt

img = Image.open("tshirt.jpg")
tshirt = TShirt(1, "Basic Tee", "Blue", "White", img)
```

### DressShirt
Formal dress shirt with optional pattern.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `pattern` (optional): Pattern type, default: None
- Category: "Dress Shirt"

**Supported Pattern Options:**
- None, "Striped", "Checkered", "Solid", "Polka Dot", "Paisley"

**Example:**
```python
shirt = DressShirt(2, "Oxford Shirt", "White", "Blue", img, pattern="Striped")
```

### Blouse
Women's blouse with sleeve type specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `sleeve_type` (optional): Sleeve length, default: "Long"
- Category: "Blouse"

**Supported Sleeve Types:**
- "Long", "Short", "3/4", "Sleeveless", "Bell", "Puff"

**Example:**
```python
blouse = Blouse(3, "Silk Blouse", "Black", "Gold", img, sleeve_type="3/4")
```

### TankTop
Sleeveless tank top.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Tank Top"

### Sweater
Knitted sweater with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Fabric material, default: "Cotton"
- Category: "Sweater"

**Supported Materials:**
- "Cotton", "Wool", "Cashmere", "Acrylic", "Alpaca", "Merino"

### Hoodie
Hooded sweatshirt with zipper option.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `has_zipper` (optional): Boolean for zipper presence, default: False
- Category: "Hoodie"

### Sweatshirt
Basic sweatshirt without hood.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Sweatshirt"

### Cardigan
Button-up sweater with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Fabric material, default: "Wool"
- Category: "Cardigan"

**Supported Materials:**
- "Wool", "Cotton", "Cashmere", "Acrylic", "Alpaca"

### WorkoutTop
Athletic top for exercise.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Top style, default: "Tank"
- Category: "Workout Top"

**Supported Styles:**
- "Tank", "T-Shirt", "Long Sleeve", "Crop Top", "Sports Bra"

---

## Bottoms

### Pants
Basic pants with fit specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `fit` (optional): Fit type, default: "Regular"
- Category: "Pants"

**Supported Fits:**
- "Regular", "Slim", "Relaxed", "Straight", "Bootcut", "Wide Leg"

### Shorts
Short pants with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Short length, default: "Knee-Length"
- Category: "Shorts"

**Supported Lengths:**
- "Knee-Length", "Mid-Thigh", "Bermuda", "Hot Pants", "Basketball"

### Jeans
Denim jeans with fit specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `fit` (optional): Fit type, default: "Regular"
- Category: "Jeans"

**Supported Fits:**
- "Regular", "Slim", "Skinny", "Straight", "Bootcut", "Relaxed", "Wide Leg"

### DressPants
Formal trousers with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Fabric material, default: "Wool"
- Category: "Dress Pants"

**Supported Materials:**
- "Wool", "Cotton", "Polyester", "Linen", "Silk"

### Trousers
General trousers with fit specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `fit` (optional): Fit type, default: "Regular"
- Category: "Trousers"

### Chinos
Casual cotton pants with fit specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `fit` (optional): Fit type, default: "Slim"
- Category: "Chinos"

### Skirt
Women's skirt with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Skirt length, default: "Knee-Length"
- Category: "Skirt"

**Supported Lengths:**
- "Mini", "Knee-Length", "Midi", "Maxi", "Floor-Length"

### Leggings
Stretchy fitted pants with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Fabric material, default: "Cotton Blend"
- Category: "Leggings"

**Supported Materials:**
- "Cotton Blend", "Spandex", "Polyester", "Nylon Blend"

### SweatPants
Casual sweatpants with fit specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `fit` (optional): Fit type, default: "Regular"
- Category: "Sweatpants"

### Joggers
Athletic jogger pants with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Fabric material, default: "Cotton Blend"
- Category: "Joggers"

### AthleticShorts
Sports shorts with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Short length, default: "Mid-Thigh"
- Category: "Athletic Shorts"

### YogaPants
Yoga and exercise pants with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Fabric material, default: "Spandex Blend"
- Category: "Yoga Pants"

---

## Footwear

### Sneakers
Athletic sneakers with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Sneaker style, default: "Athletic"
- Category: "Sneakers"

**Supported Styles:**
- "Athletic", "Casual", "High-Top", "Low-Top", "Slip-On"

### DressShoes
Formal dress shoes with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Shoe style, default: "Oxford"
- Category: "Dress Shoes"

**Supported Styles:**
- "Oxford", "Derby", "Loafer", "Monk Strap", "Brogue"

### Boots
Boots with height specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `height` (optional): Boot height, default: "Ankle"
- Category: "Boots"

**Supported Heights:**
- "Ankle", "Mid-Calf", "Knee-High", "Thigh-High", "Combat", "Chelsea"

### Sandals
Open-toe sandals with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Sandal style, default: "Flat"
- Category: "Sandals"

**Supported Styles:**
- "Flat", "Gladiator", "Flip-Flop", "Platform", "Wedge"

### Flats
Flat shoes with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Flat style, default: "Ballet"
- Category: "Flats"

**Supported Styles:**
- "Ballet", "Pointed Toe", "Round Toe", "Square Toe", "Loafer"

### Heels
High-heeled shoes with height specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `height` (optional): Heel height, default: "Medium"
- Category: "Heels"

**Supported Heights:**
- "Low", "Medium", "High", "Platform", "Stiletto"

### AthleticShoes
Sport-specific athletic shoes.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `sport` (optional): Sport type, default: "Running"
- Category: "Athletic Shoes"

**Supported Sports:**
- "Running", "Basketball", "Tennis", "Cross-Training", "Soccer"

---

## Outerwear

### Jacket
General jacket with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Jacket material, default: "Denim"
- Category: "Jacket"

**Supported Materials:**
- "Denim", "Leather", "Cotton", "Polyester", "Nylon"

### Blazer
Formal blazer with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Blazer style, default: "Single-Breasted"
- Category: "Blazer"

**Supported Styles:**
- "Single-Breasted", "Double-Breasted", "Unstructured", "Fitted"

### Coat
General coat with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Coat length, default: "Mid-Length"
- Category: "Coat"

**Supported Lengths:**
- "Short", "Mid-Length", "Long", "Trench", "Pea Coat"

### WinterCoat
Heavy winter coat with insulation specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `insulation` (optional): Insulation type, default: "Down"
- Category: "Winter Coat"

**Supported Insulations:**
- "Down", "Synthetic", "Wool", "Fleece", "Thinsulate"

### RainJacket
Waterproof rain jacket.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `waterproof` (optional): Boolean for waterproof capability, default: True
- Category: "Rain Jacket"

### Windbreaker
Lightweight wind-resistant jacket.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Windbreaker"

### Vest
Sleeveless vest with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Vest style, default: "Puffer"
- Category: "Vest"

**Supported Styles:**
- "Puffer", "Fleece", "Wool", "Down", "Utility"

---

## Accessories

### Hat
General hat with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Hat style, default: "Baseball Cap"
- Category: "Hat"

**Supported Styles:**
- "Baseball Cap", "Beanie", "Fedora", "Beret", "Sun Hat", "Bucket Hat"

### Cap
Specific cap with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Cap style, default: "Baseball"
- Category: "Cap"

**Supported Styles:**
- "Baseball", "Snapback", "Trucker", "Dad Hat", "Fitted"

### Belt
Waist belt with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Belt material, default: "Leather"
- Category: "Belt"

**Supported Materials:**
- "Leather", "Canvas", "Fabric", "Chain", "Elastic"

### Scarf
Neck scarf with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Scarf material, default: "Wool"
- Category: "Scarf"

**Supported Materials:**
- "Wool", "Silk", "Cotton", "Cashmere", "Acrylic"

### Gloves
Hand gloves with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Glove material, default: "Leather"
- Category: "Gloves"

**Supported Materials:**
- "Leather", "Wool", "Cotton", "Synthetic", "Cashmere"

### Sunglasses
Protective eyewear with lens color specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `lens_color` (optional): Lens color, default: "Black"
- Category: "Sunglasses"

**Supported Lens Colors:**
- "Black", "Brown", "Blue", "Green", "Gray", "Mirror"

### Watch
Timepiece with band material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `band_material` (optional): Watch band material, default: "Leather"
- Category: "Watch"

**Supported Band Materials:**
- "Leather", "Metal", "Rubber", "Fabric", "Plastic"

---

## Undergarments

### Underwear
Basic underwear with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Underwear style, default: "Brief"
- Category: "Underwear"

**Supported Styles:**
- "Brief", "Boxer", "Boxer Brief", "Thong", "Bikini"

### Bra
Women's bra with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Bra style, default: "Regular"
- Category: "Bra"

**Supported Styles:**
- "Regular", "Push-Up", "Wireless", "Padded", "Strapless"

### SportsBra
Athletic bra with support level specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `support_level` (optional): Support level, default: "Medium"
- Category: "Sports Bra"

**Supported Support Levels:**
- "Low", "Medium", "High", "Maximum"

### Undershirt
Base layer shirt with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Undershirt style, default: "Crew Neck"
- Category: "Undershirt"

**Supported Styles:**
- "Crew Neck", "V-Neck", "Tank Top", "Long Sleeve"

### Socks
Foot socks with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Sock length, default: "Crew"
- Category: "Socks"

**Supported Lengths:**
- "Ankle", "Crew", "Mid-Calf", "Knee-High", "No-Show"

### Pantyhose
Sheer leg hosiery with denier specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `denier` (optional): Fabric thickness, default: 15
- Category: "Pantyhose"

**Supported Denier Values:**
- 8, 10, 15, 20, 30 (higher = less sheer)

### Tights
Opaque leg hosiery with denier specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `denier` (optional): Fabric thickness, default: 40
- Category: "Tights"

**Supported Denier Values:**
- 40, 60, 80, 100, 120 (higher = more opaque)

---

## Dresses and One-Pieces

### CasualDress
Everyday dress with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Dress length, default: "Knee-Length"
- Category: "Casual Dress"

**Supported Lengths:**
- "Mini", "Knee-Length", "Midi", "Maxi", "Floor-Length"

### FormalDress
Formal occasion dress with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Dress length, default: "Floor-Length"
- Category: "Formal Dress"

### MaxiDress
Floor-length dress.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Maxi Dress"

### MiniDress
Short dress above the knee.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Mini Dress"

### Jumpsuit
One-piece garment with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Jumpsuit style, default: "Long"
- Category: "Jumpsuit"

**Supported Styles:**
- "Long", "Cropped", "Wide Leg", "Fitted", "Culotte"

### Romper
Short one-piece garment.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- Category: "Romper"

---

## Sleepwear

### Pajamas
Sleep clothing set with style specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `style` (optional): Pajama style, default: "Set"
- Category: "Pajamas"

**Supported Styles:**
- "Set", "Top Only", "Bottom Only", "One Piece", "Shorts Set"

### Nightgown
Women's sleep dress with length specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `length` (optional): Nightgown length, default: "Knee-Length"
- Category: "Nightgown"

**Supported Lengths:**
- "Short", "Knee-Length", "Mid-Calf", "Long", "Floor-Length"

### Robe
Loose sleep/lounge garment with material specification.

**Parameters:**
- `id`, `name`, `primary_color`, `secondary_color`, `image` (inherited)
- `material` (optional): Robe material, default: "Cotton"
- Category: "Robe"

**Supported Materials:**
- "Cotton", "Silk", "Terry Cloth", "Fleece", "Satin"

---

## Usage Examples

### Basic Usage
```python
from PIL import Image
from models import TShirt, Jeans, Sneakers

# Load images
tshirt_img = Image.open("tshirt.jpg")
jeans_img = Image.open("jeans.jpg")
sneakers_img = Image.open("sneakers.jpg")

# Create clothing items
tshirt = TShirt(1, "Basic Tee", "Blue", "White", tshirt_img)
jeans = Jeans(2, "Skinny Jeans", "Dark Blue", "Black", jeans_img, fit="Skinny")
sneakers = Sneakers(3, "Running Shoes", "White", "Blue", sneakers_img, style="Athletic")
```

### Import Options
```python
# Import specific classes
from models.tops import TShirt, Hoodie
from models.bottoms import Jeans
from models.footwear import Sneakers

# Import all from main module
from models import TShirt, Jeans, Sneakers, Hoodie

# Import entire modules
import models.tops as tops
import models.bottoms as bottoms
```

---

## Notes

- All `image` parameters expect PIL Image objects
- Optional parameters have sensible defaults but can be customized
- Color parameters accept any string values (consider using standardized color names)
- Categories are automatically set by each clothing class
- The base `Clothes` class should not be instantiated directly