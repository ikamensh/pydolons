from mechanics.damage import DamageEvent, Damage, DamageTypes
from mechanics.events import HealingEvent


def lightning_bolt_callback(active, single_unit_targeting):
    source = active.owner
    target = single_unit_targeting.unit

    spell = active.spell
    n_damage = spell.amount
    dmg = Damage(n_damage, DamageTypes.LIGHTNING)

    DamageEvent(dmg, target=target, source=source)

def healing_callback(active, single_unit_targeting):
    source = active.owner
    target = single_unit_targeting.unit

    spell = active.spell
    HealingEvent(spell.amount, target, source=source)