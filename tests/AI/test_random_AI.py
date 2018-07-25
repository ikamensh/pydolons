from mechanics.AI import RandomAI
from mechanics.actives import Active

def test_returns_actions(game):

    randomAI = RandomAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]

    action, target = randomAI.decide_step(unit)
    assert isinstance(action, Active)

def test_returns_targets_for_targeted_actions(game):

    battlefield = game.battlefield
    randomAI = RandomAI(game)
    unit = list(battlefield.unit_locations.keys())[2]

    for i in range(50):
        action, target = randomAI.decide_step(unit)
        if action.targeting_cls:
            assert target is not None
        else:
            assert target is None


def test_returns_different_actions(game):

    actions = set()

    for i in range(50):
        randomAI = RandomAI(game)
        unit = list(game.battlefield.unit_locations.keys())[0]

        action, target = randomAI.decide_step(unit)
        actions.add(action)

    assert 1 < len(actions) < 30


def test_returns_different_targets(game):
    targets = {}

    for i in range(50):
        randomAI = RandomAI(game)
        unit = list(game.battlefield.unit_locations.keys())[2]

        action, target = randomAI.decide_step(unit)
        targets.setdefault(action, set()).add(target)

    count_diff_targets = [1 for multiple in targets.values() if len(multiple) > 1]
    assert len(count_diff_targets) > 0