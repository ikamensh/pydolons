from dungeon.Dungeon import Dungeon
from battlefield.Battlefield import cell
from game_objects.battlefield_objects.Unit.Unit import Unit

from content.base_types import pirate_basetype, mud_golem_basetype

pirate_band = [Unit(pirate_basetype) for i in range(3)]
locations = [cell(4, 4), cell(4, 5), cell(5, 4)]


unit_locations = {pirate_band[i]: locations[i] for i in range(3)}
unit_locations[Unit(mud_golem_basetype)] = cell(3, 3)


demo_dungeon = Dungeon(unit_locations, 8, 8, hero_entrance=cell(3, 4))