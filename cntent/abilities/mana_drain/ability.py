from cntent.abilities.mana_drain.trigger import build_mana_drain_trigger
from mechanics.buffs import Ability

AMOUNT = "amount"
PCT_DRAIN = "percentage_drain"
PCT_HEAL = "percentage_heal"


def trig_factory( ability: Ability):
    owner = ability.bound_to
    return build_mana_drain_trigger(owner, getattr(ability, AMOUNT), getattr(ability, PCT_DRAIN), getattr(ability, PCT_HEAL))


def mana_drain(amount, percentage_drain, percentage_heal):
    def _():
        a = Ability(triggers=[trig_factory])

        setattr(a, AMOUNT, amount)
        setattr(a, PCT_DRAIN, percentage_drain)
        setattr(a, PCT_HEAL, percentage_heal)

        return a
    return _


