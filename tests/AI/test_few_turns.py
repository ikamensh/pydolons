import copy
from mechanics.fractions import Fractions
from mechanics.events import MovementEvent


def test_few_turns(minigame, hero, pirate):
    minigame.add_unit(hero, 1+1j, fraction=Fractions.NEUTRALS)

    for _ in range(10):
        minigame.add_unit(copy.deepcopy(pirate), 2+2j, Fractions.ENEMY)

    MovementEvent(hero, 2+2j)


    minigame.loop(turns=20)