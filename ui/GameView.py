from PySide2 import QtWidgets, QtCore
from ui.GameConfiguration import GameConfiguration


class GameView(QtWidgets.QGraphicsView):
    resized = QtCore.Signal()
    wheel_change = QtCore.Signal()
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        # Задаем минимальный размер виджета
        self.setMinimumSize(800, 600)
        # Отключаем полосы прокрутки
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #
        self.gameconfig = GameConfiguration()
        self.controller = QtWidgets.QWidget()
        self.setMouseTracking(True)
        # self.controller = None
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.slotAlarmTimer)
        self.timer.start(50)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, e):
        if e.delta() > 0.0:
            self.scale(1.05, 1.05)
        else:
            self.scale(1 / 1.05, 1 / 1.05)
        self.wheel_change.emit()



    def keyPressEvent(self, e):
        super(GameView, self).keyPressEvent(e)
        self.controller.keyPressEvent(e)

    def mouseMoveEvent(self, e):
        super(GameView, self).mouseMoveEvent(e)
        self.controller.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        super(GameView, self).mousePressEvent(e)
        self.controller.mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        super(GameView, self).mouseReleaseEvent(e)
        self.controller.mouseReleaseEvent(e)

    def resizeEvent(self, e):
        self.timer.start(50)
        super().resizeEvent(e)

    def slotAlarmTimer(self):
        w, h = self.width(), self.height()
        self.gameconfig.updateScreenSize(w, h)
        self.scene().setSceneRect(0, 0, w, h)
        self.resized.emit()
