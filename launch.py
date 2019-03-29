from cProfile import Profile
from ui.TheUI import TheUI
import sys

from PySide2 import QtWidgets, QtGui
from LEngine import LEngine


def one_game():
    # Qt application initialization
    app = QtWidgets.QApplication(sys.argv)
    app.setOverrideCursor(
        QtGui.QCursor(
            QtGui.QPixmap('resources/assets/ui/cursor.png'),
            hotX=1,
            hotY=1))
    lengine = LEngine()
    window = TheUI(lengine)
    app.aboutToQuit.connect(window.close_app)
    # sys.exit(app.exec_())
    app.exec_()

# one_game()


profiler = Profile()
profiler.runcall(one_game)
profiler.print_stats('cumulative')
