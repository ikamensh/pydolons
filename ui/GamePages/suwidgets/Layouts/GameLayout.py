
class GameLayout:
    def __init__(self):
        self.items = []
        self.items_pos = {}
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._spacing = 5

    def setPos(self, x, y):
        self._x = x
        self._y = y
        self.setGeometry()

    def pos(self):
        return self._x, self._y

    def addItem(self, item, row, col):
        pass

    def setGeometry(self):
        pass

    def sizeHint(self):
        pass

    def maxSizeWidget(self):
        pass

