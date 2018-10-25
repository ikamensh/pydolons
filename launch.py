from GameLoopThread import ProxyEmit

from ui.TheUI import TheUI
# import triggers
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger

import sys

from PySide2 import QtWidgets
from LEngine import LEngine


def one_game():
    # Qt application initialization
    app = QtWidgets.QApplication(sys.argv)
    # Logical engine initialization
    lengine = LEngine()
    # Ui engine initialization
    window = TheUI(lengine)
    game = window.game
    TheUI.singleton = window
    # NEW TRIGGER ADD THIS |
    #
    levelstatus_trigger(game),
    ui_error_message_trigger(game),
    nexunit_anim_trigger(game),
    turn_anim_trigger(game),
    perish_anim_trigger(game),
    attack_anin_trigger(game),
    damage_anim_trigger(game),
    move_anim_trigger(game)

    window.proxyEmit = ProxyEmit
    window.startGame()
    app.aboutToQuit.connect(window.close_app)
    sys.exit(app.exec_())


one_game()

# from cProfile import Profile
# profiler = Profile()
# profiler.runcall(one_game)
# profiler.print_stats('cumulative')
