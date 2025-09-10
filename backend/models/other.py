"""
Other clothing category for items that don't fit into standard categories.
"""

from .clothes import Clothes
from PIL import Image
from typing import Optional


class Other(Clothes):
    """
    Flexible class for clothing items that don't fit into standard categories.
    Includes a suggestion system to help categorize items appropriately.
    """
    
    def __init__(self, id: Optional[int], name: str, primary_color: str, 
                 secondary_color: str, image: Image.Image, 
                 item_type: str = "Unknown", suggested_category: str = "other"):
        super().__init__(id, "other", name, primary_color, secondary_color, image)
        self.item_type = item_type
        self.suggested_category = suggested_category
    
    def __str__(self):
        return f"{self.item_type}: {self.name} ({self.primary_color})"
    
    def __repr__(self):
        return f"Other(id={self.id}, name='{self.name}', item_type='{self.item_type}', suggested_category='{self.suggested_category}')"