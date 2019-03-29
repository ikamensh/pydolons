from cntent.items.std.potions import minor_healing_potion, rejuvination_potion


def test_gives_active(hero):

    actives_before = len(hero.actives)
    hero.quick_items.add(minor_healing_potion)

    assert len(hero.actives) > actives_before


def test_usage_removes_charges(hero):

    actives_no_potion = set(hero.actives)
    hero.quick_items.add(rejuvination_potion)

    charges_before = rejuvination_potion.charges
    new_active = list(set(hero.actives) - actives_no_potion)[0]
    hero.activate(new_active)

    assert charges_before == rejuvination_potion.charges + 1
    hero.activate(new_active)

    assert len(hero.actives) == len(actives_no_potion)
    assert rejuvination_potion.owner is None


def test_healing_potion_heals(hero):
    actives_no_potion = set(hero.actives)
    hero.quick_items.add(minor_healing_potion)

    new_active = list(set(hero.actives) - actives_no_potion)[0]

    hero.health /= 2
    health_before = hero.health
    hero.activate(new_active)

    assert hero.health > health_before


def test_active_lost_with_item(hero):

    hero.quick_items.add(minor_healing_potion)

    actives_before = len(hero.actives)
    minor_healing_potion.charges -= 99999

    assert len(hero.actives) < actives_before


def test_no_active_inventory(hero):

    actives_before = len(hero.actives)
    hero.inventory.add(minor_healing_potion)

    assert len(hero.actives) == actives_before


def test_no_active_lost_inventary(hero):

    hero.inventory.add(minor_healing_potion)

    actives_before = len(hero.actives)
    minor_healing_potion.charges -= 99999

    assert len(hero.actives) == actives_before
