from mechanics.events.Trigger import Trigger
from mechanics.combat.AttackEvent import AttackEvent
from content.trigger_packs.fire_damage_to_attacker import fire_damage_to_attacker


def damage_to_attackers(source, protected_unit):
    trig = Trigger(AttackEvent,
                   conditions={"target":protected_unit},
                   source=source,
                   effect_trigger_pack=fire_damage_to_attacker)

    return trig