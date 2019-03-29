from cntent.actives.std.std_ranged_attack import bow_shot_active, crossbow_shot_active
from game_objects.items import WeaponBlueprint, WeaponTypes, MaterialTypes


short_sword = WeaponBlueprint(
    "short sword",
    weapon_type=WeaponTypes.SWORD,
    material_type=MaterialTypes.METAL,
    rarity=1)
dagger = WeaponBlueprint(
    "dagger",
    weapon_type=WeaponTypes.DAGGER,
    material_type=MaterialTypes.METAL,
    rarity=1)
axe = WeaponBlueprint(
    "axe",
    weapon_type=WeaponTypes.AXE,
    material_type=MaterialTypes.METAL,
    rarity=1)
hammer = WeaponBlueprint(
    "hammer",
    weapon_type=WeaponTypes.HAMMER,
    material_type=MaterialTypes.METAL,
    rarity=1)
spear = WeaponBlueprint(
    "spear",
    weapon_type=WeaponTypes.SPEAR,
    material_type=MaterialTypes.METAL,
    rarity=1)

scimitar = WeaponBlueprint(
    "scimitar",
    weapon_type=WeaponTypes.SWORD,
    material_type=MaterialTypes.METAL,
    rarity=1,
    damage=1.1,
    durability=0.8)

occult_blade = WeaponBlueprint(
    "occult blade",
    weapon_type=WeaponTypes.SWORD,
    material_type=MaterialTypes.METAL,
    rarity=1.3,
    damage=1.1,
    durability=0.6)

rapier = WeaponBlueprint(
    "rapier",
    weapon_type=WeaponTypes.SWORD,
    material_type=MaterialTypes.METAL,
    rarity=1.6,
    durability=0.8)

heavenly_mercy = WeaponBlueprint(
    "heavenly mercy",
    weapon_type=WeaponTypes.SWORD,
    material_type=MaterialTypes.METAL,
    rarity=2.3,
    durability=1.2)


primordial_axe = WeaponBlueprint(
    "primordial axe",
    weapon_type=WeaponTypes.AXE,
    material_type=MaterialTypes.STONE,
    rarity=0.9,
    damage=1.2,
    durability=0.5)

wooden_spear = WeaponBlueprint(
    "spear",
    weapon_type=WeaponTypes.SPEAR,
    material_type=MaterialTypes.WOOD,
    rarity=1.1)
kris = WeaponBlueprint(
    "kris",
    weapon_type=WeaponTypes.DAGGER,
    material_type=MaterialTypes.METAL,
    rarity=1.2)
ritual_dagger = WeaponBlueprint(
    "ritual dagger",
    weapon_type=WeaponTypes.DAGGER,
    material_type=MaterialTypes.STONE,
    rarity=1.3,
    damage=1.2,
    durability=0.5)


bow = WeaponBlueprint("bow",
                      weapon_type=WeaponTypes.BOW,
                      material_type=MaterialTypes.WOOD,
                      rarity=0.75,
                      actives=[bow_shot_active],
                      is_ranged=True)

crossbow = WeaponBlueprint("crossbow",
                           weapon_type=WeaponTypes.CROSSBOW,
                           material_type=MaterialTypes.WOOD,
                           rarity=0.75,
                           actives=[crossbow_shot_active], is_ranged=True)


std_blueprints = [short_sword, dagger, axe, hammer, spear, bow, crossbow]
fancy_blueprints = [occult_blade, wooden_spear, kris, ritual_dagger]

if __name__ == "__main__":
    for bp in [
            short_sword,
            dagger,
            axe,
            hammer,
            spear,
            scimitar,
            primordial_axe,
            bow,
            crossbow,
            rapier,
            occult_blade,
            heavenly_mercy]:
        print(bp, bp.price)
