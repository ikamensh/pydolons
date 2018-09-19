from game_objects.battlefield_objects.CharAttributes import CharAttributes, abbrev_to_enum
from mechanics.chances.CritHitGrazeMiss import ImpactChances
from mechanics.damage import DamageTypes

from character_creation.Masteries import Masteries


class BaseType:
    default_unarmed_chances = ImpactChances(crit=0.05, hit=0.5, graze=0.6)

    def __init__(self, attributes, type_name, unarmed_damage_type=DamageTypes.CRUSH, resists=None,
                 armor_dict=None, armor_base=0, inventory_capacity = 20,
                 actives=None, icon="default.png", unarmed_chances = default_unarmed_chances, xp = None):

        self.attributes = {}
        for attr in list(attributes.keys()):
            if isinstance(attr, str):
                enum_attr = abbrev_to_enum[attr]
                self.attributes[enum_attr] = attributes[attr]
        for attr in CharAttributes:
            if attr not in self.attributes:
                self.attributes[attr] = 10
            elif self.attributes[attr] <= 0:
                self.attributes[attr] = 1

        self.type_name = type_name
        self.actives = actives or set()
        self.unarmed_damage_type = unarmed_damage_type
        self.resists = resists or {}
        self.armor_dict = armor_dict or {}
        self.inventory_capacity = inventory_capacity
        self.armor_base = armor_base
        self.icon = icon
        self.unarmed_chances = unarmed_chances

        self.xp = xp or Masteries.cumulative_cost( sum(self.attributes.values()) - 40 )