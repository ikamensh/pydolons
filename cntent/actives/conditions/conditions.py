from battlefield import Cell
from mechanics.events import MovementEvent
from mechanics.conditions import ActiveCondition


def proximity_condition(max_distance):

    def _(active, target):
        return active.game.battlefield.distance(active.owner, target) <= max_distance

    c = ActiveCondition("Proximity", _, "{target} is too far away.")

    return c

def range_condition(min_dist, max_dist):

    def _(active, target):
        return min_dist <= active.game.battlefield.distance(active.owner, target) <= max_dist

    c = ActiveCondition("Range", _,
                        f"Distance to target must be in range [{min_dist},{max_dist}].")

    return c

def __get_angle(active, target):
    bf = active.game.battlefield
    target_cell = target if isinstance(target, Cell) else bf.unit_locations[target]
    return bf.angle_to(active.owner, target_cell)


def within_angle(max_angle_inkl):
    def _(active, targeting):
        _angle = __get_angle(active, targeting)[0]
        return _angle <= max_angle_inkl

    c = ActiveCondition("Within angle", _,
                        f"You must face at most {max_angle_inkl} away from the direction to the target")

    return c

def between_angles(ang_min, ang_max):
    def _(active, targeting):
        _angle = __get_angle(active, targeting)[0]
        return ang_min <= _angle <= ang_max

    c = ActiveCondition("Angle range", _,
                        f"Angle to target must be in range [{ang_min},{ang_max}].")

    return c

def _can_move_to_target_cell(active, cell):
    e = MovementEvent(active.owner, cell, fire=False)
    return e.check_conditions()

can_move_to_target_cell = ActiveCondition("Movement possible", _can_move_to_target_cell,
                        "Can't move to the cell {target}")