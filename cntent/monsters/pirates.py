from cntent.items.std import std_items
from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster

class pirate_sound_map:
    move = "SftStep3.wav"
    hit = "fat_1_male_hit_4.wav"
    attack = "fat_1_male_attack_1.wav"
    perish = "male_1_death_3.wav"


pirate_basetype = BaseType({'int':11, 'cha':7}, "Pirate Scum", icon=["pirate.jpg","pirate.png", "pirate skirmisher.jpg"], sound_map=pirate_sound_map)
pirate_scum = Monster(pirate_basetype,
                      [
                          [std_items.sword_cheap, std_items.dagger_cheap, std_items.axe_cheap],
                          [std_items.jacket_cheap, std_items.scalemail_inferior]
                      ])


pirate_2_basetype = BaseType({'str':13, 'end':12, 'int':11, 'cha':7}, "Pirate Boatswain", icon=["pirate female.png", "pirate brute.jpg", "pirat.jpg"], sound_map=pirate_sound_map)
pirate_boatswain = Monster(pirate_2_basetype,
                           [
                                [std_items.hammer_superior, std_items.axe_cheap, std_items.sword_superior],
                                [std_items.jacket_trollhide, std_items.scalemail_inferior]
                           ])


pirate_3_basetype = BaseType({'str':13, 'end':12, 'agi':15, 'prc':16, 'int':11, 'cha':7}, "Pirate Captain", icon=["pirate captain.jpg", "pirate thief.jpg"], sound_map=pirate_sound_map)
pirate_captain = Monster(pirate_3_basetype,
                         [
                            [std_items.smiths_hammer, std_items.elven_skimitar, std_items.sword_superior],
                            [std_items.cuirass_usual, std_items.scalemail_inferior]
                         ])