import pytest

from DreamGame import Fractions
from mechanics.AI.SimGame import SimGame
from battlefield.Battlefield import Battlefield
from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject


@pytest.fixture()
def simple_battlefield():
    bf = Battlefield(6, 6)
    return bf

@pytest.fixture()
def minigame(simple_battlefield, pirate,  hero):


    _game = SimGame(simple_battlefield)

    _game.add_unit(hero, (2+2j), Fractions.PLAYER)

    _game.add_unit(pirate, (4 + 4j), Fractions.ENEMY)

    _game.set_to_context()

    return _game

@pytest.fixture()
def game(battlefield, hero):
    _game = SimGame(battlefield)
    _game.fractions.update({unit: Fractions.ENEMY for unit in battlefield.unit_locations if not unit.is_obstacle})
    _game.fractions[hero] = Fractions.PLAYER
    for unit in battlefield.unit_locations:
        _game.turns_manager.add_unit(unit)
    _game.set_to_context()
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
                                [imba_dmg_callback],
                                [ActiveTags.ATTACK],
                           "imba")

    return _imba_ability

@pytest.fixture()
def tiny_imba_ability():

    imba_dmg_callback = lambda a, unit: unit.lose_health(9, a.owner)

    _imba_ability = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                                [imba_dmg_callback],
                                [ActiveTags.ATTACK],
                           "imba")

    return _imba_ability

@pytest.fixture()
def enabler(imba_ability):

    enabler_callback = lambda a, unit: unit.give_active(imba_ability)

    _enabler = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                                [enabler_callback],
                                [ActiveTags.ATTACK],
                           "gives imba")

    return _enabler


@pytest.fixture()
def increase_utility(minigame):

    minigame.utility = lambda : 0

    def increase_utility(_, __):
        minigame.utility = lambda : 1e3


    _imba_ability = Active(BattlefieldObject,
                                [],
                                Cost(readiness=0.1),
                                [increase_utility],
                                [ActiveTags.ATTACK],
                           "imba")

    return _imba_ability


@pytest.fixture()
def take_punishment(minigame):
    minigame.utility = lambda: 0

    def drugs_callback(a, unit):
        minigame.utility = lambda: -1e3

    _imba_ability = Active(BattlefieldObject,
                           [],
                           Cost(readiness=0.1),
                           [drugs_callback],
                           [ActiveTags.ATTACK],
                           "imba")

    return _imba_ability



