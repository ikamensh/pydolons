from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import CharAttributes as ca

from mechanics.buffs import Buff


def rest_buff():
    return Buff(2, bonus=Bonus(
                {ca.EVASION: Attribute(0, -35, 0),
                 ca.PRECISION: Attribute(0, -50, 0)}))


def onguard_buff():
    return Buff(2.5, bonus=Bonus(
        {ca.EVASION: Attribute(0, 50, 0),
         ca.PRECISION: Attribute(0, 10, 0)}))
