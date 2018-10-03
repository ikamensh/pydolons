from mechanics.events import Trigger, DamageEvent, AttackEvent, UnitDiedEvent, MovementEvent
from ui.triggers.no_sim_condition import no_sim_condition
from ui.gui_util.gamechanel import gamechanel
from ui.TheUI import TheUI
from GameLoopThread import ProxyEmit

########### DAMAGE #################



def play_movement_anim(t, e):
    ProxyEmit.play_movement_anim.emit({'unit':e.unit,"cell_to":e.cell_to})
    pass


def move_anim_trigger():
    return Trigger(MovementEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_movement_anim])


def maybe_play_damage_anim(t, e):
    print('debug->damage_trig',dir(e))
    print('debug->',e.damage.type)
    ProxyEmit.maybe_play_damage_anim.emit({'type':e})
    pass

def maybe_play_hit_anim(t, e):
    print('debug->hit_trig',dir(e))
    pass

def damage_anim_trigger():
    return Trigger(DamageEvent,
                   conditions={no_sim_condition},
                   callbacks=[maybe_play_damage_anim, maybe_play_hit_anim])
