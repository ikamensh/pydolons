from battlefield.Cell import Cell
from battlefield.Vision import Vision
from battlefield.Facing import Facing


def test_dead_units_dont_block(empty_game, hero, pirate):

    hero.prc_base += 100
    empty_game.add_unit(hero, Cell(1, 1), facing=Facing.SOUTH)

    vision = empty_game.vision

    free_vision = vision.std_seen_cells(hero)

    pirate.size = 9
    empty_game.add_unit(pirate, Cell(1, 2))

    blocked_vision = vision.std_seen_cells(hero)
    assert blocked_vision != free_vision

    pirate.health -= 99999

    unblocked_vision = vision.std_seen_cells(hero)
    assert unblocked_vision == free_vision


def test_blocks(game_hvsp):

    vision = game_hvsp.vision

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(1, 4),
                           obstacle=Cell(1, 2))
    assert blocks

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(1, 2),
                           obstacle=Cell(1, 4))
    assert blocks == False

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(2, 7),
                           obstacle=Cell(1, 2))
    assert blocks

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(2, 7),
                           obstacle=Cell(1, 3))
    assert blocks


def test_symmetry(game_hvsp):

    vision = game_hvsp.vision

    cells = []
    for x in range(4):
        for y in range(4):
            cells.append(Cell(x, y))

    for cell_from in cells:
        for cell_to in cells:
            if cell_to == cell_from:
                continue
            for obstacle in cells:
                result = vision.blocks(
                    cell_from, cell_to, obstacle) == vision.blocks(
                    cell_to, cell_from, obstacle)
                if not result:
                    print(cell_from, cell_to, obstacle)
                assert result


def test_visibility(game_hvsp, hero, pirate):

    vision = game_hvsp.vision

    hero.prc_base += 100
    hero.cell = Cell(1, 1)
    hero.facing = Facing.SOUTH

    cells_seen = vision.std_seen_cells(hero)
    assert Cell(1, 4) in cells_seen
    assert Cell(1, 5) in cells_seen
    assert Cell(5, 1) in cells_seen

    game_hvsp.add_unit(pirate, cell=1 + 2j)
    pirate.size = 9

    cells_seen = vision.std_seen_cells(hero)

    assert Cell(1, 5) not in cells_seen
    assert Cell(5, 1) in cells_seen
    assert Cell(1, 4) not in cells_seen
