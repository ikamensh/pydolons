import pytest

from battlefield import Battlefield
from DreamGame import Faction
from DreamGame import DreamGame
from battlefield import Cell
from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject



@pytest.fixture()
def empty_simgame():
    bf = Battlefield(6, 6)
    yield DreamGame(bf)


@pytest.fixture()
def minigame(pirate,  hero):

    bf = Battlefield(6, 6)
    _game = DreamGame(bf)
    _game.add_unit(hero, (2+2j), Faction.PLAYER)
    _game.add_unit(pirate, (4 + 4j), Faction.ENEMY)


    return _game



@pytest.fixture()
def sim_game(hero, pirate_band):
    bf = Battlefield(8, 8)
    _game = DreamGame(bf)

    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    for p, cell in zip(pirate_band, locations):
        p.cell = cell

    hero.cell = Cell(1, 1)
    hero.faction = Faction.PLAYER

    for u in pirate_band + [hero]:
        _game.add_unit(u)

    return _game

@pytest.fixture()
def walls_game(walls_dungeon, hero):
    _game = DreamGame.start_dungeon(walls_dungeon, hero)
    return _game

@pytest.fixture()
def imba_ability():

    imba_dmg_callback = lambda a, unit: unit.lose_health(99999, a.owner)

    _imba_ability = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                            callbacks=[imba_dmg_callback],
                            tags=[ActiveTags.ATTACK],
                           name="imba")

    return _imba_ability

@pytest.fixture()
def tiny_imba_ability():

    imba_dmg_callback = lambda a, unit: unit.lose_health(9, a.owner)

    _imba_ability = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                            callbacks=[imba_dmg_callback],
                            tags=[ActiveTags.ATTACK],
                           name="imba")

    return _imba_ability

@pytest.fixture()
def enabler(imba_ability):

    enabler_callback = lambda a, unit: unit.give_active(imba_ability)

    _enabler = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                            callbacks=[enabler_callback],
                            tags=[ActiveTags.ATTACK],
                           name="gives imba")

    return _enabler


@pytest.fixture()
def increase_utility(minigame):

    minigame.utility = lambda : 0

    def increase_utility(_, __):
        minigame.utility = lambda : 1e3


    _imba_ability = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                           game=minigame,
                            callbacks=[increase_utility],
                           tags=[ActiveTags.ATTACK],
                           name="imba")

    return _imba_ability


@pytest.fixture()
def take_punishment(minigame):
    minigame.utility = lambda: 0

    def punishment_callback(a, unit):
        minigame.utility = lambda: -1e3

    _imba_ability = Active(BattlefieldObject,
                           [],
                           Cost(readiness=0.1),
                           game=minigame,
                           callbacks=[punishment_callback],
                           tags=[ActiveTags.ATTACK],
                           name="imba")

    return _imba_ability



