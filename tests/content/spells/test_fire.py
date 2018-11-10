from cntent.spells.fire.concepts import burning_hands_concept, immolation_concept
from cntent.spells.runes import double_damage_rune
from mechanics.actives import Active

def test_burning_hands(empty_game, hero, pirate_band):

    spell = burning_hands_concept.to_spell([double_damage_rune])

    hero.int_base += 100
    empty_game.add_unit(hero, 1+1j, facing=1+0j)
    new_active = hero.give_active( Active.from_spell( spell ) )

    p1, p2, p3 = pirate_band

    empty_game.add_unit(p1, 2+1j)
    empty_game.add_unit(p2, 3+1j)
    empty_game.add_unit(p3, 4+1j)

    hero.activate(new_active)

    assert p1.health < p1.max_health
    assert p2.health < p2.max_health
    assert p3.health < p3.max_health


from mechanics.events import DamageEvent, BuffAppliedEvent
from mechanics.buffs import Buff

def test_immolation(empty_game, hero, pirate):
    spell = immolation_concept.to_spell([double_damage_rune])

    #bad guy in control! - pirate casts, hero is damaged
    pirate.int_base += 100
    empty_game.add_unit(pirate, 1+1j, facing=1+0j)
    new_active = pirate.give_active( Active.from_spell( spell ) )


    empty_game.add_unit(hero, 2+1j)

    buffs_before = len(hero.buffs)
    health_before = hero.health

    pirate.activate(new_active, hero)

    h = []
    empty_game.events_platform.history = h

    assert len(hero.buffs) > buffs_before # buff applied

    empty_game.turns_manager.pass_time(0.5)

    assert hero.health == health_before



    empty_game.turns_manager.pass_time(0.51)


    assert hero.health < health_before # Damage done!

    while empty_game.turns_manager.time < 5:
        u = empty_game.turns_manager.get_next()
        u.readiness = 0

    count = 0
    for event, happened in h:
        if happened and isinstance(event, DamageEvent):
            count += 1

    assert count == 4


def test_immolation_other_buff(empty_game, hero, pirate):
    spell = immolation_concept.to_spell([double_damage_rune])

    # bad guy in control! - pirate casts, hero is damaged
    pirate.int_base += 100
    empty_game.add_unit(pirate, 1 + 1j, facing=1 + 0j)
    new_active = pirate.give_active(Active.from_spell(spell))

    empty_game.add_unit(hero, 2 + 1j)

    buffs_before = len(hero.buffs)
    health_before = hero.health

    pirate.activate(new_active, hero)

    h = []
    empty_game.events_platform.history = h

    assert len(hero.buffs) > buffs_before  # buff applied

    empty_game.turns_manager.pass_time(0.5)

    assert hero.health == health_before
    BuffAppliedEvent(Buff(3), hero)

    empty_game.turns_manager.pass_time(0.51)

    assert hero.health < health_before  # Damage done!

    while empty_game.turns_manager.time < 7:
        u = empty_game.turns_manager.get_next()
        u.readiness = 0

    count = 0
    for event, happened in h:
        if happened and isinstance(event, DamageEvent):
            count += 1

    assert count == 4

    assert len(hero.buffs) == buffs_before




