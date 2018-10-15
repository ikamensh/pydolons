from game_objects.items import Blueprint, Weapon, MaterialTypes
from game_objects.items.blueprints.types.WeaponTypes import WeaponType
from mechanics.damage import Damage


class WeaponBlueprint(Blueprint):
    damage_per_rarity = 50
    durability_per_rarity = 35

    def __init__(self, name, *, weapon_type: WeaponType, material_type, rarity,
                 damage=None, durability=None, material_count = 3):
        assert material_type in MaterialTypes
        assert damage is None or 0.05 <= damage <= 20
        super().__init__(name, weapon_type, rarity, durability, material_type=material_type, material_count=material_count)
        self.damage =  damage
        self.weapon_type = weapon_type


    def to_item(self, material, quality, *, game=None):
        assert material.material_type is self.material_type
        total_rarity = material.rarity * quality.rarity

        damage = Damage( (self.damage or 1) *
                         WeaponBlueprint.damage_per_rarity * total_rarity * \
                         self.weapon_type.damage_factor,
                         self.weapon_type.damage_type)

        durability = self.durability * total_rarity
        full_name = f"{quality.name} {self.name} of {material}"
        return Weapon(full_name, damage, self.weapon_type.chances,
                      atb_factor=self.weapon_type.atb_factor,
                      max_durability=durability,
                      mastery=self.weapon_type.mastery,
                      blueprint=self, material=material,
                      quality=quality, game=game)

    def __repr__(self):
        return f"{self.name} blueprint"


