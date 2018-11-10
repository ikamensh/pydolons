from mechanics.events import Trigger
from mechanics.events import DamageEvent, BuffAppliedEvent
from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import CharAttributes as ca

from mechanics.buffs import Buff


def battle_rage_callback(t,e:DamageEvent):
    chance = t.chance
    if e.game.random.random() < chance:
        BuffAppliedEvent(
            Buff(8, bonus=Bonus(
            {ca.STREINGTH: Attribute(1, 5, 0),
             ca.ENDURANCE: Attribute(1, 5, 0),
             ca.AGILITY: Attribute(1, 5, 0)})),
            e.target)


def battle_rage(unit, chance):
    assert 0 < chance <= 1
    trig = Trigger(DamageEvent,
                   platform=unit.game.events_platform,
                    conditions=[lambda t,e : e.target.uid == unit.uid],
                    callbacks=[battle_rage_callback])
    trig.chance = chance
    return trig