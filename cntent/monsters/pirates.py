from cntent.items.std import std_items
from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


pirate_basetype = BaseType({'int':11, 'cha':7}, "Pirate Scum", icon=["pirate.png", "female-vampire.png"])
pirate_scum = Monster(pirate_basetype,
                      [
                          [std_items.sword_cheap, std_items.dagger_cheap, std_items.axe_cheap],
                          [std_items.jacket_cheap, std_items.scalemail_inferior]
                      ])


pirate_2_basetype = BaseType({'str':13, 'end':12, 'int':11, 'cha':7}, "Pirate Boatswain", icon="pirate.png")
pirate_boatswain = Monster(pirate_2_basetype,
                           [
                                [std_items.hammer_superior, std_items.axe_cheap, std_items.sword_superior],
                                [std_items.jacket_trollhide, std_items.scalemail_inferior]
                           ])


pirate_3_basetype = BaseType({'str':13, 'end':12, 'agi':15, 'prc':16, 'int':11, 'cha':7}, "Pirate Captain", icon="pirate.png")
pirate_captain = Monster(pirate_3_basetype,
                         [
                            [std_items.smiths_hammer, std_items.elven_skimitar, std_items.sword_superior],
                            [std_items.cuirass_usual, std_items.scalemail_inferior]
                         ])