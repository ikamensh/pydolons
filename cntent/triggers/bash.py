from mechanics.events import Trigger
from mechanics.events import DamageEvent
from mechanics.damage import DamageTypeGroups



def bash_callback(t,e:DamageEvent):
    chance = t.chance
    if e.game.random.random() < chance:
        e.target.readiness -= 0.25 * e.source.str / e.target.str


def bash(unit, chance):
    assert 0 < chance <= 1
    trig = Trigger(DamageEvent,
                    conditions=[lambda t,e : e.source.uid == unit.uid,
                                lambda t,e: e.damage.type in DamageTypeGroups.physical],
                    callbacks=[bash_callback])
    trig.chance = chance
    return trig