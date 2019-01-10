from game_objects.battlefield_objects.BaseType import BaseType

class hero_sound_map:
    move = "SftStep3.wav"
    hit = "c_skeleton_hit2.mp3"
    attack = "c_skeleton_atk2.mp3"
    perish = "c_skeleton_death.mp3"


from mechanics.actives import Active, ActiveTags
from mechanics.actives import Cost
from game_objects.battlefield_objects import BattlefieldObject


imba_dmg_callback = lambda a, unit: unit.lose_health(99999, a.owner)

imba_active = Active(BattlefieldObject,
                     [],
                     Cost(readiness=0.1),
                     callbacks=[imba_dmg_callback],
                     tags=[ActiveTags.ATTACK],
                     name="imba", cooldown=5)

demohero_basetype = BaseType({'str':45, 'agi': 35,'end': 25}, "Demo Hero", icon="hero.png", sound_map=hero_sound_map,
                             actives=[imba_active])

