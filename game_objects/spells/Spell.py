from game_objects.items import Item, ItemTypes
from cntent.actives.conditions.conditions import proximity_condition


class Spell(Item):
    def __init__(self, *, runes, concept,
                 complexity, cost, cooldown,
                 amount, duration, precision_factor, range, radius,
                 resolve_callback):

        super().__init__(concept.name, ItemTypes.SPELL)
        self.targeting_cls = concept.targeting_cls

        self.range = range
        self.targeting_cond = concept.targeting_cond or self.default_cond()
        self.school = concept.school

        self.runes = runes
        self.concept = concept
        self.complexity = complexity
        self.cost = cost
        self.amount = amount
        self.cooldown = cooldown
        self.duration = duration
        self.precision_factor = precision_factor
        self.radius = radius
        self.resolve_callback = resolve_callback

    def default_cond(self):
        if self.targeting_cls:
            return proximity_condition(self.range)
        else:
            return None

    def complexity_check(self, unit):
        return unit.masteries[self.school] + unit.int >= self.complexity

