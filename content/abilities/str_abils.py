from mechanics.buffs import Ability
from mechanics.attributes import Attribute, Attributes

bonus = Attribute(2, 10, 0)
inner_power = Ability({Attributes.STR: bonus})

bonus = Attribute(0, 0, 3)
great_streingth = Ability({Attributes.STR: bonus})