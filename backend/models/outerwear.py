from .clothes import Clothes


class Jacket(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Denim"):
        super().__init__(id, "Jacket", name, primary_color, secondary_color, image)
        self.material = material

class Blazer(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Single-Breasted"):
        super().__init__(id, "Blazer", name, primary_color, secondary_color, image)
        self.style = style

class Coat(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Mid-Length"):
        super().__init__(id, "Coat", name, primary_color, secondary_color, image)
        self.length = length

class WinterCoat(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, insulation="Down"):
        super().__init__(id, "Winter Coat", name, primary_color, secondary_color, image)
        self.insulation = insulation

class RainJacket(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, waterproof=True):
        super().__init__(id, "Rain Jacket", name, primary_color, secondary_color, image)
        self.waterproof = waterproof

class Windbreaker(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Windbreaker", name, primary_color, secondary_color, image)

class Vest(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Puffer"):
        super().__init__(id, "Vest", name, primary_color, secondary_color, image)
        self.style = style