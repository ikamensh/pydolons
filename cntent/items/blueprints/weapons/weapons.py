from game_objects.items import WeaponBlueprint, WeaponTypes, MaterialTypes


short_sword = WeaponBlueprint("short sword", weapon_type=WeaponTypes.SWORD, material_type=MaterialTypes.METAL, rarity=0.75)
dagger = WeaponBlueprint("dagger", weapon_type=WeaponTypes.DAGGER, material_type=MaterialTypes.METAL, rarity=0.75)
axe = WeaponBlueprint("axe", weapon_type=WeaponTypes.AXE, material_type=MaterialTypes.METAL, rarity=0.75)
hammer = WeaponBlueprint("dagger", weapon_type=WeaponTypes.HAMMER, material_type=MaterialTypes.METAL, rarity=0.75)
spear = WeaponBlueprint("spear", weapon_type=WeaponTypes.SPEAR, material_type=MaterialTypes.METAL, rarity=0.75)

scimitar = WeaponBlueprint("scimitar", weapon_type=WeaponTypes.SWORD, material_type=MaterialTypes.METAL,
                       rarity=1, damage=1.1, durability=0.8)


primordial_great_axe = WeaponBlueprint("primordial axe", weapon_type=WeaponTypes.AXE, material_type=MaterialTypes.STONE, rarity=0.9)

from cntent.actives.std_ranged_attack import bow_shot_active, crossbow_shot_active

bow = WeaponBlueprint("bow", weapon_type=WeaponTypes.BOW, material_type=MaterialTypes.METAL, rarity=0.75, actives=[bow_shot_active])
crossbow = WeaponBlueprint("crossbow", weapon_type=WeaponTypes.CROSSBOW, material_type=MaterialTypes.METAL, rarity=0.75, actives=[crossbow_shot_active])
