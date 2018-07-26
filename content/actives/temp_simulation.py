from mechanics.actives import Active
from battlefield import Cell
from contextlib import contextmanager
import my_context

@contextmanager
def sim_move_on_target_cell(active: Active, target: Cell):
    unit = active.owner
    location_before = my_context.the_game.battlefield.unit_locations[unit]
    my_context.the_game.battlefield.move(unit, target)
    with unit.virtual():
        unit.pay(active.cost)
        yield
    my_context.the_game.battlefield.move(unit, location_before)


@contextmanager
def sim_turn_ccw(active: Active, _):

    unit = active.owner
    facing_before = my_context.the_game.battlefield.unit_facings[unit]
    my_context.the_game.battlefield.unit_facings[unit] *= 1j
    with unit.virtual():
        unit.pay(active.cost)
        yield
    my_context.the_game.battlefield.unit_facings[unit] = facing_before

@contextmanager
def sim_turn_cw(active: Active, _):

    unit = active.owner
    facing_before = my_context.the_game.battlefield.unit_facings[unit]
    my_context.the_game.battlefield.unit_facings[unit] *= -1j
    with unit.virtual():
        unit.pay(active.cost)
        yield
    my_context.the_game.battlefield.unit_facings[unit] = facing_before


