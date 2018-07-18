from DreamGame import DreamGame
from battlefield.Battlefield import Battlefield, Cell
from content.actives.melee_attack import attack_cell_active, attack_unit_active
from game_objects.battlefield_objects import Unit
from mechanics.flexi_targeting import SingleUnitTargeting, CellTargeting


#TODO program and test that actives are unique. Use factory.

def test_attack_cell(pirate_basetype, no_chances):
    bf = Battlefield(3,3)
    DreamGame(bf)
    unit1 = Unit(pirate_basetype)
    unit2 = Unit(pirate_basetype)

    loc1 = Cell(1, 1)
    loc2 = Cell(1, 2)
    bf.place(unit1, loc1)
    bf.place(unit2, loc2)

    hp_before = unit2.health

    unit1.give_active(attack_cell_active)
    target_cell = CellTargeting(loc2)
    unit1.activate(attack_cell_active, target_cell)

    assert unit2.health < hp_before

def test_attack_unit(pirate_basetype, no_chances):
    bf = Battlefield(3,3)
    game = DreamGame(bf)
    # monkeypatch.setattr(game, 'unit_died', lambda x: None)
    unit1 = Unit(pirate_basetype)
    unit2 = Unit(pirate_basetype)

    loc1 = Cell(1, 1)
    loc2 = Cell(1, 2)
    bf.place(unit1, loc1)
    bf.place(unit2, loc2)

    hp_before = unit2.health

    unit1.give_active(attack_unit_active)
    target_unit = SingleUnitTargeting(unit2)
    unit1.activate(attack_unit_active, target_unit)

    assert unit2.health < hp_before



