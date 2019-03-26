from mechanics.AI import BruteAI
from game_objects.battlefield_objects import Unit
import pytest
from cntent.actives.std.std_misc import wait_active
from DreamGame import DreamGame


def test_returns_actions(minigame):

    ai = BruteAI(minigame)
    unit = list(minigame.units)[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_basetype_gives_valid_actives(sim_game, pirate_basetype):

    pirate_basetype.actives += [wait_active]

    pirate = Unit(pirate_basetype, game=sim_game, cell=0j)
    ai = BruteAI(sim_game)

    sim_game.add_unit(pirate)
    action, target = ai.decide_step(pirate)
    assert isinstance(action, Active)

def test_is_deterministic(minigame, hero):

    actions = set()

    for i in range(30):
        ai = BruteAI(minigame)

        action, target = ai.decide_step(hero, epsilon=0)
        actions.add(action)

    assert 1 == len(actions)

def test_locations_are_intact(minigame, hero, pirate):

    locations_initial = (minigame.bf.cells_to_units,
                         [{u:u.facing} for u in minigame.units])

    for u in minigame.units:
        ai = BruteAI(minigame)

        ai.decide_step(u)
        assert locations_initial == (minigame.bf.cells_to_units,
                                     [{u: u.facing} for u in minigame.units])

def test_chooses_imba_targets_enemy(minigame, imba_ability):


    ai = BruteAI(minigame)
    unit = list(minigame.units)[0]
    unit.give_active(imba_ability)

    action, target = ai.decide_step(unit, epsilon=0)

    assert int(action.uid / 1e7) == imba_ability.uid
    assert target.faction is not unit.faction

# @pytest.mark.skip(reason="non-deterministic ai does not guarantee this.")
def test_no_suicide(sim_game):
    for i in range(10):

        sim_game.enemy_ai = BruteAI(sim_game)
        active_unit = sim_game.turns_manager.get_next()
        active, target = sim_game.enemy_ai.decide_step(active_unit)
        if isinstance(target, Unit):
            if target.faction is active_unit.faction:
                assert False
        active_unit.activate(active, target)


def test_no_friendly_fire(sim_game, hero, pirate):
    for unit in sim_game.units:
        ai = BruteAI(sim_game)
        action, target = ai.decide_step(unit, epsilon=0)
        choices = sim_game.get_all_choices(unit)
        actives = [c[0] for c in choices]
        attack_actives = [a for a in actives if ActiveTags.ATTACK in a.tags]
        if len(attack_actives)>0:
            assert action not in attack_actives

def test_with_obstacle(sim_game, hero, pirate, obstacle):

    sim_game.add_obstacle(obstacle, 5+5j)
    for unit in sim_game.units:
        ai = BruteAI(sim_game)
        choices = sim_game.get_all_choices(unit)
        actives = [c[0] for c in choices]
        real_actives = [sim_game.find_active(a) for a in actives]
    # no exceptions thrown

def test_hits_take_prio(empty_simgame, hero, pirate, no_chances):
    ai = BruteAI(empty_simgame)

    hero.cell = 5 + 5j
    hero.facing = -1j
    empty_simgame.add_unit(hero)

    pirate.cell = 5 + 4j
    pirate.facing = 1j
    empty_simgame.add_unit(pirate)

    for unit in empty_simgame.units:
        unit.fights_hero = True
        action, target = ai.decide_step(unit, epsilon=0)
        choices = empty_simgame.get_all_choices(unit)
        actives = [c[0] for c in choices]
        attack_actives = [a for a in actives if ActiveTags.ATTACK in a.tags]
        if len(attack_actives)>0:
            # delta = game.delta( (action, target) )
            # attack_active = attack_actives[0]
            # atarget = game.get_possible_targets(attack_active)[0]
            # attack_delta = game.delta( (attack_active, atarget) )
            assert action in attack_actives

def test_own_turn_first(minigame, hero, pirate):

    hero.facing = 1j
    pirate.facing = 1 + 0j

    ai = BruteAI(minigame)
    active, target = ai.decide_step(pirate, epsilon=0)

    assert active is pirate.turn_ccw_active


def test_moves_closer(minigame, hero, pirate):
    bf = minigame.bf
    hero.facing = 1j
    pirate.facing = -1j

    distance_before = bf.distance(hero,pirate)

    ai = BruteAI(minigame)
    active, target = ai.decide_step(pirate, epsilon=0)
    pirate.activate(active, target)

    distance_after = bf.distance(hero,pirate)

    assert distance_after < distance_before

def test_moves_closer_too(minigame, hero, pirate):
    bf = minigame.bf
    hero.facing = 1j
    pirate.facing = -1j

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


from DreamGame import Faction
from mechanics.actives import Active, ActiveTags
from battlefield.Facing import Facing
import copy


def test_attacks(empty_game, hero, pirate, no_chances):

    g = empty_game
    pirates = [copy.deepcopy(pirate) for _ in range(3)]
    pirate2, pirate3, pirate4 = pirates

    g.add_unit(hero, (3+3j), Faction.PLAYER)

    g.add_unit(pirate, (3 + 4j), Faction.ENEMY, facing=Facing.NORTH)
    g.add_unit(pirate2, (4 + 3j), Faction.ENEMY, facing=Facing.WEST)
    g.add_unit(pirate3, (3 + 2j), Faction.ENEMY, facing=Facing.SOUTH)
    g.add_unit(pirate4, (2 + 3j), Faction.ENEMY, facing=Facing.EAST)

    ai = BruteAI(g)

    hero.facing = Facing.WEST

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









