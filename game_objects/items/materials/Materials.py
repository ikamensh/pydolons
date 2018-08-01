from game_objects.items import Item, ItemTypes
from my_utils.named_enums import NameEnum, auto


class MaterialPieces(Item):
    def __init__(self, material, pieces):
        super().__init__(material.name, ItemTypes.MATERIAL)
        self.pieces = pieces


class Material:
    def __init__(self, material_type, name, rarity, magic_complexity=1, energy=50):
        self.material_type = material_type
        self.name = name
        self.rarity = rarity
        self.magic_complexity = magic_complexity
        self.energy = energy

    def to_pieces(self, count_pieces):
        return MaterialPieces(self, count_pieces)



