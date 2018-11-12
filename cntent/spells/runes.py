from game_objects.spells import Rune, SpellAttributes
from game_objects.attributes import Bonus, Attribute


__double_damage_bonus = Bonus({SpellAttributes.AMOUNT: Attribute(0,100,0)})
__double_duration_bonus = Bonus({SpellAttributes.DURATION: Attribute(0,100,0)})


__complexity_cost_bonus = lambda x: Bonus({SpellAttributes.COMPLEXITY: Attribute(0,0,x)})

__low_mana_cost_bonus = lambda x: Bonus({SpellAttributes.MANA_COST: Attribute(0,0,-x)})
__low_cooldown_bonus = lambda x: Bonus({SpellAttributes.COOLDOWN: Attribute(0,0,-x)})




double_damage_rune = Rune([__double_damage_bonus, __complexity_cost_bonus(15)])
double_duration_rune = Rune([__double_duration_bonus, __complexity_cost_bonus(11)])


cheap_casting_rune = Rune([__low_mana_cost_bonus(5), __complexity_cost_bonus(5)])
fast_casting_rune = Rune([__low_cooldown_bonus(1), __complexity_cost_bonus(5)])




