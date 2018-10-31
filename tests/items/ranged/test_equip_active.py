
def test_gives_active(hero, bow):

    actives_before = len(hero.actives)
    hero.equipment.equip_item(bow)

    assert len(hero.actives) > actives_before

def test_gives_active_crossbow(hero, crossbow):

    actives_before = len(hero.actives)
    hero.equipment.equip_item(crossbow)

    assert len(hero.actives) > actives_before

def test_unequip(hero, crossbow):

    hero.equipment.equip_item(crossbow)

    actives_before = len(hero.actives)
    hero.equipment.unequip_item(crossbow)

    assert len(hero.actives) < actives_before






