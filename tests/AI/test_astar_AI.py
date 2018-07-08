from mechanics.AI import AstarAI
from battlefield.Battlefield import Cell

def test_returns_cell(game):

    randomAI = AstarAI(game.battlefield, game.fractions)
    unit = list(game.battlefield.unit_locations.keys())[0]

    cell = randomAI.decide_step(unit)
    assert isinstance(cell, Cell)


def test_is_deterministic(game):
    proposed_cells = set()
    for i in range(10):
        randomAI = AstarAI(game.battlefield, game.fractions)
        unit = list(game.battlefield.unit_locations.keys())[0]

        cell = randomAI.decide_step(unit)
        proposed_cells.add(cell)
    assert len(proposed_cells) == 1

def test_avoids_wall(walls_game):
    game = walls_game
    n_turns = game.loop(player_berserk=True)

    assert n_turns < 20

