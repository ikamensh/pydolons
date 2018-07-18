from game_objects.items import Blueprint, Weapon, MaterialTypes
from game_objects.items.blueprints.types.WeaponTypes import damage_type_from_weapon_type
from mechanics.damage import Damage


class WeaponBlueprint(Blueprint):
    damage_per_rarity = 50
    durability_per_rarity = 35

    def __init__(self, name, *, target_item_type, material_type, rarity, damage=None, durability=None, material_count = 3):
        assert target_item_type in damage_type_from_weapon_type
        assert material_type in MaterialTypes
        super().__init__(name, target_item_type, rarity, durability, material_type=material_type, material_count=material_count)
        self.damage = damage or Damage(rarity * WeaponBlueprint.damage_per_rarity,
                                       type=damage_type_from_weapon_type[target_item_type])

    def to_item(self, material, quality):
        assert material.material_type is self.material_type
        total_rarity = material.rarity * quality.rarity

        damage = Damage(self.damage.amount * total_rarity, self.damage.type)
        durability = self.durability * total_rarity
        full_name = f"{quality} {self.name} of {material}"
        return Weapon(full_name, damage, durability, blueprint=self, material=material, quality=quality)

    def __repr__(self):
        return f"{self.name} blueprint"


