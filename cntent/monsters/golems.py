from cntent.abilities.generic.ability import fat
from cntent.abilities.golem.ability import golem_n_charges


from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


class golems_sound_map:
    move = "SftStep3.wav"
    hit = "c_ghast_hit2.mp3"
    attack = "c_ghast_atk1.mp3"
    perish = "c_ghast_death.mp3"



golem_bt = BaseType({'str':24, 'end':15, 'prc':0, 'agi':2, 'int':2, 'cha':1},
                     "Crude Golem", abilities=[golem_n_charges(15), fat], icon=["golem.png"], sound_map=golems_sound_map)

golem = Monster(golem_bt,
                      [

                      ])



