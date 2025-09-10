from .clothes import Clothes


class TShirt(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Shirt", name, primary_color, secondary_color, image)

class DressShirt(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, pattern=None):
        super().__init__(id, "Dress Shirt", name, primary_color, secondary_color, image)
        self.pattern = pattern

class Blouse(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, sleeve_type="Long"):
        super().__init__(id, "Blouse", name, primary_color, secondary_color, image)
        self.sleeve_type = sleeve_type

class TankTop(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Tank Top", name, primary_color, secondary_color, image)

class Sweater(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Cotton"):
        super().__init__(id, "Sweater", name, primary_color, secondary_color, image)
        self.material = material

class Hoodie(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, has_zipper=False):
        super().__init__(id, "Hoodie", name, primary_color, secondary_color, image)
        self.has_zipper = has_zipper

class Sweatshirt(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Sweatshirt", name, primary_color, secondary_color, image)

class Cardigan(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, material="Wool"):
        super().__init__(id, "Cardigan", name, primary_color, secondary_color, image)
        self.material = material

class WorkoutTop(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Tank"):
        super().__init__(id, "Workout Top", name, primary_color, secondary_color, image)
        self.style = style