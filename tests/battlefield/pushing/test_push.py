from mechanics.events import MovementEvent, PushEvent

def test_no_push(empty_game, hero, pirate, monkeypatch):
    empty_game.add_unit(hero, 1+1j)
    empty_game.add_unit(pirate, 2+2j)

    called = []
    def fake_resolved(*args):
        called.append("zip")

    monkeypatch.setattr(PushEvent, "resolve", fake_resolved)

    MovementEvent(hero, 2+2j)

    assert not called
    assert hero.cell == 2+2j

import pytest
import copy
from exceptions import PydolonsError

def test_push(empty_game, hero, pirate, monkeypatch):
    empty_game.add_unit(hero, 1+1j)

    empty_game.add_unit(copy.copy(pirate), 2+2j)
    empty_game.add_unit(copy.copy(pirate), 2+2j)
    empty_game.add_unit(copy.copy(pirate), 2+2j)


    def fake_resolved(*args):
        raise PydolonsError("bla")

    monkeypatch.setattr(PushEvent, "resolve", fake_resolved)

    with pytest.raises(PydolonsError):
        MovementEvent(hero, 2+2j)


def test_mass_push(empty_game, hero, pirate):
    empty_game.add_unit(hero, 1+1j)

    for _ in range(10):
        empty_game.add_unit(copy.copy(pirate), 2+2j)

    MovementEvent(hero, 2+2j)
    assert len(empty_game.bf.get_units_at(2+2j)) == 3






