from cntent.items.std import std_items



def test_takes_different_time(game, hero, mud_golem):

    hero_pos = game.battlefield.unit_locations[hero]
    hero_facing = game.battlefield.unit_facings[hero]

    game.battlefield.place(mud_golem, hero_pos.complex + hero_facing)

    hero.equipment.equip_item(std_items.dagger_cheap)
    assert hero.get_melee_weapon() is std_items.dagger_cheap

    rdy_before = hero.readiness
    hero.attacks[0].activate(mud_golem)
    delta_rdy_dagger = rdy_before - hero.readiness

    hero.equipment.equip_item(std_items.sword_cheap)
    assert hero.get_melee_weapon() is std_items.sword_cheap


    rdy_before = hero.readiness
    hero.attacks[0].activate(mud_golem)
    delta_rdy_sword = rdy_before - hero.readiness

    hero.equipment.equip_item(std_items.hammer_cheap)
    assert hero.get_melee_weapon() is std_items.hammer_cheap


    rdy_before = hero.readiness
    hero.attacks[0].activate(mud_golem)
    delta_rdy_hammer = rdy_before - hero.readiness

    assert delta_rdy_dagger < delta_rdy_sword
    assert delta_rdy_sword < delta_rdy_hammer




