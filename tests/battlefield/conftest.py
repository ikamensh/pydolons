from battlefield.Battlefield import Cell, Battlefield
import pytest


@pytest.fixture()
def battlefield(pirate_band, hero):
    bf = Battlefield(8, 8)
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

    units_locations = {pirate_band[i]: locations[i] for i in range(3)}
    units_locations[hero] = Cell(1, 1)
    bf.place_many(units_locations)
    yield bf