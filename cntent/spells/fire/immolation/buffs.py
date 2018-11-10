from mechanics.events import CounteredInterrupt
from mechanics.events import DamageEvent
from mechanics.events import BuffExpiredEvent
from mechanics.buffs import Buff


def burn_callback(t, e: BuffExpiredEvent):
    DamageEvent(damage=t.buff.damage_per_second ,target=t.buff.bound_to, source=t.buff.source)
    e.buff.duration = 1


def burn_trigger(buff):
    t = CounteredInterrupt(BuffExpiredEvent,
                   platform=buff.bound_to.game.events_platform,
                   conditions={lambda t, e: e.buff is buff},
                   callbacks=[burn_callback],
                   n_counters=buff.n_ticks)
    t.buff = buff
    return t

def trigger_factory(buff: Buff):
    t = burn_trigger(buff)
    return t

def build_burning_buff(dps, source, duration) -> Buff:
    b = Buff(1, triggers_factories=[trigger_factory], source=source, name= "Burning")
    b.damage_per_second = dps
    b.n_ticks = duration // 1
    return b