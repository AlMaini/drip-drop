from .clothes import Clothes


class Sneakers(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Athletic"):
        super().__init__(id, "Sneakers", name, primary_color, secondary_color, image)
        self.style = style

class DressShoes(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Oxford"):
        super().__init__(id, "Dress Shoes", name, primary_color, secondary_color, image)
        self.style = style

class Boots(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, height="Ankle"):
        super().__init__(id, "Boots", name, primary_color, secondary_color, image)
        self.height = height

class Sandals(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Flat"):
        super().__init__(id, "Sandals", name, primary_color, secondary_color, image)
        self.style = style

class Flats(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Ballet"):
        super().__init__(id, "Flats", name, primary_color, secondary_color, image)
        self.style = style

class Heels(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, height="Medium"):
        super().__init__(id, "Heels", name, primary_color, secondary_color, image)
        self.height = height

class AthleticShoes(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, sport="Running"):
        super().__init__(id, "Athletic Shoes", name, primary_color, secondary_color, image)
        self.sport = sport