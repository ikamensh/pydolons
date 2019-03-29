from battlefield.Battlefield import Cell
from cntent.base_types import mud_golem_basetype, mud_wall
from cntent.monsters.pirates import pirate_basetype
from game_objects.battlefield_objects import Unit
from game_objects.dungeon.Dungeon import Dungeon
from game_objects.battlefield_objects import Wall


def create_units(g):
    pirate_band = [Unit(pirate_basetype) for i in range(3)]
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

    unit_locations = {pirate_band[i]: locations[i] for i in range(3)}

    unit_locations[Unit(mud_golem_basetype)] = Cell(11, 0)

    for u, c in unit_locations.items():
        u.cell = c

    return list(unit_locations.keys())


def create_walls():
    return [Wall(cell=Cell(8, y)) for y in range(9)]


walls_dungeon = Dungeon("Great Wall", 12, 12,
                        construct_objs=create_units,
                        construct_walls=create_walls,
                        hero_entrance=Cell(3, 4),
                        icon="pirates_2.jpg")
