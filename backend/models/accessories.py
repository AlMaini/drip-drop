from .clothes import Clothes


class Hat(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Baseball Cap"):
        super().__init__(id, "Hat", name, primary_color, secondary_color, image)
        self.style = style

class Cap(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Baseball"):
        super().__init__(id, "Cap", name, primary_color, secondary_color, image)
        self.style = style

class Belt(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Leather"):
        super().__init__(id, "Belt", name, primary_color, secondary_color, image)
        self.material = material

class Scarf(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Wool"):
        super().__init__(id, "Scarf", name, primary_color, secondary_color, image)
        self.material = material

class Gloves(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Leather"):
        super().__init__(id, "Gloves", name, primary_color, secondary_color, image)
        self.material = material

class Sunglasses(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, lens_color="Black"):
        super().__init__(id, "Sunglasses", name, primary_color, secondary_color, image)
        self.lens_color = lens_color

class Watch(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, band_material="Leather"):
        super().__init__(id, "Watch", name, primary_color, secondary_color, image)
        self.band_material = band_material