from cntent.items.std import std_items as si
from cntent.abilities.generic import fat
from cntent.abilities.bash import bash
from cntent.abilities.battle_rage import battle_rage
from cntent.abilities.aoe_damage import aoe_damage


from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


class goblin_sound_map:
    move = "SftStep3.wav"
    hit = "c_goblin_hit2.wav"
    attack = "ATTACK_WOLF_2.wav"
    perish = "c_goblin_death.wav"

class orc_sound_map:
    move = "SftStep3.wav"
    hit = "c_goblin_hit2.wav"
    attack = "ATTACK_WOLF_2.wav"
    perish = "c_goblin_death.wav"

class ogre_sound_map:
    move = "SftStep3.wav"
    hit = "c_goblin_hit2.wav"
    attack = "ATTACK_WOLF_2.wav"
    perish = "c_goblin_death.wav"


goblin_bt = BaseType({'str':8, 'end':7, 'prc':15, 'agi':15, 'int':12, 'cha':7},
                     "Goblin", abilities=[battle_rage(1)], icon="goblin.png", sound_map=goblin_sound_map)

goblin = Monster(goblin_bt,
                      [
                          [si.dagger_cheap, si.dagger_superior, si.sword_cheap, si.spear_cheap],
                          [si.jacket_usual, si.jacket_cheap]
                      ])


orc_bt = BaseType({'str':14, 'end':14, 'prc':12, 'agi':12, 'int':6, 'cha':6},
                     "Orc", abilities=[bash(0.33), fat, battle_rage(1)], icon="orc.png", sound_map=orc_sound_map)

orc = Monster(orc_bt,
                      [
                          [si.axe_superior, si.hammer_superior, si.sword_superior],
                          [si.jacket_trollhide, si.scalemail_inferior, si.jacket_usual, si.cuirass_usual]
                      ])

ogre_bt = BaseType({'str':22, 'end':25, 'prc':14, 'agi':9, 'int':10, 'cha':4},"Ogre", sound_map=ogre_sound_map,
                   abilities=[bash(0.5), fat, battle_rage(1), aoe_damage(radius=2,percentage=0.5)], icon="ogre.png")

ogre = Monster(ogre_bt,
                      [
                          [si.smiths_hammer, si.hammer_superior, si.axe_superior, si.axe_ancient],
                          [si.jacket_trollhide, si.scalemail_inferior, si.jacket_usual, si.cuirass_usual]
                      ])