

def test_weapon_gives_damage(hero, weapon):

    damage_before = hero.get_melee_weapon().damage

    hero.equipment.equip_item(weapon)

    damage_after = hero.get_melee_weapon().damage

    assert damage_before is not damage_after


def test_tooltip_with_name(weapon):
    def is_in_tooltip(tooltip, search): return any(
        [search in val for val in tooltip.values()])

    assert is_in_tooltip(weapon.tooltip_info, str(weapon.name))


def test_tooltip_with_damage(weapon):

    def is_in_tooltip(tooltip, search): return any(
        [search in val for val in tooltip.values()])

    assert is_in_tooltip(weapon.tooltip_info, str(int(weapon.damage.amount)))


def test_tooltip_with_durab(weapon):
    def is_in_tooltip(tooltip, search): return any(
        [search in val for val in tooltip.values()])

    assert is_in_tooltip(weapon.tooltip_info, str(weapon.durability))
