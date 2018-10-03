
from PySide2 import QtCore, QtGui, QtWidgets

class ProxyEmit(object):
    """docstring for ProxyEmit."""
    play_movement_anim = None
    def __init__(self, arg):
        super(ProxyEmit, self).__init__()


class GameLoopThread(QtCore.QThread):
    play_movement_anim = QtCore.Signal(dict)
    maybe_play_damage_anim = QtCore.Signal(dict)
    maybe_play_hit_anim = QtCore.Signal(dict)
    def __init__(self, parent=None):
        super(GameLoopThread, self).__init__(parent)
        self.game = None
        self.the_ui = None

    def setSiganls(self, proxy_cls):
        proxy_cls.play_movement_anim = self.play_movement_anim
        proxy_cls.maybe_play_damage_anim = self.maybe_play_damage_anim
        proxy_cls.maybe_play_hit_anim = self.maybe_play_hit_anim
        self.setConnection()

    def setConnection(self):
        self.play_movement_anim.connect(self.the_ui.gameRoot.level.unitMoveSlot)
        # self.maybe_play_damage_anim.connect(self.the_ui.gameRoot.level.targetDamageSlot)
        # self.maybe_play_hit_anim

    def run(self):
        self.game.loop()
