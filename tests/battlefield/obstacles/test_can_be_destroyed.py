from game_objects.battlefield_objects import Obstacle
from battlefield.Cell import Cell
from mechanics.damage import DamageTypes, Damage
from mechanics.events import DamageEvent
from mechanics.combat.Attack import Attack
import pytest

@pytest.fixture()
def obstacle(game_hvsp):
    obstacle = Obstacle("dummy", 500, game=game_hvsp)
    game_hvsp.add_obstacle(obstacle, Cell(1, 2))
    return obstacle



def test_can_take_damage(obstacle):
    health_before = obstacle.health
    dmg = Damage(50, DamageTypes.SONIC)
    DamageEvent(dmg, obstacle)

    health_after = obstacle.health
    assert health_after < health_before


def test_can_be_destroyed(obstacle, empty_game):

    empty_game.add_obstacle(obstacle)
    assert obstacle in empty_game.obstacles

    obstacle.health -= 999999
    assert obstacle not in empty_game.obstacles



def test_can_be_attacked(obstacle, hero, no_chances):
    health_before = obstacle.health

    Attack.melee_attack(hero, obstacle)

    health_after = obstacle.health

    assert health_before > health_after
