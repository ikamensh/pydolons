from content.base_types.pirate import pirate_basetype
from content.items.std import std_items

import copy

from game_objects.monsters.Monster import Monster

pirate = Monster(pirate_basetype, [std_items.cheap_sword, std_items.pirate_jacket])