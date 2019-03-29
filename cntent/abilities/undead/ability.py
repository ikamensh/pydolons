from cntent.abilities.undead.trigger import undead_n_hits as undead_trigger
from mechanics.buffs import Ability
from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import CharAttributes as ca

UNDEAD_N_HITS = "undead_n_hits"


def trig_factory(ability: Ability):
    owner = ability.bound_to
    return undead_trigger(owner, getattr(ability, UNDEAD_N_HITS))


def undying(n):
    def _():
        a = Ability(bonus=Bonus({ca.STAMINA: Attribute(10, 200, 0), ca.INITIATIVE: Attribute(
            0, -25, 0)}), trigger_factories=[trig_factory])
        setattr(a, UNDEAD_N_HITS, n)
        return a
    return _
