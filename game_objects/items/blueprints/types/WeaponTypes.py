from mechanics.damage import DamageTypes
from my_utils.named_enums import NameEnum, auto
from character_creation.MasteriesEnum import MasteriesEnum


class WeaponTypes(NameEnum):
    AXE = auto()
    SWORD = auto()
    DAGGER = auto()
    SPEAR = auto()
    HAMMER = auto()
    CLUB = auto()

w = WeaponTypes
d = DamageTypes

damage_type_from_weapon_type = {w.AXE : d.SLASH, w.SWORD : d.SLASH,
                                w.DAGGER: d.PIERCE, w.SPEAR : d.PIERCE,
                                w.CLUB : d.CRUSH, w.HAMMER: d.CRUSH }

m = MasteriesEnum

mastery_from_weapon_type = {}

for wt in WeaponTypes:
    for me in MasteriesEnum:
        if repr(wt) == repr(me):
            mastery_from_weapon_type[wt] = me
