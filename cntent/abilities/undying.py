from cntent.triggers.immortality import undead_n_hits as undead_trigger
from mechanics.buffs import Ability
from game_objects.attributes import Bonus, Attribute
from game_objects.battlefield_objects import CharAttributes as ca

undead_n_hits = "undead_n_hits"

def trig_factory( ability: Ability):
    owner = ability.bound_to
    return undead_trigger(owner, getattr(ability, undead_n_hits))


def undying(n):
    def _():
        a = Ability(bonuses=[Bonus({ca.STAMINA: Attribute(10,500,0)})],
                    triggers=[trig_factory])
        setattr(a, undead_n_hits, n)
        return a
    return _


