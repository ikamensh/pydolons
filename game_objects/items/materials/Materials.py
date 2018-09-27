from game_objects import items


class MaterialPieces(items.Item):
    def __init__(self, material, pieces):
        super().__init__(material.name, items.ItemTypes.MATERIAL)
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
