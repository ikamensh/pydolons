from mechanics.AI import BruteAI
from battlefield.Battlefield import Cell

def test_returns_cell(game):

    randomAI = BruteAI(game.battlefield, game.fractions)
    unit = list(game.battlefield.unit_locations.keys())[0]

    cell = randomAI.decide_step(unit)
    assert isinstance(cell, Cell)


def test_is_deterministic(game):
    proposed_cells = set()
    for i in range(100):
        randomAI = BruteAI(game.battlefield, game.fractions)
        unit = list(game.battlefield.unit_locations.keys())[0]

        cell = randomAI.decide_step(unit)
        proposed_cells.add(cell)
    assert len(proposed_cells) == 1