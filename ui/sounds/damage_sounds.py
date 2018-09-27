from mechanics.damage import DamageTypes
import os

sep = os.path.sep
prefix = 'resources' + sep + 'sounds' + sep + 'damage'
prefix = os.path.abspath(prefix)

print(prefix)

class sound_paths:
    slash = os.path.join(prefix, 'slash.wav')
    bash = os.path.join(prefix, 'bash.wav')

    # pierce = prefix + "pierce.wav"
    pierce = os.path.join(prefix, 'pierce.wav')

    fire = os.path.join(prefix, 'fire.wav')
    ice = os.path.join(prefix, 'ice.wav')
    lightning = os.path.join(prefix, 'lightning.wav')
    acid = os.path.join(prefix, 'acid.wav')

    sonic = os.path.join(prefix, 'sonic.wav')


damage_sounds = {}
t = DamageTypes

from ui.sounds.sound import Sound


damage_sounds[t.SLASH] = sound_paths.slash
damage_sounds[t.CRUSH] = sound_paths.bash
# damage_sounds[t.PIERCE] = sound_paths.pierce

# damage_sounds[t.FIRE] = sound_paths.fire
# damage_sounds[t.FROST] = sound_paths.ice
# damage_sounds[t.LIGHTNING] = sound_paths.lightning
# damage_sounds[t.ACID] = sound_paths.acid

# damage_sounds[t.SONIC] = sound_paths.sonic

for k, v in damage_sounds.items():
    damage_sounds[k] = Sound(v)
