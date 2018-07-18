from mechanics.damage import DamageTypes


def test_weapon_gives_damage(hero, armor):
    armor_before = hero.armor

    hero.equipment["body"] = armor

    armor_after = hero.armor

    assert armor_before[DamageTypes.ACID] < armor_after[DamageTypes.ACID]