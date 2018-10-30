from battlefield import Cell

def proximity_condition(max_distance):

    def _(active, target):
        return active.game.battlefield.distance(active.owner, target) <= max_distance
    return _

def range_condition(min_dist, max_dist):

    def _(active, target):
        return min_dist <= active.game.battlefield.distance(active.owner, target) <= max_dist
    return _

def __get_angle(active, target):
    bf = active.game.battlefield
    target_cell = target if isinstance(target, Cell) else bf.unit_locations[target]
    return bf.angle_to(active.owner, target_cell)


def within_angle(max_angle_inkl):
    def _(active, targeting):
        _angle = __get_angle(active, targeting)[0]
        return _angle <= max_angle_inkl

    return _

def between_angles(ang_min, ang_max):
    def _(active, targeting):
        _angle = __get_angle(active, targeting)[0]
        return ang_min <= _angle <= ang_max

    return _

def target_cell_empty(active, cell):
    return active.game.get_units_at(cell) is None