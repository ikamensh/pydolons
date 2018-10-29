from GameLoopThread import ProxyEmit

from ui.TheUI import TheUI
# import triggers
from ui.triggers.animation_triggers import move_anim_trigger, damage_anim_trigger, attack_anin_trigger, \
    perish_anim_trigger, turn_anim_trigger, nexunit_anim_trigger, levelstatus_trigger, ui_error_message_trigger

import sys

from PySide2 import QtWidgets, QtGui
from LEngine import LEngine


def one_game():
    # Qt application initialization
    app = QtWidgets.QApplication(sys.argv)
    app.setOverrideCursor(QtGui.QCursor(QtGui.QPixmap('resources/assets/ui/cursor.png'), hotX =1, hotY= 1))
    # Logical engine initialization
    lengine = LEngine()
    # Ui engine initialization
    window = TheUI(lengine)
    window.proxyEmit = ProxyEmit
    # window.startGame()
    app.aboutToQuit.connect(window.close_app)
    sys.exit(app.exec_())


one_game()

# from cProfile import Profile
# profiler = Profile()
# profiler.runcall(one_game)
# profiler.print_stats('cumulative')
