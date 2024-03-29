from mechanics.events import Trigger, DamageEvent, AttackEvent, UnitDiedEvent, MovementEvent, TurnEvent, NextUnitEvent, ObstacleDestroyedEvent
from ui.core.events import UiErrorMessageEvent, LevelStatusEvent
from ui.core.triggers.no_sim_condition import no_sim_condition
from ui.core.GameLoopThread import ProxyEmit


########### MOVE #################


def play_movement_anim(t, e):
    # comment bug threading
    ProxyEmit.play_movement_anim.emit({'unit':e.unit,"cell_to":e.cell_to})
    # TheUI.singleton.gameRoot.level.unitMoveSlot({'unit':e.unit,"cell_to":e.cell_to})


def move_anim_trigger(game):
    return Trigger(MovementEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[play_movement_anim])


########### DAMAGE #################


def maybe_play_damage_anim(t, e):
    ProxyEmit.maybe_play_damage_anim.emit({'amount':e.amount,'target':e.target, 'damage_type':e.damage.type})
    ProxyEmit.log_event.emit(e)


def maybe_play_hit_anim(t, e):
    ProxyEmit.maybe_play_hit_anim.emit({'sound':e.target.sound_map.hit.lower()})
    ProxyEmit.log_event.emit(e)


def damage_anim_trigger(game):
    return Trigger(DamageEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[maybe_play_damage_anim, maybe_play_hit_anim])


########### ATTACK #################

def play_attack_anim(t, e):
    # print('e dir :\n',dir(e))
    ProxyEmit.maybe_play_hit_anim.emit({'sound':e.source.sound_map.attack.lower()})
    ProxyEmit.log_event.emit(e)


def attack_anin_trigger(game):
    return Trigger(AttackEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[play_attack_anim])

########### DIED #################


def play_perish_anim(t, e):
    ProxyEmit.play_perish_anim.emit({'unit':e.unit, 'corpse':e.corpse, 'sound':e.unit.sound_map.perish.lower()})
    ProxyEmit.log_event.emit(e)


def perish_anim_trigger(game):
    return Trigger(UnitDiedEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[play_perish_anim])


########### Turn #################


def play_trun_anim(t, e):
    ProxyEmit.play_trun_anim.emit({'uid':e.unit.uid,'turn':e.unit.facing})


def turn_anim_trigger(game):
    return Trigger(TurnEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[play_trun_anim])

########### NextUnit #################


def play_nextunit_anim(t, e):
    ProxyEmit.play_nextunit_anim.emit()


def nexunit_anim_trigger(game):
    return Trigger(NextUnitEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[play_nextunit_anim])

########### LevelStatus #################


def play_levelstatus(t, e):
    ProxyEmit.play_levelstatus.emit(e.status)
    ProxyEmit.log_event.emit(e)


def levelstatus_trigger(game):
    return Trigger(LevelStatusEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[play_levelstatus])

########### UiError #################


def display_ui_error(t, e):
    ProxyEmit.play_levelstatus.emit(e.message)


def ui_error_message_trigger(game):
    return Trigger(UiErrorMessageEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[display_ui_error])

########### ObstacleDestroy #################


def obstacle_destroyed(t, e):
    ProxyEmit.obstacle_destroyed.emit({'unit':e.unit})
    ProxyEmit.log_event.emit(e)


def obstacle_destroy_trigger(game):
    return Trigger(ObstacleDestroyedEvent,
                   platform=game.events_platform,
                   conditions={no_sim_condition},
                   callbacks=[obstacle_destroyed])

