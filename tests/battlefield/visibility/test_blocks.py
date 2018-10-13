from battlefield.Cell import Cell
from battlefield.Vision import Vision
from battlefield.Facing import Facing


def test_blocks(game_hvsp):

    bf = game_hvsp.battlefield


    vision = Vision(bf)
    blocks = vision.blocks(looking_from=Cell(1,1),
                           looking_to=Cell(1,4),
                           obstacle=Cell(1,2))
    assert blocks == True

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(1, 2),
                           obstacle=Cell(1, 4))
    assert blocks == False

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(2, 7),
                           obstacle=Cell(1, 2))
    assert blocks == True

    blocks = vision.blocks(looking_from=Cell(1, 1),
                           looking_to=Cell(2, 7),
                           obstacle=Cell(1, 3))
    assert blocks == True


def test_symmetry(game_hvsp):

    bf = game_hvsp.battlefield
    vision = Vision(bf)
    cells = []
    for x in range(4):
        for y in range(4):
            cells.append(Cell(x,y))

    for cell_from in cells:
        for cell_to in cells:
            if cell_to == cell_from:
                continue
            for obstacle in cells:
                result = vision.blocks(cell_from, cell_to, obstacle) == vision.blocks(cell_to, cell_from, obstacle)
                if not result:
                    print(cell_from, cell_to, obstacle)
                assert result


def test_visibility(game_hvsp, hero, pirate):

    bf = game_hvsp.battlefield
    hero.prc_base += 100
    bf.move(hero, Cell(1,1))
    bf.unit_facings[hero] = Facing.SOUTH


    vision = Vision(bf)

    cells_seen = vision.std_seen_cells(hero)
    print(cells_seen)
    assert Cell(1, 4) in cells_seen
    assert Cell(1, 5) in cells_seen
    assert Cell(5, 1) in cells_seen


    bf.place(pirate, Cell(1,2))

    cells_seen = vision.std_seen_cells(hero)

    assert Cell(1,5) not in cells_seen
    assert Cell(5,1) in cells_seen
    assert Cell(1, 4) not in cells_seen





