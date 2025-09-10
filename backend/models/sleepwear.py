from .clothes import Clothes


class Pajamas(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Set"):
        super().__init__(id, "Pajamas", name, primary_color, secondary_color, image)
        self.style = style

class Nightgown(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Knee-Length"):
        super().__init__(id, "Nightgown", name, primary_color, secondary_color, image)
        self.length = length

class Robe(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Cotton"):
        super().__init__(id, "Robe", name, primary_color, secondary_color, image)
        self.material = material