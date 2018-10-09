from ui.GamePages.widgets import AbstactWidget
from PySide2 import QtCore

class BoxValue(AbstactWidget):
    """docstring for BoxValue."""
    def __init__(self, name, w = 100, h = 20):
        super(BoxValue, self).__init__(name, w, h)
        self.ww = 1
        self.value = 0
        self.max_v = 1
        self.min_v = 0


    def setUp(self):
        """метод для описания установок виджета
        """
        pass

    def updateValue(self, value, max_v):
        self.value = value
        self.max_v = max_v
        pres = (self.value * 100) / self.max_v
        self.ww = (self.w * pres) / 100

    def paint(self, painter, option = None, widget = None):
        """метод для описания рисования виджета
        """
        self.last_brush = painter.brush()
        painter.drawRect(self.x, self.y, self.w, self.h)
        painter.setBrush(QtCore.Qt.blue)
        painter.drawRect(self.x, self.y, self.ww, self.h)
        painter.drawText(self.x + 10, self.y + 15, str(self.value))
        painter.drawText(self.x + 70, self.y + 15, str(self.max_v))
        painter.setBrush(self.last_brush)

    def collision(self, pos):
        """метод для определения находится ли точка pos.x(), pos.y()
        внутри функциональной части виджета
        """
        pass

    def release(self):
        """методя для возврата значений в текущее состояние
        """
        pass
