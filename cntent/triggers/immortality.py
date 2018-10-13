from mechanics.events import PermanentInterrupt, CounteredInterrupt
from mechanics.events import UnitDiedEvent
from mechanics.events import DamageEvent

def immortality(unit):
    trig = PermanentInterrupt(UnitDiedEvent,
                              platform=unit.game.events_platform,
                              conditions={lambda t,e : e.unit.uid == unit.uid})
    return trig

def undead_n_hits(unit, n_hits):
    trig = CounteredInterrupt(UnitDiedEvent,
                              platform=unit.game.events_platform,
                              conditions={lambda t,e : e.unit.uid == unit.uid},
                              n_counters=n_hits)
    return trig


def refraction(unit, n_hits):
    trig = CounteredInterrupt(DamageEvent,
                              platform=unit.game.events_platform,
                              conditions={lambda t,e : e.target.uid == unit.uid},
                              n_counters=n_hits)
    return trig