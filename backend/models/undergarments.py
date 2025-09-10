from .clothes import Clothes


class Underwear(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Brief"):
        super().__init__(id, "Underwear", name, primary_color, secondary_color, image)
        self.style = style

class Bra(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Regular"):
        super().__init__(id, "Bra", name, primary_color, secondary_color, image)
        self.style = style

class SportsBra(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, support_level="Medium"):
        super().__init__(id, "Sports Bra", name, primary_color, secondary_color, image)
        self.support_level = support_level

class Undershirt(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Crew Neck"):
        super().__init__(id, "Undershirt", name, primary_color, secondary_color, image)
        self.style = style

class Socks(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Crew"):
        super().__init__(id, "Socks", name, primary_color, secondary_color, image)
        self.length = length

class Pantyhose(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, denier=15):
        super().__init__(id, "Pantyhose", name, primary_color, secondary_color, image)
        self.denier = denier

class Tights(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, denier=40):
        super().__init__(id, "Tights", name, primary_color, secondary_color, image)
        self.denier = denier