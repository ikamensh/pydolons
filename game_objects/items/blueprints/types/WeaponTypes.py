from mechanics.damage import DamageTypes
from character_creation.MasteriesEnum import MasteriesEnum

from mechanics.chances.CritHitGrazeMiss import ImpactChances

default_unarmed_chances = ImpactChances(crit=0.05, hit=0.5, graze=0.6)

class WeaponType:
    def __init__(self, damage_type, mastery, chances, damage_factor=1., atb_factor=1.):
        self.damage_type = damage_type
        self.mastery = mastery
        self.chances = chances
        self.damage_factor = damage_factor
        self.atb_factor = atb_factor


d = DamageTypes
m = MasteriesEnum

class WeaponTypes:
    AXE = WeaponType(d.SLASH, m.AXE, ImpactChances(0.05, 0.3, 0.7), damage_factor=1.4, atb_factor=1.8)
    SWORD = WeaponType(d.SLASH, m.SWORD, ImpactChances(0.05, 0.4, 0.5))
    DAGGER = WeaponType(d.PIERCE, m.DAGGER, ImpactChances(0.1, 0.4, 0.5), damage_factor=0.7, atb_factor=0.55)
    SPEAR = WeaponType(d.PIERCE, m.SPEAR, ImpactChances(0.05, 0.4, 0.5))
    HAMMER = WeaponType(d.CRUSH, m.HAMMER, ImpactChances(0.1, 0.35, 0.25), damage_factor=1.5, atb_factor=2.1)
    CLUB = WeaponType(d.CRUSH, m.CLUB, ImpactChances(0.07, 0.37, 0.47))


print(WeaponTypes.AXE.damage_type)
