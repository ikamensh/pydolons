from utils.named_enums import NameEnum, auto
from mechanics.damage import DamageTypes, DamageTypeGroups

class MaterialTypes(NameEnum):
    STONE = auto()
    WOOD = auto()
    METAL = auto()
    CRYSTAL = auto()
    BONE = auto()
    SKIN = auto()
    FUR = auto()
    CLOTH = auto()


mt = MaterialTypes
dt = DamageTypes
dtg = DamageTypeGroups

armor_per_material = {m : {d:1 for d in dt} for m in mt}
for m in armor_per_material:
    armor_per_material[m][dt.SONIC] = 0.2


armor_per_material[mt.METAL].update({ d : 1.15 for d in dtg.physical})
armor_per_material[mt.METAL].update({d : 0.4 for d in dtg.elemental})
armor_per_material[mt.METAL][dt.LIGHTNING] = 0.15
armor_per_material[mt.METAL][dt.SONIC] = 0.15
armor_per_material[mt.SKIN].update({d : 1.2 for d in dtg.elemental})
armor_per_material[mt.SKIN][dt.PIERCE] = 0.7
armor_per_material[mt.SKIN][dt.SONIC] = 0.33
armor_per_material[mt.FUR].update({d : 2 for d in dtg.elemental})
armor_per_material[mt.FUR][dt.ACID] = 1
armor_per_material[mt.FUR][dt.SONIC] = 0.33
armor_per_material[mt.CRYSTAL].update({d : 2 for d in dtg.physical})
armor_per_material[mt.CRYSTAL][dt.CRUSH] = 0.5
armor_per_material[mt.CLOTH].update({d: 0.3 for d in dtg.physical})

durability_per_material = {m : 1 for m in mt}
durability_per_material[mt.STONE] = 0.6
durability_per_material[mt.METAL] = 2.5
durability_per_material[mt.CRYSTAL] = 0.15
durability_per_material[mt.WOOD] = 2
durability_per_material[mt.BONE] = 0.7






