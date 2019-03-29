from mechanics.turns.AtbTurnsManager import AtbTurnsManager


def test_different_units(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1 + 1j)
    empty_game.add_unit(pirate, 2 + 1j)
    atm = empty_game.turns_manager

    units_returned = set()

    for i in range(10):
        unit = atm.get_next()
        unit.readiness = 0
        units_returned.add(unit)

    assert hero in units_returned
    assert pirate in units_returned


def test_readiness_defines_turn(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1 + 1j)
    empty_game.add_unit(pirate, 2 + 1j)
    atm = empty_game.turns_manager

    hero.readiness = 0
    pirate.readiness = 1

    assert atm.get_next() is pirate

    hero.readiness = 1
    pirate.readiness = 0

    assert atm.get_next() is hero


def test_cycles_well(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1 + 1j)
    empty_game.add_unit(pirate, 2 + 1j)
    atm = empty_game.turns_manager

    units_returned = list()

    for i in range(10):
        unit = atm.get_next()
        unit.readiness = 0
        units_returned.append(unit)

    assert units_returned.count(hero) > 1
    assert units_returned.count(pirate) > 1


def test_disabled(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1 + 1j)
    empty_game.add_unit(pirate, 2 + 1j)
    atm = empty_game.turns_manager

    units_returned = set()

    hero.disabled = True
    for i in range(10):
        unit = atm.get_next()
        unit.readiness = 0
        units_returned.add(unit)

    assert hero not in units_returned
    assert pirate in units_returned


# def initiative(agility, stamina):
#     return 10 * ((0.4 + agility/14) ** (3/5)) * ( (stamina / 100) ** (1/3) )
#
#
# for agility in [0, 10,12,15,18,21,29,37,51,100]:
#     for stamina in [0, 5, 25, 50, 75, 100, 125, 175, 275, 400, 800, 1500]:
#         print(agility, stamina, initiative(agility, stamina))
