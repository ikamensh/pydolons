from cntent.items.std import std_items
from cntent.abilities.generic import fat
from cntent.abilities.undying import undying

from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


class zombie_sound_map:
    move = "SftStep3.wav"
    hit = "c_ghast_hit2.wav"
    attack = "c_ghast_atk1.wav"
    perish = "c_ghast_death.wav"

class skeleton_sound_map:
    move = "SftStep3.wav"
    hit = "c_skeleton_hit2.mp3"
    attack = "c_skeleton_atk2.mp3"
    perish = "c_skeleton_death.mp3"

zombie_bt = BaseType({'str':11, 'end':9, 'prc':5, 'agi':5, 'int':3, 'cha':3},
                     "Zombie", abilities=[undying(3), fat], icon="zombie.png", sound_map=zombie_sound_map)

zombie = Monster(zombie_bt,
                      [
                          [std_items.sword_cheap, std_items.hammer_cheap, std_items.axe_cheap],
                          [std_items.jacket_trollhide, std_items.scalemail_inferior]
                      ])

skeleton_bt = BaseType({'str':8, 'end':6, 'prc':5, 'agi':25, 'int':3, 'cha':3},
                     "Skeleton", abilities=[undying(1)], icon="skeleton.png", sound_map=skeleton_sound_map)

skeleton = Monster(skeleton_bt,
                      [
                          [std_items.sword_superior, std_items.hammer_cheap, std_items.axe_cheap],
                          [std_items.cuirass_usual, std_items.scalemail_inferior]
                      ])


