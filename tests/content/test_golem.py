from cntent.monsters.golems import golem
import pytest


@pytest.fixture()
def just_a_golem(empty_game):
    gol = golem.create(empty_game)
    empty_game.add_unit(gol, 1+1j)
    return gol


def test_discharges(just_a_golem, monkeypatch):

    assert just_a_golem.disabled is False

    monkeypatch.setattr(just_a_golem.turn_ccw_active.cost, "readiness", 100)
    just_a_golem.activate(just_a_golem.turn_ccw_active)

    assert just_a_golem.disabled is True

def test_discharges_stamina(just_a_golem, monkeypatch):

    assert just_a_golem.disabled is False

    just_a_golem.max_stamina += 9999


    monkeypatch.setattr(just_a_golem.turn_ccw_active.cost, "stamina", 100)
    just_a_golem.activate(just_a_golem.turn_ccw_active)

    assert just_a_golem.disabled is True

def test_can_be_disabled(just_a_golem):
    just_a_golem.disabled = True
    assert just_a_golem.disabled

def test_can_be_recharged(just_a_golem):

    just_a_golem.golem_charge = 0
    assert just_a_golem.disabled

    just_a_golem.golem_charge += 1
    assert just_a_golem.disabled is False







