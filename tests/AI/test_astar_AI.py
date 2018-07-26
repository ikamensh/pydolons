from mechanics.AI import AstarAI
from mechanics.actives import Active


def test_returns_actions(game):

    ai = AstarAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_is_deterministic(game):

    actions = set()

    for i in range(3):
        ai = AstarAI(game)
        unit = list(game.battlefield.unit_locations.keys())[0]

        action, target = ai.decide_step(unit)
        actions.add(action)

    assert 1 == len(actions)

def test_chooses_imba_targets_enemy(game, imba_ability):


    ai = AstarAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]
    unit.give_active(imba_ability)

    action, target = ai.decide_step(unit)

    assert int(action.uid / 1e7) == imba_ability.uid
    assert game.fractions[target] is not game.fractions[unit]