from mechanics.events import CounteredInterrupt
from mechanics.events import DamageEvent
from mechanics.chances import ImpactFactor


def upgrade_hits(unit, n_hits):
    def upgrade_hit_to_crit_callback(_, damage_event):
        damage_event.impact_factor = ImpactFactor.CRIT

    trig = CounteredInterrupt(
        DamageEvent,
        platform=unit.game.events_platform,
        conditions={
            lambda t,
            e: e.source is unit and e.impact_factor is ImpactFactor.HIT},
        n_counters=n_hits,
        interrupt_event=False,
        callbacks=[upgrade_hit_to_crit_callback])
    return trig
