from PySide2 import QtWidgets


class GameView(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        pass

    def wheelEvent(self, e):
        self.controller.wheelEvent(e)

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