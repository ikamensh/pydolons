from battlefield.Battlefield import Cell
from content.base_types import mud_golem_basetype
from content.monsters.pirate import pirate
from game_objects.battlefield_objects import Unit
from game_objects.dungeon.Dungeon import Dungeon


pirate_band = [pirate.create() for i in range(3)]
locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]
unit_locations = {pirate_band[i]: locations[i] for i in range(3)}

unit_locations[Unit(mud_golem_basetype)] = Cell(3, 3)


demo_dungeon = Dungeon(unit_locations, 8, 8, hero_entrance=Cell(3, 4))
