from game_objects.battlefield_objects.Unit.Unit import Unit
from game_objects.battlefield_objects.Unit.base_types.pirate import pirate_basetype
from battlefield.Battlefield import Battlefield, Coordinates
from mechanics.abstract.active.actives.melee_attack import attack_unit_active, attack_cell_active
from mechanics.abstract.active.user_targeting.UserTargeting import UserTargeting
from DreamGame import DreamGame

#TODO program and test that actives are unique. Use factory.

def test_attack_unit():
    bf = Battlefield(3,3)
    DreamGame(bf)
    unit1 = Unit(pirate_basetype)
    unit2 = Unit(pirate_basetype)

    loc1 = Coordinates(1,1)
    loc2 = Coordinates(1,2)
    bf.place(unit1, loc1)
    bf.place(unit2, loc2)

    hp_before = unit2.health

    unit1.give_active(attack_cell_active)
    target_cell = UserTargeting(loc2)
    unit1.activate(attack_cell_active, target_cell)

    assert unit2.health < hp_before



