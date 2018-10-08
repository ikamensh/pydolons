from game_objects.battlefield_objects.CharAttributes import CharAttributes, abbrev_to_enum
from mechanics.chances.CritHitGrazeMiss import ImpactChances
from mechanics.damage import DamageTypes

from character_creation.Masteries import Masteries
from ui.sounds import sound_maps

class BaseType:
    default_unarmed_chances = ImpactChances(crit=0.05, hit=0.5, graze=0.6)

    def __init__(self, attributes, type_name, *,
                 unarmed_damage_type=DamageTypes.CRUSH,
                 unarmed_chances = default_unarmed_chances,
                 resists=None,
                 armor_dict=None,
                 armor_base=0,
                 inventory_capacity = 20,
                 actives=None,
                 abilities = None,
                 icon="default.png",
                 xp = None,
                 sound_map = None):

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
        self.unarmed_damage_type = unarmed_damage_type
        self.unarmed_chances = unarmed_chances

        self.actives = actives or set()
        self.abilities = abilities or list()

        self.resists = resists or {}
        self.armor_dict = armor_dict or {}
        self.inventory_capacity = inventory_capacity
        self.armor_base = armor_base
        self.icon = icon
        self.sound_map = sound_map or sound_maps.std_sound_map

        self.xp = xp or Masteries.cumulative_cost( sum(self.attributes.values()) - 40 )