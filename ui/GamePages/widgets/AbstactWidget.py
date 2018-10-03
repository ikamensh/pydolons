from abc import ABC, abstractmethod
from PySide2 import QtCore

class AbstactWidget(QtCore.QObject):
    """docstring for AbstactWidget.
    AbstactWidget Предоставляет базовый класс для создания виджета( кнопок, полей и т.д.)
    Виджеты нужны для обеспечения интерактивности с пользователем.

    """
    @abstractmethod
    def __init__(self, name, w = 100, h = 20):
        super(AbstactWidget, self).__init__()
        self.setSize(w, h)
        self.setPos(0, 0)
        self.data = {'name':name}
        self.last_brush = None

    def setPos(self, x, y):
        """метод для установки текущей позиции виджета self.x, self.y
        """
        self.x, self.y = x, y

    def setSize(self, w, h):
        """метод для установки текущего размера виджета self.w, self.h
        """
        self.w, self.h = w, h

    @abstractmethod
    def setUp(self):
        """метод для описания установок виджета
        """
        pass

    @abstractmethod
    def paint(self, painter, option = None, widget = None):
        """метод для описания рисования виджета
        """
        pass

    @abstractmethod
    def collision(self, pos):
        """метод для определения находится ли точка pos.x(), pos.y()
        внутри функциональной части виджета
        """
        pass

    @abstractmethod
    def release(self):
        """методя для возврата значений в текущее состояние
        """
        pass
