from mechanics.AI import BroadAI
from mechanics.actives import Active
from DreamGame import  DreamGame
from mechanics.fractions import Fractions
from game_objects.battlefield_objects import Unit
import pytest


def test_returns_actions(minigame):

    ai = BroadAI(minigame)
    unit = list(minigame.battlefield.unit_locations.keys())[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_locations_are_intact(minigame):


    locations_initial = (minigame.battlefield.unit_locations, minigame.battlefield.unit_facings)

    for i in range(3):
        ai = BroadAI(minigame)
        unit = list(minigame.battlefield.unit_locations.keys())[0]

        ai.decide_step(unit)
        assert locations_initial == (minigame.battlefield.unit_locations, minigame.battlefield.unit_facings)


def test_chooses_imba_targets_enemy(minigame, imba_ability, hero, pirate):


    ai = BroadAI(minigame)
    ingame_imba = hero.give_active(imba_ability)

    action, target = ai.decide_step(hero)


    assert minigame.delta( (ingame_imba, pirate) ) > 0
    assert minigame.delta( (ingame_imba, hero) ) < 0


    assert action is ingame_imba
    assert minigame.fractions[target] is not minigame.fractions[hero]

def test_chooses_imba_targets_enemy_inverse(minigame, imba_ability, hero, pirate):
    ai = BroadAI(minigame)
    ingame_imba = pirate.give_active(imba_ability)

    action, target = ai.decide_step(pirate)


    assert minigame.delta((ingame_imba, hero)) > 0
    assert minigame.delta((ingame_imba, pirate)) < 0

    assert action is ingame_imba
    assert minigame.fractions[target] is not minigame.fractions[pirate]

def test_uses_enabler_abilities(minigame, enabler):


    ai = BroadAI(minigame)
    unit = list(minigame.battlefield.unit_locations.keys())[0]
    unit.give_active(enabler)

    action, target = ai.decide_step(unit)

    assert int(action.uid / 1e7) == enabler.uid


def test_no_friendly_fire(battlefield, hero,  mud_golem, pirate_basetype):
    _game = DreamGame(battlefield)
    _game.add_unit(mud_golem, 3+3j, Fractions.ENEMY, 1j)
    _game.add_unit(hero, 3 + 4j, Fractions.PLAYER, 1+0j)

    pirate1 = Unit(pirate_basetype)
    pirate2 = Unit(pirate_basetype)
    pirate3 = Unit(pirate_basetype)


    _game.add_unit(pirate1, 4 + 4j, Fractions.ENEMY, -1+0j)
    _game.add_unit(pirate2, 4 + 5j, Fractions.ENEMY, -1+0j)
    _game.add_unit(pirate3, 5 + 3j, Fractions.ENEMY, 1+0j)

    for i in range(50):

        active_unit = _game.turns_manager.get_next()
        active, target = _game.brute_ai.decide_step(active_unit)
        if isinstance(target, Unit):
            if _game.fractions[target] is _game.fractions[active_unit]:
                assert False
        active_unit.activate(active, target)