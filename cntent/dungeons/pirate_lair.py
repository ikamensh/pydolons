from battlefield.Battlefield import Cell
from cntent.base_types import mud_wall
from cntent.base_types.doors import wooden_door
from game_objects.dungeon.Dungeon import Dungeon

from cntent.monsters.pirates import pirate_scum, pirate_boatswain, pirate_captain


unit_locations = {}


# split into 2 areas
wall_x = 8
for wall_y in set(range(0,15)) - {12}:
    unit_locations[mud_wall()] = Cell(wall_x, wall_y)
unit_locations[wooden_door()] = Cell(wall_x, 12)

# 2 rooms in area 1
wall_y = 8
for wall_x in set(range(0,8)) - {4}:
    unit_locations[mud_wall()] = Cell(wall_x, wall_y)
unit_locations[wooden_door()] = Cell(4, wall_y)


# captains room in area 2
wall_x = 11
for wall_y in set(range(0,6)) - {4}:
    unit_locations[mud_wall()] = Cell(wall_x, wall_y)
unit_locations[wooden_door()] = Cell(wall_x, 4)

wall_y = 6
for wall_x in range(11,16):
    unit_locations[mud_wall()] = Cell(wall_x, wall_y)



pirate_band = [pirate_scum.create() for i in range(3)]
locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

unit_locations.update({pirate_band[i]: locations[i] for i in range(3)})
unit_locations[pirate_boatswain.create()] = Cell(6,6)


pirate_band = [pirate_scum.create() for i in range(3)]
locations = [Cell(4, 12), Cell(4, 13), Cell(5, 12)]

unit_locations.update({pirate_band[i]: locations[i] for i in range(3)})
unit_locations[pirate_boatswain.create()] = Cell(6,12)


unit_locations[pirate_boatswain.create()] = Cell(12,12)
unit_locations[pirate_boatswain.create()] = Cell(13,12)

unit_locations[pirate_captain.create()] = Cell(14,4)


pirate_lair = Dungeon(unit_locations, 16, 16, hero_entrance=Cell(2, 0))




