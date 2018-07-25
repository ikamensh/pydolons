import pytest

from DreamGame import DreamGame, Fractions
from battlefield.Battlefield import Battlefield

@pytest.fixture()
def simple_battlefield():
    bf = Battlefield(6, 6)
    yield bf

@pytest.fixture()
def game(simple_battlefield, pirate,  hero):


    _game = DreamGame(simple_battlefield)

    _game.add_unit(hero, (2+2j), Fractions.PLAYER)

    _game.add_unit(pirate, (4 + 4j), Fractions.ENEMY)

    _game.set_to_context()


    yield _game



