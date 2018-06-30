from mechanics.damage import DamageTypes
from game_objects.items import Equipment, Inventory

class BaseType:
    def __init__(self, str, agi, int, type_name, unarmed_damage_type=DamageTypes.CRUSH, resists=None,
                 armor_dict=None, armor_base=0, equipment=Equipment, inventory_capacity = 20,
                 actives=set()):
        self.str = str
        self.agi = agi
        self.int = int
        self.type_name = type_name
        self.actives = actives
        self.unarmed_damage_type = unarmed_damage_type
        self.resists = resists or {}
        self.armor_dict = armor_dict or {}
        self.equipment_cls = equipment
        self.inventory_capacity = inventory_capacity
        self.armor_base = armor_base