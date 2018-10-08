from cntent.items.std import std_items
from cntent.abilities.generic import fat
from cntent.abilities.undying import undying

from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster




zombie_bt = BaseType({'str':11, 'end':9, 'prc':5, 'agi':5, 'int':3, 'cha':3},
                     "Zombie", abilities=[undying(3), fat], icon="zombie.png")

zombie = Monster(zombie_bt,
                      [
                          [std_items.sword_cheap, std_items.hammer_cheap, std_items.axe_cheap],
                          [std_items.trollhide_jacket, std_items.inferior_scalemail]
                      ])

skeleton_bt = BaseType({'str':8, 'end':6, 'prc':5, 'agi':25, 'int':3, 'cha':3},
                     "Skeleton", abilities=[undying(1)], icon="skeleton.png")

skeleton = Monster(skeleton_bt,
                      [
                          [std_items.sword_superior, std_items.hammer_cheap, std_items.axe_cheap],
                          [std_items.cuirass, std_items.inferior_scalemail]
                      ])


