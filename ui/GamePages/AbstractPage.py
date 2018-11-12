from abc import ABC, abstractmethod
from PySide2 import QtWidgets


class AbstractPage(QtWidgets.QGraphicsItemGroup):
    """docstring for AbstractPage."""
    def __init__(self, gamePages):
        super(AbstractPage, self).__init__()
        self.gamePages = gamePages
        self.state = False
        self.isService = False

        
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

    def resizeBackground(self, background):
        w_screen = self.gamePages.gameRoot.cfg.dev_size[0]
        w_pic = self.background.boundingRect().width()
        prec = 0
        if w_screen > w_pic:
            prec = w_pic / w_screen
        else:
            prec = w_screen /w_pic
        print(prec)
        background.setScale(prec)

        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.background.boundingRect().width() * prec) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.background.boundingRect().height() * prec) / 2
        print(x, y)
        background.setPos(x, y)



