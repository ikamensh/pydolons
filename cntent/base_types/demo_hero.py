from game_objects.battlefield_objects.BaseType import BaseType

class hero_sound_map:
    move = "SftStep3.wav"
    hit = "c_skeleton_hit2.mp3"
    attack = "c_skeleton_atk2.mp3"
    perish = "c_skeleton_death.mp3"

demohero_basetype = BaseType({'str':45, 'agi': 35,'prc': 25}, "Demo Hero", icon="hero.png", sound_map=hero_sound_map)