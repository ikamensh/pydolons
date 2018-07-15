from game_objects.battlefield_objects.attributes import Attribute, BonusAttributes
from mechanics.buffs import Ability

bonus = Attribute(2, 10, 0)
inner_power = Ability({BonusAttributes.STR: bonus})

bonus = Attribute(0, 0, 3)
great_streingth = Ability({BonusAttributes.STR: bonus})