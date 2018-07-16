from utils.named_enums import auto, NameEnum
from game_objects.items import MaterialTypes

class ArmorTypes(NameEnum):
    T_SHIRT = auto()
    LEATHER_JACKET = auto()
    CUIRASS = auto()
    FUR_SUIT = auto()

a = ArmorTypes
m = MaterialTypes

material_type_from_armor_type = {a.T_SHIRT: m.CLOTH, a.LEATHER_JACKET: m.SKIN,
                                 a.CUIRASS : m.METAL, a.FUR_SUIT : m.FUR}

