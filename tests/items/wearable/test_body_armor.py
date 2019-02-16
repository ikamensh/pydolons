from mechanics.damage import DamageTypes


def test_body_armor_gives_armor(hero, armor):
    armor_before = hero.armor
    hero.equipment.equip_item(armor)
    armor_after = hero.armor
    assert armor_before[DamageTypes.ACID] < armor_after[DamageTypes.ACID]


def test_tooltip_with_armor(armor):
    is_in_tooltip = lambda tooltip, search: any([search in val for val in tooltip.values()])
    assert is_in_tooltip(armor.tooltip_info, str(armor.armor))