from cntent.base_types.pirate import pirate_basetype, pirate_2_basetype, pirate_3_basetype
from cntent.items.std import std_items
from game_objects.monsters.Monster import Monster

pirate_scum = Monster(pirate_basetype,
                      [
                          [std_items.sword_cheap, std_items.dagger_cheap, std_items.axe_cheap],
                          [std_items.pirate_jacket, std_items.inferior_scalemail]
                      ])

pirate_boatswain = Monster(pirate_2_basetype,
                           [
                                [std_items.hammer_superior, std_items.axe_cheap, std_items.sword_superior],
                                [std_items.trollhide_jacket, std_items.inferior_scalemail]
                           ])

pirate_captain = Monster(pirate_3_basetype,
                         [
                            [std_items.smiths_hammer, std_items.elven_skimitar, std_items.sword_superior],
                            [std_items.cuirass, std_items.inferior_scalemail]
                         ])