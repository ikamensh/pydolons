from game_objects.items import Item, ItemTypes
from utils.named_enums import NameEnum, auto


class MaterialPieces(Item):
    def __init__(self, material, pieces):
        super().__init__(material.name, ItemTypes.MATERIAL)
        self.pieces = pieces


class Material:
    def __init__(self, material_type, name, rarity):
        self.material_type = material_type
        self.name = name
        self.rarity = rarity

    def to_pieces(self, count_pieces):
        return MaterialPieces(self, count_pieces)



