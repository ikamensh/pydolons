from PySide2 import QtWidgets, QtCore
from ui.GameConfiguration import GameConfiguration


class GameView(QtWidgets.QGraphicsView):
    resized = QtCore.Signal()
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        # Задаем минимальный размер виджета
        self.setMinimumSize(800, 600)
        # Отключаем полосы прокрутки
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #
        self.gameconfig = GameConfiguration()
        self.setMouseTracking(True)
        self.controller = None
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.slotAlarmTimer)
        self.timer.start(50)

    def wheelEvent(self, e):
        self.controller.wheelEvent(e)

    def keyPressEvent(self, e):
        self.controller.keyPressEvent(e)

    def mouseMoveEvent(self, e):
        self.controller.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        self.controller.mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.controller.mouseReleaseEvent(e)

    def resizeEvent(self, e):
        self.timer.start(50)
        super().resizeEvent(e)

    def slotAlarmTimer(self):
        w, h = self.width(), self.height()
        self.gameconfig.updateScreenSize(w, h)
        self.scene().setSceneRect(0, 0, w, h)
        self.resized.emit()
