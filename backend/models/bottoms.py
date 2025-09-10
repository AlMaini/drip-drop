from .clothes import Clothes


class Pants(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, fit="Regular"):
        super().__init__(id, "Pants", name, primary_color, secondary_color, image)
        self.fit = fit

class Shorts(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Knee-Length"):
        super().__init__(id, "Shorts", name, primary_color, secondary_color, image)
        self.length = length

class Jeans(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, fit="Regular"):
        super().__init__(id, "Jeans", name, primary_color, secondary_color, image)
        self.fit = fit

class DressPants(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Wool"):
        super().__init__(id, "Dress Pants", name, primary_color, secondary_color, image)
        self.material = material

class Trousers(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, fit="Regular"):
        super().__init__(id, "Trousers", name, primary_color, secondary_color, image)
        self.fit = fit

class Chinos(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, fit="Slim"):
        super().__init__(id, "Chinos", name, primary_color, secondary_color, image)
        self.fit = fit

class Skirt(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Knee-Length"):
        super().__init__(id, "Skirt", name, primary_color, secondary_color, image)
        self.length = length

class Leggings(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Cotton Blend"):
        super().__init__(id, "Leggings", name, primary_color, secondary_color, image)
        self.material = material

class SweatPants(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, fit="Regular"):
        super().__init__(id, "Sweatpants", name, primary_color, secondary_color, image)
        self.fit = fit

class Joggers(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Cotton Blend"):
        super().__init__(id, "Joggers", name, primary_color, secondary_color, image)
        self.material = material

class AthleticShorts(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Mid-Thigh"):
        super().__init__(id, "Athletic Shorts", name, primary_color, secondary_color, image)
        self.length = length

class YogaPants(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Spandex Blend"):
        super().__init__(id, "Yoga Pants", name, primary_color, secondary_color, image)
        self.material = material