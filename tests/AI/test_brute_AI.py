from mechanics.AI import BruteAI
from mechanics.actives import Active, ActiveTags
from game_objects.battlefield_objects import Unit
import pytest


def test_returns_actions(minigame):

    ai = BruteAI(minigame)
    unit = list(minigame.battlefield.unit_locations.keys())[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_is_deterministic(minigame, hero):

    actions = set()

    for i in range(30):
        ai = BruteAI(minigame)

        action, target = ai.decide_step(hero, epsilon=0)
        actions.add(action)

    assert 1 == len(actions)

def test_locations_are_intact(minigame, hero, pirate):

    minigame.battlefield.unit_facings[hero] = 1 + 0j
    minigame.battlefield.unit_facings[pirate] = -1 + 0j

    locations_initial = (minigame.battlefield.unit_locations, minigame.battlefield.unit_facings)

    for i in range(10):
        ai = BruteAI(minigame)
        unit = list(minigame.battlefield.unit_locations.keys())[0]

        ai.decide_step(unit)
        assert locations_initial == (minigame.battlefield.unit_locations, minigame.battlefield.unit_facings)

def test_chooses_imba_targets_enemy(minigame, imba_ability):


    ai = BruteAI(minigame)
    unit = list(minigame.battlefield.unit_locations.keys())[0]
    unit.give_active(imba_ability)

    action, target = ai.decide_step(unit, epsilon=0)

    assert int(action.uid / 1e7) == imba_ability.uid
    assert minigame.fractions[target] is not minigame.fractions[unit]

# @pytest.mark.skip(reason="non-deterministic ai does not guarantee this.")
def test_no_suicide(sim_game):
    for i in range(10):

        sim_game.enemy_ai = BruteAI(sim_game)
        active_unit = sim_game.turns_manager.get_next()
        active, target = sim_game.enemy_ai.decide_step(active_unit)
        if isinstance(target, Unit):
            if sim_game.fractions[target] is sim_game.fractions[active_unit]:
                assert False
        active_unit.activate(active, target)


def test_no_friendly_fire(sim_game, hero, pirate):
    for unit in sim_game.battlefield.unit_locations:
        ai = BruteAI(sim_game)
        action, target = ai.decide_step(unit, epsilon=0)
        choices = sim_game.get_all_choices(unit)
        actives = [c[0] for c in choices]
        attack_actives = [a for a in actives if ActiveTags.ATTACK in a.tags]
        if len(attack_actives)>0:
            assert action not in attack_actives

def test_hits_take_prio(sim_game, hero, pirate, no_chances):
    for unit in sim_game.battlefield.unit_locations:
        bf = sim_game.battlefield
        bf.move(hero, 5+5j)
        bf.unit_facings[hero] = -1j
        ai = BruteAI(sim_game)
        action, target = ai.decide_step(unit, epsilon=0)
        choices = sim_game.get_all_choices(unit)
        actives = [c[0] for c in choices]
        attack_actives = [a for a in actives if ActiveTags.ATTACK in a.tags]
        if len(attack_actives)>0:
            # delta = game.delta( (action, target) )
            # attack_active = attack_actives[0]
            # atarget = game.get_possible_targets(attack_active)[0]
            # attack_delta = game.delta( (attack_active, atarget) )
            assert action in attack_actives

def test_own_turn_first(minigame, hero, pirate):

    bf = minigame.battlefield
    bf.unit_facings[hero] = 1j
    bf.unit_facings[pirate] = 1 + 0j

    ai = BruteAI(minigame)
    active, target = ai.decide_step(pirate, epsilon=0)

    assert active is pirate.turn_ccw_active


def test_moves_closer(minigame, hero, pirate):
    bf = minigame.battlefield
    bf.unit_facings[hero] = 1j
    bf.unit_facings[pirate] = -1j

    distance_before = bf.distance(hero,pirate)

    ai = BruteAI(minigame)
    active, target = ai.decide_step(pirate, epsilon=0)
    pirate.activate(active, target)

    distance_after = bf.distance(hero,pirate)

    assert distance_after < distance_before

def test_moves_closer_too(minigame, hero, pirate):
    bf = minigame.battlefield
    bf.unit_facings[hero] = 1j
    bf.unit_facings[pirate] = -1j

    distance_before = bf.distance(hero,pirate)

    ai = BruteAI(minigame)
    active, target = ai.decide_step(hero, epsilon=0)
    hero.activate(active, target)

    distance_after = bf.distance(hero,pirate)

    assert distance_after < distance_before

def chooses_rewarding_action(take_drugs, minigame, hero):

    hero.give_active(take_drugs)
    ai = BruteAI(minigame)

    action, target = ai.decide_step(hero, epsilon=0)

    assert int(action.uid / 1e7) == take_drugs.uid


def avoids_punishing_action(take_punishment, minigame, hero):
    hero.give_active(take_punishment)
    ai = BruteAI(minigame)

    action, target = ai.decide_step(hero, epsilon=0)

    assert int(action.uid / 1e7) != take_punishment.uid


import pytest

from DreamGame import Fractions
from mechanics.AI.SimGame import SimGame
from mechanics.actives import Active, ActiveTags
from battlefield.Facing import Facing
import copy



@pytest.fixture()
def just_hero_game(simple_battlefield, pirate,  hero):

    _game = SimGame(simple_battlefield)
    _game.add_unit(hero, (3+3j), Fractions.PLAYER)


    return _game

def test_attacks(just_hero_game, hero, pirate):

    g = just_hero_game
    pirates = [copy.deepcopy(pirate) for _ in range(3)]
    pirate2, pirate3, pirate4 = pirates

    g.add_unit(pirate, (3 + 4j), Fractions.ENEMY, facing=Facing.NORTH)
    g.add_unit(pirate2, (4 + 3j), Fractions.ENEMY, facing=Facing.WEST)
    g.add_unit(pirate3, (3 + 2j), Fractions.ENEMY, facing=Facing.SOUTH)
    g.add_unit(pirate4, (2 + 3j), Fractions.ENEMY, facing=Facing.EAST)

    ai = BruteAI(g)

    g.battlefield.unit_facings[hero] = Facing.WEST

    a, t = ai.decide_step(pirate)
    assert ActiveTags.ATTACK in a.tags
    assert t is hero
    a.activate(t)
    a, t = ai.decide_step(pirate2)
    assert ActiveTags.ATTACK in a.tags
    assert t is hero
    a.activate(t)
    a, t = ai.decide_step(pirate3)
    assert ActiveTags.ATTACK in a.tags
    assert t is hero
    a.activate(t)
    a, t = ai.decide_step(pirate4)
    assert ActiveTags.ATTACK in a.tags
    assert t is hero









