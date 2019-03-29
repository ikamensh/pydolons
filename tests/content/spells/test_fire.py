from cntent.spells.fire.concepts import burning_hands_concept
from cntent.spells.runes import double_damage_rune
from mechanics.actives import Active


def test_burning_hands(empty_game, hero, pirate_band):

    spell = burning_hands_concept.to_spell([double_damage_rune])

    hero.int_base += 100
    empty_game.add_unit(hero, 1 + 1j, facing=1 + 0j)
    new_active = hero.give_active(Active.from_spell(spell))

    p1, p2, p3 = pirate_band

    empty_game.add_unit(p1, 2 + 1j)
    empty_game.add_unit(p2, 3 + 1j)
    empty_game.add_unit(p3, 4 + 1j)

    hero.activate(new_active)

    assert p1.health < p1.max_health
    assert p2.health < p2.max_health
    assert p3.health < p3.max_health
