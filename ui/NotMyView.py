from PySide2 import QtWidgets

class MyView(QtWidgets.QGraphicsView):
    def __init__(self, parent = None):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)
        self.controller = None

    def wheelEvent(self, e):
        self.controller.wheelEvent(e)

    def keyPressEvent(self, e):
        self.controller.keyPressEvent(e)

    def mouseMoveEvent(self, e):
        self.controller.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        self.controller.mousePressEvent(e)