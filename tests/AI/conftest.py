import pytest

from DreamGame import Faction
from mechanics.AI.SimGame import SimGame
from battlefield import Cell, Battlefield
from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject




@pytest.fixture()
def minigame(simple_battlefield, pirate,  hero):

    _game = SimGame(simple_battlefield)
    _game.add_unit(hero, (2+2j), Faction.PLAYER)
    _game.add_unit(pirate, (4 + 4j), Faction.ENEMY)


    return _game



@pytest.fixture()
def sim_game(battlefield8, hero, pirate_band):
    _game = SimGame(battlefield8)

    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
    units_locations = {pirate_band[i]: locations[i] for i in range(3)}

    units_locations[hero] = Cell(1, 1)

    fractions = {unit: Faction.ENEMY for unit in units_locations if not unit.is_obstacle}
    fractions[hero] = Faction.PLAYER

    _game.add_many(units_locations.keys(), units_locations, fractions)
    return _game

@pytest.fixture()
def walls_game(walls_dungeon, hero):
    _game = SimGame.start_dungeon(walls_dungeon, hero)
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



