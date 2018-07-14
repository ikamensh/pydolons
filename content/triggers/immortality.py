from mechanics.events.Interrupt import PermanentInterrupt, CounteredInterrupt
from mechanics.events import UnitDiedEvent
from mechanics.damage import DamageEvent

def immortality(unit):
    trig = PermanentInterrupt(UnitDiedEvent, conditions={"unit":unit})
    return trig

def undead_n_hits(unit, n_hits):
    trig = CounteredInterrupt(UnitDiedEvent, conditions={"unit":unit},
                              n_counters=n_hits)
    return trig

def refraction(unit, n_hits):
    trig = CounteredInterrupt(DamageEvent, conditions={"target": unit},
                              n_counters=n_hits)
    return trig