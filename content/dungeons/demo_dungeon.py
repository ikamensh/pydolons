from battlefield.Battlefield import Cell
from content.base_types import pirate_basetype, mud_golem_basetype
from game_objects.battlefield_objects import Unit
from game_objects.dungeon.Dungeon import Dungeon
from content.items.std import std_items

import copy

pirate_band = [Unit(pirate_basetype) for i in range(3)]

for pirate in pirate_band:
    pirate.equipment.equip_item( copy.copy(std_items.cheap_sword) )
    pirate.equipment.equip_item( copy.copy(std_items.pirate_jacket) )


locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]


unit_locations = {pirate_band[i]: locations[i] for i in range(3)}
unit_locations[Unit(mud_golem_basetype)] = Cell(3, 3)


demo_dungeon = Dungeon(unit_locations, 8, 8, hero_entrance=Cell(3, 4))
