from mechanics.AI import AstarAI
from mechanics.actives import Active
import pytest


def test_returns_actions(minigame):

    ai = AstarAI(minigame)
    unit = list(minigame.units)[0]

    action, target = ai.decide_step(unit)
    assert isinstance(action, Active)


def test_locations_are_intact(minigame):


    locations_initial = (minigame.bf.cells_to_units,
                         [{u:u.facing} for u in minigame.units])

    for i in range(3):
        ai = AstarAI(minigame)
        unit = list(minigame.units)[0]

        ai.decide_step(unit)
        assert locations_initial == (minigame.bf.cells_to_units,
                                     [{u:u.facing} for u in minigame.units])


def test_chooses_imba_targets_enemy(minigame, imba_ability):

    ai = AstarAI(minigame)
    unit = list(minigame.units)[0]
    unit.give_active(imba_ability)

    action, target = ai.decide_step(unit)

    assert int(action.uid / 1e7) == imba_ability.uid
    assert target.faction is not unit.faction

@pytest.mark.skip(reason="not supported")
def test_uses_enabler_abilities(minigame, enabler):


    ai = AstarAI(minigame)
    unit = list(minigame.units)[0]
    unit.give_active(enabler)

    action, target = ai.decide_step(unit)

    assert int(action.uid / 1e7) == enabler.uid