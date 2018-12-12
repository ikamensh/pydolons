from cntent.abilities.golem.trigger import charge_drop_trigger, CHARGES_FIELD
from mechanics.buffs import Ability
from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import CharAttributes as ca


def trig_factory( ability: Ability):
    owner = ability.bound_to
    return charge_drop_trigger(owner, getattr(ability, CHARGES_FIELD))


def golem_n_charges(n):
    def _():
        a = Ability(bonus=Bonus({ca.ARMOR: Attribute(70, 0, 0)}),
                    trigger_factories=[trig_factory])
        setattr(a, CHARGES_FIELD, n)
        return a
    return _


