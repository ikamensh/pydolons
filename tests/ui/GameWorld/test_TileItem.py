from ui.GameWorld.TileItem import TileItem
from battlefield.Cell import Cell

def init_map(tile_map:TileItem, cells):
    for cell in cells:
        tile_map.add_cell(0, cell)

def test_calculate_bound():
    points_1 = [Cell(1,1),Cell(1,0), Cell(0,1), Cell(0,2)]
    points_2 = [Cell(1,1),Cell(0,0), Cell(0,1), Cell(1,2)]
    cell_1 = Cell(0, 0)
    cell_2 = Cell(1, 2)

    tile_map_1 = TileItem(gameRoot=None)
    init_map(tile_map_1, points_1)
    assert tile_map_1._cell_1 == cell_1
    assert tile_map_1._cell_2 == cell_2

    tile_map_2 = TileItem(gameRoot=None)
    init_map(tile_map_2, points_2)
    assert tile_map_2._cell_1 == cell_1
    assert tile_map_2._cell_2 == cell_2
