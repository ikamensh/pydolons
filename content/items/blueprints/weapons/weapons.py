from game_objects.items import WeaponBlueprint, WeaponTypes, MaterialTypes


short_sword = WeaponBlueprint("short sword", target_item_type=WeaponTypes.SWORD, material_type=MaterialTypes.METAL, rarity=0.75)
primordial_great_axe = WeaponBlueprint("primordial axe", target_item_type=WeaponTypes.AXE, material_type=MaterialTypes.STONE, rarity=0.9)

