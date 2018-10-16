from mechanics.buffs import Ability
from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import CharAttributes as ca



fat = lambda : Ability(bonus=Bonus({ca.HEALTH: Attribute(0, 60, 0),
                                     ca.INITIATIVE: Attribute(0, -30, 0)}))



