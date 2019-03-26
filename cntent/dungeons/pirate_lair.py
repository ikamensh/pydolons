from battlefield.Battlefield import Cell
from game_objects.dungeon.Dungeon import Dungeon

from cntent.monsters.pirates import pirate_scum, pirate_boatswain, pirate_captain

def create_units(g):
    unit_locations = {}

    pirate_band = [pirate_scum.create(g) for i in range(3)]
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

    unit_locations.update({pirate_band[i]: locations[i] for i in range(3)})
    unit_locations[pirate_boatswain.create(g)] = Cell(6,6)


    pirate_band = [pirate_scum.create(g) for i in range(3)]
    locations = [Cell(4, 12), Cell(4, 13), Cell(5, 12)]

    unit_locations.update({pirate_band[i]: locations[i] for i in range(3)})
    unit_locations[pirate_boatswain.create(g)] = Cell(6,12)


    unit_locations[pirate_boatswain.create(g)] = Cell(12,12)
    unit_locations[pirate_boatswain.create(g)] = Cell(13,12)

    unit_locations[pirate_captain.create(g)] = Cell(14,4)

    for u, c in unit_locations.items():
        u.cell = c

    return list(unit_locations.keys())

from game_objects.battlefield_objects import Wall
def create_walls():
    walls = []

    # split into 2 areas
    walls += [Wall(cell=Cell(8, y)) for y in set(range(0,15)) - {12}]
    # unit_locations[wooden_door()] = Cell(wall_x, 12)

    # 2 rooms in area 1
    walls += [Wall(cell=Cell(x, 8)) for x in set(range(0,8)) - {4}]
    # unit_locations[wooden_door()] = Cell(4, wall_y)

    # captains room in area 2
    walls += [Wall(cell=Cell(11, y)) for y in set(range(0,6)) - {4}]
    walls += [Wall(cell=Cell(x, 6)) for x in range(11,16)]
    # unit_locations[wooden_door()] = Cell(wall_x, 4)

    return walls


pirate_lair = Dungeon("Pirate headquaters", 16, 16,
                      construct_objs=create_units,
                      construct_walls=create_walls,
                      hero_entrance=Cell(2, 0),
                      icon="pirates_3.jpg")




