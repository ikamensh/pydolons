from game_objects.spells import SpellAttributes, Spell
from game_objects.attributes import AttributeWithBonuses, Attribute
from mechanics.actives import Cost
from my_utils.utils import flatten
from game_objects.items import Item, ItemTypes


class SpellConcept(Item):
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

    def __init__(self, name, school, targeting_cls,
                 complexity, cost,
                 amount, duration, precision_factor, distance, radius,
                 resolve_callback, targeting_cond=None):

        super().__init__(name, ItemTypes.SPELL_CONCEPT)
        self.school = school
        self.targeting_cls = targeting_cls
        self.targeting_cond = targeting_cond
        self.complexity_base = Attribute.attribute_or_none(complexity)

        self.mana_cost_base = Attribute.attribute_or_none(cost.mana)
        self.stamina_cost_base = Attribute.attribute_or_none(cost.stamina)
        self.health_cost_base = Attribute.attribute_or_none(cost.health)
        self.readiness_cost_base = Attribute.attribute_or_none(cost.readiness)

        self.amount_base = Attribute.attribute_or_none(amount)
        self.duration_base = Attribute.attribute_or_none(duration)
        self.precision_factor_base = Attribute.attribute_or_none(precision_factor)
        self.distance_base = Attribute.attribute_or_none(distance)
        self.radius_base = Attribute.attribute_or_none(radius)

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
        cost = Cost(self.mana_cost, self.stamina_cost, self.health_cost, self.readiness_cost)
        spell = Spell(runes=runes, concept=self, complexity=self.complexity,
                      cost=cost, amount=self.amount, duration=self.duration,
                      precision_factor=self.precision_factor, distance=self.distance,
                      radius=self.radius, resolve_callback=self.resolve_callback)
        self.runes = None
        return spell



