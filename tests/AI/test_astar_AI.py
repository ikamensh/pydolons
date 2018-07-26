from mechanics.AI import AstarAI
from mechanics.actives import Active


def test_returns_actions(game):

    ai = AstarAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_locations_are_intact(game):


    locations_initial = (game.battlefield.unit_locations, game.battlefield.unit_facings)

    for i in range(3):
        ai = AstarAI(game)
        unit = list(game.battlefield.unit_locations.keys())[0]

        ai.decide_step(unit)
        assert locations_initial == (game.battlefield.unit_locations, game.battlefield.unit_facings)


def test_chooses_imba_targets_enemy(game, imba_ability):


    ai = AstarAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]
    unit.give_active(imba_ability)

    action, target = ai.decide_step(unit)

    assert int(action.uid / 1e7) == imba_ability.uid
    assert game.fractions[target] is not game.fractions[unit]

def test_uses_enabler_abilities(game, enabler):


    ai = AstarAI(game)
    unit = list(game.battlefield.unit_locations.keys())[0]
    unit.give_active(enabler)

    action, target = ai.decide_step(unit)

    assert int(action.uid / 1e7) == enabler.uid