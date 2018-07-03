import pytest
from dungeon.Dungeon import Dungeon
from game_objects.battlefield_objects import Unit, BaseType
from battlefield.Battlefield import Cell, Battlefield
from DreamGame import DreamGame

@pytest.fixture(name="pirate_basetype")
def pirate_basetype_func():
    pirate_basetype = BaseType(10, 10, 5, "Pirate")
    yield  pirate_basetype


@pytest.fixture(name="demohero_basetype")
def demohero_basetype_func():
    demohero_basetype = BaseType(20, 15, 15, "Demo Hero")
    yield  demohero_basetype



@pytest.fixture()
def demo_dungeon(pirate_basetype):
    pirate_band = [Unit(pirate_basetype) for _ in range(3)]
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    units_locations = [(pirate_band[i], locations[i]) for i in range(3)]
    demo_dungeon = Dungeon(units_locations, 8, 8, hero_entrance=Cell(1, 1))

    yield  demo_dungeon


@pytest.fixture()
def hero(demohero_basetype):
    yield Unit(demohero_basetype)

@pytest.fixture()
def pirate(pirate_basetype):
    yield Unit(pirate_basetype)

@pytest.fixture()
def game(demo_dungeon, hero):
    DreamGame.start_dungeon(demo_dungeon, hero)
    yield DreamGame.the_game

@pytest.fixture()
def pirate_band(pirate_basetype):
    _pirate_band = [Unit(pirate_basetype) for i in range(3)]
    yield _pirate_band

@pytest.fixture()
def battlefield(pirate_band, hero):
    bf = Battlefield(8, 8)
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

    units_locations = {pirate_band[i]: locations[i] for i in range(3)}
    units_locations[hero] = Cell(1, 1)
    bf.place_many(units_locations)
    yield bf

@pytest.fixture()
def pirate_band(pirate_basetype):
    _pirate_band = [Unit(pirate_basetype) for i in range(3)]
    yield _pirate_band