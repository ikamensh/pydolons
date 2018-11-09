from mechanics.buffs import Ability
from cntent.abilities.bash.trigger import bash as bash_trigger

def trig_factory( ability: Ability):
    owner = ability.bound_to
    return bash_trigger(owner, ability.bash_chance if hasattr(ability, 'bash_chance') else 1)


def bash(chance=1):
    def _():
        a = Ability(triggers=[trig_factory])
        a.bash_chance = chance
        return a
    return _