from mechanics.actives import CellTargeting, SingleUnitTargeting
import my_globals

def proximity_condition(max_distance):

    def _(active, targeting):

        if isinstance(targeting, SingleUnitTargeting):
            return my_globals.the_game.battlefield.distance(active.owner, targeting.unit) <= max_distance
        elif isinstance(targeting, CellTargeting):
            return my_globals.the_game.battlefield.distance(active.owner, targeting.cell) <= max_distance
    return _