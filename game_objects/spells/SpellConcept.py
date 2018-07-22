from game_objects.spells import SpellAttributes, Spell
from game_objects.battlefield_objects.attributes import AttributeWithBonuses
from mechanics.actives import Costs
from my_utils.utils import flatten

class SpellConcept:
    complexity = AttributeWithBonuses("complexity_base", SpellAttributes.COMPLEXITY)

    mana_cost = AttributeWithBonuses("mana_cost_base", SpellAttributes.MANA_COST)
    stamina_cost = AttributeWithBonuses("stamina_cost_base", SpellAttributes.STAMINA_COST)
    health_cost = AttributeWithBonuses("health_cost_base", SpellAttributes.HEALTH_COST)
    readiness_cost = AttributeWithBonuses("readiness_cost_base", SpellAttributes.READINESS_COST)

    amount = AttributeWithBonuses("amount_base", SpellAttributes.AMOUNT)
    duration = AttributeWithBonuses("duration_base", SpellAttributes.DURATION)
    precision_factor = AttributeWithBonuses("precision_factor_base", SpellAttributes.PRECISION_FACTOR)
    distance = AttributeWithBonuses("distance_base", SpellAttributes.DISTANCE)
    radius = AttributeWithBonuses("radius_base", SpellAttributes.RADIUS)

    def __init__(self, name, school, complexity, costs,
                 amount, duration, precision_factor, distance, radius,
                 resolve_callback):

        self.name = name
        self.school = school
        self.complexity_base = complexity

        self.mana_cost_base = costs.mana
        self.stamina_cost_base = costs.stamina
        self.health_cost_base = costs.health
        self.readiness_cost_base = costs.readiness


        self.amount_base = amount
        self.duration_base = duration
        self.precision_factor_base = precision_factor
        self.distance_base = distance
        self.radius_base = radius

        self.resolve_callback = resolve_callback
        self.runes = None

    @property
    def bonuses(self):
        if self.runes is None:
            return []
        else:
            return flatten([rune.bonuses for rune in self.runes])

    def to_spell(self, runes):
        self.runes = runes
        costs = Costs(self.mana_cost, self.stamina_cost, self.health_cost, self.readiness_cost)
        spell = Spell(runes=runes, concept=self, complexity=self.complexity,
                      costs=costs, amount=self.amount, duration=self.duration,
                      precision_factor=self.precision_factor, distance=self.distance,
                      radius=self.radius, resolve_callback=self.resolve_callback)
        self.runes = None
        return spell



