from abc import ABC, abstractmethod
from PySide2 import QtWidgets, QtCore


class AbstractPage(QtCore.QObject, QtWidgets.QGraphicsItemGroup):
    """docstring for AbstractPage."""
    focusable = QtCore.Signal(bool)
    def __init__(self, gamePages, parent = None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsItemGroup.__init__(self)
        # super(AbstractPage, self).__init__()
        self.widget_pos = QtCore.QPoint()
        self.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
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
        self.setPos(self.gamePages.gameRoot.view.mapToScene(0, 0))
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
        background.setScale(prec)
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.background.boundingRect().width() * prec) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.background.boundingRect().height() * prec) / 2
        background.setPos(x, y)

    def updatePos(self):
        """ update position for scale view"""
        self.setPos(self.gamePages.gameRoot.view.mapToScene(0, 0))



