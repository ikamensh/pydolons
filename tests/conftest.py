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
def no_chances(monkeypatch):
    monkeypatch.setattr(ChanceCalculator, "chance", lambda x,y,z: 1)


@pytest.fixture()
def pirate_basetype():
    _pirate_basetype = BaseType({}, "Pirate")
    yield  _pirate_basetype


@pytest.fixture()
def demohero_basetype():
    _demohero_basetype = BaseType({'str':45, 'agi': 15,'prc': 15}, "Demo Hero")
    yield  _demohero_basetype

@pytest.fixture()
def hero(demohero_basetype):
    return Unit(demohero_basetype)

@pytest.fixture()
def pirate(pirate_basetype):
    yield Unit(pirate_basetype)

@pytest.fixture()
def mud_golem():
    yield(Unit(mud_golem_basetype))


@pytest.fixture()
def steel_wall():
    resists = {x: -0.6 for x in DamageTypeGroups.physical}
    resists.update({x: 0.75 for x in DamageTypeGroups.elemental})

    _steel_wall = Obstacle("Wall of steel!", 5000, resists=resists, armor=500, icon="wall.png")
    return _steel_wall


@pytest.fixture()
def demo_dungeon(pirate_band):
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    units_locations = {pirate_band[i]: locations[i] for i in range(3)}
    demo_dungeon = Dungeon(units_locations, 8, 8, hero_entrance=Cell(1, 1))

    yield  demo_dungeon

@pytest.fixture()
def walls_dungeon(pirate_basetype, steel_wall):

    unit_locations = {}

    wall_x = 4
    for wall_y in range(0, 6):
        unit_locations[steel_wall.clone()] =  Cell(wall_x, wall_y)

    unit_locations[Unit(pirate_basetype)] = Cell(7, 0)
    _walls_dungeon = Dungeon(unit_locations, 12, 12, hero_entrance=Cell(0, 0))

    yield  _walls_dungeon

@pytest.fixture()
def walls_game(walls_dungeon, hero):
    _game = DreamGame.start_dungeon(walls_dungeon, hero)
    yield _game


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
def game(battlefield, hero):
    _game = DreamGame(battlefield)
    _game.fractions.update({unit: Fractions.ENEMY for unit in battlefield.unit_locations if not unit.is_obstacle})
    _game.fractions[hero] = Fractions.PLAYER
    for unit in battlefield.unit_locations:
        _game.turns_manager.add_unit(unit)
    _game.set_to_context()
    yield _game






