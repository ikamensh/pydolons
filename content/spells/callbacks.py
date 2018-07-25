from mechanics.damage import Damage, DamageTypes
from mechanics.events import HealingEvent, DamageEvent


def lightning_bolt_callback(active, unit):
    source = active.owner
    target = unit

    spell = active.spell
    n_damage = spell.amount
    dmg = Damage(n_damage, DamageTypes.LIGHTNING)

    DamageEvent(dmg, target=target, source=source)

def healing_callback(active, unit):
    source = active.owner
    target = unit

    spell = active.spell
    HealingEvent(spell.amount, target, source=source)