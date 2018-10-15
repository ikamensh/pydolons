from mechanics.AI import RandomAI
from mechanics.actives import Active

def test_returns_actions(minigame):

    randomAI = RandomAI(minigame)
    unit = list(minigame.battlefield.unit_locations.keys())[0]

    action, target = randomAI.decide_step(unit)
    assert isinstance(action, Active)

def test_returns_targets_for_targeted_actions(minigame):

    battlefield = minigame.battlefield
    randomAI = RandomAI(minigame)
    unit = list(battlefield.unit_locations.keys())[1]

    for i in range(50):
        action, target = randomAI.decide_step(unit)
        if action.targeting_cls:
            assert target is not None
        else:
            assert target is None


def test_returns_different_actions(minigame):

    actions = set()

    for i in range(50):
        randomAI = RandomAI(minigame)
        unit = list(minigame.battlefield.unit_locations.keys())[0]

        action, target = randomAI.decide_step(unit)
        actions.add(action)

    assert 1 < len(actions) < 30


def test_returns_different_targets(minigame):
    targets = {}

    for i in range(50):
        randomAI = RandomAI(minigame)
        unit = list(minigame.battlefield.unit_locations.keys())[1]

        action, target = randomAI.decide_step(unit)
        targets.setdefault(action, set()).add(target)

    count_diff_targets = [1 for multiple in targets.values() if len(multiple) > 1]
    assert len(count_diff_targets) > 0