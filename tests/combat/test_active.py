from DreamGame import DreamGame
from battlefield.Battlefield import Battlefield, Cell
from cntent.actives.std_melee_attack import attack_cell_active, attack_unit_active
from game_objects.battlefield_objects import Unit


#TODO program and test that actives are unique. Use factory.

def test_attack_cell(pirate_basetype, no_chances):
    bf = Battlefield(3,3)
    game = DreamGame(bf)

    unit1 = Unit(pirate_basetype)
    unit2 = Unit(pirate_basetype)

    loc1 = Cell(1, 1)
    loc2 = Cell(1, 2)
    game.add_unit(unit1, loc1, -1j)
    game.add_unit(unit2, loc2, -1j)

    hp_before = unit2.health
    attack_cell_active.checker._conditions = []

    active_cpy = unit1.give_active(attack_cell_active)
    unit1.activate(active_cpy, loc2)

    assert unit2.health < hp_before

def test_attack_unit(pirate_basetype, no_chances):
    bf = Battlefield(3,3)
    game = DreamGame(bf)
    # monkeypatch.setattr(game, 'unit_died', lambda x: None)
    unit1 = Unit(pirate_basetype)
    unit2 = Unit(pirate_basetype)


    loc1 = Cell(1, 1)
    loc2 = Cell(1, 2)
    game.add_unit(unit1, loc1, -1j)
    game.add_unit(unit2, loc2, -1j)


    hp_before = unit2.health
    attack_unit_active.checker._conditions = []

    active_cpy = unit1.give_active(attack_unit_active)
    unit1.activate(active_cpy, unit2)

    assert unit2.health < hp_before



