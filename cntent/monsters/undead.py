from cntent.items.std import std_items, std_ranged
from cntent.abilities.generic.ability import fat, evasive
from cntent.abilities.undead.ability import undying
from cntent.abilities.mana_drain.ability import mana_drain


from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


class zombie_sound_map:
    move = "SftStep3.wav"
    hit = "c_ghast_hit2.mp3"
    attack = "c_ghast_atk1.mp3"
    perish = "c_ghast_death.mp3"



zombie_bt = BaseType({'str':11, 'end':9, 'prc':5, 'agi':5, 'int':3, 'cha':3},
                     "Zombie", abilities=[undying(3), fat], icon=["zombie.png","zombie3.png","zombie2.jpg"   ], sound_map=zombie_sound_map)

zombie = Monster(zombie_bt,
                      [
                          [std_items.sword_cheap, std_items.hammer_cheap, std_items.axe_cheap],
                          [std_items.jacket_trollhide, std_items.scalemail_inferior]
                      ])

class skeleton_sound_map:
    move = "SftStep3.wav"
    hit = "c_skeleton_hit2.mp3"
    attack = "c_skeleton_atk2.mp3"
    perish = "c_skeleton_death.mp3"


skeleton_bt = BaseType({'str':8, 'end':6, 'prc':5, 'agi':25, 'int':3, 'cha':3},
                     "Skeleton", abilities=[undying(1)], icon=["skeleton.png","kosti2.jpg","kosti.jpg","kost.jpg"], sound_map=skeleton_sound_map)

skeleton = Monster(skeleton_bt,
                      [
                          [std_items.sword_cheap]*2+[ std_items.sword_superior, std_items.hammer_cheap, std_items.axe_cheap],
                          [std_items.cuirass_usual, std_items.scalemail_inferior]
                      ])



skeleton_archer = Monster(skeleton_bt,
                      [
                          [std_ranged.cheap_bow]*3+[ std_ranged.black_bow, std_ranged.quality_crossbow],
                          [std_items.jacket_cheap, std_items.scalemail_inferior]
                      ])


from mechanics.damage import DamageTypes
ghost_bt = BaseType({'str':13, 'end':10, 'prc':13, 'agi':14, 'int':8, 'cha':7},
                     "Ghost", abilities=[undying(2), mana_drain(20, 0.03, 2), evasive(0,50,50)], unarmed_damage_type=DamageTypes.FROST,
                    icon=["skeleton.png","kosti2.jpg","kosti.jpg","kost.jpg"], sound_map=skeleton_sound_map)

ghost = Monster(ghost_bt)