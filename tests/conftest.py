import pytest

import sys, os
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path +'/../')

from DreamGame import DreamGame
from battlefield.Battlefield import Cell, Battlefield
from game_objects.battlefield_objects import Unit, BaseType, Obstacle
from game_objects.dungeon.Dungeon import Dungeon
from mechanics.damage import DamageTypeGroups
from mechanics.chances import ChanceCalculator
from mechanics.factions import Faction
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
    return Unit(demohero_basetype, game=empty_game, cell=1+1j, faction=Faction.PLAYER)

@pytest.fixture()
def pirate(pirate_basetype, empty_game):
    return Unit(pirate_basetype, game=empty_game, cell=0j)

@pytest.fixture()
def mud_golem():
    yield(Unit(mud_golem_basetype, cell=0j))


@pytest.fixture()
def steel_wall():
    resists = {x: -0.6 for x in DamageTypeGroups.physical}
    resists.update({x: 0.75 for x in DamageTypeGroups.elemental})

    _steel_wall = lambda g, c: Obstacle("Wall of steel!", 5000, game=g, cell=c, resists=resists,
                                     armor=500, icon="wall.png")
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
        units = []

        wall_x = 4
        for wall_y in range(0, 6):
            units.append( steel_wall(g, Cell(wall_x, wall_y)) )
        units.append( Unit(pirate_basetype, cell=Cell(7, 0)) )

        return units

    _walls_dungeon = Dungeon("test_walls_dung", 12, 12, objs=create_locations, hero_entrance=Cell(0, 0))

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
def empty_game():
    bf = Battlefield(6, 6)
    _game = DreamGame(bf)
    return _game

@pytest.fixture()
def huge_game():
    bf = Battlefield(60, 60)
    return DreamGame(bf)


@pytest.fixture()
def hero_only_game(battlefield8, hero):

    _game = DreamGame(battlefield8)
    _game.add_unit(hero)
    _game.the_hero = hero

    return _game

@pytest.fixture()
def game_hvsp(battlefield8, hero, pirate_band):
    _game = DreamGame(battlefield8)

    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    for pirate, cell in zip(pirate_band, locations):
        pirate.cell = cell
        pirate.faction = Faction.ENEMY

    hero.cell = Cell(1, 1)
    hero.faction = Faction.PLAYER

    for unit in pirate_band + [hero]:
        _game.add_unit(unit)



    return _game






