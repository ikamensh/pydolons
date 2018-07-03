from battlefield.Battlefield import Cell

def test_valid_placement(battlefield):


    assert len(battlefield.unit_locations) == 4
    for pirate in battlefield.unit_locations:
        assert pirate in battlefield.units_at.values()


def test_cells_eq():
    cell1 = Cell(1, 1)
    cell2 = Cell(1, 1)
    assert cell1 == cell2


