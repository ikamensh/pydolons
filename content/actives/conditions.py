from mechanics.actives import CellTargeting, SingleUnitTargeting
from battlefield import Cell
import my_globals

def proximity_condition(max_distance):

    def _(active, targeting):

        target = targeting.unit if isinstance(targeting, SingleUnitTargeting) else targeting.cell
        return my_globals.the_game.battlefield.distance(active.owner, target) <= max_distance

    return _

def __get_angle(active, targeting):
    bf = my_globals.the_game.battlefield
    target_cell = targeting.cell if isinstance(targeting, CellTargeting) else bf.unit_locations[targeting.unit]
    return bf.angle_to(active.owner, target_cell)


def within_angle(max_angle_inkl):
    def _(active, targeting):
        _angle = __get_angle(active, targeting)
        return _angle <= max_angle_inkl

    return _

def between_angles(ang_min, ang_max):
    def _(active, targeting):
        _angle = __get_angle(active, targeting)
        return ang_min <= _angle <= ang_max

    return _