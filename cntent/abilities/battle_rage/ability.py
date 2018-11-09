from mechanics.buffs import Ability
from cntent.abilities.battle_rage.trigger import battle_rage as br_trigger

def trig_factory( ability: Ability):
    owner = ability.bound_to
    return br_trigger(owner, ability.rage_chance if hasattr(ability, 'rage_chance') else 1)


def battle_rage(chance=1):
    def _():
        a = Ability(triggers=[trig_factory])
        a.rage_chance = chance
        return a
    return _