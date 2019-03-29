from PySide2 import QtWidgets, QtCore, QtGui


class DebugLayer(QtWidgets.QGraphicsItemGroup):
    def __init__(self, level):
        super(DebugLayer, self).__init__()
        self.gameRoot = level.gameRoot
        self.level = level
        self.b_red = QtCore.Qt.red
        self.b_blue = QtCore.Qt.blue
        self.b_green = QtCore.Qt.green
        self.pen = QtGui.QPen()
        self.pen.setBrush(QtCore.Qt.NoBrush)
        self.setSupportItem()
        pass

    def getItem(self, brush=None, pen=None, opacity=None):
        item = QtWidgets.QGraphicsRectItem()
        if pen is not None:
            item.setPen(pen)
        if brush is not None:
            item.setBrush(brush)
        if opacity is not None:
            item.setOpacity(opacity)
        self.addToGroup(item)
        return item

    def setSupportItem(self):
        self.frame_rect = self.getItem(self.b_red, self.pen, 0.1)
        # self.select_rect = self.getItem(self.b_green, self.pen, 0.5)
        # self.select_rect.setRect(0, 0, 128, 128)
        pass
