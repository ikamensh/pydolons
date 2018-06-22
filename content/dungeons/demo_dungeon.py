from dungeon.Dungeon import Dungeon
from battlefield.Battlefield import Coordinates
from game_objects.battlefield_objects.Unit.Unit import Unit

from content.base_types.pirate import pirate_basetype

pirate_band = [Unit(pirate_basetype) for i in range(3)]
locations = [Coordinates(4,4), Coordinates(4,5), Coordinates(5,4)]

units_locations = [(pirate_band[i], locations[i]) for i in range(3)]


demo_dungeon = Dungeon(units_locations, 8, 8, hero_entrance=Coordinates(1, 1))