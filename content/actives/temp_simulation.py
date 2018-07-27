from mechanics.actives import Active
from battlefield import Cell
from contextlib import contextmanager
from mechanics.AI.SimGame import SimGame
import my_context

@contextmanager
def sim_move_on_target_cell(active: Active, target: Cell):
    unit = active.owner
    location_before = my_context.the_game.battlefield.unit_locations[unit]
    my_context.the_game.battlefield.move(unit, target)
    with SimGame.virtual(unit):
        unit.pay(active.cost)
        yield
    my_context.the_game.battlefield.move(unit, location_before)


def sim_turn(ccw):
    turn = 1j if ccw else -1j

    @contextmanager
    def _(active: Active, _):

        unit = active.owner
        facing_before = my_context.the_game.battlefield.unit_facings[unit]
        my_context.the_game.battlefield.unit_facings[unit] *= turn
        with SimGame.virtual(unit):
            unit.pay(active.cost)
            yield
        my_context.the_game.battlefield.unit_facings[unit] = facing_before

    return _


