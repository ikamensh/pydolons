from mechanics.buffs import Ability
from cntent.abilities.aoe_damage.trigger import aoe_damage as aoe_trigger


def trig_factory(ability: Ability):
    owner = ability.bound_to
    return aoe_trigger(
        owner, ability.radius if hasattr(
            ability, 'radius') else None, ability.percentage if hasattr(
            ability, 'percentage') else None)


def aoe_damage(radius=1.5, percentage=1.):
    def _():
        a = Ability(trigger_factories=[trig_factory])
        a.radius = radius
        a.percentage = percentage
        return a
    return _
