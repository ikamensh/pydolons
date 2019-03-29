from PySide2 import QtWidgets, QtCore
from ui.gameconfig.GameConfiguration import GameConfiguration


class GameView(QtWidgets.QGraphicsView):
    resized = QtCore.Signal()
    wheel_change = QtCore.Signal()
    keyPress = QtCore.Signal(QtCore.QEvent)
    mouseMove = QtCore.Signal(QtCore.QEvent)

    def __init__(self, parent=None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        # Задаем минимальный размер виджета
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
        self.controller.wheelEvent(e)

    def keyPressEvent(self, e):
        super(GameView, self).keyPressEvent(e)
        self.keyPress.emit(e)
        self.controller.keyPressEvent(e)

    def mouseMoveEvent(self, e):
        super(GameView, self).mouseMoveEvent(e)
        self.mouseMove.emit(e)
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
        if self.gameconfig.userConfig.read_config['window']['fullscreen']:
            self.changeResolution(w, h)
        else:
            w = self.gameconfig.userConfig.read_config['window']['resolution']['width']
            h = self.gameconfig.userConfig.read_config['window']['resolution']['height']
            self.changeResolution(w, h)

    def changeResolution(self, w, h):
        self.gameconfig.deviceConfig.updateScreenSize(w, h)
        self.setMinimumSize(w, h)
        self.scene().setSceneRect(0, 0, w, h)
        self.resized.emit()
