from game_objects.attributes import Attribute, AttributesEnum
from mechanics.buffs import Bonus, Ability

attrib = Attribute(2, 10, 0)
inner_power_bonus = Bonus({AttributesEnum.STREINGTH: attrib})
inner_power = Ability([inner_power_bonus])

attrib = Attribute(0, 0, 3)
great_streingth_bonus = Bonus({AttributesEnum.STREINGTH: attrib})
great_streingth = Ability([great_streingth_bonus])
