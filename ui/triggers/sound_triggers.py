from ui.sounds.damage_sounds import damage_sounds
from mechanics.events import Trigger, DamageEvent, AttackEvent, UnitDiedEvent, MovementEvent
from ui.triggers.no_sim_condition import no_sim_condition


########### DAMAGE #################

def maybe_play_damage_sound(t, e):
    # alternative - use impact factor to determine the volume
    # volume = (e.damage.amount / e.target.health) ** (1/2)
    # if volume > 0.4:
    sound = damage_sounds[e.damage.type]
    # sound.set_volume(volume)
    sound.play()


def maybe_play_hit_sound(t, e):
    # volume = (e.amount / e.target.health) ** (1/3)
    # if volume > 0.25:
    sound = e.target.sound_map.hit
    # sound.set_volume(volume)
    sound.play()
    # sound.play(delay = 0.2)


def damage_sounds_trig():
    return Trigger(DamageEvent,
                   conditions={no_sim_condition},
                   callbacks=[maybe_play_damage_sound, maybe_play_hit_sound])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

########### ATTACK #################


def play_attack_sound(t, e):
    sound = e.source.sound_map.melee_attack
    sound.play()


def attack_sounds_trig():
    return Trigger(AttackEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_attack_sound])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

########### PERISH #################


def play_perish_sound(t, e):
    sound = e.unit.sound_map.perish
    sound.play()


def perish_sounds_trig():
    return Trigger(UnitDiedEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_perish_sound])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

########### MOVE #################


def play_move_sound(t, e):
    sound = e.unit.sound_map.move
    print(e.unit)
    sound.play()


def move_sounds_trig():
    return Trigger(MovementEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_move_sound])

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #
