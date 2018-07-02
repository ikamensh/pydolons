from battlefield.Battlefield import Battlefield, cell
from game_objects.battlefield_objects.Unit.Unit import Unit

def test_valid_placement(pirate_basetype, hero):
    bf = Battlefield(8,8)
    pirate_band = [Unit(pirate_basetype) for i in range(3)]
    locations = [cell(4, 4), cell(4, 5), cell(5, 4)]

    units_locations = [(pirate_band[i], locations[i]) for i in range(3)]
    units_locations.append((hero, cell(1, 1)))
    bf.place_many(units_locations)

    assert len(bf.units_at) == 4
    for pirate in pirate_band:
        assert pirate in bf.units_at.values()
        assert pirate in bf.unit_locations


def test_invalid_placement(pirate_basetype, hero):
    bf = Battlefield(8, 8)
    pirate_band = [Unit(pirate_basetype) for i in range(3)]
    locations = [cell(4, 4), cell(4, 5), cell(4, 5)]

    units_locations = [(pirate_band[i], locations[i]) for i in range(3)]
    units_locations.append((hero, cell(1, 1)))
    try:
        bf.place_many(units_locations)
        assert False
    except AssertionError:
        pass

def test_cells_eq():
    cell1 = cell(1,1)
    cell2 = cell(1,1)
    assert cell1 == cell2


