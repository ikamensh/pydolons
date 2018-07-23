

class Spell:
    def __init__(self, runes, concept,
                 complexity, costs,
                 amount, duration, precision_factor, distance, radius,
                 resolve_callback):

        self.name = concept.name
        self.targeting_cls = concept.targeting_cls
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