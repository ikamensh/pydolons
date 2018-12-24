from cntent.monsters.tel_razi.triggers.charge_drop import charge_drop_trigger
from mechanics.buffs import Ability
from game_objects.attributes import Bonus
from game_objects.battlefield_objects import CharAttributes as ca
from mechanics.damage import Armor


def trig_factory( ability: Ability):
    owner = ability.bound_to
    return charge_drop_trigger(owner, ability.max_golem_charges)


def golem_n_charges(n):
    def _():
        a = Ability(name=f"Golem with {n} charges",
                    bonus=Bonus({ca.ARMOR: Armor(40)}),
                    trigger_factories=[trig_factory])
        a.max_golem_charges = n
        return a
    return _


