from mechanics.events import AttackEvent
from battlefield.Cell import Cell
from battlefield.Facing import Facing

def test_backstab(game, hero, pirate):

    bf = game.battlefield

    bf.move(hero, Cell(1,1))
    bf.place(pirate, Cell(1,2))
    bf.unit_facings[hero] = Facing.NORTH
    bf.unit_facings[pirate] = Facing.NORTH

    ae = AttackEvent(pirate, hero)

    assert not ae.is_backstab
    assert ae.is_blind

    bf.unit_facings[pirate] = Facing.SOUTH
    ae = AttackEvent(pirate, hero)
    assert not ae.is_backstab
    assert not ae.is_blind

    bf.unit_facings[hero] = Facing.SOUTH
    ae = AttackEvent(pirate, hero)
    assert ae.is_backstab
    assert not ae.is_blind

