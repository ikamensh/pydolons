from game_objects.spells import Rune, SpellAttributes
from game_objects.attributes import Bonus, Attribute


__double_damage_bonus = Bonus({SpellAttributes.AMOUNT: Attribute(0,100,0)})
__complexity_cost_bonus = Bonus({SpellAttributes.COMPLEXITY: Attribute(0,0,20)})


double_damage_rune = Rune([__double_damage_bonus, __complexity_cost_bonus])


