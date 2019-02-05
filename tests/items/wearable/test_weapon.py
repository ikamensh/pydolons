

def test_weapon_gives_damage(hero, weapon):


    damage_before = hero.get_melee_weapon().damage

    hero.equipment.equip_item( weapon )

    damage_after = hero.get_melee_weapon().damage

    assert damage_before is not damage_after


def test_tooltip_with_name(weapon):
    is_in_tooltip = lambda tooltip, search: any([search in val for val in tooltip.values()])

    assert is_in_tooltip(weapon.tooltip_info, str(weapon.name))

def test_tooltip_with_damage(weapon):

    is_in_tooltip = lambda tooltip, search : any([search in val for val in tooltip.values()])

    assert is_in_tooltip(weapon.tooltip_info, str(weapon.damage.amount))

def test_tooltip_with_durab(weapon):
    is_in_tooltip = lambda tooltip, search: any([search in val for val in tooltip.values()])

    assert is_in_tooltip(weapon.durability, str(weapon.damage.amount))



