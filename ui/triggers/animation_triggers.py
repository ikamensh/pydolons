from mechanics.events import Trigger, DamageEvent, AttackEvent, UnitDiedEvent, MovementEvent, TurnEvent
from ui.triggers.no_sim_condition import no_sim_condition
from ui.gui_util.gamechanel import gamechanel
from ui.TheUI import TheUI
from GameLoopThread import ProxyEmit


########### MOVE #################


def play_movement_anim(t, e):
    ProxyEmit.play_movement_anim.emit({'unit':e.unit,"cell_to":e.cell_to})
    pass


def move_anim_trigger():
    return Trigger(MovementEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_movement_anim])

########### DAMAGE #################

def maybe_play_damage_anim(t, e):
    ProxyEmit.maybe_play_damage_anim.emit({'amount':e.amount,'target':e.target, 'damage_type':e.damage.type})
    pass

def maybe_play_hit_anim(t, e):
    ProxyEmit.maybe_play_hit_anim.emit({'sound':e.target.sound_map.hit})
    pass

def damage_anim_trigger():
    return Trigger(DamageEvent,
                   conditions={no_sim_condition},
                   callbacks=[maybe_play_damage_anim, maybe_play_hit_anim])
########### ATTACK #################

def play_attack_anim(t, e):
    # print('e dir :\n',dir(e))
    ProxyEmit.maybe_play_hit_anim.emit({'sound':e.source.sound_map.attack})
    pass

def attack_anin_trigger():
    return Trigger(AttackEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_attack_anim])

########### DIED #################


def play_perish_anim(t, e):
    ProxyEmit.play_perish_anim.emit({'unit':e.unit, 'sound':e.unit.sound_map.perish})
    pass

def perish_anim_trigger():
    return Trigger(UnitDiedEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_perish_anim])

 # gamechanel.sendMessage({'event':'TurnEvent','uid':self.unit.uid,'turn':new_turning})

########### Turn #################


def play_trun_anim(t, e):
    ProxyEmit.play_trun_anim.emit({'uid':e.unit.uid,'turn':e.battlefield.unit_facings[e.unit]})
    pass

def turn_anim_trigger():
    return Trigger(TurnEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_trun_anim])
