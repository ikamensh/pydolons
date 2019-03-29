from mechanics.events import Trigger
from mechanics.events import DamageEvent
from mechanics.damage import ImpactFactor


def aoe_damage_callback(t, e: DamageEvent):

    bf = e.game.bf
    target_cell = e.target.cell
    recipients = bf.get_units_within_radius(
        center=target_cell, radius=t.radius)
    for unit in recipients:
        new_e = DamageEvent(
            e.damage * t.percentage,
            unit,
            source=e.source,
            impact_factor=ImpactFactor.GRAZE,
            fire=False)
        new_e.secondary = True
        new_e.fire()


def aoe_damage(unit, radius, percentage):
    assert radius >= 0
    trig = Trigger(DamageEvent,
                   platform=unit.game.events_platform,
                   conditions=[lambda t, e: e.impact_factor is ImpactFactor.CRIT and
                               e.source.uid == unit.uid and
                               not hasattr(e, "secondary")],
                   callbacks=[aoe_damage_callback])
    trig.radius = radius
    trig.percentage = percentage
    return trig
