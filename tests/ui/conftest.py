import pytest

from DreamGame import DreamGame
from battlefield.Battlefield import Cell, Battlefield
from game_objects.battlefield_objects import Unit, BaseType, Obstacle
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.damage import DamageTypeGroups
from mechanics.chances import ChanceCalculator
from mechanics.fractions import Fractions
from content.base_types.mud_golem import mud_golem_basetype

@pytest.fixture()
def empty_battlefield(hero):

    bf = Battlefield(8, 8)
    units_locations = {hero: Cell(1,1)}
    bf.place_many(units_locations)

    yield bf

@pytest.fixture()
def empty_game(empty_battlefield, hero):
    _game = DreamGame(empty_battlefield)
    _game.fractions[hero] = Fractions.PLAYER
    for unit in empty_battlefield.unit_locations:
        _game.turns_manager.add_unit(unit)
    _game.set_to_context()
    _game.the_hero = hero
    yield _game