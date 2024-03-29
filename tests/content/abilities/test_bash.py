from cntent.abilities.bash.ability import bash


from mechanics.damage import DamageTypes, Damage

from mechanics.events import DamageEvent



def test_bash(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1+1j)
    hero.add_ability( bash(1)() )

    empty_game.add_unit(pirate, 2+1j)


    rdy_before = pirate.readiness
    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=pirate, source=hero)
    delta_rdy = pirate.readiness - rdy_before

    assert delta_rdy < 0


def test_pirate_no_bash(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1 + 1j)
    hero.add_ability(bash(1)())

    empty_game.add_unit(pirate, 2 + 1j)

    rdy_before = hero.readiness
    DamageEvent(damage=Damage(100, DamageTypes.CRUSH), target=hero, source=pirate)
    delta_rdy = hero.readiness - rdy_before

    assert delta_rdy == 0


def test_no_bash_magic(empty_game, hero, pirate):

    empty_game.add_unit(hero, 1 + 1j)
    hero.add_ability(bash(1)())

    empty_game.add_unit(pirate, 2 + 1j)

    rdy_before = pirate.readiness
    DamageEvent(damage=Damage(100, DamageTypes.FROST), target=pirate, source=hero)
    delta_rdy = pirate.readiness - rdy_before

    assert delta_rdy == 0





