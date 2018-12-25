from mechanics.events import Trigger
from mechanics.events import DamageEvent, HealingEvent


def mana_drain_callback(amount, percentage_mana_drained, percentage_healed):

    def _drain_cb(t,e:DamageEvent):

        mana_initially = e.target.mana

        e.target.mana -= ( e.target.mana * percentage_mana_drained + amount)

        drained = mana_initially - e.target.mana
        healed = drained * percentage_healed

        HealingEvent(healed, target=e.source)

    return _drain_cb

def build_mana_drain_trigger(unit, amount, percentage_drain, percentage_heal):


    cb = mana_drain_callback(amount, percentage_drain, percentage_heal)

    trig = Trigger(DamageEvent,
                              platform=unit.game.events_platform,
                              conditions={lambda t,e : e.source.uid == unit.uid,
                                          lambda t,e: e.amount > 0},
                              callbacks=[cb])
    return trig


