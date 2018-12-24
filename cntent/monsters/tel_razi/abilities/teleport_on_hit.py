from cntent.monsters.tel_razi.triggers.teleport_on_hit import random_teleport_trigger
from mechanics.buffs import Ability

def trig_factory( ability: Ability):
    owner = ability.bound_to
    return random_teleport_trigger(owner,
                                   ability.random_teleport_radius,
                                   ability.random_teleport_chance,
                                   ability.random_teleport_cost)


def teleport_on_hit(radius, chance, cost):
    def _():
        a = Ability(trigger_factories=[trig_factory])
        a.random_teleport_radius = radius
        a.random_teleport_chance = chance
        a.random_teleport_cost = cost
        return a
    return _


