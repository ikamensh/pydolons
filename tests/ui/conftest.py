import pytest

from DreamGame import DreamGame
from battlefield.Battlefield import Cell, Battlefield
from game_objects.battlefield_objects import Unit, BaseType, Obstacle
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.damage import DamageTypeGroups
from mechanics.chances import ChanceCalculator
from mechanics.fractions import Fractions
from cntent.base_types.mud_golem import mud_golem_basetype

@pytest.fixture()
def empty_battlefield():

    bf = Battlefield(8, 8)

    yield bf

@pytest.fixture()
def hero_only_game(empty_battlefield, hero):

    _game = DreamGame(empty_battlefield)
    _game.add_unit(hero, 1+1j, Fractions.PLAYER)
    _game.the_hero = hero

    yield _game