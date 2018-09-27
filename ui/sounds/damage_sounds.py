from mechanics.damage import DamageTypes

prefix = "resources/sounds/damage/"

class sound_paths:
    slash = prefix + "slash.wav"
    bash = prefix + "bash.wav"
    pierce = prefix + "pierce.wav"

    fire = prefix + "fire.wav"
    ice = prefix + "ice.wav"
    lightning = prefix + "lightning.wav"
    acid = prefix + "acid.wav"

    sonic = prefix + "sonic.wav"


damage_sounds = {}
t = DamageTypes

from ui.sounds.sound import Sound

damage_sounds[t.SLASH] = sound_paths.slash
damage_sounds[t.CRUSH] = sound_paths.bash
damage_sounds[t.PIERCE] = sound_paths.pierce

damage_sounds[t.FIRE] = sound_paths.fire
damage_sounds[t.FROST] = sound_paths.ice
damage_sounds[t.LIGHTNING] = sound_paths.lightning
damage_sounds[t.ACID] = sound_paths.acid

damage_sounds[t.SONIC] = sound_paths.sonic

for k, v in damage_sounds.items():
    damage_sounds[k] = Sound(v)




