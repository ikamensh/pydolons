import copy
from mechanics.factions import Faction
from mechanics.events import MovementEvent


def test_few_turns(minigame, hero, pirate):
    minigame.add_unit(hero, 1 + 1j, faction=Faction.NEUTRALS)

    for _ in range(10):
        minigame.add_unit(copy.deepcopy(pirate), 2 + 2j, Faction.ENEMY)

    MovementEvent(hero, 2 + 2j)

    minigame.loop(turns=20)
