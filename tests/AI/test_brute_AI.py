from mechanics.AI import BruteAI
from mechanics.actives import Active
from game_objects.battlefield_objects import Unit


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


def test_no_suicide(game):
    game_over = False
    # while not game_over:
    for i in range(50):

        active_unit = game.turns_manager.get_next()
        fraction = game.fractions[active_unit]
        # utility_before = game.utility(fraction)
        active, target = game.brute_ai.decide_step(active_unit)
        if isinstance(target, Unit):
            assert game.fractions[target] is not game.fractions[active_unit]
        active_unit.activate(active, target)
        # utility_after = game.utility(fraction)
        # print(utility_after - utility_before)
        game_over = game.game_over()
