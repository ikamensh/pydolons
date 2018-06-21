from battlefield.Battlefield import Battlefield, Coordinates
from game_objects.battlefield_objects.Unit.Unit import Unit
from game_objects.battlefield_objects.Unit.base_types.demo_hero import demohero_basetype
from game_objects.battlefield_objects.Unit.base_types.pirate import pirate_basetype

def test_valid_placement():
    bf = Battlefield(8,8)
    pirate_band = [Unit(pirate_basetype) for i in range(3)]
    locations = [Coordinates(4,4), Coordinates(4,5), Coordinates(5,4)]

    units_locations = [(pirate_band[i], locations[i]) for i in range(3)]
    units_locations.append((Unit(demohero_basetype), Coordinates(1,1)))
    bf.place_many(units_locations)

    assert len(bf.units) == 4
    for pirate in pirate_band:
        assert pirate in bf.units.values()
        assert pirate in bf.unit_locations


def test_invalid_placement():
    bf = Battlefield(8, 8)
    pirate_band = [Unit(pirate_basetype) for i in range(3)]
    locations = [Coordinates(4, 4), Coordinates(4, 5), Coordinates(4, 5)]

    units_locations = [(pirate_band[i], locations[i]) for i in range(3)]
    units_locations.append((Unit(demohero_basetype), Coordinates(1, 1)))
    try:
        bf.place_many(units_locations)
        assert False
    except AssertionError:
        pass


