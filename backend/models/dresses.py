from .clothes import Clothes


class CasualDress(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Knee-Length"):
        super().__init__(id, "Casual Dress", name, primary_color, secondary_color, image)
        self.length = length

class FormalDress(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, length="Floor-Length"):
        super().__init__(id, "Formal Dress", name, primary_color, secondary_color, image)
        self.length = length

class MaxiDress(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Maxi Dress", name, primary_color, secondary_color, image)

class MiniDress(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Mini Dress", name, primary_color, secondary_color, image)

class Jumpsuit(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image, style="Long"):
        super().__init__(id, "Jumpsuit", name, primary_color, secondary_color, image)
        self.style = style

class Romper(Clothes):
    def __init__(self, id, name, primary_color, secondary_color, image):
        super().__init__(id, "Romper", name, primary_color, secondary_color, image)