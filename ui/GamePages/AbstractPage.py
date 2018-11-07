from abc import ABC, abstractmethod
from PySide2 import QtWidgets


class AbstractPage(QtWidgets.QGraphicsItemGroup):
    """docstring for AbstractPage."""
    def __init__(self, gamePages):
        super(AbstractPage, self).__init__()
        self.gamePages = gamePages
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

    def checkFocus(self, pos):
        pass

    def resized(self):
        pass

    def release(self):
        pass

    def collisions(self, pos):
        pass

    def setUpGui(self):
        pass

    def destroy(self):
        pass

    def mouseMoveEvent(self, e):
        # self.sceneEvent(e)
        # super().mouseMoveEvent()
        pass

    def keyPressEvent(self, e):
        pass

