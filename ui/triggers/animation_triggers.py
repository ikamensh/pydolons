from mechanics.events import Trigger, MovementEvent
from ui.triggers.no_sim_condition import no_sim_condition
from ui.gui_util.gamechanel import gamechanel
from ui.TheUI import TheUI

########### DAMAGE #################

def play_movement_anim(t, e):

    TheUI.singleton.gameRoot.cfg.sound_maps["SftStep3.wav"].play()
    level = TheUI.singleton.gameRoot.level
    level.units.moveUnit(e.unit, e.cell_to)
    level.middleLayer.moveSupport(level.units.units_at[e.unit.uid])


def move_anim_trigger():
    return Trigger(MovementEvent,
                   conditions={no_sim_condition},
                   callbacks=[play_movement_anim])