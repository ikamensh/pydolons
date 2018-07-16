from utils.named_enums import NameEnum, auto

class Material:
    def __init__(self, material_type, name, rarity):
        self.material_type = material_type
        self.name = name
        self.rarity = rarity

# class MaterialProps(NameEnum):
#     DURABILITY = auto()
#     HARDNESS = auto()
#     MAGIC_CAPACITY = auto()
#     ENERGY = auto()
#     DAMAGE_TYPE_RESISTANCE = auto()

