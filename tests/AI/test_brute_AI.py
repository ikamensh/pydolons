from mechanics.AI import BruteAI
from mechanics.actives import Active


def test_returns_actions(game):

    ai = BruteAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_is_deterministic(game):

    actions = set()

    for i in range(3):
        ai = BruteAI(game)
        unit = list(game.battlefield.unit_locations.keys())[0]

        action, target = ai.decide_step(unit, epsilon=0)
        actions.add(action)

    assert 1 == len(actions)