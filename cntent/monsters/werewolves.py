from cntent.items.std import std_items as si
from cntent.abilities.generic.ability import fat
from cntent.abilities.bash.ability import bash
from cntent.abilities.battle_rage.ability import battle_rage
from cntent.abilities.aoe_damage.ability import aoe_damage
from mechanics.damage import DamageTypes as dt

from game_objects.battlefield_objects import BaseType
from game_objects.monsters.Monster import Monster


class WerewolfSoundMap:
    move = "SftStep3.wav"
    hit = "c_ogre_hit1.wav"
    attack = "c_ogre_atk1.wav"
    perish = "c_ogre_death.wav"


werewolf_bt = BaseType(
    {'str': 22, 'end': 25, 'prc': 20, 'agi': 15, 'int': 20, 'cha': 12},
    "Werewolf",
    sound_map=WerewolfSoundMap,
    resists={dt.SLASH: 0.30},
    abilities=[bash(0.5), battle_rage(1), aoe_damage(radius=2,percentage=0.5)],
    icon=["werewolf.jpg"]
)

werewolf = Monster(
    werewolf_bt,
    [
        [si.smiths_hammer, si.hammer_superior, si.axe_superior, si.axe_ancient],
        [si.jacket_trollhide, si.scalemail_inferior, si.jacket_usual, si.cuirass_usual]
    ]
)