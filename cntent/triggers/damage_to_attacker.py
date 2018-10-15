from mechanics.events import Trigger
from mechanics.events import AttackEvent
from mechanics.events import DamageEvent


def damage_to_attackers(source, protected_unit, damage, interrupt=False):

    def callback_deal_damage(_, attack_event):
        DamageEvent(damage, target=attack_event.source, source=source)


    trig = Trigger(AttackEvent,
                   conditions={lambda t,e: e.target == protected_unit},
                   platform=protected_unit.game.events_platform,
                   source=source,
                   callbacks=[callback_deal_damage],
                   is_interrupt=interrupt)

    return trig