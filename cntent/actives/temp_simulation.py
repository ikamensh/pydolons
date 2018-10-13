from mechanics.actives import Active
from mechanics.combat import Attack
from battlefield import Cell
from game_objects.battlefield_objects import BattlefieldObject
from contextlib import contextmanager
import mechanics.AI.SimUtils as SimUtils

@contextmanager
def sim_move_on_target_cell(active: Active, target: Cell):
    unit = active.owner
    location_before = active.game.battlefield.unit_locations[unit]
    active.game.battlefield.move(unit, target)
    with SimUtils.virtual(unit):
        unit.pay(active.cost)
        yield
    active.game.battlefield.move(unit, location_before)


@contextmanager
def sim_attack(active: Active, target: BattlefieldObject):
    source = active.owner
    expected_dmg = Attack.expected_dmg(source, target)
    with SimUtils.virtual(source):
        source.pay(active.cost)

        if target.health > expected_dmg:
            with SimUtils.virtual(target):
                target.lose_health(expected_dmg)
                yield
        else:
            with SimUtils.simulate_death(active.game, target):
                yield





def sim_turn(ccw):
    turn = -1j if ccw else 1j

    @contextmanager
    def _(active: Active, _):

        unit = active.owner
        facing_before = active.game.battlefield.unit_facings[unit]
        active.game.battlefield.unit_facings[unit] *= turn
        with SimUtils.virtual(unit):
            unit.pay(active.cost)
            yield
        active.game.battlefield.unit_facings[unit] = facing_before

    return _


