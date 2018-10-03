from ui.GamePages.widgets import AbstactWidget
from PySide2 import QtCore, QtGui

class Button(AbstactWidget):
    """docstring for Button.
    Signal: presed -- сигнализирует о нажатии
    """
    presed = QtCore.Signal()
    def __init__(self, name, text, w = 100, h = 20):
        super(Button, self).__init__(name, w, h)
        self.data['text'] = text
        self.data['presed'] = True

    def setUp(self):
        pass

    def paint(self, painter, option = None, widget = None):
        self.last_brush = painter.brush()
        if self.data['presed']:
            painter.setBrush(QtGui.QColor(128,128,128))
        else:
            painter.setBrush(QtCore.Qt.black)
        painter.drawRect(self.x, self.y, self.w, self.h)
        painter.drawText(self.x + 10, self.y + 15, self.data['text'])
        painter.setBrush(self.last_brush)

    def collision(self, pos):
        if pos.x() > self.x and pos.x() < self.x + self.w and pos.y() > self.y and pos.y() < self.y + self.h:
            self.data['presed'] = False
            self.presed.emit()

    def release(self):
        self.data['presed'] = True
