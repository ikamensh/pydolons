from game_objects.attributes import Attribute, Bonus
from game_objects.battlefield_objects import CharAttributes
from mechanics.buffs import Ability

attrib = Attribute(2, 10, 0)
inner_power_bonus = Bonus({CharAttributes.STREINGTH: attrib})
inner_power = Ability([inner_power_bonus])

attrib = Attribute(0, 0, 3)
great_streingth_bonus = Bonus({CharAttributes.STREINGTH: attrib})
great_streingth = Ability([great_streingth_bonus])
