from cntent.monsters.tel_razi.triggers.zone_control import zone_control_trigger, zone_control_damage_cond_trigger
from mechanics.buffs import Ability


def trig_factory(ability: Ability):
    owner = ability.bound_to
    return zone_control_trigger(
        owner,
        ability.zone_control_radius,
        ability.zone_control_chance)


def zone_control(radius, chance):
    def _():
        a = Ability(trigger_factories=[trig_factory])
        a.zone_control_radius = radius
        a.zone_control_chance = chance
        return a
    return _


def trig_factory_damage(ability: Ability):
    owner = ability.bound_to
    return zone_control_damage_cond_trigger(
        owner, ability.zone_control_radius, ability.zone_control_chance)


def zone_control_damage(radius, chance):
    def _():
        a = Ability(trigger_factories=[trig_factory_damage])
        a.zone_control_radius = radius
        a.zone_control_chance = chance
        return a
    return _
