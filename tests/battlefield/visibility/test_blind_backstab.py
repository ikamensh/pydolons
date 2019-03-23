from mechanics.events import AttackEvent
from battlefield.Cell import Cell
from battlefield.Facing import Facing

def test_backstab(empty_game, hero, pirate):

    empty_game.add_unit(hero, Cell(1,1))
    empty_game.add_unit(pirate, Cell(1,2))


    hero.facing = Facing.SOUTH
    pirate.facing = Facing.SOUTH

    ae = AttackEvent(pirate, hero)

    assert not ae.is_backstab
    assert ae.is_blind

    pirate.facing = Facing.NORTH
    ae = AttackEvent(pirate, hero)
    assert not ae.is_backstab
    assert not ae.is_blind

    hero.facing = Facing.NORTH
    ae = AttackEvent(pirate, hero)
    assert ae.is_backstab
    assert not ae.is_blind

