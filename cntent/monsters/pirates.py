from cntent.base_types.pirate import pirate_basetype, pirate_2_basetype, pirate_3_basetype
from cntent.items.std import std_items

import copy

from game_objects.monsters.Monster import Monster

pirate = Monster(pirate_basetype, [std_items.sword_cheap, std_items.pirate_jacket])