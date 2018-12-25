from mechanics.damage import DamageTypes


def test_body_armor_gives_armor(hero, armor):
    armor_before = hero.armor

    hero.equipment.equip_item( armor )



    armor_after = hero.armor

    assert armor_before[DamageTypes.ACID] < armor_after[DamageTypes.ACID]