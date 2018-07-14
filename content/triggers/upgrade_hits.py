from mechanics.events.Interrupt import CounteredInterrupt
from mechanics.damage import DamageEvent
from mechanics.chances import ImpactFactor


def upgrade_hits(unit, n_hits):
    def upgrade_hit_to_crit_callback(_,  damage_event ):
        damage_event.impact_factor = ImpactFactor.CRIT

    trig = CounteredInterrupt(DamageEvent,
                              conditions={"source":unit, "impact_factor":ImpactFactor.HIT},
                              n_counters=n_hits,
                              interrupt_event=False,
                              event_callbacks=[upgrade_hit_to_crit_callback])
    return trig

