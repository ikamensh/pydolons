from abc import ABC, abstractmethod
from PySide2 import QtCore, QtGui, QtWidgets


class AbstractPage(QtWidgets.QGraphicsItemGroup):
    """docstring for AbstractPage."""
    def __init__(self):
        super(AbstractPage, self).__init__()
        self.gamePages = None
        self.state = False
        
    @abstractmethod
    def setUp(self, arg):
        """
        Устанавливаем настройки страницы
        """
        pass
    @abstractmethod
    def showPage(self, arg):
        """
        Показать  страницу
        """
        pass
    @abstractmethod
    def updatePage(self, arg):
        """
        Обновить страницу
        """
        pass

    @abstractmethod
    def addButton(self, arg):
        pass
