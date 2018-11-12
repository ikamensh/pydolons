import pytest

from DreamGame import DreamGame
from battlefield.Battlefield import Cell, Battlefield
from game_objects.battlefield_objects import Unit, BaseType, Obstacle
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.damage import DamageTypeGroups
from mechanics.chances import ChanceCalculator
from mechanics.fractions import Fractions
from cntent.base_types.mud_golem import mud_golem_basetype
from game_objects.battlefield_objects import Obstacle

@pytest.fixture()
def obstacle():
    obstacle = Obstacle("dummy", 500)
    return obstacle


@pytest.fixture()
def no_chances(monkeypatch):
    monkeypatch.setattr(ChanceCalculator, "chance", lambda x,y,z: 1)


@pytest.fixture()
def pirate_basetype():
    _pirate_basetype = BaseType({}, "Pirate")
    yield  _pirate_basetype


@pytest.fixture()
def demohero_basetype():
    _demohero_basetype = BaseType({'str':25, 'agi': 35,'prc': 15}, "Demo Hero")
    yield  _demohero_basetype

@pytest.fixture()
def hero(demohero_basetype, empty_game):
    return Unit(demohero_basetype, game=empty_game)

@pytest.fixture()
def pirate(pirate_basetype, empty_game):
    return Unit(pirate_basetype, game=empty_game)

@pytest.fixture()
def mud_golem():
    yield(Unit(mud_golem_basetype))


@pytest.fixture()
def steel_wall():
    resists = {x: -0.6 for x in DamageTypeGroups.physical}
    resists.update({x: 0.75 for x in DamageTypeGroups.elemental})

    _steel_wall = lambda g: Obstacle("Wall of steel!", 5000, game=g, resists=resists, armor=500, icon="wall.png")
    return _steel_wall


@pytest.fixture()
def demo_dungeon(pirate_band):
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    units_locations = {pirate_band[i]: locations[i] for i in range(3)}
    demo_dungeon = Dungeon(units_locations, 8, 8, hero_entrance=Cell(1, 1))

    yield  demo_dungeon

@pytest.fixture()
def walls_dungeon(pirate_basetype, steel_wall):

    def create_locations(g):
        unit_locations = {}

        wall_x = 4
        for wall_y in range(0, 6):
            unit_locations[steel_wall(g)] =  Cell(wall_x, wall_y)

        unit_locations[Unit(pirate_basetype)] = Cell(7, 0)
        return unit_locations
    _walls_dungeon = Dungeon("test_walls_dung", 12, 12, unit_locations=create_locations, hero_entrance=Cell(0, 0))

    yield  _walls_dungeon

@pytest.fixture()
def walls_game(walls_dungeon, hero):
    _game = DreamGame.start_dungeon(walls_dungeon, hero)
    yield _game


@pytest.fixture()
def pirate_band(pirate_basetype):
    _pirate_band = [Unit(pirate_basetype) for i in range(3)]
    return _pirate_band

@pytest.fixture()
def battlefield8():
    bf = Battlefield(8, 8)

    return bf

@pytest.fixture()
def simple_battlefield():
    bf = Battlefield(6, 6)
    return bf

@pytest.fixture()
def empty_game(simple_battlefield):

    _game = DreamGame(simple_battlefield)

    return _game

@pytest.fixture()
def hero_only_game(battlefield8, hero):

    _game = DreamGame(battlefield8)
    _game.add_unit(hero, 1+1j, Fractions.PLAYER)
    _game.the_hero = hero

    return _game

@pytest.fixture()
def game_hvsp(battlefield8, hero, pirate_band):
    _game = DreamGame(battlefield8)

    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    units_locations = {pirate_band[i]: locations[i] for i in range(3)}

    units_locations[hero] = Cell(1, 1)

    fractions = {unit: Fractions.ENEMY for unit in units_locations if not unit.is_obstacle}
    fractions[hero] = Fractions.PLAYER

    _game.add_many(units_locations.keys(), units_locations, fractions)



    return _game






