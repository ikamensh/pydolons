import pytest

from DreamGame import DreamGame, Fractions
from battlefield.Battlefield import Battlefield
from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject
from battlefield import Cell

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

@pytest.fixture()
def imba_ability():

    imba_dmg_callback = lambda a, unit: unit.lose_health(99999, a.owner)

    _imba_ability = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                                [imba_dmg_callback],
                                [ActiveTags.ATTACK],
                           "imba")

    return _imba_ability




