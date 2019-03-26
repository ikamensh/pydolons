from mechanics.AI import BroadAI
from mechanics.actives import Active
from DreamGame import  DreamGame
from mechanics.AI.SimGame import SimGame
from mechanics.factions import Faction
from game_objects.battlefield_objects import Unit
import pytest


def test_returns_actions(minigame):

    ai = BroadAI(minigame)
    unit = list(minigame.units)[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_locations_are_intact(minigame):

    ai = BroadAI(minigame)
    locations_initial = (minigame.bf.cells_to_objs,
                         [{u:u.facing} for u in minigame.units])

    for u in minigame.units:
        ai.decide_step(u)

        assert locations_initial == (minigame.bf.cells_to_objs,
                                     [{u: u.facing} for u in minigame.units])


def test_chooses_imba_targets_enemy(minigame, imba_ability, hero, pirate):


    ai = BroadAI(minigame)

    ingame_imba = hero.give_active(imba_ability)

    action, target = ai.decide_step(hero)


    assert minigame.delta( (ingame_imba, pirate) ) > 0
    assert minigame.delta( (ingame_imba, hero) ) < 0


    assert action is ingame_imba
    assert target.faction is not hero.faction

def test_chooses_imba_targets_enemy_inverse(minigame, imba_ability, hero, pirate):
    ai = BroadAI(minigame)
    ingame_imba = pirate.give_active(imba_ability)

    action, target = ai.decide_step(pirate)


    assert minigame.delta((ingame_imba, hero)) > 0
    assert minigame.delta((ingame_imba, pirate)) < 0

    assert action is ingame_imba
    assert target.faction is not pirate.faction

def test_uses_enabler_abilities(minigame, enabler):


    ai = BroadAI(minigame)
    unit = list(minigame.units)[0]
    unit.cell = 0j
    ingame_imba = unit.give_active(enabler)

    action, target = ai.decide_step(unit)

    assert action is ingame_imba

@pytest.mark.skip(reason="actions are rolled out and can seem harmless.")
def test_no_friendly_fire(simple_battlefield, hero,  mud_golem, pirate_basetype):
    _game = DreamGame(simple_battlefield)
    _game.add_unit(mud_golem, 3 + 3j, Faction.ENEMY, 1j)
    _game.add_unit(hero, 3 + 4j, Faction.PLAYER, 1 + 0j)

    pirate1 = Unit(pirate_basetype)
    pirate2 = Unit(pirate_basetype)
    pirate3 = Unit(pirate_basetype)


    _game.add_unit(pirate1, 4 + 4j, Faction.ENEMY, -1 + 0j)
    _game.add_unit(pirate2, 4 + 5j, Faction.ENEMY, -1 + 0j)
    _game.add_unit(pirate3, 5 + 3j, Faction.ENEMY, 1 + 0j)

    for i in range(10):

        active_unit = _game.turns_manager.get_next()
        active, target = _game.enemy_ai.decide_step(active_unit)
        if isinstance(target, Unit):
            if target.faction is active_unit.faction:
                assert False
        active_unit.activate(active, target)