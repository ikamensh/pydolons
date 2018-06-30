import pytest
from dungeon.Dungeon import Dungeon
from game_objects.battlefield_objects.Unit.Unit import Unit
from battlefield.Battlefield import Coordinates
from game_objects.battlefield_objects.Unit.BaseType import BaseType
from DreamGame import DreamGame

@pytest.fixture(name="pirate_basetype")
def pirate_basetype_func():
    pirate_basetype = BaseType(10, 10, 5, "Pirate")
    yield  pirate_basetype


@pytest.fixture(name="demohero_basetype")
def demohero_basetype_func():
    demohero_basetype = BaseType(15, 15, 15, "Demo Hero")
    yield  demohero_basetype



@pytest.fixture()
def demo_dungeon(pirate_basetype):
    pirate_band = [Unit(pirate_basetype) for _ in range(3)]
    locations = [Coordinates(4, 4), Coordinates(4, 5), Coordinates(5, 4)]
    units_locations = [(pirate_band[i], locations[i]) for i in range(3)]
    demo_dungeon = Dungeon(units_locations, 8, 8, hero_entrance=Coordinates(1, 1))

    yield  demo_dungeon


@pytest.fixture()
def hero(demohero_basetype):
    yield Unit(demohero_basetype)

@pytest.fixture(name="game")
def game_demo_dung(demo_dungeon, hero):
    DreamGame.start_dungeon(demo_dungeon, hero)
    yield DreamGame.the_game
