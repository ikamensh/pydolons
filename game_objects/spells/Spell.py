from game_objects.items import Item, ItemTypes


def proximity_condition(active, target):
        return active.game.battlefield.distance(active.owner, target) <= active.spell.distance

class Spell(Item):
    def __init__(self, runes, concept,
                 complexity, cost,
                 amount, duration, precision_factor, distance, radius,
                 resolve_callback):
        super().__init__(concept.name, ItemTypes.SPELL)
        self.targeting_cls = concept.targeting_cls

        self.targeting_cond = concept.targeting_cond or self.default_cond()
        self.school = concept.school

        self.runes = runes
        self.concept = concept
        self.complexity = complexity
        self.cost = cost
        self.amount = amount
        self.duration = duration
        self.precision_factor = precision_factor
        self.distance = distance
        self.radius = radius
        self.resolve_callback = resolve_callback

    def default_cond(self):
        if self.targeting_cls:
            return proximity_condition
        else:
            return lambda a, t: True

    def complexity_check(self, unit):
        return unit.masteries[self.school] + unit.int >= self.complexity

