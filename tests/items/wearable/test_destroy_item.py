from mechanics.events import ItemDestroyedEvent


def test_breaks_into_blueprint(hero, real_weapon):
    hero.equipment["hands"] = real_weapon

    len_inventory_before = len(hero.inventory)

    ItemDestroyedEvent(real_weapon)

    len_inventory_after = len(hero.inventory)


    assert hero.equipment["hands"] is None
    assert len_inventory_after == len_inventory_before + 2

def test_destroyed_on_0_durability(hero, real_weapon):
    hero.equipment["hands"] = real_weapon

    len_inventory_before = len(hero.inventory)

    real_weapon.durability = 0

    len_inventory_after = len(hero.inventory)


    assert hero.equipment["hands"] is None
    assert len_inventory_after == len_inventory_before + 2