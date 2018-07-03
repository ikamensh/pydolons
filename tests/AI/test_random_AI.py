from mechanics.AI import RandomAI
from battlefield.Battlefield import Cell

def test_returns_cell(battlefield):

    randomAI = RandomAI(battlefield)
    unit = list(battlefield.unit_locations.keys())[0]

    cell = randomAI.decide_step(unit)
    assert isinstance(cell, Cell)


def test_returns_different_cells(battlefield):
    proposed_cells = set()
    for i in range(100):
        randomAI = RandomAI(battlefield)
        unit = list(battlefield.unit_locations.keys())[0]

        cell = randomAI.decide_step(unit)
        proposed_cells.add(cell)
    assert 1 < len(proposed_cells) < 10