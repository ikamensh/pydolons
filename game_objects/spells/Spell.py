from game_objects.items import Item, ItemTypes

from mechanics.actives import CellTargeting, SingleUnitTargeting
import my_globals


def proximity_condition_unit(active, unit_targeting):
        return my_globals.the_game.battlefield.distance(active.owner, unit_targeting.unit) <= active.spell.distance

def proximity_condition_cell(active, cell_targeting):
        return my_globals.the_game.battlefield.distance(active.owner, cell_targeting.cell) <= active.spell.distance


class Spell(Item):
    def __init__(self, runes, concept,
                 complexity, costs,
                 amount, duration, precision_factor, distance, radius,
                 resolve_callback):
        super().__init__(concept.name, ItemTypes.SPELL)
        self.targeting_cls = concept.targeting_cls

        self.targeting_cond = concept.targeting_cond or self.default_cond()
        self.school = concept.school

        self.runes = runes
        self.concept = concept
        self.complexity = complexity
        self.costs = costs
        self.amount = amount
        self.duration = duration
        self.precision_factor = precision_factor
        self.distance = distance
        self.radius = radius
        self.resolve_callback = resolve_callback

    def default_cond(self):
        if self.targeting_cls is SingleUnitTargeting:
            return proximity_condition_unit
        elif self.targeting_cls is CellTargeting:
            return proximity_condition_cell
        else:
            return lambda a, t: True

    def complexity_check(self, unit):
        return unit.masteries[self.school] + unit.int >= self.complexity

