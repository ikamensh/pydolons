from mechanics.damage import DamageTypes
from utils.named_enums import NameEnum, auto


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