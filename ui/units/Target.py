from PySide2 import QtCore, QtGui,QtWidgets

from battlefield import Cell


class Target(QtWidgets.QGraphicsItem):

    def __init__(self, *arg):
        super(Target, self).__init__(*arg)
        self.pen = QtGui.QPen(QtCore.Qt.red)
        self.pen.setWidth(10)
        self.setOpacity(0.3)
        self.w, self.h = 1, 1
        self.worldPos = Cell(0, 0)

    def setWorldX(self, x):
        self.worldPos.x = x
        self.setX(x * self.w)

    def boundingRect(self):
        return  QtCore.QRectF(self.x(), self.y(), self.w, self.h)

    def setWorldY(self, y):
        self.worldPos.y = y
        self.setY(y * self.h )


    def setWorldPos(self, x, y):
        self.setWorldX(x)
        self.setWorldY(y)


    def paint(self, painter, option = None, widget = None):
        tempPen = painter.pen()
        painter.setPen(self.pen)
        painter.drawLine(self.x() + self.w / 2 , self.y(), self.x()+ self.w/2, self.y()+ self.h)
        painter.drawLine(self.x()  , self.y() + self.h/ 2, self.x()+ self.w, self.y()+ self.h/2)
        painter.setPen(tempPen)