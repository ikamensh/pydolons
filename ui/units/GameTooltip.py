from PySide2 import QtWidgets


class GameTooltip(QtWidgets.QGraphicsRectItem):

    def __init__(self, arg):
        super(GameTooltip, self).__init__()
        self.setRect(0, 0, 32, 32)
