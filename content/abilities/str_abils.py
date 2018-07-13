from mechanics.buffs import Ability
from mechanics.attributes import Attribute, BonusAttributes

bonus = Attribute(2, 10, 0)
inner_power = Ability({BonusAttributes.STR: bonus})

bonus = Attribute(0, 0, 3)
great_streingth = Ability({BonusAttributes.STR: bonus})