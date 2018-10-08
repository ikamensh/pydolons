from cntent.triggers.immortality import undead_n_hits
from mechanics.buffs import Ability


def trig_factory( ability: Ability):
    owner = ability.bound_to
    return undead_n_hits(owner, ability.undead_n_hits if hasattr(ability, 'undead_n_hits') else 2)


def undying(n):
    def _():
        a = Ability(triggers=[trig_factory])
        a.undead_n_hits = n
        return a
    return _


