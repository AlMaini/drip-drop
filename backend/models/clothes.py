from PIL import Image

class Clothes:
    def __init__(self, id, clothing_category, name, primary_color, secondary_color, image, is_owned=True):
        self.id = id
        self.clothing_category = clothing_category
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.image = image
        self.is_owned = is_owned