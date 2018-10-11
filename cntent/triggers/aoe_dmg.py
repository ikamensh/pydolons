from mechanics.events import Trigger
from mechanics.events import DamageEvent
from mechanics.damage import ImpactFactor

import my_context

import random


def aoe_damage_callback(t,e:DamageEvent):

    bf = my_context.the_game.battlefield
    target_cell = bf.unit_locations[e.target]
    recipients = bf.get_units_within_radius(center=target_cell, radius=t.radius)
    for unit in recipients:
        new_e = DamageEvent(e.damage*t.percentage, unit,
                    source=e.source, impact_factor=ImpactFactor.GRAZE, fire=False)
        new_e.secondary = True
        new_e.fire()


def aoe_damage(unit, radius, percentage):
    assert radius >= 0
    trig = Trigger(DamageEvent,
                    conditions=[lambda t,e : e.impact_factor is ImpactFactor.CRIT and
                                             e.source.uid == unit.uid and
                                             not hasattr(e, "secondary")],
                    callbacks=[aoe_damage_callback])
    trig.radius = radius
    trig.percentage = percentage
    return trig